import streamlit as st
import crud_operations  # Import the CRUD module
import sqlqueries_analysis
import mysqlqueries_analysis
import filter_data

# Sidebar Navigation
st.sidebar.title("📍 Navigation to Food Wastage Management")
page = st.sidebar.radio("Go to", ["Project Overview", "Filter Data by ID","Manage Data (CRUD)","15 SQL Queries & Analysis","My SQL Queries & Analysis","About Me"])

# 📌 Page 1: Project Overview
if page == "Project Overview":
    st.title("🍽️ Local Food Wastage Management System")
    st.write("""
    The **Local Food Wastage Management System** helps track and analyze food donations, claims, and distribution.
    
    **Features:**
    - 📌 Real-time food tracking
    - ⏳ Expiration alerts for food listings
    - ✅ Claim tracking & statistics
    - 📊 Provider & Receiver Management
    
    🔄 **Switch to 'Manage Data (CRUD)' in the sidebar to manage database records.**
    """)

# 📌 Page 2: CRUD Operations
elif page == "Manage Data (CRUD)":
    # st.title("🔧 Manage Data (CRUD)")
    # st.write("Use this page to create, read, update, and delete records.")
    crud_operations.manage_crud()  # Call the CRUD function

# 📌 Page 3: Filter Data by ID
elif page == "Filter Data by ID":
    filter_data.filter_data_page()  # Call the filtering UI

# 📌 Page 4: 15 SQL Queries & Analysis
elif page == "15 SQL Queries & Analysis":
    # st.title("📊 15 SQL Queries & Analysis")
    sqlqueries_analysis.analytics_page()  # Call the analytics function

# 📌 Page 5: My SQL Queries & Analysis
elif page == "My SQL Queries & Analysis":
    # st.title("📊 My SQL Queries & Analysis")
    mysqlqueries_analysis.analytics_page()  # Call the analytics function

# 📌 Page 6: About Me
elif page == "About Me":
    st.title("👨‍💻 About Me")
    
    st.markdown("""
    **Programmer Analyst** with over **2 years** of experience in developing and maintaining **RESTful APIs** using **Java** and **Flask (Python)**.  
    Skilled in **full-stack development**, utilizing **JavaScript, CSS, and HTML** for frontend development and **Java with Hibernate** for backend services.
    """)
    
    # Adding Contact Information
    st.subheader("📬 Contact Information")
    st.write("📧 Email: prabhakarankumar28@gmail.com")  # Replace with your actual email
    st.write("💼 LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/in/prabhakaran-kumar-661441223/)")  # Replace with your LinkedIn URL
    st.write("📂 GitHub: [Your GitHub Profile](https://github.com/yourusername)")  # Replace with your GitHub URL