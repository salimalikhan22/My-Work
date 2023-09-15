#!/usr/bin/python3

import sys
import json
import re
import requests
import ast


token=sys.argv[1]
#print(token)

with open('data.json', 'r') as file:
    json_data = json.load(file)

# Define a list to store the modified objects
modified_objects = []

# Iterate over the JSON objects
for item in json_data:
    FQDN = item['FQDN']
    URL = item['URL']
    AppName = item['APPNAME'] 
    # Extract app_id and server_id from FQDN
    server_id = FQDN.split('-')[1]
    app_id = FQDN.split('-')[2].split('.')[0]

    # Create a new JSON object with app_id, server_id, and URL
    new_object = {
        'app_id': app_id,
        'server_id': server_id,
        'FQDN': FQDN,
        'URL': URL,
        'APPNAME' : AppName
        
    }

    # Append the modified object to the list
    modified_objects.append(new_object)

# Save the modified objects back to data.json
with open('data.json', 'w') as file:
    json.dump(modified_objects, file, indent=4)

# Print the modified objects
#print(json.dumps(modified_objects, indent=4))


# Read JSON data from the data.json file
with open('data.json', 'r') as file:
    data = json.load(file)

# Iterate over the list of JSON objects
for json_object in data:
    # Work on one JSON object at a time
#    print("FQDN:", json_object["FQDN"])
#    print("URL:", json_object["URL"])
#    print("server_id:", json_object["server_id"])
#    print("app_id:", json_object["app_id"])
    server_id=json_object["server_id"]
    app_id=json_object["app_id"]
    url=json_object["URL"]
    appname = json_object["APPNAME"]
    # Construct the URL with variables
    url_with_params = f"https://api.cloudways.com/api/v1/app/manage/cronList?server_id={server_id}&app_id={app_id}"

    headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
    }

# Send the GET request
    response = requests.get(url_with_params, headers=headers)

# Check the response
    if response.status_code == 200:
        # Request was successful, process the response here
        data = response.json()
#        print("Response:", data)
        print("Successfully Get the Cron for App ID: {}, Appname: {}".format(app_id,appname))
    else:
        # Request failed
#        print(f"Request failed with status code: {response.status_code}")
#        print("Response content:", response.text)
        print("Failed to Get the Cron for App ID: {}, Appname: {}".format(app_id,appname))
    response_str = str(response.json()) 

# Extract the 'script' part from the response
    response_dict = ast.literal_eval(response_str)  # Convert the string to a dictionary
    script_part = response_dict.get('script')  # Get the 'script' value or an empty string if not found

# Split the 'script' part into a list of lines
#    script_lines = script_part.split('\n')
    script_lines = [line.strip() for line in script_part.split('\n') if line.strip()]
# Append the additional string to the end of the list
    additional_string = "*/5 * * * * wget -q -O - '{url}/wp-cron.php?doing_wp_cron' >/dev/null 2>&1"
    additional_string=additional_string.replace("{url}", url)
    
    if additional_string not in script_lines:

        script_lines.append(additional_string)
# Print the formatted list of script lines
#    print(script_lines)
    
        request_url = "https://api.cloudways.com/api/v1/app/manage/cronList"

# Define headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        crons = json.dumps(script_lines)

# Define the data payload
        data = {
            "server_id": server_id,
            "app_id": app_id,
            "crons": crons,
            "is_script": "True",
        }

# Send the POST request
        response = requests.post(request_url, headers=headers, data=data)

# Check the response
        if response.status_code == 200:
        # Request was successful, process the response here
            data = response.json()
            print("Response:", data)
            print("Successfully Added the Cron for App ID: {}, Appname: {}".format(app_id, appname))
        else:
        # Request failed
    #    print(f"Request failed with status code: {response.status_code}")
    #    print("Response content:", response.text)
            print("Failed to add the Cron for App ID: {}, Appname: {}".format(app_id, appname))
    else:
        print("Cron already Exists")


