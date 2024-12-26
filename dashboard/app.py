import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

st.header('Dicoding Collection Dashboard :sparkles:')
st.subheader('Daily Orders')

geo_df = pd.read_csv("..\data_set\geolocation_dataset.csv")
customer_df = pd.read_csv("..\data_set\customer_dataset.csv"
                          )