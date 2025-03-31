import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def analytics_page():
    # Database Connection
    conn = sqlite3.connect("DS_Project_local_food_wastage_database.db", check_same_thread=False)
    cursor = conn.cursor()
    
    st.title("📊 My SQL Queries & Analysis")
    
    # Select Query to Run
    query_selection = st.selectbox("Select an Analysis Query", [
        "What is the trend of completed claims over the past 15 days?",
        "What is the distribution of food types among unclaimed listings?",
        "Which provider has the highest food wastage (food expired before being claimed)?",
        "Which receiver type claims the most food?",
        "Which meal type has the highest unclaimed food?",
        "Which city has the highest percentage of unclaimed food?(LIMIT 5)",
        "The most frequent food providers and their contributions",
        "The highest demand locations based on food claims",
        "Which provider category (restaurant, grocery, etc.) has the most Pending or Cancelled claims?",
        "Which provider category (restaurant, grocery, etc.) has the most Completed claims?"
    ])

    if query_selection == "What is the trend of completed claims over the past 15 days?":

        # Query to get completed claims over the last 15 days
        completed_claims_past15_query = "SELECT strftime('%Y-%m-%d', Timestamp) AS Claim_Date, COUNT(*) AS Completed_Claims FROM Claims WHERE Status = 'Completed' AND Timestamp >= DATE('now', '-15 days') GROUP BY Claim_Date ORDER BY Claim_Date;"

        df_completed_claims_past15_query = pd.read_sql(completed_claims_past15_query, conn)
        st.dataframe(df_completed_claims_past15_query)

        # Visualization in Streamlit
        st.title("📈 Completed Claims Trend Over the Last 15 Days")

        if df_completed_claims_past15_query.empty:
            st.write("No completed claims in the last 15 days.")
        else:
            # Line Chart
            fig, ax = plt.subplots()
            ax.plot(df_completed_claims_past15_query["Claim_Date"], df_completed_claims_past15_query["Completed_Claims"], marker='o', linestyle='-', color='b', label="Completed Claims")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Claims")
            ax.set_title("Trend of Completed Claims Over the Past 15 Days")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

    elif query_selection == "What is the distribution of food types among unclaimed listings?":
    
        # Query to get the count of unclaimed food types
        unclaimed_food_query = "SELECT Food_Type, COUNT(*) AS Unclaimed_Count FROM Food_Listings WHERE Food_ID NOT IN (SELECT Food_ID FROM Claims) GROUP BY Food_Type ORDER BY Unclaimed_Count DESC;"

        df_unclaimed_food = pd.read_sql(unclaimed_food_query, conn)
        st.dataframe(df_unclaimed_food)

        # Visualization in Streamlit
        st.title("🥗 Distribution of Food Types Among Unclaimed Listings")

        if df_unclaimed_food.empty:
            st.write("No unclaimed food listings available.")
        else:
            # Pie Chart
            fig, ax = plt.subplots()
            ax.pie(df_unclaimed_food["Unclaimed_Count"], labels=df_unclaimed_food["Food_Type"], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            ax.set_title("Unclaimed Food Types Distribution")
            st.pyplot(fig)

    elif query_selection == "Which provider has the highest food wastage (food expired before being claimed)?":

        # Query to get providers with the most expired unclaimed food
        food_wastage_query = "SELECT Providers.Name AS Provider_Name, COUNT(Food_Listings.Food_ID) AS Expired_Unclaimed_Count FROM Food_Listings JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID WHERE Food_Listings.Expiry_Date < DATE('now') AND Food_Listings.Food_ID NOT IN (SELECT Food_ID FROM Claims) GROUP BY Providers.Provider_ID ORDER BY Expired_Unclaimed_Count DESC;"

        df_food_wastage = pd.read_sql(food_wastage_query, conn)
        st.dataframe(df_food_wastage)

    elif query_selection == "Which receiver type claims the most food?":
    
        # Query to get the total quantity of food claimed by each receiver type
        receiver_claims_query = "SELECT Receivers.Type AS Receiver_Type, SUM(Food_Listings.Quantity) AS Total_Claimed FROM Claims JOIN Receivers ON Claims.Receiver_ID = Receivers.Receiver_ID JOIN Food_Listings ON Claims.Food_ID = Food_Listings.Food_ID GROUP BY Receivers.Type ORDER BY Total_Claimed DESC;"

        df_receiver_claims = pd.read_sql(receiver_claims_query, conn)
        st.dataframe(df_receiver_claims)

        # Visualization in Streamlit
        st.title("🍽️ Total Food Claimed by Receiver Type")

        if df_receiver_claims.empty:
            st.write("No claims data available.")
        else:
            # Pie Chart
            fig, ax = plt.subplots()
            ax.pie(df_receiver_claims["Total_Claimed"], labels=df_receiver_claims["Receiver_Type"], autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
            ax.set_title("Food Claimed Distribution by Receiver Type")
            st.pyplot(fig)

    elif query_selection == "Which meal type has the highest unclaimed food?":

        # Query to get the meal type with the most unclaimed food
        unclaimed_meal_query = "SELECT Meal_Type, COUNT(*) AS Unclaimed_Count FROM Food_Listings WHERE Food_ID NOT IN (SELECT Food_ID FROM Claims) GROUP BY Meal_Type ORDER BY Unclaimed_Count DESC;"


        df_unclaimed_meal = pd.read_sql(unclaimed_meal_query, conn)
        st.dataframe(df_unclaimed_meal)
         # Visualization in Streamlit
        st.title("🍽️ Total Food UnClaimed by Meal Type")
        fig, ax = plt.subplots()
        ax.pie(df_unclaimed_meal["Unclaimed_Count"], labels=df_unclaimed_meal["Meal_Type"], autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
        ax.set_title("Food Unclaimed Distribution by Meal Type")
        st.pyplot(fig)
    
    elif query_selection == "Which city has the highest percentage of unclaimed food?(LIMIT 5)":

        # Query to find the city with the highest percentage of unclaimed food
        unclaimed_city_query = "SELECT Providers.City, ROUND((COUNT(Food_Listings.Food_ID) * 100.0) / (SELECT COUNT(*) FROM Food_Listings), 2) AS Unclaimed_Percentage FROM Food_Listings JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID WHERE Food_Listings.Food_ID NOT IN (SELECT Food_ID FROM Claims) GROUP BY Providers.City ORDER BY Unclaimed_Percentage DESC LIMIT 5;"


        df_unclaimed_city = pd.read_sql(unclaimed_city_query, conn)
        st.dataframe(df_unclaimed_city)

    

    elif query_selection == "The most frequent food providers and their contributions":
    
        frequent_providers_query = "SELECT Providers.Name AS Provider_Name, COUNT(Food_Listings.Food_ID) AS Total_Contributions FROM Food_Listings JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID GROUP BY Providers.Provider_ID ORDER BY Total_Contributions DESC LIMIT 10;"


        df_frequent_providers = pd.read_sql(frequent_providers_query, conn)
        st.dataframe(df_frequent_providers)

        # Visualization: Bar Chart
        fig, ax = plt.subplots()
        ax.barh(df_frequent_providers["Provider_Name"], df_frequent_providers["Total_Contributions"], color="skyblue")
        ax.set_xlabel("Total Contributions")
        ax.set_ylabel("Provider Name")
        ax.set_title("Top 10 Most Frequent Food Providers")
        plt.gca().invert_yaxis()  # To display highest on top
        st.pyplot(fig)

    elif query_selection == "The highest demand locations based on food claims":
    
        demand_locations_query = "SELECT Providers.City, COUNT(Claims.Claim_ID) AS Total_Claims FROM Claims JOIN Food_Listings ON Claims.Food_ID = Food_Listings.Food_ID JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID GROUP BY Providers.City ORDER BY Total_Claims DESC LIMIT 10;"

        df_demand_locations = pd.read_sql(demand_locations_query, conn)
        st.dataframe(df_demand_locations)

        # Visualization: Bar Chart
        fig, ax = plt.subplots()
        ax.barh(df_demand_locations["City"], df_demand_locations["Total_Claims"], color="lightcoral")
        ax.set_xlabel("Total Claims")
        ax.set_ylabel("City")
        ax.set_title("Top 10 Cities with Highest Food Demand")
        plt.gca().invert_yaxis()
        st.pyplot(fig)

    elif query_selection == "Trends in food wastage to improve distribution efforts":
    
        food_wastage_trends_query = "SELECT strftime('%Y-%m-%d', Food_Listings.Expiry_Date) AS Day, COUNT(Food_Listings.Food_ID) AS Expired_Food_Count FROM Food_Listings WHERE Food_Listings.Expiry_Date < DATE('now') AND Food_Listings.Food_ID NOT IN (SELECT Food_ID FROM Claims) GROUP BY Day ORDER BY Day DESC;"

        df_food_wastage_trends = pd.read_sql(food_wastage_trends_query, conn)
        st.dataframe(df_food_wastage_trends)

    elif query_selection == "Which provider category (restaurant, grocery, etc.) has the most Pending or Cancelled claims?":
        
        # SQL query to determine which provider category has the most pending or canceled claims
        provider_category_query = "SELECT Providers.Type AS Provider_Type, COUNT(Claims.Claim_ID) AS Total_Claims, SUM(CASE WHEN Claims.Status IN ('Pending', 'Cancelled') THEN 1 ELSE 0 END) AS Pending_Cancelled_Claims, ROUND((SUM(CASE WHEN Claims.Status IN ('Pending', 'Cancelled') THEN 1 ELSE 0 END) * 100.0) / COUNT(Claims.Claim_ID), 2) AS Pending_Cancelled_Rate FROM Claims JOIN Food_Listings ON Claims.Food_ID = Food_Listings.Food_ID JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID GROUP BY Providers.Type ORDER BY Pending_Cancelled_Claims DESC;"

        # Execute the query and load results into a DataFrame
        df_provider_category = pd.read_sql(provider_category_query, conn)

        # Display the result in Streamlit as a table
        st.dataframe(df_provider_category)

        st.subheader("📊 Distribution of Pending or Cancelled Claims by Provider Category")

        fig, ax = plt.subplots(figsize=(7, 7))
        colors = plt.cm.tab10.colors[:len(df_provider_category)]
        ax.pie(df_provider_category["Pending_Cancelled_Claims"], labels=df_provider_category["Provider_Type"], autopct="%1.1f%%", colors=colors, startangle=140)
        ax.set_title("Pending or Cancelled Claims by Provider Category")

        # Display the visualization in Streamlit
        st.pyplot(fig)

    elif query_selection == "Which provider category (restaurant, grocery, etc.) has the most Completed claims?":

        # SQL query to find provider category with the most completed claims
        provider_completed_claims_query = "SELECT Providers.Type AS Provider_Type, COUNT(Claims.Claim_ID) AS Completed_Claims FROM Claims JOIN Food_Listings ON Claims.Food_ID = Food_Listings.Food_ID JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID WHERE Claims.Status = 'Completed' GROUP BY Providers.Type ORDER BY Completed_Claims DESC;"


        # Execute the query and load results into a DataFrame
        df_provider_completed_claims = pd.read_sql(provider_completed_claims_query, conn)
        st.dataframe(df_provider_completed_claims)

        # Display DataFrame in Streamlit
        st.subheader("📊 Top Provider Categories by Completed Claims")

        # Visualization: Bar Chart
        fig, ax = plt.subplots()
        ax.bar(df_provider_completed_claims["Provider_Type"], df_provider_completed_claims["Completed_Claims"], 
            color=['blue', 'green', 'orange', 'purple', 'red'])
        ax.set_xlabel("Provider Category")
        ax.set_ylabel("Completed Claims")
        ax.set_title("Top Provider Categories by Completed Claims")
        plt.xticks(rotation=45)
        st.pyplot(fig)




    




