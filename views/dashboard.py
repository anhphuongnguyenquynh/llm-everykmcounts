import mysql.connector
import pandas as pd
import streamlit as st 
import os
from os.path import join, dirname
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import dayplot as dp

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

connection = mysql.connector.connect(
    host = os.environ.get("MYSQL_HOST"),
    port = os.environ.get("MYSQL_PORT"),
    user = os.environ.get("MYSQL_USER"),
    password = os.environ.get("MYSQL_PASSWORD"),
    database = os.environ.get("MYSQL_DATABASE")
)

print('connected')

cursor = connection.cursor()

cursor.execute("SELECT * FROM activities")
data = cursor.fetchall()

st.title('Your activities list')

#CONVERT DATAFRAME
df = pd.DataFrame(data, columns = cursor.column_names)


#STREAMLIT HEATMAP VISUALIZATION
fig, ax = plt.subplots()
df['date'] = pd.to_datetime(df['start_date_local'])
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

#st.pyplot(fig)

#2025 heatmap
fig25, ax = plt.subplots(figsize=(12, 5), dpi=300)
dp.calendar(
    dates=df["date"],
    values=df["distance_meter"],
    start_date="2025-01-01",
    end_date="2025-12-31",
    boxstyle="circle",
    ax=ax,
)
st.pyplot(fig25)

#2024 heatmap
fig25, ax = plt.subplots(figsize=(12, 5), dpi=300)
dp.calendar(
    dates=df["date"],
    values=df["distance_meter"],
    start_date="2024-01-01",
    end_date="2024-12-31",
    boxstyle="circle",
    ax=ax,
)
st.pyplot(fig25)



#STREAMLIT VISUALIZE TABLE
st.dataframe(df)
