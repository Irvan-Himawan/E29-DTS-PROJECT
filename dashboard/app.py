import pandas as pd
import seaborn as sns
import streamlit as st

#style
sns.set(style='dark')

st.header('E-Commerce Transaction Data Analysis')
st.subheader('Dicoding course final project')
st.text('by Irvan Alvisa Himawan')

# Read Data
merged_df = pd.read_csv('https://raw.githubusercontent.com/Irvan-Himawan/E29-DTS-PROJECT/refs/heads/master/dashboard/cleaned_dataset/merge_order_product_cust.csv')

# Assesing Data
## Extract unique customer states
customer_states = merged_df['customer_state'].unique()


# Row 1
st.subheader('Sample data E-Commerce Transaction that delivered to Customer')
st.write(merged_df.head())

# Row 2
## Filtered ten states has most transaction
state_transaction = merged_df['customer_state'].value_counts().head(10)
# Sort the values in ascending order
state_transaction = state_transaction.sort_values(ascending=True)
### Create a bar chart
st.subheader('Top 10 States Has Most Transaction')
st.bar_chart(state_transaction)


# Row 3
## Filtered ten cities has most transaction
city_transaction = merged_df['customer_city'].value_counts().head(10)
# Sort the values in ascending order
city_transaction = city_transaction.sort_values(ascending=True)
### Create a bar chart
st.subheader('Top 10 Cities Has Most Transaction')
st.bar_chart(city_transaction)

# Row 4
## Create a selectbox for customer states
selected_state = st.selectbox('Select State', customer_states)
## Filter the DataFrame based on the selected state
filtered_df = merged_df[merged_df['customer_state'] == selected_state]
## Count the product categories
category_counts = filtered_df['product_category_name_english'].value_counts().head(10)
### Create a bar chart
st.subheader(f'Most Selling Product Category for {selected_state}')
st.bar_chart(category_counts)

# Row 5
## Filter the DataFrame based on the selected state
filtered_df_state = merged_df[merged_df['customer_state'] == selected_state]
## Extract unique customer cities based on the selected state
customer_cities = filtered_df_state['customer_city'].unique()
## Create a selectbox for customer cities
selected_city = st.selectbox('Select City', customer_cities)
## Filter the DataFrame based on the selected city
filtered_df_city = filtered_df_state[filtered_df_state['customer_city'] == selected_city]
## Count the product categories with pivot_table
pivot_table = filtered_df_city.pivot_table(
    index='product_category_name_english',
    values=['order_id', 'price'],
    aggfunc={'order_id': 'count', 'price': 'sum'}
).reset_index().sort_values('order_id', ascending=False)
## Rename columns for clarity
pivot_table.columns = ['Product Category', 'Order Count', 'Total Price']
### Display the pivot table
st.subheader(f'Product Category Analysis for {selected_city}, {selected_state}')
st.write(pivot_table)

# Row 6
## Convert order_purchase_timestamp to datetime
filtered_df_city['order_purchase_timestamp'] = pd.to_datetime(filtered_df_city['order_purchase_timestamp'])
## Extract year from order_purchase_timestamp
filtered_df_city['year'] = filtered_df_city['order_purchase_timestamp'].dt.year
## Group by year and calculate the sum of price
yearly_sales = filtered_df_city.groupby('year')['price'].sum().reset_index()
## Convert year to string to ensure proper display on X-axis
yearly_sales['year'] = yearly_sales['year'].astype(str)
### Create a line chart
st.subheader(f'Yearly Sales for {selected_city}, {selected_state}')
st.line_chart(yearly_sales.set_index('year'))