"""
Forecast Agent - Handles time series forecasting for coffee sales
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class ForecastAgent:
    """
    Responsible for:
    - Time series forecasting
    - Trend projection
    - Seasonal analysis
    - Demand prediction
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """Initialize the Forecast Agent"""
        self.data = data
        self.forecasts = {}
        
    def set_data(self, data: pd.DataFrame):
        """Set the data for forecasting"""
        self.data = data
        
    def simple_moving_average(self, column: str, window: int = 7) -> pd.Series:
        """
        Calculate simple moving average
        
        Args:
            column: Column to calculate MA for
            window: Window size for moving average
            
        Returns:
            pd.Series: Moving average values
        """
        if self.data is None or column not in self.data.columns:
            return None
        
        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        ma = df[column].rolling(window=window).mean()
        
        return ma
    
    def exponential_smoothing(self, column: str, alpha: float = 0.3) -> pd.Series:
        """
        Calculate exponential smoothing
        
        Args:
            column: Column to smooth
            alpha: Smoothing factor (0-1)
            
        Returns:
            pd.Series: Smoothed values
        """
        if self.data is None or column not in self.data.columns:
            return None
        
        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        smoothed = df[column].ewm(span=int(1/alpha)).mean()
        
        return smoothed
    
    def forecast_revenue(self, periods: int = 30, method: str = 'linear') -> Dict:
        """
        Forecast future revenue
        
        Args:
            periods: Number of periods to forecast
            method: 'linear' or 'exponential'
            
        Returns:
            Dict: Forecast data
        """
        if self.data is None or 'date' not in self.data.columns:
            return {}
        
        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        daily_revenue = df.groupby('date')['revenue'].sum().reset_index()
        
        X = np.arange(len(daily_revenue)).reshape(-1, 1)
        y = daily_revenue['revenue'].values
        
        if method == 'linear':
            # Simple linear regression
            coefficients = np.polyfit(X.flatten(), y, 1)
            poly = np.poly1d(coefficients)
            
            future_X = np.arange(len(daily_revenue), len(daily_revenue) + periods)
            future_y = poly(future_X)
        else:
            # Exponential smoothing
            alpha = 0.3
            future_y = []
            last_value = y[-1]
            
            for _ in range(periods):
                last_value = alpha * last_value + (1 - alpha) * np.mean(y)
                future_y.append(last_value)
            
            future_y = np.array(future_y)
        
        future_dates = [daily_revenue['date'].max() + timedelta(days=i+1) 
                       for i in range(periods)]
        
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'forecast': future_y,
            'method': method
        })
        
        return {
            'forecast': forecast_df.to_dict(),
            'method': method,
            'periods': periods
        }
    
    def forecast_by_product(self, product: str, periods: int = 30) -> Dict:
        """
        Forecast sales for a specific product
        
        Args:
            product: Product name
            periods: Forecast periods
            
        Returns:
            Dict: Product forecast
        """
        if self.data is None or 'product' not in self.data.columns:
            return {}
        
        df = self.data[self.data['product'] == product].copy()
        
        if len(df) == 0:
            return {'error': f'No data for product: {product}'}
        
        df['date'] = pd.to_datetime(df['date'])
        daily_sales = df.groupby('date')['quantity'].sum().reset_index()
        
        # Simple trend forecast
        X = np.arange(len(daily_sales)).reshape(-1, 1)
        y = daily_sales['quantity'].values
        
        coefficients = np.polyfit(X.flatten(), y, 1)
        poly = np.poly1d(coefficients)
        
        future_X = np.arange(len(daily_sales), len(daily_sales) + periods)
        future_y = np.maximum(poly(future_X), 0)  # Ensure non-negative
        
        future_dates = [daily_sales['date'].max() + timedelta(days=i+1) 
                       for i in range(periods)]
        
        return {
            'product': product,
            'forecast_dates': [str(d) for d in future_dates],
            'forecast_quantities': future_y.tolist(),
            'trend': 'increasing' if coefficients[0] > 0 else 'decreasing'
        }
    
    def seasonal_analysis(self) -> Dict:
        """
        Analyze seasonal patterns
        
        Returns:
            Dict: Seasonal analysis
        """
        if self.data is None or 'date' not in self.data.columns:
            return {}
        
        df = self.data.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        
        monthly_pattern = df.groupby('month')['revenue'].mean().to_dict()
        daily_pattern = df.groupby('day_of_week')['revenue'].mean().to_dict()
        
        return {
            'monthly_pattern': monthly_pattern,
            'daily_pattern': daily_pattern,
            'peak_month': max(monthly_pattern, key=monthly_pattern.get),
            'peak_day': max(daily_pattern, key=daily_pattern.get)
        }
    
    def get_forecast_summary(self) -> Dict:
        """Get summary of all forecasts"""
        return self.forecasts
