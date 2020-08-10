## What are Environment Variables?

Here is the best definition I've seen to date:

"An [*environment variable*](https://en.wikipedia.org/wiki/Environment_variable) is a variable whose value is set outside the program, typically through functionality built into the operating system or microservice. An environment variable is made up of a name/value pair, and any number may be created and available for reference at a point in time. " - From *[An Introduction to Environment Variables and How to Use Them](https://medium.com/chingu/an-introduction-to-environment-variables-and-how-to-use-them-f602f66d15fa)* by Jim Medlock

So basically defined variable or key/value pair in the memory of your operating system.

### How do they get there?

Some are set automatically. Some are set when you install a program.  Some you set yourself.

If you've ever had to manipulate your PATH environment variable (you may have had to when installing Python) then you have already worked with environment variables.

#### Linux and Mac OSX Systems

On Linux based systems (including Mac OS X) setting your own environment variable is easy!

```bash
claudia@Claudias-iMac ~ % export CLAUDIAS_FAVORITE_COLOR=Blue
claudia@Claudias-iMac ~ % echo $CLAUDIAS_FAVORITE_COLOR
Blue
claudia@Claudias-iMac ~ % python3
Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.environ.get('CLAUDIAS_FAVORITE_COLOR')
'Blue'
>>> os.environ.get('PATH')
'/Library/Frameworks/Python.framework/Versions/3.7/bin:/Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
>>> exit()
claudia@Claudias-iMac ~ % 

```

###### Handy Links:

[How to Set Environment Variables in Bash on Linux](https://www.howtogeek.com/668503/how-to-set-environment-variables-in-bash-on-linux/)



#### Windows Systems

On Windows based systems, get [Windows Subsytem for Linux (WSL)](https://fossbytes.com/what-is-windows-subsystem-for-linux-wsl/) or run a Linux based VM, I beg you.

But here is a comparable example with the Windows Command Prompt:

Things to remember:

1. Open the Command Prompt as an Administrator
2. Be mindful of the scope.  Scope to user or machine
3. Restart your IDE or CLI Window so it can re-read the new environment.

\* *remember to open this window as Administrator*

```shell
Microsoft Windows [Version 10.0.19041.388]
(c) 2020 Microsoft Corporation. All rights reserved.

C:\WINDOWS\system32>setx /M NETPASS "Cisco123"

SUCCESS: Specified value was saved.

C:\WINDOWS\system32>echo %NETPASS%
%NETPASS%

C:\WINDOWS\system32>
```

Notice that the echo returns nothing.  

Open up a **new** command window.  

Now the echo command should return the value you entered with the setx command.

If you jump into the Python shell and import the os module you can see that the environment variable can also be used within Python.

```
Microsoft Windows [Version 10.0.19041.388]
(c) 2020 Microsoft Corporation. All rights reserved.

C:\Users\claud>echo %NETPASS%
Cisco123

C:\Users\claud>python
Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.environ.get("NETPASS")
'Cisco123'
>>>
```



###### Handy Links:

[Create Environment Variable in Windows 10](https://winaero.com/blog/create-environment-variable-windows-10/)

[Use PowerShell to Set Environment Variables](https://www.tachytelic.net/2019/03/powershell-environment-variables/)

[Get started with the Windows Subsystem for Linux](https://docs.microsoft.com/en-us/learn/modules/get-started-with-windows-subsystem-for-linux/)

[PowerShell and Environment Variables: Everything You Ever Wanted to Know](https://adamtheautomator.com/powershell-environment-variables/)

---

[Back to README](README.md)