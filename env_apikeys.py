#!/usr/bin/python -tt
# Project: creds_in_env
# Filename: env_apikeys
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "8/9/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import json

# For this script to run sucessfully, the request module needs to be installed
# https://www.geeksforgeeks.org/how-to-install-requests-in-python-for-windows-linux-mac/
import requests

# Import the add_2env scritp as a module so that we can interactively define the API key in an environment variable
import add_2env

# Import the python-dotenv module
import dotenv


def iss_info(debug=False):
    """
    This function uses the http://open-notify.org/Open-Notify-API/ API to obtain information about the International
    Space Station

    ISS Location
    http://api.open-notify.org/iss-now.json?callback=?

    ISS will Pass a location
    http://api.open-notify.org/iss-pass.json?lat=45.0&lon=-122.3&alt=20&n=5&callback=?

    Number of people in space
    http://api.open-notify.org/astros.json?callback=?

    :return:
    """

    response = requests.get("http://api.open-notify.org/astros.json")
    # Print the status code of the response.
    if debug:
        print(response.status_code)
        print(dir(response))
        print(json.dumps(response.json(), indent=4))


    # The response is a list of the timestamp or each pass along with the duration in seconds.
    response = requests.get("http://api.open-notify.org/iss-pass.json?lat=45.0&lon=-122.3&alt=20&n=5")
    # Print the status code of the response.
    if debug:
        print(response.status_code)
        print(dir(response))
        print(json.dumps(response.json(), indent=4))

    response = requests.get("http://api.open-notify.org/iss-now.json")
    # Print the status code of the response.
    if debug:
        print(response.status_code)

    return response


def get_iss_location():

    iss_data = iss_info(debug=False)

    iss_data_dict = iss_data.json()

    latitude = iss_data_dict['iss_position']['latitude']
    longitude = iss_data_dict['iss_position']['longitude']

    return latitude, longitude


def check_iss_location(key_valid, lat, lng, api_key):

    ## BUILD the REST API URL

    # HERE REST API Query for Current ISS Location
    # url = "https://revgeocode.search.hereapi.com/v1/revgeocode
    # ?
    # at=-44.9295,-145.5073
    # &
    # lang=en-US
    # &
    # limit=20
    # &
    # apiKey=QEAoB66NeqP4_lZmkRJtMc6aY9bHMq7-p7Y-u8OzY04"
    base_url = "https://revgeocode.search.hereapi.com/v1/revgeocode"
    lang = "en-US"
    limit = 20

    if key_valid:
        print(f"{base_url}?at={lat},{lng}&lang={lang}&limit={limit}&apiKey=*******")
    else:
        print(f"ERROR!  Invalid API Key.  Aborting script run...")
        exit()

    # Actual URL used for the REST Call
    # https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics/endpoint-reverse-geocode-brief.html
    # API Reference
    # https://developer.here.com/documentation/geocoding-search-api/api-reference-swagger.html
    # Format: {latitude},{longitude}
    # Type: {decimal},{decimal}
    # Example: -13.163068,-72.545128 (Machu Picchu Mountain, Peru)

    url = f"{base_url}?at={lat},{lng}&lang={lang}&limit={limit}&apiKey={api_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    resp_json = json.loads(response.text.encode('utf8'))

    if response.status_code == 200:
        print(json.dumps(resp_json, indent=4))
        if resp_json['items']:
            print(f"\n====== ISS is over {resp_json['items'][0]['address']['countryName']} ({resp_json['items'][0]['address']['label']}).\n")
        else:
            print(f"\n====== ISS is over water.\n")
    else:
        print(f"ERROR! Call returned Response Code: {response.status_code}")
        print(json.dumps(resp_json, indent = 4))


def main():

    # Get current ISS location
    lat, lng = get_iss_location()
    print(f"\n====== ISS is at latitude {lat} and longitude {lng}\n")

    ## show two methods of working with the API Key

    # Store API Key in .env file and load with python-dotenv module
    # This method requires the python-dotenv module
    # This section is executed when the script is run with the -f option
    if arguments.file_env:

        # This loads the variables found in the local .env file into memory
        dotenv.load_dotenv()

        # Lets use our existing check_env function to make sure we have the key and that it is valid
        # Note that "API_KEY" is the name of the variable in the .env_sample file
        env_var_info_dict = add_2env.check_env('API_KEY')
        api_key_valid = env_var_info_dict['VALID']
        api_key_value = env_var_info_dict['VALUE']

    # Interactively add the API Key as an environment variable
    # This method can be done with only Python
    else:
        # SET and Validate ENVIRONMENT VARIABLE for the HERE API Key
        api_key_valid, api_key_dict = add_2env.set_env(desc="HERE API Key", sensitive=True)
        api_key_value = api_key_dict['VALUE']

    # The call to the function translating lat/long to a location is the same once the required parameters are set
    # either by interactively adding the key or obtaining it from a .env file
    check_iss_location(api_key_valid, lat, lng, api_key_value)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python env_apikeys' ")
    parser.add_argument("-f", "--file_env", help="Use .env file to load environment variable(s)",
                        action="store_true", default=False)
    arguments = parser.parse_args()
    main()
