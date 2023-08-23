import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

ts = datetime.now()
date = ts.strftime("%d-%m-%y")
timestamp = ts.strftime("%H-%M-%S")


csv_file_path = "attendance/attendance_" + date + ".csv"

count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")

if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

try:
    df = pd.read_csv(csv_file_path)
    st.dataframe(df.style.highlight_max(axis=0))
except FileNotFoundError:
    st.write(f"No attendance file found for date: {date}")
