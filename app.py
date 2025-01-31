import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

st.title("🔧 Malaysia GSP Warranty Ticket Database")
st.write("Welcome to the Warranty Ticket Database!")

try:
    # Define the correct OAuth scopes
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load credentials from Streamlit Secrets
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )

    # Authorize Google Sheets access
    client = gspread.authorize(creds)

    # Open Google Sheet (Using Your Actual Sheet ID)
    SPREADSHEET_ID = "1y06jOiqqFZFuBExnKIe3vF3ijXo6p2dDjgzelUx-ac4"
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Open the specific sheet
    SHEET_NAME = "GSP - MY (2025)"
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
# Fetch column headers from Google Sheet
headers = sheet.row_values(1)  # Assuming headers are in the first row

# Section to Add New Ticket
st.subheader("➕ Add New Ticket")

with st.form("new_ticket_form"):
    user_inputs = {}  # Store user inputs dynamically

    for header in headers:
        user_inputs[header] = st.text_input(header, placeholder=f"Enter {header}")

    submit_button = st.form_submit_button("Submit Ticket")

    if submit_button:
        # Check if required fields (APAC Ticket & PIC) are filled
        if not user_inputs["APAC Ticket"] or not user_inputs["PIC"]:
            st.error("⚠️ APAC Ticket and PIC are required!")
        else:
            # Convert user input to a list (matching column order)
            new_row = [user_inputs[col] for col in headers]
            sheet.append_row(new_row)
            st.success("✅ Ticket added successfully!")
