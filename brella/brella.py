# import the libraries
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import logging
import sys
import json

# Get the variables from the .env file
event = os.getenv('brella_event')
email = os.getenv('brella_email')
session_cookie = os.getenv('brella_session_cookie')

# Define the list of attributes we want to get
attributes = ['email', 'first-name', 'last-name', 'company-title', 'company-name', 'website', 'linkedin']

# Define the parameters for the Brella API call
url = "https://api.brella.io/api/events/"+event+"/attendees"
payload = {
    'ignore_networking': True,
    'order': 'newest',
    'page[number]': 1,
    'page[size]': 2000,
    'search': '' 
}
headers = {
  'authority': 'api.brella.io',
  'accept': 'application/vnd.brella.v4+json',
  'accept-language': 'en-US,en;q=0.9,fr;q=0.8,es;q=0.7',
  'access-token': 'mFNi1B5jlGB3IQ8G5JaZJw',
  'cache-control': 'no-cache',
  'client': 'r-tonX__wAuuf4iHVxhKWg',
  'dnt': '1',
  'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'uid': email,
  'Cookie': '_brella_session=' + session_cookie
}

# Define a function that takes in the attendee_attributes JSON and returns the desired values
def get_attendee_values(attendee_attributes):
    # Create a string to store the values
    attendee_string = ''

    # For each attribute we want to get
    for attribute in attributes:
        # If the attribute is not empty
        if attendee_attributes.get(attribute) is not None:
            # Add the attribute to the string, add " to escape commas
            attendee_string += '"'+attendee_attributes[attribute] + '",'
        # If the attribute is empty
        else:
            # Add an empty string to the string
            attendee_string += ','

    # Return the dictionary of values
    return attendee_string



# Create a function that makes an API call to Brella
def brella_api_call(url, method, payload, headers):
    # Make the API call
    response = requests.request(method, url, headers=headers, data=payload)
    # If the API call was successful
    if response.status_code == 200:
        # parse the JSON response to get the data in a format we can write into a CSV file
        data = response.json()

        # Log the raw JSON response in a file for debugging
        with open('./data/brella.json', 'w') as f:
            json.dump(data, f)
        
        # The data we need seems to only be in the included key
        attendees = data['included']

        # Create a header row in the CSV file based on the attributes we defined above
        with open('./data/brella.csv', 'w') as f:
            f.write(','.join(attributes) + '\n')

        # For each attendee, get their attributes and write them to a CSV file
        for attendee in attendees:
            # check that we have the attributes key
            if attendee.get('attributes') is not None:
                # Get the attendee's attributes
                attendee_attributes = attendee['attributes']

                # Get the attendee's values
                attendee_values = get_attendee_values(attendee_attributes)

                # check that the attendee_values has characters other than commas
                if attendee_values.replace(',', '')=='':
                    # skip this attendee
                    continue
                # Write the attendee's attributes to the CSV file
                with open('./data/brella.csv', 'a') as f:
                    f.write(attendee_values + '\n')

    # If the API call was unsuccessful
    else:
        # Log the error
        logging.error('Brella API call failed with status code: ' + str(response.status_code))
        # Exit the program
        sys.exit()

# Define our main function that will run the program
def main():
    # Call the Brella API
    brella_api_call(url, 'GET', payload, headers)

# Run the main function
if __name__ == "__main__":
    main()
