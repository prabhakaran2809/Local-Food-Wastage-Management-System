import streamlit as st
import sqlite3
import pandas as pd

# Database Connection
def get_connection():
    """Establish a database connection."""
    return sqlite3.connect("DS_Project_local_food_wastage_database.db")

# Filtering Functions
def filter_providers(provider_id=None, provider_name=None, provider_type=None, city=None):
    """Fetch providers based on ID, name, type, or city."""
    conn = get_connection()
    query = "SELECT * FROM Providers WHERE 1=1"
    
    if provider_id:
        query += f" AND Provider_ID = {provider_id}"
    if provider_name:
        query += f" AND Name LIKE '%{provider_name}%'"
    if provider_type:
        query += f" AND Type = '{provider_type}'"
    if city:
        query += f" AND City LIKE '%{city}%'"
        
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_receivers(receiver_id=None, receiver_name=None, city=None, receiver_type=None):
    """Fetch receivers based on ID, name, city, or type."""
    conn = get_connection()
    query = "SELECT * FROM Receivers WHERE 1=1"
    
    if receiver_id:
        query += f" AND Receiver_ID = {receiver_id}"
    if receiver_name:
        query += f" AND Name LIKE '%{receiver_name}%'"
    if city:
        query += f" AND City LIKE '%{city}%'"
    if receiver_type:
        query += f" AND Type = '{receiver_type}'"
        
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_food_listings(food_id=None, food_type=None, meal_type=None, location=None, provider_type=None):
    """Fetch food listings based on ID, food type, meal type, location, or provider type."""
    conn = get_connection()
    query = "SELECT * FROM Food_Listings WHERE 1=1"
    
    if food_id:
        query += f" AND Food_ID = {food_id}"
    if food_type:
        query += f" AND Food_Type = '{food_type}'"
    if meal_type:
        query += f" AND Meal_Type = '{meal_type}'"
    if location:
        query += f" AND Location LIKE '%{location}%'"
    if provider_type:
        query += f" AND Provider_Type = '{provider_type}'"
        
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_claims(claim_id=None, status=None):
    """Fetch claims based on ID or status."""
    conn = get_connection()
    query = "SELECT * FROM Claims WHERE 1=1"
    
    if claim_id:
        query += f" AND Claim_ID = {claim_id}"
    if status:
        query += f" AND Status = '{status}'"
        
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit UI
def filter_data_page():
    """Streamlit UI for filtering data based on multiple parameters."""
    st.title("🔍 Filter Data")

    # Sidebar selection
    filter_option = st.selectbox("Choose a Table to Filter", ["Providers", "Receivers", "Food Listings", "Claims"])

    # Filtering UI based on selection
    if filter_option == "Providers":
        provider_id = st.text_input("Enter Provider ID (Leave Blank for All)")
        provider_name = st.text_input("Enter Provider Name (Leave Blank for All)")
        provider_type = st.selectbox("Select Provider Type", ["All", "Restaurant", "Supermarket", "Catering Service", "Grocery Store"])
        city = st.text_input("Enter City (Leave Blank for All)")

        provider_type = None if provider_type == "All" else provider_type
        df = filter_providers(int(provider_id) if provider_id else None, provider_name or None, provider_type, city or None)

    elif filter_option == "Receivers":
        receiver_id = st.text_input("Enter Receiver ID (Leave Blank for All)")
        receiver_name = st.text_input("Enter Receiver Name (Leave Blank for All)")
        city = st.text_input("Enter City (Leave Blank for All)")
        receiver_type = st.selectbox("Select Receiver Type", ["All", "Charity", "NGO", "Individual", "Shelter"])

        receiver_type = None if receiver_type == "All" else receiver_type
        df = filter_receivers(int(receiver_id) if receiver_id else None, receiver_name or None, city or None, receiver_type)

    elif filter_option == "Food Listings":
        food_id = st.text_input("Enter Food ID (Leave Blank for All)")
        food_type = st.selectbox("Select Food Type", ["All", "Vegetarian", "Vegan", "Non-Vegetarian"])
        meal_type = st.selectbox("Select Meal Type", ["All", "Breakfast", "Lunch", "Snacks", "Dinner"])
        location = st.text_input("Enter Location (Leave Blank for All)")
        provider_type = st.selectbox("Select Provider Type", ["All", "Restaurant", "Supermarket", "Catering Service", "Grocery Store"])

        food_type = None if food_type == "All" else food_type
        meal_type = None if meal_type == "All" else meal_type
        provider_type = None if provider_type == "All" else provider_type

        df = filter_food_listings(int(food_id) if food_id else None, food_type, meal_type, location or None, provider_type)

    elif filter_option == "Claims":
        claim_id = st.text_input("Enter Claim ID (Leave Blank for All)")
        status = st.selectbox("Select Claim Status", ["All", "Pending", "Completed", "Cancelled"])

        status = None if status == "All" else status
        df = filter_claims(int(claim_id) if claim_id else None, status)

    # Display Results
    st.subheader(f"📋 Filtered Data: {filter_option}")
    if df.empty:
        st.write("No matching data found.")
    else:
        st.dataframe(df)
