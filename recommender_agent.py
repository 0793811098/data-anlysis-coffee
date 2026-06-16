"""
Recommender Agent - Provides actionable recommendations and insights
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class RecommenderAgent:
    """
    Responsible for:
    - Generating insights from analysis
    - Making recommendations
    - Identifying opportunities
    - Risk assessment
    """
    
    def __init__(self, analysis_results: Dict = None):
        """Initialize the Recommender Agent"""
        self.analysis_results = analysis_results or {}
        self.recommendations = []
        
    def set_analysis_results(self, results: Dict):
        """Set analysis results to generate recommendations from"""
        self.analysis_results = results
        
    def generate_recommendations(self, data: pd.DataFrame = None) -> List[Dict]:
        """
        Generate strategic recommendations
        
        Args:
            data: Raw data for context
            
        Returns:
            List[Dict]: List of recommendations
        """
        recommendations = []
        
        if data is None or len(data) == 0:
            return recommendations
        
        # Recommendation 1: Product mix optimization
        if 'product' in data.columns:
            product_sales = data['product'].value_counts()
            low_performing = product_sales.nsmallest(2).index.tolist()
            
            recommendations.append({
                'category': 'Product Strategy',
                'priority': 'High',
                'recommendation': f'Review underperforming products: {", ".join(low_performing)}',
                'action': 'Conduct market analysis or consider product discontinuation',
                'impact': 'Improved product portfolio efficiency'
            })
        
        # Recommendation 2: Regional expansion
        if 'region' in data.columns and 'revenue' in data.columns:
            region_revenue = data.groupby('region')['revenue'].sum()
            best_region = region_revenue.idxmax()
            worst_region = region_revenue.idxmin()
            
            recommendations.append({
                'category': 'Market Expansion',
                'priority': 'Medium',
                'recommendation': f'Expand operations in {best_region} region; improve performance in {worst_region}',
                'action': 'Allocate more resources to high-performing regions',
                'impact': f'Potential revenue increase in {worst_region}'
            })
        
        # Recommendation 3: Pricing optimization
        if 'price' in data.columns and 'quantity' in data.columns:
            avg_price = data['price'].mean()
            high_price = data[data['price'] > avg_price * 1.2]
            low_volume = high_price['quantity'].mean()
            
            recommendations.append({
                'category': 'Pricing Strategy',
                'priority': 'Medium',
                'recommendation': 'Consider dynamic pricing strategy',
                'action': 'Test price elasticity with A/B testing',
                'impact': 'Increased revenue and market share'
            })
        
        # Recommendation 4: Inventory management
        if 'product' in data.columns and 'quantity' in data.columns:
            avg_quantity = data['quantity'].mean()
            volatile_products = data.groupby('product')['quantity'].std()
            high_variance = volatile_products[volatile_products > avg_quantity].index.tolist()
            
            recommendations.append({
                'category': 'Inventory Management',
                'priority': 'High',
                'recommendation': f'Implement safety stock for volatile products: {", ".join(high_variance[:2])}',
                'action': 'Use forecasting to optimize inventory levels',
                'impact': 'Reduced stockouts and carrying costs'
            })
        
        # Recommendation 5: Seasonal preparation
        if 'date' in data.columns and 'revenue' in data.columns:
            df = data.copy()
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            
            monthly_revenue = df.groupby('month')['revenue'].sum()
            peak_month = monthly_revenue.idxmax()
            
            recommendations.append({
                'category': 'Seasonal Planning',
                'priority': 'Medium',
                'recommendation': f'Prepare for peak season (Month {peak_month})',
                'action': 'Increase staffing and inventory ahead of peak',
                'impact': 'Better capacity utilization and customer satisfaction'
            })
        
        self.recommendations = recommendations
        return recommendations
    
    def get_top_recommendations(self, top_n: int = 3) -> List[Dict]:
        """
        Get top N recommendations by priority
        
        Args:
            top_n: Number of recommendations to return
            
        Returns:
            List[Dict]: Top recommendations
        """
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        sorted_recs = sorted(
            self.recommendations,
            key=lambda x: priority_order.get(x.get('priority', 'Low'), 3)
        )
        
        return sorted_recs[:top_n]
    
    def identify_opportunities(self, data: pd.DataFrame = None) -> List[Dict]:
        """
        Identify growth opportunities
        
        Args:
            data: Raw data for context
            
        Returns:
            List[Dict]: Identified opportunities
        """
        opportunities = []
        
        if data is None or len(data) == 0:
            return opportunities
        
        # Opportunity 1: Cross-selling
        if 'product' in data.columns:
            product_freq = data['product'].value_counts()
            opportunities.append({
                'opportunity': 'Cross-selling',
                'description': f'Bundle top products: {product_freq.index[0]} with {product_freq.index[1]}',
                'potential_impact': 'Increased average transaction value'
            })
        
        # Opportunity 2: Customer loyalty program
        opportunities.append({
            'opportunity': 'Loyalty Program',
            'description': 'Implement tiered loyalty rewards based on purchase frequency',
            'potential_impact': 'Improved customer retention by 15-25%'
        })
        
        # Opportunity 3: Data-driven marketing
        if 'region' in data.columns:
            opportunities.append({
                'opportunity': 'Targeted Marketing',
                'description': 'Create region-specific marketing campaigns',
                'potential_impact': 'Higher conversion rates in key regions'
            })
        
        return opportunities
    
    def assess_risks(self, data: pd.DataFrame = None) -> List[Dict]:
        """
        Assess potential risks
        
        Args:
            data: Raw data for context
            
        Returns:
            List[Dict]: Identified risks
        """
        risks = []
        
        if data is None or len(data) == 0:
            return risks
        
        # Risk 1: Revenue concentration
        if 'product' in data.columns and 'revenue' in data.columns:
            product_revenue = data.groupby('product')['revenue'].sum()
            top_product_share = product_revenue.max() / product_revenue.sum()
            
            if top_product_share > 0.4:
                risks.append({
                    'risk': 'Revenue Concentration',
                    'severity': 'High',
                    'description': f'Top product accounts for {top_product_share*100:.1f}% of revenue',
                    'mitigation': 'Diversify product portfolio'
                })
        
        # Risk 2: Seasonal volatility
        if 'date' in data.columns and 'quantity' in data.columns:
            df = data.copy()
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            
            monthly_quantity = df.groupby('month')['quantity'].sum()
            volatility = monthly_quantity.std() / monthly_quantity.mean()
            
            if volatility > 0.3:
                risks.append({
                    'risk': 'Demand Volatility',
                    'severity': 'Medium',
                    'description': f'High seasonal variability (CV: {volatility:.2f})',
                    'mitigation': 'Implement flexible staffing and inventory strategies'
                })
        
        # Risk 3: Margin pressure
        if 'price' in data.columns and 'quantity' in data.columns:
            risks.append({
                'risk': 'Price Competition',
                'severity': 'Medium',
                'description': 'Potential margin pressure from competitors',
                'mitigation': 'Focus on value differentiation and cost optimization'
            })
        
        return risks
    
    def create_action_plan(self, data: pd.DataFrame = None) -> Dict:
        """
        Create comprehensive action plan
        
        Args:
            data: Raw data for context
            
        Returns:
            Dict: Action plan
        """
        recommendations = self.generate_recommendations(data)
        opportunities = self.identify_opportunities(data)
        risks = self.assess_risks(data)
        
        action_plan = {
            'recommendations': self.get_top_recommendations(top_n=5),
            'opportunities': opportunities,
            'risks': risks,
            'priorities': {
                'immediate': [r for r in recommendations if r.get('priority') == 'High'],
                'short_term': [r for r in recommendations if r.get('priority') == 'Medium'],
                'long_term': [r for r in recommendations if r.get('priority') == 'Low']
            }
        }
        
        return action_plan
