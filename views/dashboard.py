import mysql.connector
import pandas as pd
import streamlit as st 
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# connection = mysql.connector.connect(
#     host = 'localhost',
#     user = 'root',
#     password = '7913qpzm&',
#     database = 'llm_everykmcounts'
# )

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

df = pd.DataFrame(data, columns = cursor.column_names)
st.dataframe(df)

