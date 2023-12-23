import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key and webhook URL from environment variables
api_key = os.getenv("API_KEY")
webhook_url = os.getenv("WEBHOOK_URL")

# Create an empty list to store domain names
domains = []


def send_to_discord(message):
    # Prepare the Discord webhook request
    payload = {"content": message}

    # Send the Discord webhook request
    response = requests.request("POST", webhook_url, data=payload)

    # Process the response
    if response.status_code == 204:
        print("Message sent to Discord!")
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)


def get_domains():
    # Prompt the user to enter domain names
    prompt = "Enter domain names (or 'quit' to exit): "
    while True:
        domain = input(prompt)
        if domain == "quit":
            break
        domains.append(domain)

    # Iterate through each domain name
    for domain in domains:
        # Create the API URL for the domain
        url = f"https://api.apilayer.com/whois/check?domain={domain}"

        # Prepare the API request
        payload = {}
        headers = {"apikey": api_key}

        print(f"Checking {domain}...")
        print("===================================")

        # Send the API request
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code

        # Process the API response
        if status_code == 200:
            try:
                result = response.json()
                registration_status = result.get("result")
                if registration_status == "registered":
                    message = f"{domain} is still registered!"
                elif registration_status == "available":
                    message = f"{domain} is available."
                else:
                    message = f"Unexpected registration status for {domain}: {registration_status}"
                print("Sending message to Discord...")
                send_to_discord(message)
            except ValueError:
                print(f"Error: Unable to parse JSON response for {domain}.")
        else:
            print(f"Error: {status_code}")
            print("Response:", response.text)

        print("===================================")


# Call the get_domains function to start the program
get_domains()
