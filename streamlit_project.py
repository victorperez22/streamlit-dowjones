import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time

#Fetch Google Sheets URL from Streamlit Secrets
gsheet_url = st.secrets["connections"]["gsheet_url"]

#Load Data Directly from Google Sheets
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_data():
    return pd.read_csv(gsheet_url)

df = load_data()

#Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

#Define the chart functions
def create_line_chart():
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x=df.index, y="Price",ax=ax,color="blue")
    ax.set_title("Dow Jones Price Over Time (Line Chart)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price")
    return fig

def create_area_chart():
    fig, ax =plt.subplots(figsize=(10, 5))
    ax.fill_between(df.index,df["Price"],color="blue",alpha=0.3)
    ax.set_title("Dow Jones Price Over Time (Area Chart)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price")
    return fig

#Streamlit App Layout
st.title("💸 Dow Jones Price Analysis")
st.markdown("###How has the Dow Jones stock price changed over time?")

#Initialize the session state variables
if "selected_chart" not in st.session_state:
    st.session_state.selected_chart = None
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "show_answer_button" not in st.session_state:
    st.session_state.show_answer_button = False

#Show the Random Chart Button
if st.button("Show a Random Chart"):
    st.session_state.selected_chart = random.choice(["line", "area"])
    st.session_state.start_time = time.time()
    st.session_state.show_answer_button = True

#Display the selected chart
if st.session_state.selected_chart is not None:
    if st.session_state.selected_chart == "line":
        st.pyplot(create_line_chart())
    else:
        st.pyplot(create_area_chart())

#Show Timer Button
if st.session_state.show_answer_button:
    if st.button("I answered your question"):
        end_time = time.time()
        time_taken = round(end_time-st.session_state.start_time, 2)
        st.success(f"You took {time_taken} seconds to answer the question!")
