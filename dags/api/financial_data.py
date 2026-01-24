import requests
import json
import os
from dotenv import load_dotenv
from datetime import date

from airflow.decorators import task
from airflow.model import Variable


#load_dotenv(dotenv_path="./.env")

#Api_key = os.getenv("Api_key")
Api_key = Variable.get("Api_key")

max_result = 10

@task
def get_finance_id():

    try:
        url = f'https://api.massive.com/v3/reference/dividends?apiKey={Api_key}'
        res = requests.get(url)
        
        data = res.json()
        #print(json.dumps(data,indent=4))
        #print(data['results'][0]['id'])   
        return data['results'][0]['id']

    except requests.exceptions.RequestException as e:
        raise e

@task 
def get_divident_ids():
    divident_ids = []
    url = f'https://api.massive.com/v3/reference/dividends?apiKey={Api_key}'

    try:
        res = requests.get(url)
        data = res.json()

        for i in range(len(data['results'])):
            divident_ids.append(data['results'][i]['id'])
        return divident_ids
    
    except requests.exceptions.RequestException as e:
        raise e

@task
def get_data():

    extracted_data = []
    url = f'https://api.massive.com/v3/reference/dividends?apiKey={Api_key}'

    try:

        res = requests.get(url)
        data = res.json()

        for i in range(len(data['results'])):
            
            filtered_data = {
                "id":data['results'][i]["id"],
                "amount":data['results'][i]["cash_amount"],
                "frequency":data['results'][i]['frequency'],
                "date":data['results'][i]['pay_date'],
                "ticker":data['results'][i]['ticker']
            }

            extracted_data.append(filtered_data)
        return extracted_data 

    except requests.exceptions.RequestException as e:
        raise e
    
@task    
def save_to_jason(extracted_data):
    file_path = f"./data/divident_{date.today()}.json"
    with open(file_path,"w",encoding="utf-8") as json_ouput:
        json.dump(extracted_data,json_ouput,indent=4,ensure_ascii=False)

if __name__ == "__main__":
    get_finance_id()
    get_divident_ids()
    extracted_data = get_data()
    save_to_jason(extracted_data)
