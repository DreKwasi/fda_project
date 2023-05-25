from firebase_admin import credentials, storage as fb_storage
import firebase_admin
from google.cloud import storage
from google.oauth2 import service_account
import time
import streamlit as st
import json
from google.oauth2 import service_account
import pandas as pd

# key_dict = json.loads(st.secrets["firestore_auth"])
cred = st.secrets["firestore_auth"]
with open("cred.json", "w") as f:
    json.dump(cred, f, default=dict)

if not firebase_admin._apps:
    firebase_cred = credentials.Certificate("cred.json")
    app = firebase_admin.initialize_app(
        firebase_cred,
        {"storageBucket": "fdaproject-7ce4d.appspot.com"},
    )
bucket_name = fb_storage.bucket().name
google_cred = service_account.Credentials.from_service_account_file("cred.json")

# connecting to firebase

# file_path = "text_docs/sample_text_file.txt"
# bucket = storage.bucket() # storage bucket
# blob = bucket.blob(file_path)
# blob.upload_from_filename(file_path)


def upload_blob(source_file_name, destination_blob_name):
    storage_client = storage.Client(credentials=google_cred)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


@st.cache_resource(show_spinner="Accessing Database ...", ttl=3*3600)
def download_blob(source_file_name, destination_blob_name):
    start = time.perf_counter()
    
    storage.Client(credentials=google_cred).bucket(bucket_name).blob(
        source_file_name
    ).download_to_filename(destination_blob_name)
    data = pd.read_parquet(destination_blob_name)
    end = time.perf_counter()
    st.write(f"Total Time: {end - start}")
    return data


if __name__ == "__main__":
    start = time.perf_counter()

    # upload_blob(
    #     "registered_products.parquet",
    #     "data/registered_products.parquet",
    # )
    download_blob(
        "data/registered_products.parquet",
        "assets/registered_products.parquet",
    )

    end = time.perf_counter()
    print(f"Total Time: {end - start}")
