import os
import json
import pandas as pd
import pymysql
import streamlit as st
import plotly.express as px
from PIL import Image
from sqlalchemy import create_engine

# database connection using SQLAlchemy
engine = create_engine("mysql+pymysql://root:Teddy756@localhost:3306/phonepepulse")

#Streamlit app config
icon = Image.open(r"C:\Users\Pragadheesh\Downloads\phone1.png")
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Data has been cloned from Phonepe Pulse Github Repo"}
)

#connection to pymySQL
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="Teddy756",
    port=3306
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepepulse")
mycursor.execute("USE phonepepulse")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS agg_trans (
        Transaction_Type VARCHAR(255),
        Transaction_Count INT,
        Transaction_Amount DECIMAL(10, 2),
        Transaction_Year INT,
        Quarters INT,
        States VARCHAR(255)
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS agg_user (
        District VARCHAR(255),
        Transaction_Type VARCHAR(255),
        Transaction_Count INT,
        Transaction_Amount DECIMAL(10, 2),
        Transaction_Year INT, 
        Quarters INT,
        States VARCHAR(255)
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS map_trans (
        States VARCHAR(255),
        Transaction_Year INT,
        Quarters INT,
        District VARCHAR(255),
        Transaction_Type VARCHAR(255),
        Transaction_Count INT
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS map_user (
        District VARCHAR(255),
        Transaction_Year INT, 
        Quarter INT,
        States VARCHAR(255),
        RegisteredUsers INT
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS top_trans (
        District VARCHAR(255),
        Transaction_Type VARCHAR(255),
        Transaction_Count INT,
        Transaction_Amount INT,
        Transaction_Year INT, 
        Quarters INT,
        States VARCHAR(255) 
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS top_user (
        District VARCHAR(255),
        Transaction_Year INT, 
        Quarter INT,
        States VARCHAR(255),
        RegisteredUsers INT
    )
""")

#function to fetch data from MySQL
def fetch_data(query):
    mycursor = mydb.cursor()
    mycursor.execute(query)
    data = mycursor.fetchall()
    columns = [i[0] for i in mycursor.description]
    df = pd.DataFrame(data, columns=columns)
    return df

# Load data from CSV files into dataframes
Agg_trans = pd.read_csv('D:/Subhashini/Datascience/project/Phonepe/agg_trans.csv')
Map_trans = pd.read_csv('D:/Subhashini/Datascience/project/Phonepe/map_tran.csv')
Top_trans = pd.read_csv('D:/Subhashini/Datascience/project/Phonepe/top_tran.csv')
Agg_user = pd.read_csv('D:/Subhashini/Datascience/project/Phonepe/agg_user.csv')
Map_user = pd.read_csv('D:/Subhashini/Datascience/project/Phonepe/map_user.csv')
Top_user = pd.read_csv('D:/Subhashini/Datascience/project/Phonepe/top_user.csv')

# Load data into MySQL tables
Agg_trans.to_sql('agg_trans', engine, if_exists='replace', index=False)
Map_trans.to_sql('map_trans', engine, if_exists='replace', index=False)
Top_trans.to_sql('top_trans', engine, if_exists='replace', index=False)
Agg_user.to_sql('agg_user', engine, if_exists='replace', index=False)
Map_user.to_sql('map_user', engine, if_exists='replace', index=False)
Top_user.to_sql('top_user', engine, if_exists='replace', index=False)

#functions for data visualization
def visualize_map_transaction_data():
    st.subheader("Map Transaction Data")
    fig = px.scatter_mapbox(
        Map_trans,
        lat="Latitude",
        lon="Longitude",
        color="Transaction_Type",
        hover_name="States",
        hover_data=["Transaction_Count", "Transaction_Amount"],
        zoom=3
    )

    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig)

def visualize_map_user_data():
    st.subheader("Map User Data")
    fig = px.scatter_mapbox(
        Map_user,
        lat="Latitude",
        lon="Longitude",
        color="RegisteredUsers",
        hover_name="States",
        hover_data=["Quarter", "RegisteredUsers"],
        zoom=3
    )

    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig)

def visualize_top_transaction_data():
    st.subheader("Top Transaction Data")
    fig = px.bar(
        Top_trans,
        x="Transaction_Type",
        y="Transaction_Count",
        color="States",
        labels={"Transaction_Type": "Transaction Type", "Transaction_Count": "Transaction Count"},
        title="Top Transactions by Transaction Type",
    )

    st.plotly_chart(fig)

def visualize_top_user_data():
    st.subheader("Top User Data")
    fig = px.bar(
        Top_user,
        x="States",
        y="Registered_User",
        color="District",
        labels={"States": "State", "RegisteredUsers": "Registered Users"},
        title="Top Users by State",
    )

    st.plotly_chart(fig)

def home():
    st.sidebar.header("Menu")
    selected = st.sidebar.selectbox("Select an option", ["🏠 Home", "📈 Top Charts", "📊 Explore Data", "❗ About"], key="home_selectbox")

    if selected == "🏠 Home":
        Img1 = Image.open(r"C:\Users\Pragadheesh\Downloads\phone1.png")
        st.image(Img1)
        st.markdown("# Phonepe Data Visualization and Exploration")
        st.markdown("## A User-Friendly Tool Using Streamlit and Plotly")
        col1, col2 = st.columns([3, 2], gap="medium")
        with col1:
            st.write(" ")
            st.write(" ")
            st.markdown("### Domain: Fintech")
            st.markdown("### Technologies: Github Cloning, Python, MySQL, Pandas, Streamlit, Mysql-connector-python, and Plotly.")
            st.markdown("### Overview: In this Streamlit web app, you can visualize the PhonePe Pulse data and gain insights on transactions, the number of users, top 10 states, districts, pincodes, and which brand has the most number of users. Bar charts, Pie charts, and Geo map visualizations are used to provide insights.")

def top_charts():
    st.header("Top Charts")
    Type = st.sidebar.radio("Select Data Type", ["Transactions", "Users"])
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        Year = st.slider("Year", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    with col2:
        st.info(
            """
            From this menu, we can get insights like:
            - Overall ranking for a particular Year and Quarter.
            - Top 10 State, District, Pincode based on the Total number of transactions and Total amount spent on Phonepe.
            - Top 10 State, District, Pincode based on Total PhonePe users and their app opening frequency.
            - Top 10 mobile brands and their percentage based on how many people use Phonepe.
            """
        )

    if Type == "Transactions":
       col1, col2 = st.columns([1, 1], gap="small")

       with col1:
        st.markdown("### State")
        try:
            mycursor.execute(f"SELECT States, SUM(Transaction_Count) as Total_Transaction_Count, SUM(Transaction_Amount) as Total_Amount FROM top_trans WHERE Transaction_Year = {Year} AND Quarters = {Quarter} GROUP BY States ORDER BY Total_Amount DESC LIMIT 10")
            data = mycursor.fetchall()
            columns = [i[0] for i in mycursor.description]
            df = pd.DataFrame(data, columns=columns)
            fig = px.pie(
                df,
                values='Total_Amount',
                names='States',
                title='Top 10 States by Total Transaction Amount',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                hover_data=['Total_Transaction_Count'],
                labels={'Total_Transaction_Count': 'Transaction Count'}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            pass
        except Exception as e:
            st.error(f"An error occurred: {e}")

       with col2:
        st.markdown("### District")
        try:
            mycursor.execute(f"SELECT District, SUM(Transaction_Count) as Total_Count FROM top_trans WHERE Transaction_Year = {Year} AND Quarters = {Quarter} GROUP BY District ORDER BY Total_Count DESC LIMIT 10")
            data = mycursor.fetchall()
            columns = [i[0] for i in mycursor.description]
            df = pd.DataFrame(data, columns=columns)
            fig = px.pie(
                df,
                values='Total_Count',
                names='District',
                title='Top 10 Districts by Total Transaction Amount',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                hover_data=['Total_Count'],
                labels={'Total_Count': 'Transaction Count'}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            pass
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if Type == "Users":
       col1, col2, col3 = st.columns([1, 1, 1], gap="small")

       with col1:
        st.markdown("### State")
        try:
            mycursor.execute(f"SELECT States, SUM(RegisteredUsers) as Total_Users FROM map_user WHERE Transaction_Year = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY Total_Users DESC LIMIT 10")
            data = mycursor.fetchall()
            columns = [i[0] for i in mycursor.description]
            df = pd.DataFrame(data, columns=columns)
            fig = px.bar(
                df,
                x='States',
                y='Total_Users',
                title='Top 10 States by Total Users',
                labels={'Total_Users': 'Total Users'},
            )
            fig.update_traces(marker_color='blue')
            st.plotly_chart(fig, use_container_width=True)
            pass
        except Exception as e:
            st.error(f"An error occurred: {e}")

       with col2:
        st.markdown("### District")
        try:
            mycursor.execute(f"SELECT District, States, SUM(RegisteredUsers) as Total_Users FROM map_user WHERE Transaction_Year = {Year} AND Quarter = {Quarter} GROUP BY District, States ORDER BY Total_Users DESC LIMIT 10")
            data = mycursor.fetchall()
            columns = [i[0] for i in mycursor.description]
            df = pd.DataFrame(data, columns=columns)
            fig = px.bar(
                df,
                x='District',
                y='Total_Users',
                title='Top 10 Districts by Total Users',
                labels={'Total_Users': 'Total Users'},
            )
            fig.update_traces(marker_color='blue')
            st.plotly_chart(fig, use_container_width=True)
            pass
        except Exception as e:
            st.error(f"An error occurred: {e}")

       with col3:
        st.markdown("### Pincode")
        try:
            mycursor.execute(f"SELECT Quarter, States, SUM(RegisteredUsers) as Total_Users FROM map_user WHERE Transaction_Year = {Year} AND Quarter = {Quarter} GROUP BY Quarter, States ORDER BY Total_Users DESC LIMIT 10")
            data = mycursor.fetchall()
            columns = [i[0] for i in mycursor.description]
            df = pd.DataFrame(data, columns=columns)
            fig = px.bar(
                df,
                x='States',
                y='Total_Users',
                title='Top 10 Pincode-wise Users',
                labels={'Total_Users': 'Total Users'},
            )
            fig.update_traces(marker_color='blue')
            st.plotly_chart(fig, use_container_width=True)
            pass
        except Exception as e:
            st.error(f"An error occurred: {e}")

def explore_data():
    st.header("Explore Data")
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### Transaction Data")
        data_option = st.selectbox("Select Data", ["State-wise Transactions", "District-wise Transactions", "Pincode-wise Transactions"])
        st.info("Select the data you want to explore and analyze.")

    with col2:
        st.markdown("### User Data")
        user_data_option = st.selectbox("Select User Data", ["State-wise Users", "District-wise Users", "Pincode-wise Users"])
        st.info("Select the user data you want to explore and analyze.")

# Explore Data - Transaction Data
    if data_option == "State-wise Transactions":
      st.markdown("### State-wise Transactions")
      selected_year = st.slider("Select a Year", min_value=2018, max_value=2023)
      selected_quarter = st.slider("Select a Quarter", min_value=1, max_value=4)

      query = f"SELECT States, SUM(Transaction_Count) as Total_Transactions, SUM(Transaction_Amount) as Total_Amount FROM agg_trans WHERE Transaction_Year = {selected_year} AND Quarters = {selected_quarter} GROUP BY States ORDER BY Total_Amount DESC"
      df = fetch_data(query)
      st.dataframe(df)

    if data_option == "District-wise Transactions":
       st.markdown("### District-wise Transactions")
       selected_year = st.slider("Select a Year", min_value=2018, max_value=2023)
       selected_quarter = st.slider("Select a Quarter", min_value=1, max_value=4)

       query = f"SELECT District, SUM(Transaction_Count) as Total_Transactions FROM map_trans WHERE Transaction_Year = {selected_year} AND Quarters = {selected_quarter} GROUP BY District ORDER BY Total_Transactions DESC"
       df = fetch_data(query)
       st.dataframe(df)

    if data_option == "Pincode-wise Transactions":
       st.markdown("### Pincode-wise Transactions")
       selected_year = st.slider("Select a Year", min_value=2018, max_value=2023)
       selected_quarter = st.slider("Select a Quarter", min_value=1, max_value=4)

       query = f"SELECT District, Transaction_Year, Quarter, States, SUM(RegisteredUsers) as Total_Users FROM map_user WHERE Transaction_Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY District ORDER BY Total_Users DESC"
       df = fetch_data(query)
       st.dataframe(df)

def about():
    st.header("About")
    st.markdown("## About")
    st.markdown("This Streamlit app allows you to explore PhonePe Pulse data and gain insights into transactions and user statistics.")
    st.info("Data has been cloned from PhonePe Pulse Github Repo.")

def main():
    st.sidebar.header("Menu")
    selected = st.sidebar.selectbox("Select an option", ["🏠 Home", "📈 Top Charts", "📊 Explore Data", "❗ About"])

    if selected == "🏠 Home":
        home()
    elif selected == "📈 Top Charts":
        top_charts()
    elif selected == "📊 Explore Data":
        explore_data()
    elif selected == "❗ About":
        about()

if __name__ == "__main__":
    main()

mydb.close()
    
