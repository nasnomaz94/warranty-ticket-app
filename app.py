import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Enable full-screen mode
st.set_page_config(layout="wide")

# App title
st.title("🔧 Malaysia GSP Warranty Ticket Database")

# Load credentials from Streamlit Secrets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
SPREADSHEET_ID = "1y06jOiqqFZFuBExnKIe3vF3ijXo6p2dDjgzelUx-ac4"
SHEET_NAME = "GSP - MY (2025)"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# Create tabs
tab1, tab2 = st.tabs(["📊 View Tickets", "📝 Add New Ticket"])

# 📊 Tab 1: View the full sheet
with tab1:
    st.subheader("📊 All Tickets")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.warning("⚠️ No tickets found!")
    else:
        st.dataframe(df)  # Display data in table format

# 📝 Tab 2: Form to Add New Ticket
with tab2:
    st.subheader("📝 Add New Ticket")

    # Fetch column headers from Google Sheet
    headers = sheet.row_values(1)  # Assuming headers are in the first row

    # Define which columns should use dropdowns (Replace with actual dropdown columns)
    dropdown_columns = ["Column1", "Column2", "Column3"]  # Example: ["Status", "Priority", "Category"]

    with st.form("new_ticket_form"):
        user_inputs = {}  # Store user inputs dynamically

        for header in headers:
            if header in dropdown_columns:
                dropdown_values = sheet.col_values(headers.index(header) + 1)[1:]  # Get dropdown values (excluding header)
                dropdown_values = list(set(dropdown_values))  # Remove duplicates
                user_inputs[header] = st.selectbox(header, dropdown_values)
            else:
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
