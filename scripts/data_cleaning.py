"""
Data Cleaning & Preparation Module
==================================
Standalone module for cleaning and preparing the Superstore dataset.
Handles data validation, null values, invalid records, and feature engineering.

Author: Data Analyst
Date: 2026
"""

import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataCleaner:
    """
    A comprehensive data cleaning class for the Superstore dataset.
    Handles missing values, duplicates, type conversions, and validation.
    """
    
    def __init__(self, filepath, output_dir='data'):
        """
        Initialize the DataCleaner.
        
        Args:
            filepath (str): Path to the raw CSV file
            output_dir (str): Directory to save cleaned data
        """
        self.filepath = filepath
        self.output_dir = output_dir
        self.df = None
        self.original_shape = None
        self.cleaning_report = {}
        
    def load_data(self, encoding=None):
        """
        Load CSV with automatic encoding detection.
        
        Args:
            encoding (str): Optional encoding (auto-detect if None)
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Loading data from: {self.filepath}")
        
        if not os.path.exists(self.filepath):
            logger.error(f"File not found: {self.filepath}")
            return False
        
        try:
            # Try different encodings if not specified
            if encoding:
                self.df = pd.read_csv(self.filepath, encoding=encoding)
            else:
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                for enc in encodings:
                    try:
                        self.df = pd.read_csv(self.filepath, encoding=enc)
                        logger.info(f"Successfully loaded with encoding: {enc}")
                        break
                    except (UnicodeDecodeError, UnicodeError):
                        continue
            
            if self.df is None:
                logger.error("Could not load file with any standard encoding")
                return False
            
            self.original_shape = self.df.shape
            logger.info(f"Data loaded successfully: {self.original_shape[0]} rows × {self.original_shape[1]} columns")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def standardize_columns(self):
        """
        Standardize column names to lowercase with underscores.
        """
        logger.info("Standardizing column names...")
        original_names = list(self.df.columns)
        
        self.df.columns = (
            self.df.columns
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
            .str.replace('.', '_')
        )
        
        logger.info(f"Column names standardized: {list(self.df.columns)}")
        self.cleaning_report['columns_standardized'] = original_names
        
    def handle_null_values(self, strategy='drop'):
        """
        Handle null/missing values.
        
        Args:
            strategy (str): 'drop' (remove rows) or 'fill' (fill with median/mode)
        """
        logger.info("Analyzing null values...")
        null_counts = self.df.isnull().sum()
        
        if null_counts.sum() == 0:
            logger.info("✓ No null values detected")
            self.cleaning_report['null_values_removed'] = 0
            return
        
        logger.info(f"Null values found:\n{null_counts[null_counts > 0]}")
        
        initial_rows = len(self.df)
        
        if strategy == 'drop':
            self.df = self.df.dropna()
            rows_removed = initial_rows - len(self.df)
            logger.info(f"✓ Removed {rows_removed} rows with null values")
            self.cleaning_report['null_values_removed'] = rows_removed
        elif strategy == 'fill':
            # Fill numeric with median, categorical with mode
            for col in self.df.columns:
                if self.df[col].isnull().sum() > 0:
                    if self.df[col].dtype in ['int64', 'float64']:
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                    else:
                        self.df[col].fillna(self.df[col].mode()[0], inplace=True)
            logger.info(f"✓ Filled null values using median/mode strategy")
            self.cleaning_report['null_values_filled'] = null_counts.sum()
    
    def remove_duplicates(self):
        """
        Remove duplicate records based on all columns.
        """
        logger.info("Checking for duplicate records...")
        initial_rows = len(self.df)
        
        self.df = self.df.drop_duplicates()
        duplicates_removed = initial_rows - len(self.df)
        
        if duplicates_removed == 0:
            logger.info("✓ No duplicate records found")
        else:
            logger.info(f"✓ Removed {duplicates_removed} duplicate records")
        
        self.cleaning_report['duplicates_removed'] = duplicates_removed
    
    def validate_numeric_fields(self):
        """
        Validate and clean numeric fields.
        Remove negative quantities, invalid prices, etc.
        """
        logger.info("Validating numeric fields...")
        
        initial_rows = len(self.df)
        invalid_rows = 0
        
        # Check for negative quantity
        if 'quantity' in self.df.columns:
            negative_qty = (self.df['quantity'] < 0).sum()
            if negative_qty > 0:
                logger.warning(f"Found {negative_qty} records with negative quantity")
                self.df = self.df[self.df['quantity'] >= 0]
                invalid_rows += negative_qty
        
        # Check for negative sales/revenue
        if 'sales' in self.df.columns:
            negative_sales = (self.df['sales'] < 0).sum()
            if negative_sales > 0:
                logger.warning(f"Found {negative_sales} records with negative sales (keep as valid discounts/returns)")
        
        # Check for unrealistic discount values
        if 'discount' in self.df.columns:
            invalid_discount = ((self.df['discount'] < 0) | (self.df['discount'] > 1)).sum()
            if invalid_discount > 0:
                logger.warning(f"Found {invalid_discount} records with invalid discount (should be 0-1)")
                self.df = self.df[(self.df['discount'] >= 0) & (self.df['discount'] <= 1)]
                invalid_rows += invalid_discount
        
        rows_removed = initial_rows - len(self.df)
        logger.info(f"✓ Validated numeric fields: {rows_removed} invalid records removed")
        self.cleaning_report['invalid_numeric_removed'] = rows_removed
    
    def convert_dates(self, date_columns=None):
        """
        Convert date columns to datetime format.
        
        Args:
            date_columns (list): List of column names containing dates (auto-detect if None)
        """
        logger.info("Converting date columns...")
        
        if date_columns is None:
            # Auto-detect date columns
            date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        
        for col in date_columns:
            try:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                logger.info(f"✓ Converted '{col}' to datetime")
            except Exception as e:
                logger.warning(f"Could not convert '{col}': {str(e)}")
        
        self.cleaning_report['dates_converted'] = date_columns
    
    def engineer_features(self):
        """
        Create useful features from existing columns.
        """
        logger.info("Engineering features...")
        features_created = []
        
        # Temporal features from order_date
        if 'order_date' in self.df.columns:
            self.df['year'] = self.df['order_date'].dt.year
            self.df['month'] = self.df['order_date'].dt.month
            self.df['month_name'] = self.df['order_date'].dt.strftime('%B')
            self.df['quarter'] = self.df['order_date'].dt.quarter
            self.df['day_of_week'] = self.df['order_date'].dt.day_name()
            self.df['year_month'] = self.df['order_date'].dt.strftime('%Y-%m')
            
            features_created.extend(['year', 'month', 'month_name', 'quarter', 'day_of_week', 'year_month'])
            logger.info(f"✓ Created temporal features: {features_created}")
        
        # Revenue from sales and quantity
        if 'sales' in self.df.columns and 'quantity' in self.df.columns:
            self.df['unit_price'] = self.df['sales'] / self.df['quantity']
            self.df['unit_price'] = self.df['unit_price'].replace([np.inf, -np.inf], np.nan)
            features_created.append('unit_price')
            logger.info(f"✓ Created unit_price feature")
        
        # Profit margin
        if 'profit' in self.df.columns and 'sales' in self.df.columns:
            self.df['profit_margin'] = (self.df['profit'] / self.df['sales']).replace([np.inf, -np.inf], np.nan)
            features_created.append('profit_margin')
            logger.info(f"✓ Created profit_margin feature")
        
        self.cleaning_report['features_engineered'] = features_created
    
    def generate_summary(self):
        """
        Generate a data quality summary report.
        
        Returns:
            dict: Summary statistics
        """
        logger.info("\n" + "="*70)
        logger.info("DATA QUALITY SUMMARY")
        logger.info("="*70)
        
        summary = {
            'original_records': self.original_shape[0],
            'final_records': len(self.df),
            'records_removed': self.original_shape[0] - len(self.df),
            'columns': len(self.df.columns),
            'null_values': self.df.isnull().sum().sum(),
            'duplicates': self.df.duplicated().sum(),
            'data_types': dict(self.df.dtypes),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        logger.info(f"Original Records: {summary['original_records']}")
        logger.info(f"Final Records: {summary['final_records']}")
        logger.info(f"Records Removed: {summary['records_removed']}")
        logger.info(f"Total Columns: {summary['columns']}")
        logger.info(f"Remaining Null Values: {summary['null_values']}")
        logger.info(f"Remaining Duplicates: {summary['duplicates']}")
        logger.info(f"Memory Usage: {summary['memory_usage_mb']:.2f} MB")
        
        return summary
    
    def save_cleaned_data(self, filename='superstore_cleaned.csv'):
        """
        Save the cleaned dataset to CSV.
        
        Args:
            filename (str): Output filename
        """
        logger.info("\nSaving cleaned dataset...")
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_path = os.path.join(self.output_dir, filename)
        self.df.to_csv(output_path, index=False)
        
        file_size_mb = os.path.getsize(output_path) / 1024**2
        logger.info(f"✓ Cleaned data saved to: {output_path}")
        logger.info(f"✓ File size: {file_size_mb:.2f} MB")
        
        return output_path
    
    def clean_all(self):
        """
        Execute the complete cleaning pipeline.
        
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        logger.info("\n" + "="*70)
        logger.info("STARTING DATA CLEANING PIPELINE")
        logger.info("="*70 + "\n")
        
        # Execute pipeline
        if not self.load_data():
            return None
        
        self.standardize_columns()
        self.remove_duplicates()
        self.handle_null_values(strategy='drop')
        self.validate_numeric_fields()
        self.convert_dates()
        self.engineer_features()
        
        # Generate summary
        summary = self.generate_summary()
        
        logger.info("\n" + "="*70)
        logger.info("✓ CLEANING PIPELINE COMPLETE")
        logger.info("="*70 + "\n")
        
        # Save the cleaned data
        self.save_cleaned_data()
        
        return self.df


# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """
    Example usage of the DataCleaner class.
    """
    # Find the data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    possible_paths = [
        os.path.join(project_dir, 'data', 'superstore.csv'),
        os.path.join(os.path.dirname(project_dir), 'data', 'superstore.csv'),
        'superstore.csv'
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
    
    if data_path is None:
        print("⚠️  Error: superstore.csv not found")
        print("Searched paths:")
        for path in possible_paths:
            print(f"  - {path}")
        return
    
    # Initialize and run cleaner
    output_dir = os.path.join(project_dir, 'data')
    cleaner = DataCleaner(data_path, output_dir=output_dir)
    
    # Clean all
    cleaned_df = cleaner.clean_all()
    
    if cleaned_df is not None:
        print("\n✓ Data cleaning successful!")
        print(f"✓ Output saved to: {os.path.join(output_dir, 'superstore_cleaned.csv')}")
    else:
        print("\n❌ Data cleaning failed!")


if __name__ == "__main__":
    main()
