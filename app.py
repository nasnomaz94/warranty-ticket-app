import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

st.title("🔧 Malaysia GSP Warranty Ticket Database")
st.write("Welcome to the Warranty Ticket Database!")

# Path to JSON key file
json_key_path = "lyrical-cacao-449509-f7-c73130c05ea5.json"

try:
    # Authenticate with Google Sheets
    creds = Credentials.from_service_account_file(json_key_path, scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
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

    # Debug: Check if DataFrame is empty
    if df.empty:
        st.warning("⚠️ No data found in Google Sheet!")
    else:
        st.dataframe(df)  # Show data in table format

except Exception as e:
    st.error(f"Error loading data: {e}")

