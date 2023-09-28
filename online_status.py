import requests
from datetime import datetime, timedelta

api_url = "https://sef.podkolzin.consulting/api/users/lastSeen?offset=0"

# Commit Message: Add function for loading user data from the API

def load_user_data(offset):
    try:
        response = requests.get(api_url + str(offset))
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None



