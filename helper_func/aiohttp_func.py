import aiohttp
import asyncio
import time
import copy
import pandas as pd
from helper_func.firestore_func import upload_blob
import streamlit as st


URL = "http://196.61.32.245:98/publicsearch"
RECORDS = 5000
PARAMS = {
    "draw": 1,
    # "columns[0][data]": "DT_RowIndex",
    # # "columns[0][searchable]": false
    # "columns[1][data]": "client_name",
    # "columns[1][name]": "tbl_client_details.client_name",
    # "columns[2][data]": "product_name",
    # "columns[3][data]": "product_category",
    # "columns[4][data]": "expiry_date",
    # "columns[5][data]": "status",
    # "columns[5][name]": "tbl_products_details.status",
    # "order[0][column]": "1",
    # "order[0][dir]": "desc",
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


async def get_data(session, url, params):
    async with session.get(url, params=params) as response:
        json_data = await response.json()
    return json_data["data"]

async def main_async_call():
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
            api_call = asyncio.create_task(get_data(session, URL, params_copy))
            api_calls.append(api_call)
            del params_copy

        json_list = await asyncio.gather(*api_calls)

    df = pd.DataFrame(
        (dict_data for inner_list in json_list for dict_data in inner_list)
    )
    df.drop("action", axis=1, inplace=True)
    df = df.astype(
        {
            "client_ref_uuid": "string",
            "client_ref_number": "string",
            "client_name": "string",
            "postal_address": "string",
            "sim_contact": "string",
            "telephone_number": "string",
            "email": "string",
            "dep_bg": "string",
            "created_at": "string",
            "updated_at": "string",
            "registerd_importers": "string",
            "cert_number": "string",
            "registration_type": "string",
            "status": "string",
            "country_origin": "string",
            "region": "category",
            "applicant": "string",
            "product_name": "string",
            "generic_name": "string",
            "strength": "string",
            "classification": "string",
            "active_ingredient": "string",
            "dosage_form_indication": "string",
            "representative_company_local_agent_applicant": "string",
            "manufacturer": "string",
            "registration_date": "string",
            "expiry_date": "string",
            "product_uuid": "string",
            "product_id": "string",
            "product_category": "string",
            "product_sub_category": "string",
            "registration_number": "string",
        }
    )
    columns_with_only_nulls = df.columns[df.isna().all()].tolist()
    df = df.drop(columns_with_only_nulls, axis=1)
    df.to_parquet("assets/registered_products.parquet")
    end = time.perf_counter()
    
    print(f"Total Time (Api Calls): {end - start}")
    st.write(f"Total Time (Api Calls): {end - start}")
    

    start = time.perf_counter()
    upload_blob(
        "assets/registered_products.parquet",
        "data/registered_products.parquet",
    )
    end = time.perf_counter()
    print(f"Total Time (Uploading To Firestore): {end - start}")
    st.write(f"Total Time (Uploading To Firestore): {end - start}")
    

if __name__ == "__main__":
    asyncio.run(main_async_call())
