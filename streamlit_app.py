import streamlit as st 

#---PAGE SETUP---
chatbot_page = st.Page(
    page = "views/chatbot.py",
    title = "Chatbot",
    #icon = ":robot_face:",
    default = True,
)

dashboard_page = st.Page(
    page = "views/dashboard.py",
    title = "Dashboard",
    #icon = ":chart_with_upwards_trend:",
)

# --- NAVIGATION SETUP (WITHOUT SECTIONS) ---
pg = st.navigation(pages = [chatbot_page, dashboard_page])

# --- RUN NAVIGATION ---
pg.run()