import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import aiohttp
import asyncio
import time
import copy
import pandas as pd
from helper_func.firestore_func import upload_blob
from aiolimiter import AsyncLimiter
import json
from html import unescape

URL = "http://196.61.32.245:98/publicsearch"
RECORDS = 5000
PARAMS = {
    "draw": 1,
    "start": 0,
    "length": f"{RECORDS}",
    # "search[value]": "",
    # "_": "1684885652658",
}
HEADERS = {
    # "Cookie": cookie,
    "DNT": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Referer": "http://196.61.32.245:98/publicsearch",
    "X-Requested-With": "XMLHttpRequest",
    "Host": "196.61.32.245:98",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}


async def get_total_records(session, url, params):
    async with session.get(url, params=params) as response:
        json_data = await response.json()
    return json_data["recordsTotal"]


async def get_data(session, url, params, limiter):
    async with limiter:
        async with session.get(url, params=params) as response:
            json_data = await response.json()
    data = json_data["data"]
    return data


async def main_async_call():
    limiter = AsyncLimiter(2, 2)

    start = time.perf_counter()
    api_calls = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        first_params = copy.deepcopy(PARAMS)
        first_params["length"] = 5
        total_records = await get_total_records(session, URL, first_params)
        # total_records = total_records - 40253
        print(total_records)
        for i in range(0, total_records, RECORDS):
            params_copy = copy.deepcopy(
                PARAMS
            )  # Create a copy of PARAMS for each iteration

            params_copy["start"] = i
            params_copy["draw"] = i
            api_call = asyncio.create_task(get_data(session, URL, params_copy, limiter))
            api_calls.append(api_call)
            del params_copy

        json_list = await asyncio.gather(*api_calls)

    df = pd.DataFrame(
        (dict_data for inner_list in json_list for dict_data in inner_list)
    )
    end = time.perf_counter()
    print(f"Total Time (Api Calls): {end - start}")

    start = time.perf_counter()
    df.drop("action", axis=1, inplace=True)
    data_types = {
        "id": int,
        "product_uuid": str,
        "product_id": str,
        "client_id": str,
        "dpt_id": str,
        "product_category": str,
        "product_sub_category": str,
        "registration_number": str,
        "product_name": str,
        "generic_name": str,
        "strength": str,
        "classification": str,
        "active_ingredient": str,
        "dosage_form_indication": str,
        "representative_company_local_agent_applicant": str,
        "manufacturer": str,
        "registration_type": str,
        "status": str,
        "country_origin": str,
        "region": str,
        "applicant": str,
        "variation": str,
        "registerd_importers": str,
        "cert_number": str,
        "hrb_type": str,
        "client_ref_uuid": str,
        "client_ref_number": str,
        "client_name": str,
        "postal_address": str,
        "sim_contact": str,
        "telephone_number": str,
        "email": str,
        "DT_RowIndex": int,
    }
    string_keys = [key for key, value in data_types.items() if value == str]
    df[string_keys] = df[string_keys].fillna("Not Specified").apply(unescape)
    
    df = df.astype(data_types)

    df["registration_date"] = pd.to_datetime(
        df["registration_date"], dayfirst=True, format="mixed", errors="coerce"
    )
    df["expiry_date"] = pd.to_datetime(
        df["expiry_date"], yearfirst=True, errors="coerce"
    )
    df["created_at"] = pd.to_datetime(df["created_at"], format="ISO8601")
    df["updated_at"] = pd.to_datetime(df["updated_at"], format="ISO8601")

    columns_with_only_nulls = df.columns[df.isna().all()].tolist()
    df = df.drop(columns_with_only_nulls, axis=1)
    df = df.apply(
        unescape,
    )
    df.to_parquet("assets/registered_products.parquet")
    end = time.perf_counter()
    print(f"Total Time (Dataset Cleaning): {end - start}")

    start = time.perf_counter()
    upload_blob(
        "assets/registered_products.parquet",
        "data/registered_products.parquet",
    )
    end = time.perf_counter()
    print(f"Total Time (Uploading To Firestore): {end - start}")
    # st.write(f"Total Time (Uploading To Firestore): {end - start}")


if __name__ == "__main__":
    asyncio.run(main_async_call())
