# import the necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import datetime as dt
import seaborn as sns

import timeit
import time
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
# from pages.User import get_data

st.title('Credit Card Fraud Detection')


tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
   #st.write(get_data)



with tab2:
   # st.header("A dog")
   # st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
   with st.empty():
    for seconds in range(60):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write("✔️ 1 minute over!")

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)