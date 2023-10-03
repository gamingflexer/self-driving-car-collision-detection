import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read in the file
data = pd.read_csv("/Users/cosmos/Documents/app_spark/BMS_data.csv")

st.set_page_config(page_title = 'Streamlit Dashboard', 
    layout='wide',
    page_icon='💹')

### top row 

st.markdown("## BMS DATA SPARK")

first_kpi, second_kpi, third_kpi = st.columns(3)

# ---------------------------------------------------------------------

with first_kpi:
    st.markdown("**Average Cell Voltage**")
    number1 = 111 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Average Battery temperature**")
    number2 = 222 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Pack Voltage**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)


# ---------------------------------------------------------------------

### second row 

st.markdown("<hr/>", unsafe_allow_html=True)

st.markdown("## Temperature Sensor")

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi, seveth_kpi, eight_kpi = st.columns(8)


with first_kpi:
    st.markdown("**#1**")
    number1 = 111 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**#2**")
    number2 = 222 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**#3**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------------------

with fourth_kpi:
    st.markdown("**#4**")
    number1 = 111 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**#5**")
    number2 = 222 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown("**#6**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

with seveth_kpi:
    st.markdown("**#7**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

with eight_kpi:
    st.markdown("**#8**")
    number3 = 333 
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# ---------------------------------------------------------------------

st.markdown("## Chart Section: 1")

first_chart, second_chart = st.columns(2)


with first_chart:
    chart_data = pd.DataFrame(np.random.randn(20, 1),columns=['a'])
    st.line_chart(chart_data)

with second_chart:
    chart_data = pd.DataFrame(np.random.randn(20, 1),columns=['a'])
    st.line_chart(chart_data)

# ---------------------------------------------------------------------

st.markdown("## Chart Section: 2")

first_chart, second_chart = st.columns(2)

# ---------------------------------------------------------------------

with first_chart:
    chart_data = pd.DataFrame(np.random.randn(100, 1),columns=['a'])
    st.line_chart(chart_data)

with second_chart:
    chart_data = pd.DataFrame(np.random.randn(2000, 1),columns=['a'])
    st.line_chart(chart_data)