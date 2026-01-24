from airflow import DAG
import pendulum 
from datetime import datetime , timedelta
from api.financial_data import get_finance_id,get_divident_ids,get_data