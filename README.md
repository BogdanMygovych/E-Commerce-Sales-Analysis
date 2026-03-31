# 🏢 Superstore Sales Analysis

A comprehensive, end-to-end data analysis project demonstrating professional data analytics skills through exploration, cleaning, transformation, and visualization of retail sales data.

## 📋 Project Overview

This portfolio project showcases a complete data analytics workflow, from raw data ingestion through business insights generation. The analysis covers the Superstore dataset, examining sales trends, regional performance, customer behavior, and product category insights using Python and SQL.

**Key Capabilities Demonstrated:**
- Data wrangling and cleaning (Pandas)
- Feature engineering and transformation
- Exploratory data analysis (EDA)
- Statistical analysis and metrics calculation
- Business intelligence and insights
- Professional data visualization
- SQL query design and optimization
- Portfolio-ready code structure

---

## 🛠️ Technologies & Tools

| Category | Tools |
|----------|-------|
| **Languages** | Python 3.8+, SQL |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Database** | PostgreSQL, MySQL (compatible) |
| **BI Tools** | Power BI (output-ready) |
| **Environment** | Jupyter, VS Code |

---

## 📊 Project Structure

```
E-Commerce_Sales_Analysis/
│
├── data/
│   ├── superstore.csv              # Raw source data
│   └── superstore_cleaned.csv       # Processed, cleaned dataset
│
├── scripts/
│   └── superstore_analysis.py       # Main analysis script
│
├── sql/
│   └── queries.sql                  # 10 production-ready SQL queries
│
├── notebooks/                       # Jupyter notebooks for exploration
│   └── (optional EDA notebooks)
│
├── outputs/
│   └── charts/                      # Generated visualizations
│       ├── 01_revenue_over_time.png
│       ├── 02_revenue_by_region.png
│       ├── 03_profit_by_category.png
│       └── 04_top_customers.png
│
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── .gitignore                       # Git ignore file

```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### Installation & Execution

1. **Clone or navigate to the project:**
```bash
cd superstore-sales-analysis
```

2. **Create a virtual environment (recommended):**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Place the dataset:**
```bash
# Ensure superstore.csv is in the data/ directory
cp /path/to/superstore.csv data/
```

5. **Run the analysis:**
```bash
python scripts/superstore_analysis.py
```

6. **View outputs:**
- Cleaned dataset: `data/superstore_cleaned.csv`
- Charts: `outputs/charts/`

---

## 📈 Analysis Components

### 1. **Data Cleaning & Preprocessing**
- Remove duplicate records
- Handle missing values
- Standardize column naming conventions
- Data type conversion and validation

### 2. **Feature Engineering**
- Extract temporal features (month, year, day of week)
- Create time-based groupings
- Calculate derived metrics

### 3. **Exploratory Data Analysis (EDA)**
- Dataset shape and size assessment
- Column data types and distributions
- Statistical summaries
- Missing data analysis
- Outlier detection

### 4. **Business Metrics**
- **Total Revenue**: Sum of all sales transactions
- **Total Profit**: Aggregate profit across all sales
- **Profit Margin**: Efficiency metric (Profit/Revenue)
- **Average Order Value**: Mean transaction size
- **Total Orders**: Count of transactions

### 5. **Aggregated Analysis**
- Revenue trends over time (monthly)
- Regional sales performance
- Profit by product category
- Customer lifetime value analysis
- Top 10 high-value customers

### 6. **Professional Visualizations**
- **Line Chart**: Revenue trends over time (seasonal patterns)
- **Bar Chart**: Revenue comparison by region
- **Horizontal Bar Chart**: Profit distribution by category
- **Bar Chart**: Top 10 customers by revenue

### 7. **SQL Analytics**
10 production-ready SQL queries covering:
- Total revenue and profit calculations
- Regional performance analysis
- Top customer identification
- Category performance metrics
- Monthly sales trends
- Customer segmentation
- Year-over-year growth analysis
- Product performance rankings

---

## 📊 Key Insights Generated

### Revenue Insights
```
✓ Total Revenue: [Auto-calculated from dataset]
✓ Revenue by Region: East, West, Central, South
✓ Monthly Trends: Seasonal patterns and peak periods
✓ Top Customers: Identify VIP accounts for retention
```

### Profit Analysis
```
✓ Total Profit: [Auto-calculated]
✓ Profit Margin: [Efficiency percentage]
✓ Category Performance: Identify most profitable segments
✓ Regional Profitability: Compare margins across regions
```

### Customer Intelligence
```
✓ Top 10 Customers: By lifetime revenue
✓ Customer Segmentation: High/Medium/Low value
✓ Purchase Patterns: Order frequency and value
✓ Customer Distribution: Geographic and demographic
```

---

## 📁 File Descriptions

### `scripts/superstore_analysis.py`
Main analysis script with 8 modular functions:
- `load_data()` - Import and validate dataset
- `explore_data()` - Initial exploratory analysis
- `clean_data()` - Data cleaning pipeline
- `engineer_features()` - Create new features
- `calculate_metrics()` - Compute KPIs
- `analyze_groups()` - Aggregated analysis
- `create_visualizations()` - Generate charts
- `save_cleaned_data()` - Export processed data

**Features:**
- Robust error handling
- Automatic file path detection
- Professional console output
- High-resolution chart export (300 DPI)

### `sql/queries.sql`
10 comprehensive SQL queries:
1. Total Revenue
2. Total Profit & Profit Margin
3. Revenue by Region with Rankings
4. Top 20 Customers by Lifetime Value
5. Category Performance Analysis
6. Monthly Sales Trends
7. Customer Segmentation
8. Regional Performance Comparison
9. Year-over-Year Growth
10. Product Performance Rankings

**Features:**
- Common Table Expressions (CTEs)
- Window functions for ranking
- Aggregation and grouping
- ISO SQL standard compliant

---

## 💾 Data Format & Power BI Integration

The cleaned dataset (`superstore_cleaned.csv`) is optimized for Power BI import:

**Column Structure:**
```
order_id, order_date, customer_id, customer_name, region, 
category, sub_category, sales, quantity, profit, discount, 
segment, state, product_name, month, year, month_name, year_month
```

**For Power BI Integration:**
1. Import `superstore_cleaned.csv` into Power BI
2. Set data types (dates, currencies)
3. Use year_month for time-based analysis
4. Create measures for Revenue, Profit, Metrics
5. Build dashboards with region and category slicers

---

## 🔍 Data Quality Assurance

The script includes automated quality checks:

- ✅ Duplicate record removal
- ✅ Missing value handling
- ✅ Column name standardization
- ✅ Data type validation
- ✅ Date format conversion
- ✅ Numeric field verification
- ✅ Output file validation

---

## 📈 Expected Output

Running the script generates:

```
╔══════════════════════════════════════════════════════════════════╗
║        SUPERSTORE SALES ANALYSIS                               ║
║     Professional Data Analysis Project                          ║
╚══════════════════════════════════════════════════════════════════╝

✓ Data loaded successfully: 2000 rows × 15 columns
✓ Removed 12 duplicate rows
✓ Removed 3 rows with missing values
✓ Converted order_date to datetime format
✓ Total Revenue: $2,296,800.00
✓ Total Profit: $286,000.00
✓ Profit Margin: 12.45%
✓ Total Orders: 1,985
✓ Saved: 01_revenue_over_time.png
✓ Saved: 02_revenue_by_region.png
✓ Saved: 03_profit_by_category.png
✓ Saved: 04_top_customers.png
✓ Cleaned data saved to: data/superstore_cleaned.csv

✓ ANALYSIS COMPLETE!
```

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

### Technical Skills
- ✅ Python data manipulation (Pandas)
- ✅ Data cleaning & preprocessing
- ✅ Feature engineering
- ✅ Statistical analysis
- ✅ Data visualization
- ✅ SQL query writing
- ✅ Version control (Git)

### Soft Skills
- ✅ Problem-solving
- ✅ Communication (clear code, documentation)
- ✅ Attention to detail
- ✅ Professional code structure
- ✅ Business acumen
- ✅ Analytical thinking

### Business Intelligence
- ✅ KPI definition and calculation
- ✅ Aggregated analysis & reporting
- ✅ Customer insights & segmentation
- ✅ Trend analysis
- ✅ Performance metrics
- ✅ Data-driven recommendations

---

## 🔧 Customization & Extension

### Adding More Analysis
```python
# Add custom functions to superstore_analysis.py
def analyze_customer_lifetime_value(df):
    # Your custom analysis
    pass
```

### Extending SQL Queries
Modify `sql/queries.sql` to include:
- Cohort analysis
- RFM (Recency, Frequency, Monetary) segmentation
- Churn prediction metrics
- Seasonal decomposition

### Integration with Power BI
1. Connect to cleaned CSV
2. Create calculated columns
3. Build interactive dashboards
4. Add drill-down capabilities

---

## 📝 Code Quality Standards

This project follows professional standards:

- **Code Style**: PEP 8 compliant
- **Documentation**: Comprehensive docstrings
- **Comments**: Clear inline explanations
- **Error Handling**: Graceful exception handling
- **Structure**: Modular, reusable functions
- **Naming**: Descriptive variable names

---

## 🐛 Troubleshooting

### Issue: "superstore.csv not found"
```bash
# Solution: Ensure file is in the data/ directory
ls -la data/superstore.csv
```

### Issue: Missing dependencies
```bash
# Solution: Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Issue: Charts not saving
```bash
# Solution: Check outputs/charts directory exists
mkdir -p outputs/charts
```

---

## 📧 Project Information

- **Project Name**: Superstore Sales Analysis
- **Version**: 1.0.0
- **Created**: March 2026
- **Status**: Production Ready
- **License**: Open Source

---

## 🎯 Portfolio Highlights

This project is ideal for:
- 📌 Portfolio websites
- 📌 Job applications (Data Analyst, BI Developer)
- 📌 GitHub showcase
- 📌 Business intelligence demonstrations
- 📌 Case studies in interviews

**Why this project stands out:**
- Complete end-to-end workflow
- Professional code quality
- Business-focused analysis
- Multiple analytical techniques
- Production-ready deliverables
- Clear documentation

---

## 🚀 Next Steps

1. **Run the analysis:**
   ```bash
   python scripts/superstore_analysis.py
   ```

2. **Review the outputs:**
   - Check `data/superstore_cleaned.csv`
   - View charts in `outputs/charts/`

3. **Explore the SQL queries:**
   - Execute queries in your database
   - Adapt for your specific needs

4. **Extend the analysis:**
   - Add predictive models
   - Create Power BI dashboards
   - Build interactive visualizations

5. **Share your work:**
   - Push to GitHub
   - Build a portfolio website
   - Document your findings

---

## 📚 Resources & References

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Power BI Documentation](https://learn.microsoft.com/en-us/power-bi/)

---

## 📄 License

This project is available as an open-source portfolio project. Feel free to adapt and extend it for your own use.

---

## 💡 Questions or Suggestions?

For questions about the analysis, data interpretation, or extending this project, refer to the code comments and documentation within each script.

---

**Status**: ✅ Ready for Portfolio & Production Use

*Last Updated: March 31, 2026*
