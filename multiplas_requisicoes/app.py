from dotenv import load_dotenv

import pandas as pd
import asyncio 
import functools
import httpx
import os


load_dotenv()


try:
    TOKEN = os.getenv("TOKEN")
    URL_RISK_DEALS = os.getenv("URL_RISK_DEALS")
    URL_ACCOUNTS = os.getenv("URL_ACCOUNTS")
    URL_RISK_STATS = os.getenv("URL_RISK_STATS")
except Exception as e:
    print(f'Error: {e}, Please check your .env file!')


def transform(func):
    @functools.wraps(func) 
    async def wrapper(*args, **kwargs):

        response_data = await func(*args, **kwargs)
        
        if isinstance(response_data, list):
            df = pd.json_normalize(response_data)
        elif isinstance(response_data, dict) and response_data:

            df = pd.json_normalize(response_data)
        else:
            df = pd.DataFrame()
        

        return df 
    
    return wrapper 


class Analysis:

        
    @staticmethod
    def fast_trades(data_frame) -> dict:
        pass

    @staticmethod
    def consistency(data_frame) -> dict:
        pass


@transform    
async def get_trades(client:any,token:str, account_number:str, url:str)-> pd.DataFrame:
    
    print(f"Iniciando get_trades para conta {account_number}! ✔️")
    
    headers = {
        "Authorization":token,
        "Content-Type": "application/json"
    }

    params = {
        "filter[account_number][_eq]": account_number,
        "limit":-1
    }

    try:

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()['data']

        return data
    except Exception as e:
        return {}


@transform
async def get_account_info(client:any,token:str, account_number:str, url:str)-> pd.DataFrame:
    
    print(f"Iniciando get_account_info para conta {account_number}! 🚨")
    
    headers = {
        "Authorization":token,
        "Content-Type": "application/json"
    }

    params = {
        "filter[account_number][_eq]": account_number,
        "limit":-1
    }
    
    try:

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()['data']

        return data
    except Exception as e:
        return {}


@transform
async def get_stats(client:any,token:str, account_number:str, url:str) -> pd.DataFrame:

    print(f"Iniciando get_stats para conta {account_number}! ⚡")

    headers = {
        "Authorization":token,
        "Content-Type": "application/json"
    }

    params = {
        "filter[account_number][_eq]": account_number,
        "limit":-1
    }

    try:

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()['data']

        return data
    except Exception as e:
        return {}


async def get_analysis():
    pass


async def main():

    async with httpx.AsyncClient() as client:

        trades_df, accounts_df, stats_df = await asyncio.gather(
            get_trades(
                client,
                token=TOKEN,
                account_number="8800",
                url=URL_RISK_DEALS
            ),
            get_account_info(
                client,
                token=TOKEN,
                account_number="8800",
                url=URL_ACCOUNTS
            ),
            get_stats(
                client,
                token=TOKEN,
                account_number="8800",
                url=URL_RISK_STATS
            )
        )
    


if __name__  == "__main__":
    asyncio.run(main())