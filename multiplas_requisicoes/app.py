from dotenv import load_dotenv

import pandas as pd
import asyncio 
import functools
import httpx
import os
import logging


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


try:
    TOKEN = os.getenv("TOKEN")
    URL_RISK_DEALS = os.getenv("URL_RISK_DEALS")
    URL_ACCOUNTS = os.getenv("URL_ACCOUNTS")
    URL_RISK_STATS = os.getenv("URL_RISK_STATS")
except Exception as e:
    logger.error(f'Error: {e}, Please check your .env file!')


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
        
        logger.info("Iniciando fast_trades! ⚡")
        logger.debug(f"Data frame: {data_frame}")
        if data_frame.empty:
            logger.warning("Não há dados para o conta ❌")
            return {}
        
        data_frame['duration'] = data_frame['duration'].astype('float')

        fast_trades = data_frame[data_frame['duration'] < 60].to_dict(orient='records')
        
        return fast_trades



@transform    
async def get_trades(client:any,token:str, account_number:str, url:str)-> pd.DataFrame:
    
    logger.info(f"Iniciando get_trades para conta {account_number}! ✔️")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "filter[account_number][_eq]": account_number,
        "limit":-1
    }

    try:

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()
        data = response_json.get('data', [])

        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"[get_trades] HTTP Error {e.response.status_code}: {e.response.text}")
        return {}
    except Exception as e:
        logger.error(f"[get_trades] Error: {type(e).__name__}: {e}")
        return {}


@transform
async def get_account_info(client:any,token:str, account_number:str, url:str)-> pd.DataFrame:
    
    logger.info(f"Iniciando get_account_info para conta {account_number}! 🚨")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "filter[account_number][_eq]": account_number,
        "limit":-1
    }
    
    try:

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()
        logger.info(f"[get_account_info] Response status: {response.status_code}")
        data = response_json.get('data', [])

        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"[get_account_info] HTTP Error {e.response.status_code}: {e.response.text}")
        return {}
    except Exception as e:
        logger.error(f"[get_account_info] Error: {type(e).__name__}: {e}")
        return {}


@transform
async def get_stats(client:any,token:str, account_number:str, url:str) ->pd.DataFrame:

    logger.info(f"Iniciando get_stats para conta {account_number}! ⚡")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "filter[account_number][_eq]": account_number,
        "limit":-1
    }

    try:

        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()
        data = response_json.get('data', [])

        return data
    except httpx.HTTPStatusError as e:
        logger.error(f"[get_stats] HTTP Error {e.response.status_code}: {e.response.text}")
        return {}
    except Exception as e:
        logger.error(f"[get_stats] Error: {type(e).__name__}: {e}")
        return {}



async def main():

    async with httpx.AsyncClient() as client:

        trades_df, accounts_df, stats_df = await asyncio.gather(
            get_trades(
                client,
                token=TOKEN,
                account_number="8837",
                url=URL_RISK_DEALS
            ),
            get_account_info(
                client,
                token=TOKEN,
                account_number="8837",
                url=URL_ACCOUNTS
            ),
            get_stats(
                client,
                token=TOKEN,
                account_number="8837",
                url=URL_RISK_STATS
            )
        )
    
    fast_trades = Analysis.fast_trades(trades_df)
    logger.info(f"Fast trades < 60s: {len(fast_trades)}")
    logger.info(f"Accounts result: {accounts_df}")
    logger.info(f"Stats result: {stats_df}")

if __name__  == "__main__":
    asyncio.run(main())