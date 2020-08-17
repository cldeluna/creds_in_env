# How Network Engineers Can Manage Credentials and Keys More Securely in Python

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/cldeluna/creds_in_env)

For me, 2020 is going to be the year of taking my automation skills to the next level, and a Pandemic is not going to get in the way of that goal (much)!

At the top of the list is handling credentials and API keys in a more secure fashion.   When you are first learning, most of the examples you find (mine included) put passwords in clear text in files or have you input them interactively.  

Both approaches work well when getting started but do a disservice in teaching you how to ready your network automation scripts for production and in getting into good habits.  

Lets look at the problem we are trying to solve:

- We don't want to expose our credentials in clear text or accidentally include them in a shared repository, particularly one that is public (i.e. GitHub - and here I speak from experience).
- Entering them interactively can be limiting, particularly when you are acting on a variety of devices which may have different credentials.  Its also annoying.

In short, what we all already know:

- exposing credentials BAD
- stopping program executions to enter values BAD

In my mind, these are the broad categories of approaches:

- Interactive 
  - With this method, the script will interactively ask for the credentials during run time or you provide them during execution via parameters.
  - In fact you can pass them as arguments using something like [argparse](https://docs.python.org/3/library/argparse.html) and [getpass/getuser](https://docs.python.org/3/library/getpass.html). See Useful Links below for more on that.
- File - Encrypted and Unencrypted
  - Put credentials and keys in a file which may or may not be encrypted.  At runtime you decrypt the file as needed and load the sensitive information into your script.  The problem here is that you need a key to decrypt the file and unless you enter that interactively you have to store it somewhere so that its accessible at run time and at that point, if someone has access to the script they likely have access to the key so you are not much better off.
- Environment Variables 
  - Set credentials and keys as environment variables that your script can access during runtime.
  - In fact these can be set interactively (think CLI) and via a file as well (look for .env or .ini files in repositories and you now know what they are)
- Tap into Operating System credentials store (Subset of File - Encrypted File)
  - The python [keyring](https://pypi.org/project/keyring/) module allows you to access a systems' keyring service (Mac OS X Keychain, windows, etc.)  from within python.  
  - I never went down this path because at any given time I am bouncing between various desktops, laptops, and operating systems.  
  - Also, working as a consultant, I never wanted to store client credentials in any kind of shared system capability or mix them in with my own.  I need maximum portability and maximum  flexibility.
- Tap into a Password Safe type of file (Subset of File - Encrypted File)
  - I'm a huge fan of KeePass but the python module does not seem to be maintained and the disclaimers were enough to make me pass.
  - Python Password Safe looked interesting but is clearly documented as a learning project and I don't have much hope for continued development.
  - I've not spent much time in this area as it would put me back to file management, encryption, and decryption.

For me, environment variables made the most sense.  

If you are not familiar with environment variables I've tried to provide a short introduction [here](what_are_env_variables.md).

Why environment variables?  Well, I've been waffling with different approaches over the years but Chris Crook ([@ctopher78](https://twitter.com/ctopher78)) shared an example in the Nornir Slack channel late last year that was one of those "golden nuggets" for me.  Talk about hitting all the mandatory requirements:

- No additional Python modules needed and minimal dependencies
  - Worst case, in client environments where all I could count on was Python, I could still use this method.  Basically no module requirements other than Python3.  Also, if I don't have Internet access (it happens) my script is still fully functional.
- Cross platform
  - On any platform, Mac, Windows, Linux, I was in business
- No required interactivity after set up
  - One time set up and then execute what I needed to in the environment

In addition, this sets up a nice framework so that however I get the environment setup (files,  interactive, additional modules, etc.),  I can modularize my code easily.   

My hope is that the scripts in this repository will show you some ways this can be done and get you thinking about which way works best for you.  

#### File Encryption

A word about file encryption.   None of the examples in this repository get into encrypting files.  That is a valid approach and I'm a huge fan of [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) and [HashiCorp Vault](https://www.vaultproject.io/) but over time I found the environment variable approach much easier to work with.   There is quite alot out there on this topic and I encourage you to do your own research.   If HashiCorp Vault is of interest to you start with Kareem Iskander's post *[Secure Your Cisco DNA Center API Authentication with Vault](https://blogs.cisco.com/developer/dna-center-api-authentication-with-vault)*.

For me,  the portability and flexibility requirements makes the environment variable approach far superior.   With Ansible, I generally work with one control server pre client or my laptop and so its not onerous to keep an encrypted file on the control server, but outside of Ansible, I don't want to be moving encrypted files around, syncing them, etc. 

And, as it is often pointed out, you need a key or password to decrypt that file.  Unless you pass it interactively at run time (which may work for you), you need to store that key somewhere where the script can access it.  Now you are back to securing a file or setting an environment variable.  



### Pros/Cons of Python Modules Discussed

| Module          | Pros                                                         | Cons                                                         |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| os.environ      | Part of Python base. No need for any additional modules      | You have to get the environment variables into the environment which is pretty easy to do. <br />Either:<br />- Interactive (one time or you can make the persistent) <br />or <br />- read in a file and then set the environment variables (requires a bit more work unless you use the python-dotenv module) |
| python-dotenv   | Very easy to use, with one line you set one or more variables  in an .env or .ini file as environment variables. | Needs to be installed.  If you need non string values you have to do that conversion in your code |
| python-decouple | This is the module you want if you need other variable types than string in your script and do not want or cannot do the conversion in your code (.ie a settings file) | Brings variables from an .env or .ini file into your scripts name space so they can be used but does **not set the environment variables**. |



### Script Overview

| Script Name          | 3rd Party Module Requirements | Notes                                                        |
| -------------------- | ----------------------------- | ------------------------------------------------------------ |
| add_2env.py          | None                          | This is a pure Python3 script which defines a set of reusable modules to manipulate the execution environment so that network automation tools can be executed using credentials set as environment variables.<br /><br />The script has the following functions:<br />**all_env_vars**<br />*get, and optionally print, all the currently defined environment variables*<br />**check_env**<br /><br />*check to see if a specific environment variable is defined*<br />**set_env**<br />*set an environment variable* |
| env_creds.py         | nornir                        | Example standalone script that incorporates use of environment variables to execute Nornir actions on a network topology.  The script checks for the specified environment variables, and if they are not set either as environment variables or within the topology YAML files then the script will prompt for the needed values. |
| load_2env_dotenv.py  | python-dotenv                 | Some functions using the python-dotenv module to set and load environment variables into your Python script. |
| load_env_decouple.py | python-decouple               | Some functions using the python-decouple module to load key/value pairs into your Python script.  This module does not actually get or set environment variables but it does use a .env file.   I don't use this module much because you are right back to credentials in clear text stored in a file.  The .env convention means if my .gitignore file is set up properly to exclude .env I won't put it into my repository and it means I can remove any credentials or keys from my topology YAML and other files that I do want to be part of the repo. |
| env_apikeys.py       | requests                      | Example script working with APIs (one of which requires a key).  Includes the use of functions in the other scripts to set and check environment variables and .env files to save API Keys.  Shows both a Python only option with os.environ as well as an option using python-dotenv. |



## Installation

1. [Define a virtual environment with Python3](https://realpython.com/python-virtual-environments-a-primer/).
2. Activate your new virtual environment
3. Install all the required modules with the pip install command as shown below

```
pip install -r requirements.txt
```



## Code Review

### Python built in os module

Distinguishing features:

- Easy to use
- No 3rd party modules required
- Allows you to set a default value

Keeping the general goal of "simpler is better" in mind, you always want to see what you can do with Python's built in capabilities.  You won't be disappointed here.

Python comes with the **os** module which allows you to interact with the operating system.  Since environment variables are fundamentally part of the OS, you won't be surprised that the **os** module can tap into your environment variables with **os.envirion**.

This repository began when I tool some of my early Nornir scripts and converted them to use environment variables.  The main example here is the ***env\_creds.py*** script. You will notice that it has similar functions to the ***add\_2env.py*** script.  This is included here to give you an idea of what can be done but also so you have something to work with.   Later versions of this script use the python-dotenv module and, if the expected variables are not set, then it leverages the interactive functions.

The *set_creds* function in ***env\_creds.py*** script can be directly attributed to Chris Crook ([@ctopher78](https://twitter.com/ctopher78)) with some minor updates to allow setting credentials at the default level, at the group level, or at the device level.  See a typical run of the script [here](run_output_for_env_creds.txt).

The ***add\_2env.py*** script and its re-usable modules (which you will see in the subsequent scripts) needs no 3rd party modules.   In main() you have examples of how the various functions within the script can be used.  

1. First the script outputs all the current environment variables with the *all_env_vars* function.
2. Next, the *set\_env* function is called to set a Username.   This function allows you to set a name. By default it will turn the name into all uppercase as is the environment variable convention.  It will also echo back the value.  Before existing, the function calls the *check\_env* function to validate that the environmental variable is set.
3. Once the Username environment variable is set the script calls the *set\_env* function again but overrides some of the default behavior.  The description is set to "Password" so that the user knows what is being requested and the sensitivity option is set to true.  That triggers the use of the **getpass** module so that the password is not echoed back to the screen.  It also adjusts the notifications (if they are set) to not display the password.
4. Lastly, the script outputs all the current environment variables again.  This can be used as a final visual check that the variables set are in fact there.

Example of script execution:

```bash
(env_variables) claudia@Claudias-iMac creds_in_env % python add_2env.py         

Current Environment Variables:

======== ENVIRONMENT VARIABLES for USER claudia ======== 
{'HOME': '/Users/claudia',
 'LC_CTYPE': 'en_US.UTF-8',
 'LOGIN_SHELL': '1',
 'LOGNAME': 'claudia',
 'OLDPWD': '/Users/claudia/Dropbox '
           '(Indigo '
           'Wire '
           'Networks)/scripts/python/2020/creds_in_env',
 'PATH': '/Users/claudia/vEnvs/env_variables/bin:/Library/Frameworks/Python.framework/Versions/3.7/bin:/Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Frameworks/Python.framework/Versions/3.7/bin:/Library/Frameworks/Python.framework/Versions/3.8/bin',
 'PS1': '(env_variables) '
        '%n@%m '
        '%1~ '
        '%# ',
 'PWD': '/Users/claudia/Dropbox '
        '(Indigo '
        'Wire '
        'Networks)/scripts/python/2020/creds_in_env',
 'SHELL': '/bin/zsh',
 'SHLVL': '1',
 'SSH_AUTH_SOCK': '/private/tmp/com.apple.launchd.Afgdexb2wz/Listeners',
 'TERM': 'xterm-256color',
 'TERMINAL_EMULATOR': 'JetBrains-JediTerm',
 'TMPDIR': '/var/folders/vt/xfhvc3690wz75cm9cjd6mpxr0000gn/T/',
 'USER': 'claudia',
 'VIRTUAL_ENV': '/Users/claudia/vEnvs/env_variables',
 'XPC_FLAGS': '0x0',
 'XPC_SERVICE_NAME': '0',
 'ZDOTDIR': '',
 '_': '/Users/claudia/vEnvs/env_variables/bin/python',
 '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0',
 '__INTELLIJ_COMMAND_HISTFILE__': '/Users/claudia/Library/Preferences/PyCharm2019.3/terminal/history/history-126'}

======== Creating Environment Variable for Username ========
**** Variable NAME will be set to all uppercase per convention...

Please enter Username environment variable name: NETUSER
Please enter Username environment variable value: cisco

======== ENV SET Environment Variable NETUSER set with valid value cisco ========


======== Creating Environment Variable for Password ========
**** Variable NAME will be set to all uppercase per convention...

Please enter Password environment variable name: netpass
Please enter Password sensitive environment variable value (will not echo to screen): 

======== ENV SET Environment Variable NETPASS set and valid ========


UPDATED Environment Variables:
{
    "HOME": "/Users/claudia",
    "LC_CTYPE": "en_US.UTF-8",
    "LOGIN_SHELL": "1",
    "LOGNAME": "claudia",
    "NETPASS": "cisco",
    "NETUSER": "cisco",
    "OLDPWD": "/Users/claudia/Dropbox (Indigo Wire Networks)/scripts/python/2020/creds_in_env",
    "PATH": "/Users/claudia/vEnvs/env_variables/bin:/Library/Frameworks/Python.framework/Versions/3.7/bin:/Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Frameworks/Python.framework/Versions/3.7/bin:/Library/Frameworks/Python.framework/Versions/3.8/bin",
    "PS1": "(env_variables) %n@%m %1~ %# ",
    "PWD": "/Users/claudia/Dropbox (Indigo Wire Networks)/scripts/python/2020/creds_in_env",
    "SHELL": "/bin/zsh",
    "SHLVL": "1",
    "SSH_AUTH_SOCK": "/private/tmp/com.apple.launchd.Afgdexb2wz/Listeners",
    "TERM": "xterm-256color",
    "TERMINAL_EMULATOR": "JetBrains-JediTerm",
    "TMPDIR": "/var/folders/vt/xfhvc3690wz75cm9cjd6mpxr0000gn/T/",
    "USER": "claudia",
    "VIRTUAL_ENV": "/Users/claudia/vEnvs/env_variables",
    "XPC_FLAGS": "0x0",
    "XPC_SERVICE_NAME": "0",
    "ZDOTDIR": "",
    "_": "/Users/claudia/vEnvs/env_variables/bin/python",
    "__CF_USER_TEXT_ENCODING": "0x1F5:0x0:0x0",
    "__INTELLIJ_COMMAND_HISTFILE__": "/Users/claudia/Library/Preferences/PyCharm2019.3/terminal/history/history-126"
}
(env_variables) claudia@Claudias-iMac creds_in_env % 

```



### python-dotenv module

[python-dotenv module on PyPI](https://pypi.org/project/python-dotenv/)

Distinguishing features:

- Easy to use
- Accepts stream of data
- Allows you to set a default value
- Does not overwrite existing system environment variables by default but gives you the option to do so
- There is an optional CLI interface you can use to update the .env file

The python-dotenv module is pretty effortless.

If you look at how it was used in the ***env\_apikeys.py*** script, its one line (of course, you have to make sure you have your .env file with the values you need).

```python
    dotenv.load_dotenv()
```

In the ***load\_2env\_dotenv.py*** script, there is a bit more structure around the usage.  It's pulled out into a function for reusability and requires a path (explicit is good) for flexibility.  There is also some very basic checking to make sure the .env file actually exists and if not to exit out of the script gracefully.

```python
load_env_from_dotenv_file(path)
```

In this way, you can import the  ***load\_2env\_dotenv.py*** and have access to the *load_env_from_dotenv_file* function from any other script.

The **main()** part of the script provides examples of how to use the function and validate that the variables you want have been set.

The one other noteworthy feature of the python-dotenv module is that it will not only accept an .env file but it will also accept a "filelike" stream of data and present it to you as a dictionary.  There may be some instances where you want to use information in the .env file but not actually set the environment variables.

Example execution:

```bash
(env_variables) claudia@Claudias-iMac creds_in_env % python load_2env_dotenv.py

======= Confirm variables loaded from .env file are valid environment variables: 
        Environment Variable API_KEY is valid!
        Environment Variable MY_ENV is valid!
        Environment Variable MY_REPO is valid!
        Environment Variable CONTEXT is valid!
        Environment Variable NETUSER is valid!
        Environment Variable NETPASS is valid!
        Environment Variable MY_BOOL is valid!
        Environment Variable MY_INT is valid!
        Environment Variable NOT_THERE does not exist!
(env_variables) claudia@Claudias-iMac creds_in_env % 

```



### Python-decouple module

[Python-decouple module on PyPI](https://pypi.org/project/python-decouple/)

Distinguishing features:

- Allows you to "cast" the variable to a specific type (integer, boolean). This is an important capability and can be quit handy.
- Easy to use
- Allows you to set a default value
- Note: This module **does not actually set environment variable**s but does read key/value pairs  from a .env file and make them available to your script in a very easy and intuitive manner.

If you need values of type boolean or integer then this is the module might be of interest.  This module does not actually set environment variables for just that reason.  It does allow you to put your configuration settings into a .ini or .env file and easily read them.  Like python-dotenv, its important to remember to exclude those files in your .gitignore.

For completeness I have a ***load_env_decouple.py*** script.

The mechanism for the module is a little different than what we have been working with.  Obviously we are not setting environment variables but rather loading them into the scripts name space and manipulating types and defaults as needed.    

Example execution:

```
(env_variables) claudia@Claudias-iMac creds_in_env % python load_env_decouple.py

======= View Variables loaded from .env file: 
.env file variable name: API_KEY with value: Secret_API_Key of type <class 'str'>
.env file variable name: MY_ENV with value: Claudia's iMac of type <class 'str'>
.env file variable name: MY_REPO with value: creds_in_env of type <class 'str'>
.env file variable name: CONTEXT with value: DEV of type <class 'str'>
.env file variable name: NETUSER with value: cisco of type <class 'str'>
.env file variable name: NETPASS with value: cisco of type <class 'str'>
.env file variable name: MY_BOOL with value: True of type <class 'str'>
.env file variable name: MY_INT with value: 12 of type <class 'str'>
.env file variable name: TEST with value: Will this show up? of type <class 'str'>

Boolean Value with default and cast set:  variable MY_BOOL with value: True of type <class 'bool'>

Integer Value with default and cast set:  variable MY_INT with value: 12 of type <class 'int'>


Checking for environment variable: TEST:
        Exists: False
        Valid: False
        Value: None
(env_variables) claudia@Claudias-iMac creds_in_env % 

```



### API Keys

Working with APIs is always an eye opener on what is possible with the data that is out there.

Open Notify provides [Open APIs From Space](http://open-notify.org/Open-Notify-API/).  Here you can openly (no key or authentication is needed) query a REST API and get: 

- the location of the International Space Station (ISS), 
- predictions as to when the ISS will pass over a given location, and 
- how many people are currently in space!

When the ISS is over land the location call to the Open Notify REST API will return a JSON payload which looks something like this:

```json
{
    "timestamp": 1596979351,
    "iss_position": {
        "longitude": "-66.5110",
        "latitude": "10.3088"
    },
    "message": "success"
}
```

I know you all share my excitement at having this data at our fingertips but some might suggest that it would be nice to translate LAT/LONG to a more commonly recognizable location.

There are [number of services](https://gisgeography.com/reverse-geocoding-services-addresses-free-paid/) for this and in this example we shall use the [HERE Geocoding API](https://developer.here.com/c/geocoding) because its so easy to use and its free.

Let's not lose sight of our goal here, which is to deal responsibly with our credentials and keys.

Once you have an [API Key](https://developer.here.com/c/geocoding), the **env_apikeys.py** script provides <u>**two examples**</u> of working with the key.

###### Interactively add the key as an environment variable

The first, and default, is to interactively set an environment variable with the key.  This method can be done with just Python (no extra modules for key manipulation), although the script requires the **requests** module for the REST API interactions.

###### Store the key in a .env file

The second is to create a .env file with the key and read it in during script execution using the python-dotenv module.

*Tip*:  When working with structured data returned from APIs or other calls, its important to understand how to get to the data you need.   See [Decomposing Data Structures](https://gratuitous-arp.net/decomposing-complex-json-data-structures/) for more information on this topic.

Example of script execution using the default method (interactively add environment variable):

```bash
(env_variables) claudia@Claudias-iMac creds_in_env % python env_apikeys.py

====== ISS is at latitude 43.3414 and longitude -76.7761


======== Creating Environment Variable for HERE API Key ========
**** Variable NAME will be set to all uppercase per convention...

Please enter HERE API Key environment variable name: api_key
Please enter HERE API Key sensitive environment variable value (will not echo to screen): 

======== ENV SET Environment Variable API_KEY set and valid ========

https://revgeocode.search.hereapi.com/v1/revgeocode?at=43.3414,-76.7761&lang=en-US&limit=20&apiKey=*******
{
    "items": [
        {
            "title": "Wayne, NY, United States",
            "id": "here:cm:namedplace:21020101",
            "resultType": "administrativeArea",
            "administrativeAreaType": "county",
            "address": {
                "label": "Wayne, NY, United States",
                "countryCode": "USA",
                "countryName": "United States",
                "state": "New York",
                "county": "Wayne"
            },
            "position": {
                "lat": 43.32212,
                "lng": -77.04566
            },
            "distance": 0,
            "mapView": {
                "west": -77.38013,
                "south": 43.01234,
                "east": -76.70237,
                "north": 43.68059
            }
        },
        {
            "title": "NY, United States",
            "id": "here:cm:namedplace:21010819",
            "resultType": "administrativeArea",
            "administrativeAreaType": "state",
            "address": {
                "label": "NY, United States",
                "countryCode": "USA",
                "countryName": "United States",
                "state": "New York"
            },
            "position": {
                "lat": 42.65155,
                "lng": -73.75521
            },
            "distance": 0,
            "mapView": {
                "west": -79.76212,
                "south": 40.47742,
                "east": -71.66864,
                "north": 45.01608
            }
        },
        {
            "title": "United States",
            "id": "here:cm:namedplace:21000001",
            "resultType": "administrativeArea",
            "administrativeAreaType": "country",
            "address": {
                "label": "United States",
                "countryCode": "USA",
                "countryName": "United States"
            },
            "position": {
                "lat": 38.89037,
                "lng": -77.03196
            },
            "distance": 0,
            "mapView": {
                "west": -124.749,
                "south": 24.5018,
                "east": -66.9406,
                "north": 49.3845
            }
        }
    ]
}

====== ISS is over United States (Wayne, NY, United States).

(env_variables) claudia@Claudias-iMac creds_in_env % 


```

Example of script execution using the -f (file_env) option to read in the environment variables from the .env file using the python-dotenv module.

```bash
(env_variables) claudia@Claudias-iMac creds_in_env % python env_apikeys.py -f

====== ISS is at latitude 26.9096 and longitude 25.6794

https://revgeocode.search.hereapi.com/v1/revgeocode?at=26.9096,25.6794&lang=en-US&limit=20&apiKey=*******
{
    "items": [
        {
            "title": "Markaz El Farafra, Egypt",
            "id": "here:cm:namedplace:23712950",
            "resultType": "locality",
            "localityType": "city",
            "address": {
                "label": "Markaz El Farafra, Egypt",
                "countryCode": "EGY",
                "countryName": "Egypt",
                "county": "El Wadi El Gedeed",
                "city": "Markaz El Farafra"
            },
            "position": {
                "lat": 27.1965,
                "lng": 26.85411
            },
            "distance": 0,
            "mapView": {
                "west": 25.0,
                "south": 26.3844,
                "east": 28.68207,
                "north": 27.69663
            }
        },
        {
            "title": "El Wadi El Gedeed, Egypt",
            "id": "here:cm:namedplace:23713426",
            "resultType": "administrativeArea",
            "administrativeAreaType": "county",
            "address": {
                "label": "El Wadi El Gedeed, Egypt",
                "countryCode": "EGY",
                "countryName": "Egypt",
                "county": "El Wadi El Gedeed"
            },
            "position": {
                "lat": 25.44683,
                "lng": 30.54944
            },
            "distance": 0,
            "mapView": {
                "west": 25.0,
                "south": 22.0,
                "east": 32.72483,
                "north": 27.69663
            }
        },
        {
            "title": "Egypt",
            "id": "here:cm:namedplace:23713588",
            "resultType": "administrativeArea",
            "administrativeAreaType": "country",
            "address": {
                "label": "Egypt",
                "countryCode": "EGY",
                "countryName": "Egypt"
            },
            "position": {
                "lat": 30.04427,
                "lng": 31.23525
            },
            "distance": 0,
            "mapView": {
                "west": 24.6981,
                "south": 21.99992,
                "east": 36.89468,
                "north": 31.67418
            }
        }
    ]
}

====== ISS is over Egypt (Markaz El Farafra, Egypt).

(env_variables) claudia@Claudias-iMac creds_in_env % 

```



#### Who was in outer space at the time of this writing 

2020-08-09

```
{
    "number": 3,
    "people": [
        {
            "craft": "ISS",
            "name": "Chris Cassidy"
        },
        {
            "craft": "ISS",
            "name": "Anatoly Ivanishin"
        },
        {
            "craft": "ISS",
            "name": "Ivan Vagner"
        }
    ],
    "message": "success"
}
```



# Useful Links

- [Hiding secret info in Python using environment variables](https://medium.com/dataseries/hiding-secret-info-in-python-using-environment-variables-a2bab182eea) - Raivat Shah on Medium
- [AskPython](https://www.askpython.com/python/environment-variables-in-python) 
- [Libhunt comparison of dotenv vs decouple](https://python.libhunt.com/compare-python-dotenv-vs-python-decouple) 
- Stackoverflow: [Is it possible to encrypt the information in .env file (in Laravel)?](https://stackoverflow.com/questions/62245142/is-it-possible-to-encrypt-the-information-in-env-file-in-laravel)
- Stackoverflow: [Python: Using getpass with argparse](https://stackoverflow.com/questions/27921629/python-using-getpass-with-argparse)
- [Keeping Development Credentials Secure](https://portalzine.de/dev/hosting/keeping-development-credentials-secure/)
- [Securing Environment Variables](https://www.honeybadger.io/blog/securing-environment-variables/)
- [Your Serverless Function has a Secret](https://www.metaltoad.com/blog/how-to-encrypt-serverless-environment-variable-secrets-with-kms)



For more examples, check out my articles on getting started with Nornir at [The Gratuitous Arp](https://gratuitous-arp.net/):

- [Nornir – A New Network Automation Framework](https://github.com/cldeluna/nornir_intro2)
- [Configuration Creation with Nornir](https://gratuitous-arp.net/configuration-creation-with-nornir/)



## Licensing

This code is licensed under the BSD 3-Clause License. See [LICENSE](https://github.com/CiscoDevNet/code-exchange-repo-template/blob/master/manual-sample-repo/LICENSE) for details.

