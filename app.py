# Importing Libraries
import pandas as pd
import pymysql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
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
    port=3306,
    database="phonepe"
)
mycursor = mydb.cursor()


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    st.image(Image.open(r"D:\Subhashini\Datascience\Tools\Phonepe.png"))
    st.markdown("# :violet[Phonepe Pulse Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, PyMySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image(Image.open("D:\Subhashini\Datascience\Tools\home.jpg"))
        

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2= st.columns([1,1.5],gap="large")
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with col2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            if (Year == 2023 and Quarter in [3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
                mycursor.execute(f"select State, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by State order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            if (Year == 2023 and Quarter in [3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
               mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
               df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

               fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

               fig.update_traces(textposition='inside', textinfo='percent+label')
               st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            if (Year == 2023 and Quarter in [3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
               mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
               df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
               fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

               fig.update_traces(textposition='inside', textinfo='percent+label')
               st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if (Year == 2022 and Quarter in [2, 3, 4]) or (Year == 2023 and Quarter in [1, 2, 3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            if (Year == 2023 and Quarter in [3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
              mycursor.execute(f"select district, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
              df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
              df.Total_Users = df.Total_Users.astype(float)
              fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
              st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :violet[Pincode]")
            if (Year == 2023 and Quarter in [3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
               mycursor.execute(f"SELECT Pincode, SUM(RegisteredUsers) AS Total_Users FROM top_user WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY Pincode ORDER BY Total_Users DESC LIMIT 10")
               df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
               fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
               fig.update_traces(textposition='inside', textinfo='percent+label')
               st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            if (Year == 2023 and Quarter in [3, 4]):
                st.markdown("#### Sorry No Data to Display")
            else:
               mycursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
               df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
               fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})
               fig.update_traces(textposition='inside', textinfo='percent+label')
               st.plotly_chart(fig, use_container_width=True)

            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            mycursor.execute(f"SELECT State, SUM(count) as Total_Transactions, SUM(amount) as Total_amount FROM map_trans WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])

           # Data for the second map - Total Transactions Count
            mycursor.execute(f"SELECT State, SUM(count) as Total_Transactions, SUM(amount) as Total_amount FROM map_trans WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State")
            df2 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])

           # Merge your data with the 'df2' DataFrame based on 'State' column
            df1 = df1.merge(df2, on='State', suffixes=('_TotalAmount', '_TotalTransactions'))

           # Now, create the choropleth maps
            fig1 = px.choropleth(df1,
                 geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                 featureidkey='properties.ST_NM',
                 locations='State',
                 color='Total_amount_TotalAmount',
                 color_continuous_scale='sunset',
                 title="Overall State Data - Transactions Amount")

            fig2 = px.choropleth(df1,
                 geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                 featureidkey='properties.ST_NM',
                 locations='State',
                 color='Total_Transactions_TotalTransactions',
                 color_continuous_scale='sunset',
                 title="Overall State Data - Transactions Count")

            # Display the maps
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
           
            
# BAR CHART - TOP PAYMENT TYPE
            st.markdown("## :violet[Top Payment Type]")
            mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("## :violet[Select any State to explore more]")
            selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
            mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
      with col1:
        # Data for the first map - Total Users
        mycursor.execute(f"SELECT State, SUM(RegisteredUser) as Total_Users, SUM(AppOpens) as Total_AppOpens FROM map_user WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_AppOpens'])
        
        # Data for the second map - Total App Opens
        mycursor.execute(f"SELECT State, SUM(RegisteredUser) as Total_Users, SUM(AppOpens) as Total_AppOpens FROM map_user WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State")
        df2 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_AppOpens'])
        
        # Merge your data with the 'df2' DataFrame based on 'State' column
        df1 = df1.merge(df2, on='State', suffixes=('_TotalUsers', '_TotalAppOpens'))
        
        # Now, create the choropleth maps
        fig1 = px.choropleth(df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Users_TotalUsers',
            color_continuous_scale='sunset',
            title="Overall State Data - User Total Users")
        
        fig2 = px.choropleth(df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_AppOpens_TotalAppOpens',
            color_continuous_scale='sunset',
            title="Overall State Data - User Total App Opens")
        
        # Display the maps
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)


    # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
      st.markdown("## :violet[Select any State to explore more]")
      selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
      mycursor.execute(f"select State,year,quarter,District,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by State,district")
        
      df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
      df.Total_Users = df.Total_Users.astype(int)
        
      fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
      st.plotly_chart(fig,use_container_width=True)

    
# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/SubhashiniSelvakumar/Phonepepulse")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image(Image.open(r"C:\Users\Pragadheesh\Downloads\phone1.png"))
