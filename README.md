# Coffee Analytics Copilot

A comprehensive multi-agent data analysis system for coffee sales and business intelligence.

## Overview

Coffee Analytics Copilot is an intelligent system that uses multiple specialized agents to analyze coffee sales data, identify trends, forecast demand, and provide actionable business recommendations.

## System Architecture

### Agents

1. **Data Agent** (`data_agent.py`)
   - Loads data from multiple sources (CSV, Excel, JSON)
   - Performs data cleaning and preprocessing
   - Generates sample data for testing
   - Provides data quality summaries

2. **Analysis Agent** (`analysis_agent.py`)
   - Calculates key performance metrics
   - Analyzes sales by product and region
   - Identifies trends over time
   - Performs statistical correlations
   - Segments data based on criteria
   - Generates actionable insights

3. **Forecast Agent** (`forecast_agent.py`)
   - Time series forecasting for revenue and sales
   - Moving average calculations
   - Exponential smoothing
   - Seasonal pattern analysis
   - Product-specific forecasts

4. **Recommender Agent** (`recommender_agent.py`)
   - Generates strategic recommendations
   - Identifies business opportunities
   - Assesses potential risks
   - Creates actionable action plans

5. **Supervisor** (`supervisor.py`)
   - Orchestrates all agents in a coordinated pipeline
   - Manages data flow between agents
   - Generates comprehensive reports
   - Handles error management and logging

## Features

### Data Analysis
- **Revenue Analysis**: Total, average, and statistical summaries
- **Product Analysis**: Sales by product type
- **Regional Analysis**: Geographic sales patterns
- **Trend Analysis**: Daily, weekly, and monthly trends
- **Correlation Analysis**: Identify relationships between variables
- **Segmentation**: Customer/transaction segmentation

### Forecasting
- **Revenue Forecasting**: 30-day revenue predictions
- **Demand Forecasting**: Product-specific demand predictions
- **Seasonal Analysis**: Identify peak seasons and patterns
- **Trend Direction**: Increasing vs. decreasing trends

### Recommendations
- **Product Strategy**: Portfolio optimization
- **Market Expansion**: Regional growth opportunities
- **Pricing Strategy**: Dynamic pricing recommendations
- **Inventory Management**: Stock optimization
- **Seasonal Planning**: Peak season preparation

### Risk Assessment
- **Revenue Concentration**: Dependency analysis
- **Demand Volatility**: Seasonal variability metrics
- **Market Competition**: Pricing pressure analysis

## Installation

### Prerequisites
- Python 3.8+
- pandas
- numpy
- scipy

### Setup

```bash
# Install dependencies
pip install pandas numpy scipy

# Clone the repository
git clone https://github.com/0793811098/data-anlysis-coffee.git
cd data-anlysis-coffee
```

## Usage

### Quick Start

```python
from supervisor import Supervisor

# Initialize the system
supervisor = Supervisor()

# Run the complete analysis pipeline with sample data
results = supervisor.run_analysis_pipeline(use_sample=True)

# Print formatted report
supervisor.print_report()

# Export results to JSON
supervisor.export_results('coffee_analytics_report.json')
```

### Using Your Own Data

```python
from supervisor import Supervisor

# Initialize the system
supervisor = Supervisor()

# Run with your CSV file
results = supervisor.run_analysis_pipeline(
    data_source='your_data.csv',
    use_sample=False
)

# Print report
supervisor.print_report()
```

### Individual Agent Usage

```python
from data_agent import DataAgent
from analysis_agent import AnalysisAgent

# Load and clean data
data_agent = DataAgent()
data = data_agent.load_data('sales_data.csv')
clean_data = data_agent.clean_data()

# Perform analysis
analysis_agent = AnalysisAgent(clean_data)
metrics = analysis_agent.calculate_metrics()
insights = analysis_agent.get_insights()

print(metrics)
print(insights)
```

## Data Format

Expected columns in your data:
- `date`: Transaction date (YYYY-MM-DD format)
- `product`: Product name (e.g., Espresso, Latte)
- `quantity`: Units sold
- `price`: Unit price
- `revenue`: Total revenue (quantity × price)
- `region`: Geographic region
- `temperature`: Environmental temperature (optional)

Example:
```csv
date,product,quantity,price,revenue,region,temperature
2024-01-01,Latte,5,4.50,22.50,North,72
2024-01-01,Espresso,3,2.50,7.50,South,68
```

## Output

### Executive Summary
Includes:
- Key performance metrics
- Top insights
- Top recommendations
- Forecast summary
- Risk and opportunity count

### Detailed Report
Includes:
- Complete metrics analysis
- Product performance breakdown
- Regional performance analysis
- Trend analysis
- Statistical correlations
- Customer segmentation
- Revenue forecasts
- Recommendations with priority levels
- Risk assessment
- Action plan

### JSON Export
All results can be exported to JSON format for further processing or visualization.

## API Reference

### Supervisor
```python
# Run complete pipeline
supervisor.run_analysis_pipeline(data_source=None, use_sample=True)

# Get executive summary
supervisor.get_executive_summary()

# Export results
supervisor.export_results(filename='analysis_results.json')

# Get execution log
supervisor.get_execution_log()

# Print formatted report
supervisor.print_report()
```

### Data Agent
```python
# Load data
data_agent.load_data(filepath)

# Generate sample data
data_agent.generate_sample_data(n_records=1000)

# Clean data
data_agent.clean_data()

# Get summary
data_agent.get_summary()
```

### Analysis Agent
```python
# Calculate metrics
analysis_agent.calculate_metrics()

# Analyze by product
analysis_agent.analyze_by_product()

# Analyze by region
analysis_agent.analyze_by_region()

# Analyze trends
analysis_agent.analyze_trends(period='D')  # 'D', 'W', or 'M'

# Get correlations
analysis_agent.correlation_analysis()

# Segment data
analysis_agent.segment_customers(method='revenue')

# Get insights
analysis_agent.get_insights()
```

### Forecast Agent
```python
# Forecast revenue
forecast_agent.forecast_revenue(periods=30, method='linear')

# Forecast by product
forecast_agent.forecast_by_product(product='Latte', periods=30)

# Analyze seasonality
forecast_agent.seasonal_analysis()

# Simple moving average
forecast_agent.simple_moving_average(column='revenue', window=7)

# Exponential smoothing
forecast_agent.exponential_smoothing(column='revenue', alpha=0.3)
```

### Recommender Agent
```python
# Generate recommendations
recommender_agent.generate_recommendations(data)

# Get top recommendations
recommender_agent.get_top_recommendations(top_n=3)

# Identify opportunities
recommender_agent.identify_opportunities(data)

# Assess risks
recommender_agent.assess_risks(data)

# Create action plan
recommender_agent.create_action_plan(data)
```

## Examples

### Example 1: Full Analysis Pipeline

```python
from supervisor import Supervisor

supervisor = Supervisor()
results = supervisor.run_analysis_pipeline(use_sample=True)
supervisor.print_report()
```

### Example 2: Custom Data Analysis

```python
from data_agent import DataAgent
from analysis_agent import AnalysisAgent
from forecast_agent import ForecastAgent

# Load data
data_agent = DataAgent()
data = data_agent.load_data('sales_data.csv')
clean_data = data_agent.clean_data()

# Analyze
analysis = AnalysisAgent(clean_data)
metrics = analysis.calculate_metrics()
product_analysis = analysis.analyze_by_product()

# Forecast
forecaster = ForecastAgent(clean_data)
revenue_forecast = forecaster.forecast_revenue(periods=30)

print(f"Total Revenue: ${metrics['total_revenue']:.2f}")
print(f"Product Analysis: {product_analysis}")
print(f"Revenue Forecast: {revenue_forecast}")
```

### Example 3: Risk Assessment

```python
from supervisor import Supervisor

supervisor = Supervisor()
results = supervisor.run_analysis_pipeline(use_sample=True)

risks = results['recommendations']['risks']
for risk in risks:
    print(f"Risk: {risk['risk']} ({risk['severity']})")
    print(f"Description: {risk['description']}")
    print(f"Mitigation: {risk['mitigation']}")
    print()
```

## Performance Metrics

The system tracks and reports:
- **Transaction Count**: Total number of transactions
- **Total Revenue**: Sum of all revenue
- **Average Revenue**: Mean revenue per transaction
- **Revenue Std Dev**: Standard deviation of revenue
- **Total Quantity**: Total units sold
- **Average Price**: Mean price per unit

## Limitations

- Forecasts are based on historical patterns and may not account for external factors
- Sample data uses randomized values for demonstration
- Statistical tests assume normal distribution
- Seasonal analysis requires sufficient historical data

## Future Enhancements

- Machine learning forecasting models
- Advanced anomaly detection
- Real-time data streaming
- Interactive dashboards
- Multi-language support
- API endpoints
- Database integration
- Advanced segmentation algorithms

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Contact

For questions or support, please contact: murithititus33@gmail.com

## Changelog

### Version 0.1.0 (Initial Release)
- Initial multi-agent system
- Data loading and cleaning
- Statistical analysis
- Time series forecasting
- Recommendation generation
- Comprehensive reporting
