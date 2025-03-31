import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def analytics_page():
    # Database Connection
    conn = sqlite3.connect("DS_Project_local_food_wastage_database.db", check_same_thread=False)
    cursor = conn.cursor()
    
    st.title("📊 15 SQL Queries & Analysis")
    
    # Select Query to Run
    query_selection = st.selectbox("Select an Analysis Query", [
        "How many food providers and receivers are there in each city?",
        "Which type of food provider (restaurant, grocery store, etc.) contributes the most food?",
        "What is the contact information of food providers in a specific city?",
        "Which receivers have claimed the most food?",
        "What is the total quantity of food available from all providers?",
        "Which city has the highest number of food listings?",
        "What are the most commonly available food types?",
        "Which food listings are expiring soon (within the next 3 days)?",
        "How many food claims have been made for each food item?",
        "Which provider has had the highest number of successful food claims?",
        "Which city has the fastest claim rate (measured by average time between food listing and claim)?",
        "What percentage of food claims are completed vs. pending vs. canceled?",
        "What is the average quantity of food claimed per receiver?",
        "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?",
        "What is the total quantity of food donated by each provider?"
    ])
    
    if query_selection == "How many food providers and receivers are there in each city?":
        query_providers = "SELECT City, COUNT(*) AS Provider_Count FROM Providers GROUP BY City ORDER BY Provider_Count DESC"
        providers_df = pd.read_sql(query_providers, conn)
        st.subheader("📊 Providers per City")
        st.dataframe(providers_df)
        
        query_receivers = "SELECT City, COUNT(*) AS Receiver_Count FROM Receivers GROUP BY City ORDER BY Receiver_Count DESC"
        receivers_df = pd.read_sql(query_receivers, conn)
        st.subheader("📊 Receivers per City")
        st.dataframe(receivers_df)
    
    elif query_selection == "Which type of food provider (restaurant, grocery store, etc.) contributes the most food?":
        query = "SELECT Provider_Type, SUM(Quantity) AS Total_Food_Quantity FROM Food_Listings GROUP BY Provider_Type ORDER BY Total_Food_Quantity DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
        st.subheader("📊 Type of Food Provider Contribution")
        plt.figure(figsize=(7, 7))
        plt.pie(df["Total_Food_Quantity"], labels=df["Provider_Type"], autopct="%1.1f%%")
        st.pyplot(plt)
    
    elif query_selection == "What is the contact information of food providers in a specific city?":
        city_name = st.text_input("Enter City Name")
        if city_name:
            query = f"SELECT Name, Contact FROM Providers WHERE City = '{city_name}'"
            df = pd.read_sql(query, conn)
            st.dataframe(df)
    
    elif query_selection == "Which receivers have claimed the most food?":
        query = "SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID ORDER BY Total_Claims DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "What is the total quantity of food available from all providers?":
        query = "SELECT SUM(Quantity) AS Total_Food_Quantity FROM Food_Listings"
        df = pd.read_sql(query, conn)
        st.metric("Total Food Available", df["Total_Food_Quantity"][0])
    
    elif query_selection == "Which city has the highest number of food listings?":
        query = "SELECT Location AS City, COUNT(Food_ID) AS Total_Listings FROM Food_Listings GROUP BY Location ORDER BY Total_Listings DESC LIMIT 1"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "What are the most commonly available food types?":
        query = "SELECT Food_Type, COUNT(Food_ID) AS Total_Availability FROM Food_Listings GROUP BY Food_Type ORDER BY Total_Availability DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
           # Visualization - Bar Chart
        st.subheader("📊 Food Type Availability")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(df["Food_Type"], df["Total_Availability"], color='skyblue')
        ax.set_xlabel("Total Availability")
        ax.set_ylabel("Food Type")
        ax.set_title("Most Commonly Available Food Types")
        ax.invert_yaxis()  # Invert to show the highest count at the top

        st.pyplot(fig)
    
    elif query_selection == "Which food listings are expiring soon (within the next 3 days)?":
        query = "SELECT * FROM Food_Listings WHERE julianday(Expiry_Date) - julianday('now') BETWEEN 0 AND 3"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "How many food claims have been made for each food item?":
        query = "SELECT Food_ID, COUNT(*) AS Claim_Count FROM Claims GROUP BY Food_ID ORDER BY Claim_Count DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "Which provider has had the highest number of successful food claims?":
        query = "SELECT f.Provider_ID, p.Name, COUNT(*) AS Successful_Claims FROM Claims c JOIN Food_Listings f ON c.Food_ID = f.Food_ID JOIN Providers p ON f.Provider_ID = p.Provider_ID WHERE c.Status = 'Completed' GROUP BY f.Provider_ID ORDER BY Successful_Claims DESC LIMIT 1"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "Which city has the fastest claim rate (measured by average time between food listing and claim)?":
        query = "SELECT r.City FROM Claims c JOIN Food_Listings f ON c.Food_ID = f.Food_ID JOIN Providers p ON f.Provider_ID = p.Provider_ID JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID WHERE c.Status = 'Completed' GROUP BY r.City ORDER BY AVG(JULIANDAY(c.Timestamp) - JULIANDAY(f.Expiry_Date)) ASC LIMIT 1"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "What percentage of food claims are completed vs. pending vs. canceled?":
        query = "SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Claims) AS Percentage FROM Claims GROUP BY Status"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
        st.subheader("📊 Percentage of Food Claims")
        plt.figure(figsize=(6, 6))
        plt.pie(df["Percentage"], labels=df["Status"], autopct="%1.1f%%")
        st.pyplot(plt)
    
    elif query_selection == "What is the average quantity of food claimed per receiver?":
        query = "SELECT Receiver_ID, AVG(Quantity) AS Avg_Claimed_Quantity FROM Claims JOIN Food_Listings ON Claims.Food_ID = Food_Listings.Food_ID GROUP BY Receiver_ID ORDER BY Avg_Claimed_Quantity DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    elif query_selection == "Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?":
        query = "SELECT Meal_Type, SUM(Quantity) AS Total_Claimed_Quantity FROM Claims JOIN Food_Listings ON Claims.Food_ID = Food_Listings.Food_ID GROUP BY Meal_Type ORDER BY Total_Claimed_Quantity DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
        st.subheader("📊 Most Claimed Meal Types")
        plt.figure(figsize=(7, 7))
        plt.pie(df["Total_Claimed_Quantity"], labels=df["Meal_Type"], autopct="%1.1f%%", colors=["red", "blue", "green", "orange"])
        plt.title("Most Claimed Meal Types")
        st.pyplot(plt)
    
    elif query_selection == "What is the total quantity of food donated by each provider?":
        query = "SELECT p.Provider_ID,p.Name AS Provider_Name, SUM(f.Quantity) AS Total_Donated_Quantity FROM Food_Listings f JOIN Providers p ON f.Provider_ID = p.Provider_ID GROUP BY p.Name ORDER BY Total_Donated_Quantity DESC"
        df = pd.read_sql(query, conn)
        st.dataframe(df)
    
    # Close Database Connection
    conn.close()