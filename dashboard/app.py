import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

st.header('E-Commerce Transaction Data Analysis')
st.subheader('Dicoding course final project')
st.text('by Irvan Alvisa Himawan')

## Read Data
merged_df = pd.read_csv('cleaned_data/merge_order_product_cust.csv')

st.subheader('Sample data E-Commerce Transaction that delivered to Customer')
st.write(merged_df.head())

# Extract unique customer states
customer_states = merged_df['customer_state'].unique()

# Create a selectbox for customer states
selected_state = st.selectbox('Select State', customer_states)

# Filter the DataFrame based on the selected state
filtered_df = merged_df[merged_df['customer_state'] == selected_state]

# Count the product categories
category_counts = filtered_df['product_category_name_english'].value_counts().head(10)

# Create a bar chart
st.subheader(f'Most Selling Product Category for {selected_state}')
st.bar_chart(category_counts)

# Filter the DataFrame based on the selected state
filtered_df_state = merged_df[merged_df['customer_state'] == selected_state]

# Extract unique customer cities based on the selected state
customer_cities = filtered_df_state['customer_city'].unique()

# Create a selectbox for customer cities
selected_city = st.selectbox('Select City', customer_cities)

# Filter the DataFrame based on the selected city
filtered_df_city = filtered_df_state[filtered_df_state['customer_city'] == selected_city]

# Create a pivot table
pivot_table = filtered_df_city.pivot_table(
    index='product_category_name_english',
    values=['order_id', 'price'],
    aggfunc={'order_id': 'count', 'price': 'sum'}
).reset_index().sort_values('order_id', ascending=False)

# Rename columns for clarity
pivot_table.columns = ['Product Category', 'Order Count', 'Total Price']

# Display the pivot table
st.subheader(f'Product Category Analysis for {selected_city}, {selected_state}')
st.write(pivot_table)


# Convert order_purchase_timestamp to datetime
filtered_df_city['order_purchase_timestamp'] = pd.to_datetime(filtered_df_city['order_purchase_timestamp'])

# Extract year from order_purchase_timestamp
filtered_df_city['year'] = filtered_df_city['order_purchase_timestamp'].dt.year

# Group by year and calculate the sum of price
yearly_sales = filtered_df_city.groupby('year')['price'].sum().reset_index()


# Convert year to string to ensure proper display on X-axis
yearly_sales['year'] = yearly_sales['year'].astype(str)


# Create a line chart
st.subheader(f'Yearly Sales for {selected_city}, {selected_state}')
st.line_chart(yearly_sales.set_index('year'))