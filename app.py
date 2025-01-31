import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Enable full-screen mode
st.set_page_config(layout="wide")

# Custom styling for smaller title
st.markdown("<h2 style='text-align: center;'>🔧 Sungrow Malaysia Ticket Database</h2>", unsafe_allow_html=True)

# Load credentials from Streamlit Secrets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
SPREADSHEET_ID = "1y06jOiqqFZFuBExnKIe3vF3ijXo6p2dDjgzelUx-ac4"
SHEET_NAME = "GSP - MY (2025)"
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# Initialize session state for user authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# User Authentication
if not st.session_state.authenticated:
    st.subheader("🔐 Enter Your Name to Access")

    with st.form("login_form"):
        username = st.text_input("Enter PIC Name", placeholder="Enter your name here")
        submit = st.form_submit_button("Login")

        if submit:
            if username.strip().lower() == "nabil":
                st.session_state.authenticated = True
                st.rerun()  # Refresh the page after successful login
            else:
                st.error("❌ Access Denied! Please enter a valid PIC name.")
else:
    st.success("✅ Access granted!")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 View Tickets", "📝 Add New Ticket", "🔎 Search Ticket"])

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

        # Define dropdown options based on Excel analysis
        dropdown_options = {
            "Material Application": ["On Hold", "Completed"],
            "Post & Ship": ["On Hold", "Completed"],
            "Material Recieve": ["On Hold", "Completed"],
            "Material Consumption": ["On Hold", "Completed"],
            "Return Faulty": ["On Hold", "Scrap"],
            "Ticket Status": ["Approving", "Closed"]
        }

        with st.form("new_ticket_form"):
            user_inputs = {}  # Store user inputs dynamically

            for header in headers:
                if header in dropdown_options:
                    user_inputs[header] = st.selectbox(header, dropdown_options[header])
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

    # 🔎 Tab 3: Search Ticket
    with tab3:
        st.subheader("🔎 Search Ticket by APAC Ticket or Service Ticket")

        search_type = st.radio("Search by:", ["APAC Ticket", "Service Ticket"])
        search_query = st.text_input(f"Enter {search_type}")

        if st.button("Search"):
            if not search_query:
                st.error("⚠️ Please enter a ticket number!")
            else:
                df = pd.DataFrame(sheet.get_all_records())  # Load full data
                
                # Search for APAC Ticket or Service Ticket
                result = df[df[search_type] == search_query]

                if not result.empty:
                    st.success("✅ Ticket found!")

                    # Ask user whether to display all or select specific fields
                    display_option = st.radio("What data do you want to see?", ["All Data", "Select Specific Data"])

                    if display_option == "All Data":
                        st.dataframe(result)
                    else:
                        # Allow user to select specific columns
                        selected_columns = st.multiselect("Select Data to Display", result.columns.tolist())

                        if selected_columns:
                            # Display selected data in a vertical table format
                            formatted_data = pd.DataFrame({
                                "Parameter": selected_columns,
                                "Details": result.iloc[0][selected_columns].values
                            })
                            st.table(formatted_data)
                        else:
                            st.warning("⚠️ Please select at least one data field to display.")
                else:
                    st.error("❌ Ticket not found! Please check the ticket number and try again.")