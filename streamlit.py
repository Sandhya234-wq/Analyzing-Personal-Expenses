import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Expense Tracker", layout="wide")

# Function to load data
@st.cache_data
def load_data():
    # CHANGE HERE: Update the path to your CSV file
    data = pd.read_csv(r"D:\guvi\monthly_expenses.csv")  # Replace 'your_file_name.csv' with your actual CSV filename
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def main():
    # CHANGE HERE: Update the title if you want a different name
    st.title("Analyzing Personal Expenses")
    
    try:
        # Load data
        df = load_data()
        
        # Sidebar filters
        st.sidebar.header("Filters")
        
        # Date filter
        date_range = st.sidebar.date_input(
            "Select Date Range",
            [df['Date'].min(), df['Date'].max()]
        )
        
        # Category filter
        categories = ['All'] + list(df['Category'].unique())
        selected_category = st.sidebar.selectbox("Select Category", categories)
        
        # Payment mode filter
        payment_modes = ['All'] + list(df['Payment Mode'].unique())
        selected_payment = st.sidebar.selectbox("Select Payment Mode", payment_modes)
        
        # Filter data
        filtered_df = df.copy()
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        if selected_payment != 'All':
            filtered_df = filtered_df[filtered_df['Payment Mode'] == selected_payment]
            
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Expenses", f"₹{filtered_df['Amount Paid'].sum():,.2f}")
        with col2:
            st.metric("Total Cashback", f"₹{filtered_df['Cashback'].sum():,.2f}")
        with col3:
            st.metric("Average Expense", f"₹{filtered_df['Amount Paid'].mean():,.2f}")
        with col4:
            st.metric("Number of Transactions", len(filtered_df))
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Spending by Category")
            category_spending = filtered_df.groupby('Category')['Amount Paid'].sum().reset_index()
            fig = px.pie(category_spending, values='Amount Paid', names='Category',
                        title='Category-wise Spending Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Payment Mode Analysis")
            payment_spending = filtered_df.groupby('Payment Mode')['Amount Paid'].sum().reset_index()
            fig = px.bar(payment_spending, x='Payment Mode', y='Amount Paid',
                        title='Spending by Payment Mode')
            st.plotly_chart(fig, use_container_width=True)
        
        # Monthly Trend
        st.subheader("Monthly Spending Trend")
        monthly_trend = filtered_df.groupby('Date')['Amount Paid'].sum().reset_index()
        fig = px.line(monthly_trend, x='Date', y='Amount Paid',
                     title='Daily Spending Trend')
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Data View
        st.subheader("Transaction Details")
        st.dataframe(
            filtered_df.style.format({
                'Amount Paid': '₹{:,.2f}',
                'Cashback': '₹{:,.2f}'
            })
        )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please make sure your CSV file is in the correct location and format.")

if __name__ == "__main__":
    main()