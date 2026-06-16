"""
Analysis Agent - Performs statistical analysis on coffee data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from scipy import stats


class AnalysisAgent:
    """
    Responsible for:
    - Statistical analysis
    - Trend identification
    - Correlation analysis
    - Segmentation analysis
    - Performance metrics
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """Initialize the Analysis Agent"""
        self.data = data
        self.results = {}
        
    def set_data(self, data: pd.DataFrame):
        """Set the data to analyze"""
        self.data = data
        
    def calculate_metrics(self) -> Dict:
        """
        Calculate key performance metrics
        
        Returns:
            Dict: KPI metrics
        """
        if self.data is None:
            return {}
        
        df = self.data
        
        metrics = {
            'total_revenue': float(df['revenue'].sum()) if 'revenue' in df.columns else None,
            'average_revenue': float(df['revenue'].mean()) if 'revenue' in df.columns else None,
            'revenue_std_dev': float(df['revenue'].std()) if 'revenue' in df.columns else None,
            'total_quantity': int(df['quantity'].sum()) if 'quantity' in df.columns else None,
            'average_price': float(df['price'].mean()) if 'price' in df.columns else None,
            'transaction_count': len(df),
        }
        
        return metrics
    
    def analyze_by_product(self) -> Dict:
        """
        Analyze sales by product
        
        Returns:
            Dict: Product-wise analysis
        """
        if self.data is None or 'product' not in self.data.columns:
            return {}
        
        df = self.data
        product_analysis = df.groupby('product').agg({
            'quantity': 'sum',
            'revenue': ['sum', 'mean', 'count'],
            'price': 'mean'
        }).round(2)
        
        return product_analysis.to_dict()
    
    def analyze_by_region(self) -> Dict:
        """
        Analyze sales by region
        
        Returns:
            Dict: Region-wise analysis
        """
        if self.data is None or 'region' not in self.data.columns:
            return {}
        
        df = self.data
        region_analysis = df.groupby('region').agg({
            'quantity': 'sum',
            'revenue': ['sum', 'mean', 'count'],
        }).round(2)
        
        return region_analysis.to_dict()
    
    def analyze_trends(self, period: str = 'D') -> Dict:
        """
        Analyze trends over time
        
        Args:
            period: 'D' for daily, 'W' for weekly, 'M' for monthly
            
        Returns:
            Dict: Trend analysis
        """
        if self.data is None or 'date' not in self.data.columns:
            return {}
        
        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        trend = df.groupby(df['date'].dt.to_period(period))['revenue'].agg(['sum', 'mean', 'count']).round(2)
        
        return trend.to_dict()
    
    def correlation_analysis(self) -> Dict:
        """
        Perform correlation analysis on numeric columns
        
        Returns:
            Dict: Correlation matrix
        """
        if self.data is None:
            return {}
        
        numeric_df = self.data.select_dtypes(include=[np.number])
        correlation = numeric_df.corr().round(3)
        
        return correlation.to_dict()
    
    def perform_statistical_test(self, column: str, groups: List[str]) -> Dict:
        """
        Perform ANOVA test on groups
        
        Args:
            column: Column to analyze
            groups: Grouping column
            
        Returns:
            Dict: ANOVA results
        """
        if self.data is None:
            return {}
        
        df = self.data
        group_data = [df[df[groups] == group][column].dropna().values 
                      for group in df[groups].unique()]
        
        f_stat, p_value = stats.f_oneway(*group_data)
        
        return {
            'f_statistic': float(f_stat),
            'p_value': float(p_value),
            'significant': p_value < 0.05
        }
    
    def segment_customers(self, method: str = 'revenue') -> Dict:
        """
        Segment data based on criteria
        
        Args:
            method: Segmentation method
            
        Returns:
            Dict: Segmentation results
        """
        if self.data is None:
            return {}
        
        df = self.data.copy()
        
        if method == 'revenue':
            df['segment'] = pd.qcut(df['revenue'], q=3, labels=['Low', 'Medium', 'High'])
        elif method == 'quantity':
            df['segment'] = pd.qcut(df['quantity'], q=3, labels=['Low', 'Medium', 'High'])
        
        segment_dist = df['segment'].value_counts().to_dict()
        
        return {
            'segments': segment_dist,
            'method': method
        }
    
    def get_insights(self) -> List[str]:
        """
        Generate key insights from the data
        
        Returns:
            List[str]: List of insights
        """
        insights = []
        
        if self.data is None:
            return insights
        
        df = self.data
        
        # Most popular product
        if 'product' in df.columns:
            top_product = df['product'].value_counts().index[0]
            insights.append(f"Most popular product: {top_product}")
        
        # Highest revenue region
        if 'region' in df.columns:
            top_region = df.groupby('region')['revenue'].sum().idxmax()
            insights.append(f"Highest revenue region: {top_region}")
        
        # Average revenue trend
        if 'revenue' in df.columns:
            avg_revenue = df['revenue'].mean()
            insights.append(f"Average transaction revenue: ${avg_revenue:.2f}")
        
        return insights
