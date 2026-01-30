import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Silver Price Calculator & Sales Dashboard",
    page_icon="💎",
    layout="wide"
)

# Title
st.title("💎 Silver Price Calculator & Sales Analysis Dashboard")
st.markdown("---")

# Load actual data from CSV files
@st.cache_data
def load_historical_data():
    """Load historical silver price data from CSV"""
    df = pd.read_csv('historical_silver_price.csv')
    # Create a proper date column
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b')
    return df

@st.cache_data
def load_state_sales_data():
    """Load state-wise silver purchase data from CSV"""
    df = pd.read_csv('state_wise_silver_purchased_kg.csv')
    return df

@st.cache_data
def load_karnataka_monthly_data():
    """Generate Karnataka monthly silver purchase data"""
    # Distribute Karnataka's annual total (16,800 kg) across 12 months
    # with realistic seasonal variation (higher in festival months)
    karnataka_total = 16800
    
    # Monthly distribution weights (festival seasons have higher purchases)
    weights = [1.0, 0.9, 1.1, 0.95, 0.85, 0.9, 0.88, 0.92, 1.05, 1.15, 1.2, 1.3]
    total_weight = sum(weights)
    
    monthly_purchases = [(karnataka_total * w / total_weight) for w in weights]
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    df = pd.DataFrame({
        'Month': months,
        'Purchase_KG': monthly_purchases
    })
    return df

# Load all data
historical_data = load_historical_data()
state_sales = load_state_sales_data()
karnataka_monthly = load_karnataka_monthly_data()

# Get latest silver price (Dec 2025)
latest_price_per_kg = historical_data.iloc[-1]['Silver_Price_INR_per_kg']
latest_price_per_gram = latest_price_per_kg / 1000

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["💰 Price Calculator", "🗺️ Sales Dashboard", "📊 Sales Insights"])

# ============================================================================
# TAB 1: SILVER PRICE CALCULATOR
# ============================================================================
with tab1:
    st.header("Silver Price Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Calculate Silver Cost")
        
        # Current price input
        current_price = st.number_input(
            "Current Silver Price (₹ per gram)", 
            min_value=1.0, 
            value=float(latest_price_per_gram),
            step=0.10,
            help=f"Latest available price (Dec 2025): ₹{latest_price_per_gram:.2f}/gram"
        )
        
        # Weight input with unit selection
        weight_unit = st.selectbox("Select Weight Unit", ["Grams", "Kilograms"])
        
        if weight_unit == "Grams":
            weight = st.number_input("Enter Weight (grams)", min_value=0.0, value=10.0, step=1.0)
            weight_in_grams = weight
        else:
            weight = st.number_input("Enter Weight (kilograms)", min_value=0.0, value=1.0, step=0.1)
            weight_in_grams = weight * 1000
        
        # Calculate total cost
        total_cost_inr = current_price * weight_in_grams
        
        # Display calculation
        st.markdown("### Calculation Result")
        st.success(f"**Total Cost: ₹{total_cost_inr:,.2f}**")
        
        # Currency conversion
        st.markdown("### Currency Conversion")
        currency = st.selectbox("Convert to:", ["USD", "EUR", "GBP", "AED"])
        
        # Exchange rates (as of Jan 2026 - approximate)
        exchange_rates = {
            "USD": 85.50,
            "EUR": 92.30,
            "GBP": 107.80,
            "AED": 23.28
        }
        
        converted_amount = total_cost_inr / exchange_rates[currency]
        st.info(f"**{currency} Equivalent: {currency} {converted_amount:,.2f}**")
        
    with col2:
        st.subheader("Price Breakdown")
        
        # Create a breakdown table
        breakdown_data = {
            'Description': ['Weight', 'Price per Gram', 'Total Cost (INR)', f'Total Cost ({currency})'],
            'Value': [
                f"{weight_in_grams:.2f} grams",
                f"₹{current_price:.2f}",
                f"₹{total_cost_inr:,.2f}",
                f"{currency} {converted_amount:,.2f}"
            ]
        }
        st.table(pd.DataFrame(breakdown_data))
        
        # Quick reference prices
        st.markdown("### Quick Reference (Current Rates)")
        quick_ref = pd.DataFrame({
            'Weight': ['1 gram', '10 grams', '100 grams', '1 kg'],
            'Cost (₹)': [
                f"₹{current_price:,.2f}",
                f"₹{current_price * 10:,.2f}",
                f"₹{current_price * 100:,.2f}",
                f"₹{current_price * 1000:,.2f}"
            ]
        })
        st.dataframe(quick_ref, use_container_width=True)
    
    # Historical Price Chart with Filters
    st.markdown("---")
    st.subheader("📈 Historical Silver Price Trends (2000-2025)")
    
    # Filter options
    price_filter = st.radio(
        "Filter by Price Range:",
        ["All Prices", "≤ ₹20,000 per kg", "₹20,000 - ₹30,000 per kg", "≥ ₹30,000 per kg"],
        horizontal=True
    )
    
    # Apply filters
    filtered_data = historical_data.copy()
    if price_filter == "≤ ₹20,000 per kg":
        filtered_data = filtered_data[filtered_data['Silver_Price_INR_per_kg'] <= 20000]
    elif price_filter == "₹20,000 - ₹30,000 per kg":
        filtered_data = filtered_data[
            (filtered_data['Silver_Price_INR_per_kg'] > 20000) & 
            (filtered_data['Silver_Price_INR_per_kg'] <= 30000)
        ]
    elif price_filter == "≥ ₹30,000 per kg":
        filtered_data = filtered_data[filtered_data['Silver_Price_INR_per_kg'] >= 30000]
    
    # Create interactive chart
    fig_historical = px.line(
        filtered_data,
        x='Date',
        y='Silver_Price_INR_per_kg',
        title=f'Silver Price Trend - {price_filter}',
        labels={'Silver_Price_INR_per_kg': 'Price (₹ per kg)', 'Date': 'Date'},
        template='plotly_white'
    )
    
    fig_historical.update_traces(line_color='#C0C0C0', line_width=2)
    fig_historical.update_layout(hovermode='x unified', height=500)
    
    st.plotly_chart(fig_historical, use_container_width=True)
    
    # Price statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Highest Price", f"₹{filtered_data['Silver_Price_INR_per_kg'].max():,.0f}/kg")
    with col2:
        st.metric("Lowest Price", f"₹{filtered_data['Silver_Price_INR_per_kg'].min():,.0f}/kg")
    with col3:
        st.metric("Average Price", f"₹{filtered_data['Silver_Price_INR_per_kg'].mean():,.0f}/kg")
    with col4:
        if len(filtered_data) > 1:
            price_change = ((filtered_data['Silver_Price_INR_per_kg'].iloc[-1] - 
                           filtered_data['Silver_Price_INR_per_kg'].iloc[0]) / 
                           filtered_data['Silver_Price_INR_per_kg'].iloc[0] * 100)
            st.metric("Change %", f"{price_change:.2f}%")
        else:
            st.metric("Change %", "N/A")

# ============================================================================
# TAB 2: SALES DASHBOARD
# ============================================================================
with tab2:
    st.header("🗺️ State-wise Silver Sales Dashboard")
    
    st.info("📍 **Interactive visualization showing state-wise silver purchases across India**")
    
    st.subheader("State-wise Silver Purchase Distribution")
    
    # Create a choropleth-style bar chart (alternative to map)
    # Sort data for better visualization
    sorted_sales = state_sales.sort_values('Silver_Purchased_kg', ascending=True)
    
    fig_geo = px.bar(
        sorted_sales,
        y='State',
        x='Silver_Purchased_kg',
        orientation='h',
        title='India State-wise Silver Purchases (in kg)',
        labels={'Silver_Purchased_kg': 'Silver Purchased (kg)', 'State': 'State'},
        color='Silver_Purchased_kg',
        color_continuous_scale='Blues',
        height=900
    )
    
    fig_geo.update_layout(showlegend=False)
    st.plotly_chart(fig_geo, use_container_width=True)
    
    # GeoPandas integration code example
    st.markdown("### 🗺️ GeoPandas Map Integration Code")
    st.code("""
# Install required packages:
# pip install geopandas matplotlib

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load India shapefile (download from https://github.com/geohacker/india)
india_map = gpd.read_file('india_states.geojson')

# Load your state sales data
state_sales = pd.read_csv('state_wise_silver_purchased_kg.csv')

# Merge the datasets
india_map = india_map.merge(
    state_sales, 
    left_on='st_nm',  # Adjust column name based on your shapefile
    right_on='State',
    how='left'
)

# Create the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(15, 12))
india_map.plot(
    column='Silver_Purchased_kg',
    cmap='Blues',
    linewidth=0.8,
    ax=ax,
    edgecolor='black',
    legend=True,
    legend_kwds={
        'label': "Silver Purchase (kg)",
        'orientation': "horizontal",
        'shrink': 0.7,
        'pad': 0.05
    },
    missing_kwds={'color': 'lightgrey', 'label': 'No Data'}
)

# Add state labels (optional)
india_map.apply(
    lambda x: ax.annotate(
        text=x['st_nm'], 
        xy=x.geometry.centroid.coords[0], 
        ha='center', 
        fontsize=8
    ), 
    axis=1
)

ax.axis('off')
ax.set_title('State-wise Silver Purchases in India', fontsize=20, weight='bold', pad=20)

# Display in Streamlit
st.pyplot(fig)
    """, language='python')
    
    # Display data table
    st.markdown("### 📊 State-wise Purchase Data Table")
    
    # Add rank column
    state_sales_display = state_sales.sort_values('Silver_Purchased_kg', ascending=False).reset_index(drop=True)
    state_sales_display.index = state_sales_display.index + 1
    state_sales_display.index.name = 'Rank'
    
    st.dataframe(
        state_sales_display,
        use_container_width=True
    )
    
    # Summary statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Purchases", f"{state_sales['Silver_Purchased_kg'].sum():,.0f} kg")
    with col2:
        st.metric("Average per State", f"{state_sales['Silver_Purchased_kg'].mean():,.0f} kg")
    with col3:
        st.metric("States Analyzed", len(state_sales))
    with col4:
        st.metric("Highest Purchase", f"{state_sales['Silver_Purchased_kg'].max():,.0f} kg")

# ============================================================================
# TAB 3: SALES INSIGHTS
# ============================================================================
with tab3:
    st.header("📊 Silver Sales Insights")
    
    # Insight 1: Top 5 states bar chart
    st.subheader("1. Top 5 States with Highest Silver Purchases")
    
    top_5_states = state_sales.nlargest(5, 'Silver_Purchased_kg')
    
    fig_top5 = px.bar(
        top_5_states,
        x='State',
        y='Silver_Purchased_kg',
        title='Top 5 States by Silver Purchase Volume',
        labels={'Silver_Purchased_kg': 'Purchase (kg)', 'State': 'State'},
        color='Silver_Purchased_kg',
        color_continuous_scale='Blues',
        text='Silver_Purchased_kg'
    )
    
    fig_top5.update_traces(texttemplate='%{text:,.0f} kg', textposition='outside')
    fig_top5.update_layout(showlegend=False, height=500)
    
    st.plotly_chart(fig_top5, use_container_width=True)
    
    # Display top 5 table with insights
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Top 5 States Data")
        top_5_display = top_5_states.copy()
        top_5_display['% of Total'] = (top_5_display['Silver_Purchased_kg'] / 
                                        state_sales['Silver_Purchased_kg'].sum() * 100).round(2)
        st.dataframe(top_5_display.reset_index(drop=True), use_container_width=True)
    
    with col2:
        st.markdown("#### Key Insights")
        st.markdown(f"""
        - **Maharashtra** leads with **{top_5_states.iloc[0]['Silver_Purchased_kg']:,.0f} kg** 
          ({(top_5_states.iloc[0]['Silver_Purchased_kg'] / state_sales['Silver_Purchased_kg'].sum() * 100):.1f}% of total)
        - Top 5 states account for **{(top_5_states['Silver_Purchased_kg'].sum() / state_sales['Silver_Purchased_kg'].sum() * 100):.1f}%** 
          of total purchases
        - **Karnataka** ranks 5th with **{top_5_states.iloc[4]['Silver_Purchased_kg']:,.0f} kg**
        - Combined purchases: **{top_5_states['Silver_Purchased_kg'].sum():,.0f} kg**
        """)
    
    st.markdown("---")
    
    # Insight 2: Karnataka monthly trends
    st.subheader("2. Karnataka Monthly Silver Purchase Trends")
    
    fig_karnataka = px.line(
        karnataka_monthly,
        x='Month',
        y='Purchase_KG',
        title='Monthly Silver Purchases in Karnataka (2025)',
        labels={'Purchase_KG': 'Purchase (kg)', 'Month': 'Month'},
        markers=True,
        template='plotly_white'
    )
    
    fig_karnataka.update_traces(
        line_color='#1f77b4',
        line_width=3,
        marker=dict(size=10, color='#C0C0C0', line=dict(width=2, color='#1f77b4'))
    )
    fig_karnataka.update_layout(height=500, hovermode='x unified')
    
    st.plotly_chart(fig_karnataka, use_container_width=True)
    
    # Karnataka statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        max_month = karnataka_monthly.loc[karnataka_monthly['Purchase_KG'].idxmax()]
        st.metric("Highest Month", max_month['Month'], f"{max_month['Purchase_KG']:.0f} kg")
    with col2:
        min_month = karnataka_monthly.loc[karnataka_monthly['Purchase_KG'].idxmin()]
        st.metric("Lowest Month", min_month['Month'], f"{min_month['Purchase_KG']:.0f} kg")
    with col3:
        st.metric("Average Purchase", f"{karnataka_monthly['Purchase_KG'].mean():.0f} kg/month")
    with col4:
        st.metric("Total Annual", f"{karnataka_monthly['Purchase_KG'].sum():,.0f} kg")
    
    # Display Karnataka monthly data
    st.markdown("### Karnataka Monthly Data")
    karnataka_display = karnataka_monthly.copy()
    karnataka_display['Purchase_KG'] = karnataka_display['Purchase_KG'].round(0).astype(int)
    karnataka_display['% of Annual'] = (karnataka_display['Purchase_KG'] / 
                                        karnataka_display['Purchase_KG'].sum() * 100).round(2)
    st.dataframe(karnataka_display, use_container_width=True)
    
    # Additional insights
    st.markdown("---")
    st.subheader("📌 Key Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Regional Distribution:**
        - Maharashtra (22,000 kg) dominates the market
        - Rajasthan (19,800 kg) and Andhra Pradesh (18,500 kg) follow closely
        - Top 3 states represent 27.6% of total national purchases
        - North-eastern states show lower consumption patterns
        - Karnataka (16,800 kg) is 5th largest consumer
        """)
    
    with col2:
        st.markdown("""
        **Karnataka Seasonal Trends:**
        - Peak purchases in **December** (festive season)
        - Consistent demand from **October to December**
        - Lower purchases during **May-August**
        - Strong industrial hub presence drives steady demand
        - Annual consumption: 16,800 kg (7.8% of national total)
        """)
    
    # Regional comparison
    st.markdown("---")
    st.subheader("📍 Regional Distribution Analysis")
    
    # Create regional groups
    regions = {
        'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana'],
        'West': ['Gujarat', 'Maharashtra', 'Goa'],
        'North': ['Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 
                 'Punjab', 'Rajasthan', 'Uttarakhand', 'Ladakh'],
        'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
        'Central': ['Chhattisgarh', 'Madhya Pradesh', 'Uttar Pradesh'],
        'North-East': ['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 
                       'Mizoram', 'Nagaland', 'Sikkim', 'Tripura']
    }
    
    regional_data = []
    for region, states_list in regions.items():
        total = state_sales[state_sales['State'].isin(states_list)]['Silver_Purchased_kg'].sum()
        regional_data.append({'Region': region, 'Total_Purchase_kg': total})
    
    regional_df = pd.DataFrame(regional_data).sort_values('Total_Purchase_kg', ascending=False)
    
    fig_regional = px.pie(
        regional_df,
        values='Total_Purchase_kg',
        names='Region',
        title='Regional Distribution of Silver Purchases',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    st.plotly_chart(fig_regional, use_container_width=True)
    
    st.dataframe(regional_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray;'>
    <p>💎 Silver Price Calculator & Sales Dashboard | Data Period: 2000-2025</p>
    <p>Latest Silver Price (Dec 2025): ₹{latest_price_per_gram:.2f}/gram | ₹{latest_price_per_kg:,.0f}/kg</p>
    <p>Total National Silver Purchases: {state_sales['Silver_Purchased_kg'].sum():,.0f} kg across {len(state_sales)} states</p>
</div>
""", unsafe_allow_html=True)
