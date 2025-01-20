import pandas as pd
import seaborn as sns
import streamlit as st
import altair as alt

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


# Display the DataFrame
st.subheader('Sample data E-Commerce Transaction that delivered to Customer')
st.write(merged_df.head())

# Question 1 : Sebutkan 10 Kota terbanyak yang melakukan transaksi dan berhasil terkirim ?
st.subheader('Question 1:')
st.write('10 kota yang memiliki transaksi terbanyak dan berhasil terkirim')
city_transaction = merged_df['customer_city'].value_counts().head(10)
city_transaction = city_transaction.sort_values(ascending=True)

# Convert to DataFrame for Altair
city_transaction_df = city_transaction.reset_index()
city_transaction_df.columns = ['customer_city', 'transaction_count']

# Create a bar chart with Altair
chart = alt.Chart(city_transaction_df).mark_bar().encode(
    x=alt.X('transaction_count:Q', title='Transaction Count'),
    y=alt.Y('customer_city:N', sort='-x', title='Customer City'),
)

st.altair_chart(chart, use_container_width=True)

# Question 2 : Dari 10 kota tersebut, sebutkan masing-masing 3 produk yang paling banyak dibeli?
st.subheader('Question 2:')
st.write('Dari 10 kota tersebut, sebutkan masing-masing 3 produk yang paling banyak dibeli')

# Find top 3 products for each of the top 10 cities
top_cities = city_transaction.index
top_products_list = []

for city in top_cities:
    city_df = merged_df[merged_df['customer_city'] == city]
    top_products = city_df['product_category_name_english'].value_counts().head(3)
    for product, count in top_products.items():
        top_products_list.append({'city': city, 'product': product, 'count': count})

# Convert to DataFrame for Altair
top_products_df = pd.DataFrame(top_products_list)

# Aggregate total sales count for each city
city_sales_total = top_products_df.groupby('city')['count'].sum().reset_index()

# Sort cities by total sales count in ascending order
sorted_cities = city_sales_total.sort_values(by='count', ascending=False)['city']

# Create a simplified bar chart with Altair
chart = alt.Chart(top_products_df).mark_bar().encode(
    x=alt.X('city:N', title='City', sort=sorted_cities.tolist()),
    y=alt.Y('count:Q', title='Count'),
    color=alt.Color('product:N', title='Product')
).properties(
    title='Top 3 Products in Each of the Top 10 Cities'
).configure_axis(
    labelFontSize=10,
    titleFontSize=12
).configure_legend(
    titleFontSize=12,
    labelFontSize=10
)

st.altair_chart(chart, use_container_width=True)


## Create a selectbox for customer states
selected_state = st.selectbox('Select State', customer_states)
## Filter the DataFrame based on the selected state
filtered_df = merged_df[merged_df['customer_state'] == selected_state]
## Count the product categories
category_counts = filtered_df['product_category_name_english'].value_counts().head(10)
### Create a bar chart
st.subheader(f'Most Selling Product Category for {selected_state}')
st.bar_chart(category_counts)


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
