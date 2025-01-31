import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Enable full-screen mode
st.set_page_config(layout="wide")

# Custom CSS to match the provided UI design
custom_css = """
<style>
    body {
        background-color: white;
        font-family: Tahoma;
        color: black;
    }
    .stApp {
        background-color: white;
    }
    .custom-header {
        font-size: 20px;
        font-weight: bold;
        color: black;
        background-color: white;
        padding: 10px;
        text-align: center;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Custom header to match UI
def custom_header():
    st.markdown("""
    <div class="custom-header">
        🔧 Sungrow Malaysia Service
    </div>
    """, unsafe_allow_html=True)

# Load credentials from Streamlit Secrets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
SPREADSHEET_ID = "1y06jOiqqFZFuBExnKIe3vF3ijXo6p2dDjgzelUx-ac4"
SHEET_NAME = "GSP - MY (2025)"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# Login System
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Enter Your Credentials to Access")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if username == "admin" and password == "pw1111":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials! Please try again.")
else:
    st.success("✅ Access granted!")
    custom_header()

    # Create tabs
    tab1, tab2 = st.tabs(["📊 Warranty Ticket Summary", "🔎 Search Warranty Ticket"])

    # 📊 Tab 1: Display the full sheet
    with tab1:
        st.subheader("📊 Warranty Ticket Summary")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("⚠️ No tickets found!")
        else:
            st.dataframe(df)  # Display data in table format

    # 🔎 Tab 2: Search Warranty Ticket
    with tab2:
        st.subheader("🔎 Search Warranty Ticket by APAC Ticket or Service Ticket")
        search_type = st.radio("Search by:", ["APAC Ticket", "Service Ticket"])
        search_query = st.text_input(f"Enter {search_type}")

        if st.button("Search"):
            if not search_query:
                st.error("⚠️ Please enter a ticket number!")
            else:
                df = pd.DataFrame(sheet.get_all_records())  # Load full data
                result = df[df[search_type] == search_query]

                if not result.empty:
                    st.success("✅ Ticket found!")
                    display_option = st.radio("What data do you want to see?", ["All Data", "Select Specific Data"], index=None)
                    
                    if display_option == "All Data":
                        st.write("### Ticket Details")
                        formatted_data = pd.DataFrame({
                            "Parameter": result.columns.tolist(),
                            "Details": result.iloc[0].values
                        })
                        st.table(formatted_data)
                    
                    elif display_option == "Select Specific Data":
                        selected_columns = st.multiselect("Select Data to Display", result.columns.tolist())
                        if selected_columns:
                            st.write("### Selected Data")
                            formatted_data = pd.DataFrame({
                                "Parameter": selected_columns,
                                "Details": result.iloc[0][selected_columns].values
                            })
                            st.table(formatted_data)
                        else:
                            st.warning("⚠️ Please select at least one data field to display.")
                else:
                    st.error("❌ Ticket not found! Please check the ticket number and try again.")
