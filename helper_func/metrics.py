import pandas as pd
import streamlit as st
from helper_func.data_parser import human_format


def number_of_applicants(data):
    return human_format(data['applicant'][data['applicant'] != "Not Specified"].nunique())

def number_of_products(data):
    return human_format(data['product_uuid'][data['product_uuid'] != "Not Specified"].nunique())

def number_of_registrations(data):
    return human_format(data['registration_number'][data['registration_number'] != "Not Specified"].nunique())

def number_of_renewals(data):
    return human_format(data[data['registration_type'] == "Renewal"].shape[0])