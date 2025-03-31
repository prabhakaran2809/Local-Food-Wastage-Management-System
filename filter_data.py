import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
def get_connection():
    """Establish a database connection."""
    return sqlite3.connect("DS_Project_local_food_wastage_database.db")

# Filtering Functions
def filter_providers(provider_id=None):
    """Fetch providers based on ID (or all providers if None)."""
    conn = get_connection()
    query = "SELECT * FROM Providers" if provider_id is None else f"SELECT * FROM Providers WHERE Provider_ID = {provider_id}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_receivers(receiver_id=None):
    """Fetch receivers based on ID (or all receivers if None)."""
    conn = get_connection()
    query = "SELECT * FROM Receivers" if receiver_id is None else f"SELECT * FROM Receivers WHERE Receiver_ID = {receiver_id}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_food_listings(food_id=None):
    """Fetch food listings based on ID (or all listings if None)."""
    conn = get_connection()
    query = "SELECT * FROM Food_Listings" if food_id is None else f"SELECT * FROM Food_Listings WHERE Food_ID = {food_id}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_claims(claim_id=None):
    """Fetch claims based on ID (or all claims if None)."""
    conn = get_connection()
    query = "SELECT * FROM Claims" if claim_id is None else f"SELECT * FROM Claims WHERE Claim_ID = {claim_id}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI
def filter_data_page():
    """Streamlit UI for filtering data based on ID."""
    st.title("🔍 Filter Data by ID")

    # Sidebar selection
    filter_option = st.selectbox("Choose a Table to Filter", ["Providers", "Receivers", "Food Listings", "Claims"])

    # User input for filtering
    if filter_option == "Providers":
        provider_id = st.text_input("Enter Provider ID (Leave Blank for All)")
        df = filter_providers(int(provider_id)) if provider_id else filter_providers()

    elif filter_option == "Receivers":
        receiver_id = st.text_input("Enter Receiver ID (Leave Blank for All)")
        df = filter_receivers(int(receiver_id)) if receiver_id else filter_receivers()

    elif filter_option == "Food Listings":
        food_id = st.text_input("Enter Food ID (Leave Blank for All)")
        df = filter_food_listings(int(food_id)) if food_id else filter_food_listings()

    elif filter_option == "Claims":
        claim_id = st.text_input("Enter Claim ID (Leave Blank for All)")
        df = filter_claims(int(claim_id)) if claim_id else filter_claims()

    # Display Results
    st.subheader(f"📋 Filtered Data: {filter_option}")
    if df.empty:
        st.write("No matching data found.")
    else:
        st.dataframe(df)
