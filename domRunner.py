import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
domains = []
prompt = "Enter domain names (or 'quit' to exit): "
while True:
    domain = input(prompt)
    if domain == "quit":
        break
    domains.append(domain)
for domain in domains:
    url = f"https://api.apilayer.com/whois/check?domain={domain}"
    payload = {}
    headers = {"apikey": api_key}

    print(f"Checking {domain}...")
    print("===================================")

    response = requests.request("GET", url, headers=headers, data=payload)
    status_code = response.status_code
    result = response.text

    # print the results
    print(result)
    print("===================================")
