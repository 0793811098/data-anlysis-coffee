"""
Data Agent - Handles data loading, cleaning, and preprocessing
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import json


class DataAgent:
    """
    Responsible for:
    - Loading coffee data from various sources
    - Data validation and cleaning
    - Preprocessing and feature engineering
    - Data quality checks
    """
    
    def __init__(self, data_source: str = None):
        """Initialize the Data Agent"""
        self.data_source = data_source
        self.df = None
        self.metadata = {}
        
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load data from CSV, Excel, or JSON
        
        Args:
            filepath: Path to the data file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if filepath.endswith('.csv'):
                self.df = pd.read_csv(filepath)
            elif filepath.endswith(('.xls', '.xlsx')):
                self.df = pd.read_excel(filepath)
            elif filepath.endswith('.json'):
                self.df = pd.read_json(filepath)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")
            
            self.metadata['source'] = filepath
            self.metadata['rows'] = len(self.df)
            self.metadata['columns'] = list(self.df.columns)
            
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def generate_sample_data(self, n_records: int = 1000) -> pd.DataFrame:
        """
        Generate sample coffee sales data for testing
        
        Args:
            n_records: Number of records to generate
            
        Returns:
            pd.DataFrame: Sample dataset
        """
        np.random.seed(42)
        
        dates = [datetime.now() - timedelta(days=x) for x in range(n_records)]
        
        data = {
            'date': sorted(dates),
            'product': np.random.choice(['Espresso', 'Americano', 'Latte', 'Cappuccino', 'Macchiato'], n_records),
            'quantity': np.random.randint(1, 10, n_records),
            'price': np.random.uniform(2.50, 5.00, n_records),
            'revenue': None,  # Will be calculated
            'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
            'temperature': np.random.uniform(65, 85, n_records),
            'day_of_week': None,  # Will be calculated
        }
        
        self.df = pd.DataFrame(data)
        self.df['revenue'] = self.df['quantity'] * self.df['price']
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        
        self.metadata['source'] = 'generated'
        self.metadata['rows'] = len(self.df)
        self.metadata['columns'] = list(self.df.columns)
        
        return self.df
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the data
        
        Returns:
            pd.DataFrame: Cleaned data
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        df = self.df.copy()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))
        
        # Remove outliers (values beyond 3 standard deviations)
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            mean = df[col].mean()
            std = df[col].std()
            df = df[(df[col] >= mean - 3*std) & (df[col] <= mean + 3*std)]
        
        self.df = df
        self.metadata['cleaning_applied'] = True
        
        return self.df
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics of the data
        
        Returns:
            Dict: Summary information
        """
        if self.df is None:
            return {}
        
        return {
            'total_records': len(self.df),
            'date_range': {
                'start': str(self.df['date'].min()) if 'date' in self.df.columns else None,
                'end': str(self.df['date'].max()) if 'date' in self.df.columns else None,
            },
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'numeric_summary': self.df.describe().to_dict(),
        }
    
    def get_data(self) -> pd.DataFrame:
        """Return the current dataset"""
        return self.df
