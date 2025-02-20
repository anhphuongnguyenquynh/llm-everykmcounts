import mysql.connector
import pandas as pd
import streamlit as st 
import os
from os.path import join, dirname
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import july

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

connection = mysql.connector.connect(
    host = os.environ.get("MYSQL_HOST"),
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

july.heatmap(
    dates = df.date,
    data = df.distance_meter,
    cmap = 'github',
    fontsize=8,
    title = "Your daily exercises",
    ax = ax
)

st.pyplot(fig)

#STREAMLIT VISUALIZE TABLE
st.dataframe(df)
