"""
Superstore Sales Analysis Script
=================================
A comprehensive data analysis script for the Superstore dataset.
Includes data cleaning, feature engineering, analysis, and visualization.

Author: Data Analyst
Date: 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Configure plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# ============================================================================
# STEP 1: LOAD DATASET
# ============================================================================
def load_data(filepath):
    """
    Load the Superstore dataset from CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    print("=" * 70)
    print("STEP 1: LOADING DATA")
    print("=" * 70)
    
    try:
        # Try multiple encodings to handle different file formats
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                print(f"✓ Data loaded successfully from: {filepath}")
                print(f"✓ Used encoding: {encoding}")
                print(f"✓ Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
                return df
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if df is None:
            raise ValueError("Could not load CSV with any standard encoding")
            
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        raise


# ============================================================================
# STEP 2: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================
def explore_data(df):
    """
    Perform initial exploratory data analysis.
    
    Args:
        df (pd.DataFrame): Dataset to explore
    """
    print("\n" + "=" * 70)
    print("STEP 2: EXPLORATORY DATA ANALYSIS")
    print("=" * 70)
    
    print("\n📊 FIRST 5 ROWS:")
    print(df.head())
    
    print("\n📋 COLUMN NAMES & DATA TYPES:")
    print(df.dtypes)
    
    print("\n📈 DATASET INFO:")
    print(f"Total rows: {df.shape[0]}")
    print(f"Total columns: {df.shape[1]}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\n🔍 MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("✓ No missing values detected")
    else:
        print(missing[missing > 0])
    
    print("\n📊 BASIC STATISTICS:")
    print(df.describe())


# ============================================================================
# STEP 3: DATA CLEANING
# ============================================================================
def clean_data(df):
    """
    Clean and preprocess the dataset.
    
    Args:
        df (pd.DataFrame): Raw dataset
        
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    print("\n" + "=" * 70)
    print("STEP 3: DATA CLEANING")
    print("=" * 70)
    
    df = df.copy()
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    print(f"✓ Removed {duplicates_removed} duplicate rows")
    
    # Drop rows with missing values
    initial_rows = len(df)
    df = df.dropna()
    na_removed = initial_rows - len(df)
    print(f"✓ Removed {na_removed} rows with missing values")
    
    # Standardize column names (lowercase + underscores)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    print(f"✓ Standardized column names")
    print(f"  Columns: {list(df.columns)}")
    
    return df


# ============================================================================
# STEP 4: FEATURE ENGINEERING
# ============================================================================
def engineer_features(df):
    """
    Create new features from existing columns.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        pd.DataFrame: Dataset with new features
    """
    print("\n" + "=" * 70)
    print("STEP 4: FEATURE ENGINEERING")
    print("=" * 70)
    
    df = df.copy()
    
    # Convert order_date to datetime (handle common column name variations)
    date_columns = [col for col in df.columns if 'date' in col.lower() and 'order' in col.lower()]
    if date_columns:
        date_col = date_columns[0]
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        print(f"✓ Converted '{date_col}' to datetime format")
        
        # Extract month and year
        df['month'] = df[date_col].dt.month
        df['year'] = df[date_col].dt.year
        df['month_name'] = df[date_col].dt.strftime('%B')
        df['year_month'] = df[date_col].dt.strftime('%Y-%m')
        print(f"✓ Created month, year, and year_month features")
    
    return df


# ============================================================================
# STEP 5: CREATE BUSINESS METRICS
# ============================================================================
def calculate_metrics(df):
    """
    Calculate key business metrics.
    
    Args:
        df (pd.DataFrame): Dataset with features
        
    Returns:
        dict: Dictionary of key metrics
    """
    print("\n" + "=" * 70)
    print("STEP 5: BUSINESS METRICS")
    print("=" * 70)
    
    # Identify revenue and profit columns
    revenue_col = next((col for col in df.columns if 'sales' in col.lower() or 'revenue' in col.lower()), None)
    profit_col = next((col for col in df.columns if 'profit' in col.lower()), None)
    
    metrics = {}
    
    if revenue_col:
        total_revenue = df[revenue_col].sum()
        metrics['total_revenue'] = total_revenue
        print(f"✓ Total Revenue: ${total_revenue:,.2f}")
    
    if profit_col:
        total_profit = df[profit_col].sum()
        metrics['total_profit'] = total_profit
        profit_margin = (total_profit / total_revenue * 100) if revenue_col else 0
        print(f"✓ Total Profit: ${total_profit:,.2f}")
        print(f"✓ Profit Margin: {profit_margin:.2f}%")
    
    # Count total orders
    total_orders = len(df)
    metrics['total_orders'] = total_orders
    print(f"✓ Total Orders: {total_orders:,}")
    
    if revenue_col:
        avg_order_value = total_revenue / total_orders
        print(f"✓ Average Order Value: ${avg_order_value:,.2f}")
    
    return metrics


# ============================================================================
# STEP 6: GROUPING ANALYSIS
# ============================================================================
def analyze_groups(df):
    """
    Perform grouping analysis by region, category, customer, etc.
    
    Args:
        df (pd.DataFrame): Dataset with features
        
    Returns:
        dict: Dictionary of grouped analyses
    """
    print("\n" + "=" * 70)
    print("STEP 6: GROUPING ANALYSIS")
    print("=" * 70)
    
    revenue_col = next((col for col in df.columns if 'sales' in col.lower() or 'revenue' in col.lower()), None)
    profit_col = next((col for col in df.columns if 'profit' in col.lower()), None)
    region_col = next((col for col in df.columns if 'region' in col.lower()), None)
    category_col = next((col for col in df.columns if 'category' in col.lower()), None)
    customer_col = next((col for col in df.columns if 'customer' in col.lower() and 'id' in col.lower()), None)
    year_month_col = 'year_month' if 'year_month' in df.columns else None
    
    analyses = {}
    
    # Revenue by Month
    if revenue_col and year_month_col:
        revenue_by_month = df.groupby(year_month_col)[revenue_col].sum().sort_index()
        analyses['revenue_by_month'] = revenue_by_month
        print(f"\n✓ Revenue by Month (Top 5):")
        print(revenue_by_month.tail().to_string())
    
    # Revenue by Region
    if revenue_col and region_col:
        revenue_by_region = df.groupby(region_col)[revenue_col].sum().sort_values(ascending=False)
        analyses['revenue_by_region'] = revenue_by_region
        print(f"\n✓ Revenue by Region:")
        print(revenue_by_region.to_string())
    
    # Profit by Category
    if profit_col and category_col:
        profit_by_category = df.groupby(category_col)[profit_col].sum().sort_values(ascending=False)
        analyses['profit_by_category'] = profit_by_category
        print(f"\n✓ Profit by Category:")
        print(profit_by_category.to_string())
    
    # Top 10 Customers
    if revenue_col and customer_col:
        top_customers = df.groupby(customer_col)[revenue_col].sum().sort_values(ascending=False).head(10)
        analyses['top_customers'] = top_customers
        print(f"\n✓ Top 10 Customers by Revenue:")
        print(top_customers.to_string())
    
    return analyses


# ============================================================================
# STEP 7: VISUALIZATIONS
# ============================================================================
def create_visualizations(df, analyses, output_dir):
    """
    Create professional visualizations and save them.
    
    Args:
        df (pd.DataFrame): Dataset
        analyses (dict): Grouped analyses
        output_dir (str): Directory to save charts
    """
    print("\n" + "=" * 70)
    print("STEP 7: CREATING VISUALIZATIONS")
    print("=" * 70)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    revenue_col = next((col for col in df.columns if 'sales' in col.lower() or 'revenue' in col.lower()), None)
    profit_col = next((col for col in df.columns if 'profit' in col.lower()), None)
    region_col = next((col for col in df.columns if 'region' in col.lower()), None)
    category_col = next((col for col in df.columns if 'category' in col.lower()), None)
    
    # Chart 1: Revenue Over Time
    if 'revenue_by_month' in analyses:
        plt.figure(figsize=(14, 6))
        analyses['revenue_by_month'].plot(kind='line', marker='o', color='#2E86AB', linewidth=2)
        plt.title('Revenue Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=11)
        plt.ylabel('Revenue ($)', fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        chart_path = os.path.join(output_dir, '01_revenue_over_time.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: 01_revenue_over_time.png")
    
    # Chart 2: Sales by Region
    if 'revenue_by_region' in analyses:
        plt.figure(figsize=(10, 6))
        analyses['revenue_by_region'].plot(kind='bar', color='#A23B72')
        plt.title('Revenue by Region', fontsize=14, fontweight='bold')
        plt.xlabel('Region', fontsize=11)
        plt.ylabel('Revenue ($)', fontsize=11)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        chart_path = os.path.join(output_dir, '02_revenue_by_region.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: 02_revenue_by_region.png")
    
    # Chart 3: Profit by Category
    if 'profit_by_category' in analyses:
        plt.figure(figsize=(10, 6))
        analyses['profit_by_category'].plot(kind='barh', color='#F18F01')
        plt.title('Profit by Category', fontsize=14, fontweight='bold')
        plt.xlabel('Profit ($)', fontsize=11)
        plt.ylabel('Category', fontsize=11)
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        chart_path = os.path.join(output_dir, '03_profit_by_category.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: 03_profit_by_category.png")
    
    # Chart 4: Top Customers
    if 'top_customers' in analyses:
        plt.figure(figsize=(10, 6))
        top_10 = analyses['top_customers'].head(10)
        top_10.sort_values().plot(kind='barh', color='#06A77D')
        plt.title('Top 10 Customers by Revenue', fontsize=14, fontweight='bold')
        plt.xlabel('Revenue ($)', fontsize=11)
        plt.ylabel('Customer ID', fontsize=11)
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        chart_path = os.path.join(output_dir, '04_top_customers.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: 04_top_customers.png")


# ============================================================================
# STEP 8: SAVE CLEANED DATA
# ============================================================================
def save_cleaned_data(df, output_path):
    """
    Save the cleaned dataset to CSV.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        output_path (str): Path to save the CSV file
    """
    print("\n" + "=" * 70)
    print("STEP 8: SAVING CLEANED DATA")
    print("=" * 70)
    
    df.to_csv(output_path, index=False)
    print(f"✓ Cleaned data saved to: {output_path}")
    print(f"✓ File size: {os.path.getsize(output_path) / 1024:.2f} KB")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """
    Main execution function for the Superstore analysis.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "SUPERSTORE SALES ANALYSIS" + " " * 27 + "║")
    print("║" + " " * 18 + "Professional Data Analysis Project" + " " * 16 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # File paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Try multiple possible data paths
    possible_paths = [
        os.path.join(project_dir, 'data', 'superstore.csv'),
        os.path.join(os.path.dirname(project_dir), 'data', 'superstore.csv'),
        '../data/superstore.csv',
        'superstore.csv'
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
    
    if data_path is None:
        print("\n⚠️  WARNING: superstore.csv not found in expected locations")
        print("Searched paths:")
        for path in possible_paths:
            print(f"  - {path}")
        print("\nPlease ensure the superstore.csv file is in the data/ directory")
        return
    
    output_dir = os.path.join(project_dir, 'outputs', 'charts')
    cleaned_data_path = os.path.join(project_dir, 'data', 'superstore_cleaned.csv')
    
    try:
        # Execute pipeline
        df = load_data(data_path)
        explore_data(df)
        df = clean_data(df)
        df = engineer_features(df)
        metrics = calculate_metrics(df)
        analyses = analyze_groups(df)
        create_visualizations(df, analyses, output_dir)
        save_cleaned_data(df, cleaned_data_path)
        
        # Final summary
        print("\n" + "=" * 70)
        print("✓ ANALYSIS COMPLETE!")
        print("=" * 70)
        print("\nGenerated files:")
        print(f"  - Cleaned data: {cleaned_data_path}")
        print(f"  - Charts: {output_dir}/")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
