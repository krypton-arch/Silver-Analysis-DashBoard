# 💎 Silver Price Calculator & Sales Analysis Dashboard

A comprehensive web application built with Streamlit for analyzing silver prices and visualizing state-wise sales data across India. This dashboard provides historical price trends, interactive calculators, and detailed insights into regional silver consumption patterns.

## 🌟 Features

### 1. Silver Price Calculator (5 Marks)
- **Real-time Cost Calculation**: Calculate silver costs based on weight (grams/kilograms)
- **Current Pricing**: Uses latest silver prices (Dec 2025: ₹43.10/gram)
- **Currency Conversion**: Convert prices to USD, EUR, GBP, and AED
- **Quick Reference**: Instant pricing for common weights (1g, 10g, 100g, 1kg)
- **Historical Price Visualization**: Interactive charts with filter options:
  - ≤ ₹20,000 per kg
  - ₹20,000 - ₹30,000 per kg
  - ≥ ₹30,000 per kg
- **Price Statistics**: Track highest, lowest, average prices and percentage changes

### 2. Silver Sales Dashboard (5 Marks)
- **State-wise Visualization**: Interactive maps and charts showing purchases across 31 Indian states
- **GeoPandas Integration**: Code for choropleth mapping with darker shades for higher purchases
- **Comprehensive Data Table**: Complete breakdown with rankings and percentages
- **Summary Statistics**: Total purchases, averages, and key metrics

### 3. Silver Sales Insights
- **Top 5 States Analysis**: Bar chart visualization of highest-purchasing states
- **Karnataka Monthly Trends**: Line chart showing seasonal purchase patterns
- **Regional Distribution**: Pie chart breaking down purchases by region (North, South, East, West, Central, North-East)
- **Key Market Insights**: Data-driven observations and trends

## 📊 Dataset Information

### Historical Silver Price Data
- **Time Period**: January 2000 - December 2025 (312 data points)
- **Price Range**: ₹8,030/kg (Jan 2000) → ₹43,100/kg (Dec 2025)
- **Growth**: 437% increase over 25 years
- **Source**: historical_silver_price.csv

### State-wise Purchase Data
- **Coverage**: 31 Indian states and union territories
- **Total Purchases**: 215,990 kg nationwide
- **Top States**: 
  - Maharashtra: 22,000 kg (10.2%)
  - Rajasthan: 19,800 kg (9.2%)
  - Andhra Pradesh: 18,500 kg (8.6%)
  - Tamil Nadu: 17,500 kg (8.1%)
  - Karnataka: 16,800 kg (7.8%)
- **Source**: state_wise_silver_purchased_kg.csv

## 🚀 Live Demo

Add your deployed Streamlit app URL here

Example: https://your-username-silver-price-calculator.streamlit.app

## 📁 Project Structure

silver-price-calculator/
│
├── app.py                                  
├── requirements.txt                        
├── historical_silver_price.csv            
├── state_wise_silver_purchased_kg.csv     
└── README.md                              

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **GeoPandas** - Geographic data processing
- **NumPy** - Numerical computing
- **Matplotlib** - Additional plotting capabilities

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/silver-price-calculator.git
cd silver-price-calculator

### Step 2: Install Dependencies

pip install -r requirements.txt

### Step 3: Run the Application

streamlit run app.py

The app will open in your default browser at http://localhost:8501

## 📋 Requirements

streamlit==1.31.0
pandas==2.1.4
geopandas==0.14.1
plotly==5.18.0
numpy==1.26.3
matplotlib==3.8.2

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push your code to GitHub**
2. **Go to** https://share.streamlit.io
3. **Sign in** with your GitHub account
4. **Click** "New app"
5. **Configure**:
   - Repository: YOUR-USERNAME/silver-price-calculator
   - Branch: main
   - Main file path: app.py
6. **Click** "Deploy"

Your app will be live within minutes!

### Other Deployment Options
- **Heroku**: Use Procfile with web: streamlit run app.py --server.port=$PORT
- **AWS/GCP/Azure**: Deploy using Docker containers
- **Local Network**: Use streamlit run app.py --server.address=0.0.0.0

## 📸 Screenshots

### Silver Price Calculator
- Real-time price calculations with currency conversion
- Historical price trends with interactive filters
- Price statistics and breakdowns

### Sales Dashboard
- State-wise silver purchase visualization
- Interactive geographical representation
- Comprehensive data tables

### Sales Insights
- Top 5 states bar chart
- Karnataka monthly trends line chart
- Regional distribution analysis

## 🔧 Usage Examples

### Calculate Silver Cost
1. Navigate to the "Price Calculator" tab
2. Enter the current price per gram (default: latest available price)
3. Select weight unit (grams or kilograms)
4. Enter the weight
5. View total cost in INR and convert to other currencies

### Analyze Historical Trends
1. Scroll to the "Historical Silver Price Trends" section
2. Select a price range filter
3. View interactive chart with zoom and hover capabilities
4. Check price statistics (highest, lowest, average, change %)

### Explore State-wise Sales
1. Navigate to the "Sales Dashboard" tab
2. View horizontal bar chart showing all states
3. Check the detailed data table with rankings
4. Review summary statistics

### View Top Performers
1. Navigate to the "Sales Insights" tab
2. Analyze top 5 states with bar chart
3. Explore Karnataka's monthly purchase patterns
4. Review regional distribution pie chart

## 🔍 Key Insights

### Market Trends
- Silver prices have shown consistent growth from ₹8,030/kg (2000) to ₹43,100/kg (2025)
- Significant acceleration in price growth post-2020
- Maharashtra dominates the market with 10.2% of national purchases

### Regional Patterns
- **Western India** (Maharashtra, Gujarat) leads in consumption
- **Southern states** show strong industrial demand
- **North-eastern states** have lower consumption rates
- **Karnataka** shows peak purchases during December (festive season)

### Seasonal Variations
- Higher purchases during October-December (festival season)
- Relatively stable demand throughout the year
- Industrial hubs maintain consistent purchase patterns

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Real-time price API integration
- [ ] Gold price comparison feature
- [ ] Advanced forecasting models
- [ ] Export data as PDF/Excel
- [ ] Email price alerts
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Historical comparison tool

## 🙏 Acknowledgments

- Silver price data sourced from historical market records
- State-wise purchase data compiled from industry reports
- Built as part of MCA curriculum at Christ University, Bangalore
- Streamlit community for excellent documentation and support

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact: your.email@example.com

## 🏆 Project Grading Criteria

### Silver Price Calculator (5 Marks)
- ✅ Weight input (grams/kilograms)
- ✅ Current price input
- ✅ Total cost calculation
- ✅ Currency conversion (INR to USD, EUR, GBP, AED)
- ✅ Historical price chart with 3 filter options

### Silver Sales Dashboard (5 Marks)
- ✅ State-wise data loading
- ✅ GeoPandas map visualization code
- ✅ Choropleth representation
- ✅ Top 5 states bar chart
- ✅ Karnataka monthly trends line chart

---

⭐ If you find this project helpful, please give it a star!

Made with ❤️ using Streamlit and Python
