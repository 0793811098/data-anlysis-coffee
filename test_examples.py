# Coffee Analytics System - Testing Examples

import pandas as pd
from supervisor import Supervisor
from data_agent import DataAgent
from analysis_agent import AnalysisAgent
from forecast_agent import ForecastAgent
from recommender_agent import RecommenderAgent


def test_data_agent():
    """
    Test the Data Agent
    """
    print("\n" + "="*80)
    print("Testing Data Agent")
    print("="*80)
    
    data_agent = DataAgent()
    
    # Generate sample data
    print("\n1. Generating sample data...")
    data = data_agent.generate_sample_data(n_records=500)
    print(f"   Generated {len(data)} records")
    
    # Get summary
    print("\n2. Getting data summary...")
    summary = data_agent.get_summary()
    print(f"   Total records: {summary['total_records']}")
    print(f"   Columns: {summary['columns']}")
    print(f"   Date range: {summary['date_range']}")
    
    # Clean data
    print("\n3. Cleaning data...")
    cleaned = data_agent.clean_data()
    print(f"   Cleaned records: {len(cleaned)}")
    
    return data


def test_analysis_agent(data):
    """
    Test the Analysis Agent
    """
    print("\n" + "="*80)
    print("Testing Analysis Agent")
    print("="*80)
    
    analysis_agent = AnalysisAgent(data)
    
    # Calculate metrics
    print("\n1. Calculating metrics...")
    metrics = analysis_agent.calculate_metrics()
    print(f"   Total Revenue: ${metrics['total_revenue']:.2f}")
    print(f"   Average Revenue: ${metrics['average_revenue']:.2f}")
    print(f"   Transaction Count: {metrics['transaction_count']}")
    
    # Product analysis
    print("\n2. Analyzing by product...")
    product_analysis = analysis_agent.analyze_by_product()
    print(f"   Products analyzed: {len(product_analysis)}")
    
    # Regional analysis
    print("\n3. Analyzing by region...")
    region_analysis = analysis_agent.analyze_by_region()
    print(f"   Regions analyzed: {len(region_analysis)}")
    
    # Get insights
    print("\n4. Extracting insights...")
    insights = analysis_agent.get_insights()
    for i, insight in enumerate(insights, 1):
        print(f"   {i}. {insight}")
    
    return analysis_agent


def test_forecast_agent(data):
    """
    Test the Forecast Agent
    """
    print("\n" + "="*80)
    print("Testing Forecast Agent")
    print("="*80)
    
    forecast_agent = ForecastAgent(data)
    
    # Revenue forecast
    print("\n1. Forecasting revenue (30 days)...")
    revenue_forecast = forecast_agent.forecast_revenue(periods=30)
    print(f"   Forecast method: {revenue_forecast.get('method')}")
    print(f"   Forecast periods: {revenue_forecast.get('periods')}")
    
    # Seasonal analysis
    print("\n2. Analyzing seasonal patterns...")
    seasonal = forecast_agent.seasonal_analysis()
    print(f"   Peak month: {seasonal.get('peak_month')}")
    print(f"   Peak day: {seasonal.get('peak_day')}")
    
    return forecast_agent


def test_recommender_agent(data):
    """
    Test the Recommender Agent
    """
    print("\n" + "="*80)
    print("Testing Recommender Agent")
    print("="*80)
    
    recommender_agent = RecommenderAgent()
    
    # Generate recommendations
    print("\n1. Generating recommendations...")
    recommendations = recommender_agent.generate_recommendations(data)
    print(f"   Recommendations generated: {len(recommendations)}")
    for rec in recommendations[:2]:
        print(f"   - [{rec['priority']}] {rec['recommendation']}")
    
    # Identify opportunities
    print("\n2. Identifying opportunities...")
    opportunities = recommender_agent.identify_opportunities(data)
    print(f"   Opportunities found: {len(opportunities)}")
    for opp in opportunities[:2]:
        print(f"   - {opp['opportunity']}: {opp['description']}")
    
    # Assess risks
    print("\n3. Assessing risks...")
    risks = recommender_agent.assess_risks(data)
    print(f"   Risks identified: {len(risks)}")
    for risk in risks[:2]:
        print(f"   - {risk['risk']} ({risk['severity']})")
    
    return recommender_agent


def test_supervisor():
    """
    Test the Supervisor (complete pipeline)
    """
    print("\n" + "="*80)
    print("Testing Supervisor (Complete Pipeline)")
    print("="*80)
    
    supervisor = Supervisor()
    
    # Run complete pipeline
    print("\nRunning complete analysis pipeline...")
    results = supervisor.run_analysis_pipeline(use_sample=True)
    
    if results:
        print("\nPipeline completed successfully!")
        
        # Get executive summary
        summary = supervisor.get_executive_summary()
        print(f"\nExecutive Summary:")
        print(f"  - Key Metrics: {len(summary['key_metrics'])}")
        print(f"  - Top Insights: {len(summary['top_insights'])}")
        print(f"  - Recommendations: {len(summary['top_recommendations'])}")
        print(f"  - Risks: {summary['risks_identified']}")
        print(f"  - Opportunities: {summary['opportunities_identified']}")
        
        return supervisor
    else:
        print("Pipeline failed!")
        return None


def run_all_tests():
    """
    Run all tests
    """
    print("\n" + "#"*80)
    print("# COFFEE ANALYTICS COPILOT - COMPREHENSIVE TEST SUITE")
    print("#"*80)
    
    # Test individual agents
    print("\n\nPhase 1: Testing Individual Agents")
    print("-" * 80)
    
    data = test_data_agent()
    test_analysis_agent(data)
    test_forecast_agent(data)
    test_recommender_agent(data)
    
    # Test supervisor
    print("\n\nPhase 2: Testing Supervisor (Integration)")
    print("-" * 80)
    
    supervisor = test_supervisor()
    
    if supervisor:
        # Print full report
        print("\n\nPhase 3: Full Report")
        print("-" * 80)
        supervisor.print_report()
        
        # Export results
        output_file = supervisor.export_results('test_results.json')
        print(f"\nResults exported to: {output_file}")
    
    print("\n" + "#"*80)
    print("# TEST SUITE COMPLETED")
    print("#"*80 + "\n")


if __name__ == '__main__':
    run_all_tests()
