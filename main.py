import streamlit as st
import crud_operations  # Import the CRUD module
import sqlqueries_analysis
import mysqlqueries_analysis
import filter_data

# Sidebar Navigation
st.sidebar.title("📍 Navigation to Food Wastage Management")
page = st.sidebar.radio("Go to", ["Project Overview", "Filter Data","Manage Data (CRUD)","15 SQL Queries & Analysis","My Custom SQL Queries & Analysis","About Me"])

# 📌 Page 1: Project Overview
if page == "Project Overview":
    st.title("🍽️ Local Food Wastage Management System")
    st.write("""
    ## 🌍 Efficient Food Redistribution & Wastage Management  
    The **Local Food Wastage Management System** helps track, manage, and analyze food donations, claims, and distribution to minimize wastage and improve food availability.

    ### 🔹 Core Features:
    - 🛠 **Manage Data (CRUD)**: Add, update, delete, and view records for providers, receivers, food listings, and claims.
    - 🎯 **Filter Data**: Retrieve and analyze specific records with ease.
    - 📊 **Data Insights & Analytics**:
      - 🔍 **15 SQL Queries & Analysis**: Get key insights on food donation trends, provider activity, and unclaimed food.
      - 💡 **My Custom SQL Queries & Analysis**: Run my personalized queries for deeper analysis.
    - ⏳ **Timestamp Tracking**: Automated tracking when claims are modified.
    - ✅ **Claim Status Updates**: Monitor food claims (`Pending`, `Completed`, `Cancelled`) in real time.

    ### 📌 Get Started:
    Use the sidebar to navigate through different sections and manage food wastage effectively!
    """)


# 📌 Page 2: Filter Data by ID
elif page == "Filter Data":
    filter_data.filter_data_page()  # Call the filtering UI

# 📌 Page 3: CRUD Operations
elif page == "Manage Data (CRUD)":
    crud_operations.manage_crud()  # Call the CRUD function

# 📌 Page 4: 15 SQL Queries & Analysis
elif page == "15 SQL Queries & Analysis":
    sqlqueries_analysis.analytics_page()  # Call the analytics function

# 📌 Page 5: My SQL Queries & Analysis
elif page == "My Custom SQL Queries & Analysis":
    mysqlqueries_analysis.analytics_page()  # Call the analytics function

# 📌 Page 6: About Me
elif page == "About Me":
    st.title("👨‍💻 About Me")

    st.markdown("**Prabhakaran Kumar**")
    st.markdown("**2018-2022 Mechanical Engineering Batch - SKCET,CBE**")
    st.markdown("**2.5 years of Programmer Analyst**")
    
    st.markdown("""
    **Programmer Analyst** with over **2 years** of experience in developing and maintaining **RESTful APIs** using **Java** and **Flask (Python)**.  
    Skilled in **full-stack development**, utilizing **JavaScript, CSS, and HTML** for frontend development and **Java with Hibernate** for backend services.
    """)
    
    # Adding Contact Information
    st.subheader("📬 Contact Information")
    st.write("📧 Email: prabhakarankumar28@gmail.com")  # Replace with your actual email
    st.write("💼 LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/in/prabhakaran-kumar-661441223/)")  # Replace with your LinkedIn URL
    st.write("📂 GitHub: [Your GitHub Profile](https://github.com/prabhakaran2809)")  # Replace with your GitHub URL
