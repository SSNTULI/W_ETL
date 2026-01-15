import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

Api_key = os.getenv("Api_key")

def get_finance_id():

    try:
        url = f'https://api.massive.com/v3/reference/dividends?apiKey={Api_key}'
        res = requests.get(url)
        
        data = res.json()

        #print(json.dumps(data,indent=4))
        print(data['results'][0]['id'])
        return data['results'][0]['id']

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    get_finance_id()
