import httpx
import asyncio
import time
import copy
import pandas as pd
from helper_func.firestore_func import upload_blob



URL = "http://196.61.32.245:98/publicsearch"
cookie = "XSRF-TOKEN=eyJpdiI6ImhHd2xjVkVTS2lQRlZrUVFzWisyamc9PSIsInZhbHVlIjoibG9taE5HSm1ORC9SWE42aW15L1dHZGIvVlpLSDNZSzAySWRRWXdSZDVwOW11blh6OHZTd0JYa0tsOFJTeXFoNTBUUzhmNzJHc09mSElHK3pFbmFtT3VsMTRHYTh3Z2IvVDErWGFKMTJqWHRaUWhtT296LzNTVXVKWXdMYjJtWE4iLCJtYWMiOiJiMWJhZjdjYWZhODcwNjRjNGU1MmE3NWRmMjFkMWMwZDAzNmNmMzUyM2EyN2U2ZDk0YTVkZWUxMzA5MWVhYjNlIiwidGFnIjoiIn0%3D; clientdbs_v3_session=eyJpdiI6IjlmY3ZHZjdRT0YvLzFmWVQ0RGxZdmc9PSIsInZhbHVlIjoiai93Z1d6dmtLSklDRjdSalh2Y3RmZmRvTTQ0aDFacXNtanBWRkY2ZmlUdDQyQXdPWlhnTkJPQ0tqTTBtOGxhNVN3b2VCSlZ0emNpMDlGYWQxOUpIcGwyenA1ZFp4OXlpRUFtcUpOenZBUW9MQVdsTXZBZTk5R0JoWnM5c2VXVGgiLCJtYWMiOiIyNDJlYzBkN2FhNGNiNWM3NjM4NjcxNGVkMzBlNDhjNmJjZmU3OWUwY2ZhYzEyNDMwZjAzOWRjYjg3NTE1ZWYxIiwidGFnIjoiIn0%3D"
RECORDS = 5000
PARAMS = {
    "draw": 1,
    "columns[0][data]": "DT_RowIndex",
    # "columns[0][searchable]": false
    "columns[1][data]": "client_name",
    "columns[1][name]": "tbl_client_details.client_name",
    "columns[2][data]": "product_name",
    "columns[3][data]": "product_category",
    "columns[4][data]": "expiry_date",
    "columns[5][data]": "status",
    "columns[5][name]": "tbl_products_details.status",
    "order[0][column]": "1",
    "order[0][dir]": "desc",
    "start": 0,
    "length": f"{RECORDS}",
    "search[value]": "",
    "_": "1684885652658",
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


async def get_data(client, url, params):
    response = await client.get(url, params=params)
    return response.json()['data']


async def main():
    start = time.perf_counter()
    api_calls = []
    async with httpx.AsyncClient(headers=HEADERS) as client:
        for i in range(0, 40_000, RECORDS):
            params_copy = copy.deepcopy(
                PARAMS
            )  # Create a copy of PARAMS for each iteration

            params_copy["start"] = i

            api_calls.append(get_data(client=client, url=URL, params=params_copy))
            del params_copy

        json_list = await asyncio.gather(*api_calls)
        # for response in json_list:
            # print(f"Total Records: {response.json()['recordsTotal']}")
            # print(f"Start: {response['input']['start']}")
            # print(f"Data: {response['data']}")

    df = pd.DataFrame((dict_data for inner_list in json_list for dict_data in inner_list))
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
    df.to_parquet("registered_products.parquet")
    end = time.perf_counter()
    print(f"Total Time (Api Calls): {end - start}")
    
    start = time.perf_counter()
    upload_blob("registered_products.parquet", "data/registered_products.parquet")
    end = time.perf_counter()
    print(f"Total Time (Uploading To Firestore): {end - start}")

if __name__ == "__main__":
    asyncio.run(main())
