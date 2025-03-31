import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

def get_db_connection():
    return sqlite3.connect("DS_Project_local_food_wastage_database.db", check_same_thread=False)

def manage_crud():
    st.title("🛠️ Manage Data (CRUD Operations)")

    # Select Action & Table
    action = st.selectbox("Select Operation", ["Create", "Read", "Update", "Delete"])
    table = st.selectbox("Select Table", ["providers", "receivers", "food_listings", "claims"])

    # ✅ Open database connection inside the function
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read Data
    if action == "Read":
        st.subheader(f"📋 {table.capitalize()} Table Data")
        df = pd.read_sql_query(f"SELECT * FROM {table};", conn)
        st.dataframe(df)

    # Create Data
    elif action == "Create":
        st.subheader(f"➕ Add New Entry to {table}")

        if table == "providers":
            name = st.text_input("Provider Name")
            provider_type = st.selectbox("Type", ["Restaurant", "Supermarket", "Catering Service", "Grocery Store"])
            address = st.text_input("Address")
            city = st.text_input("City")
            contact = st.text_input("Contact")

            if st.button("Add Provider"):
                cursor.execute("INSERT INTO providers (Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?)",
                               (name, provider_type, address, city, contact))
                conn.commit()
                st.success("Provider Added Successfully!")

        elif table == "receivers":
            name = st.text_input("Receiver Name")
            receiver_type = st.selectbox("Type", ["Charity", "NGO", "Individual", "Shelter"])
            city = st.text_input("City")
            contact = st.text_input("Contact")

            if st.button("Add Receiver"):
                cursor.execute("INSERT INTO receivers (Name, Type, City, Contact) VALUES (?, ?, ?, ?)",
                               (name, receiver_type, city, contact))
                conn.commit()
                st.success("Receiver Added Successfully!")

        elif table == "food_listings":
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date")
            provider_id = st.number_input("Provider ID", min_value=1)

            # Fetch Provider Type and Location automatically
            provider_type, location = "", ""
            if provider_id:
                cursor.execute("SELECT Type, City FROM Providers WHERE Provider_ID = ?", (provider_id,))
                result = cursor.fetchone()
                if result:
                    provider_type, location = result  # Unpack provider type and location

            # Display provider type and location (auto-filled, read-only)
            st.text_input("Provider Type", provider_type, disabled=True)
            st.text_input("Location", location, disabled=True)

            # Dropdowns for Food Type and Meal Type
            food_type = st.selectbox("Food Type", ["Vegetarian", "Vegan", "Non-Vegetarian"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Snacks", "Dinner"])

            if st.button("Add Food Listing"):
                cursor.execute(
                    "INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (food_name, quantity, expiry_date.strftime("%Y-%m-%d 23:59:00"), provider_id, provider_type, location, food_type, meal_type)
                )
                conn.commit()
                st.success("Food Listing Added Successfully!")


        elif table == "claims":
            food_id = st.number_input("Food ID", min_value=1)
            receiver_id = st.number_input("Receiver ID", min_value=1)
            status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
            # Capture the current timestamp when the button is clicked
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if st.button("Add Claim"):
                cursor.execute(
                    "INSERT INTO claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, ?)",
                    (food_id, receiver_id, status, current_timestamp)
                )
                conn.commit()
                st.success("Claim Added Successfully!")

    # Update Data
    elif action == "Update":
        st.subheader(f"✏️ Update Data in {table}")

        # Define primary keys for each table
        primary_keys = {
            "providers": "Provider_ID",
            "receivers": "Receiver_ID",
            "food_listings": "Food_ID",
            "claims": "Claim_ID"
        }

        # Ensure the table is valid
        if table in primary_keys:
            primary_key = primary_keys[table]
            row_id = st.number_input(f"Enter {primary_key} to Update", min_value=1)

            # Fetch column names dynamically, excluding the primary key
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall() if col[1] != primary_key]

            column_name = st.selectbox("Select Column to Update", columns)

            # Handle specific column inputs based on the table
            new_value = None  # Initialize the new value variable

            if table == "providers":
                if column_name == "Type":
                    new_value = st.selectbox("New Value", ["Restaurant", "Supermarket", "Catering Service", "Grocery Store"])
                else:
                    new_value = st.text_input(f"Enter New Value for {column_name}")

            elif table == "receivers":
                if column_name == "Type":
                    new_value = st.selectbox("New Value", ["Charity", "NGO", "Individual", "Shelter"])
                else:
                    new_value = st.text_input(f"Enter New Value for {column_name}")

            elif table == "food_listings":
                if column_name == "Food_Type":
                    new_value = st.selectbox("New Value", ["Vegetarian", "Vegan", "Non-Vegetarian"])
                elif column_name == "Meal_Type":
                    new_value = st.selectbox("New Value", ["Breakfast", "Lunch", "Snacks", "Dinner"])
                elif column_name == "Expiry_Date":
                    new_value = st.date_input("New Expiry Date").strftime("%Y-%m-%d 23:59:00")
                else:
                    new_value = st.text_input(f"Enter New Value for {column_name}")

            elif table == "claims":
                if column_name == "Status":
                    new_value = st.selectbox("New Value", ["Pending", "Completed", "Cancelled"])
                elif column_name == "Timestamp":
                    fill_option = st.radio("Select Input Method for Timestamp", ["Autofill (Current Time)", "Fill Manually"])

                    if fill_option == "Fill Manually":
                        new_value = st.text_input("Enter New Timestamp (YYYY-MM-DD HH:MM:SS)")
                    else:  # Autofill with current time
                        new_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.text_input("Autofilled Timestamp", new_value, disabled=True)

                    query = f"UPDATE {table} SET Timestamp = ? WHERE {primary_key} = ?"
                    cursor.execute(query, (new_value, row_id))
                elif column_name in ["Receiver_ID", "Food_ID"]:
                    new_value = st.number_input(f"Enter New Value for {column_name}", min_value=1, step=1)
                    query = f"UPDATE {table} SET {column_name} = ?, Timestamp = ? WHERE {primary_key} = ?"
                    cursor.execute(query, (new_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row_id))
                else:
                    query = f"UPDATE {table} SET {column_name} = ?, Timestamp = ? WHERE {primary_key} = ?"
                    cursor.execute(query, (new_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row_id))


            # Perform the update
            if new_value is not None and st.button("Update"):
                try:
                    if table == "claims":
                        # Auto-update timestamp for claims
                        query = f"UPDATE {table} SET {column_name} = ?, Timestamp = ? WHERE {primary_key} = ?"
                        cursor.execute(query, (new_value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row_id))
                    else:
                        query = f"UPDATE {table} SET {column_name} = ? WHERE {primary_key} = ?"
                        cursor.execute(query, (new_value, row_id))

                    conn.commit()
                    st.success(f"{table.capitalize()} Updated Successfully!")

                except sqlite3.Error as e:
                    st.error(f"Error updating {table}: {e}")
        else:
            st.error("Invalid table selection!")


    # Delete Data
    elif action == "Delete":
        st.subheader(f"❌ Delete Data from {table}")
        row_id = st.number_input("Enter ID to Delete", min_value=1)

        # Define primary keys for each table
        primary_keys = {
            "providers": "Provider_ID",
            "receivers": "Receiver_ID",
            "food_listings": "Food_ID",
            "claims": "Claim_ID"
        }

        # Check if the table is valid
        if table in primary_keys:
            primary_key = primary_keys[table]

            if st.button("Delete"):
                try:
                    if table == "providers":
                        # Delete dependent claims and food listings first
                        cursor.execute("DELETE FROM claims WHERE Food_ID IN (SELECT Food_ID FROM food_listings WHERE Provider_ID = ?)", (row_id,))
                        cursor.execute("DELETE FROM food_listings WHERE Provider_ID = ?", (row_id,))

                    elif table == "receivers":
                        # Delete dependent claims first
                        cursor.execute("DELETE FROM claims WHERE Receiver_ID = ?", (row_id,))

                    # Delete from the main table
                    query = f"DELETE FROM {table} WHERE {primary_key} = ?"
                    cursor.execute(query, (row_id,))
                    conn.commit()
                    st.success("Data Deleted Successfully!")
                except sqlite3.Error as e:
                    st.error(f"Error deleting data: {e}")
        else:
            st.error("Invalid table selection!")



    # ✅ Ensure the connection is closed properly
    conn.close()
