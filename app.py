import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

st.title("🔧 Malaysia GSP Warranty Ticket Database")
st.write("Welcome to the Warranty Ticket Database!")

# Load credentials from Streamlit Secrets
try:
    creds_dict = st.secrets["gcp_service_account"]  # No need for json.loads()
    creds = Credentials.from_service_account_info(creds_dict)

    client = gspread.authorize(creds)

    # Open Google Sheet
    SPREADSHEET_ID = "1y06jOiqqFZFuBExnKIe3vF3ijXo6p2dDjgzelUx-ac4"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Open specific sheet
    SHEET_NAME = "GSP - MY (2024)"
    sheet = spreadsheet.worksheet(SHEET_NAME)

    # Fetch data
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("⚠️ No data found in Google Sheet!")
    else:
        st.dataframe(df)

except Exception as e:
    st.error(f"Error loading data: {e}")