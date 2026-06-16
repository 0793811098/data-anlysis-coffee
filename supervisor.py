"""
Supervisor - Orchestrates all agents in the coffee analytics system
"""
import json
from typing import Dict, List
from datetime import datetime

from data_agent import DataAgent
from analysis_agent import AnalysisAgent
from forecast_agent import ForecastAgent
from recommender_agent import RecommenderAgent


class Supervisor:
    """
    Orchestrates the multi-agent system:
    - Coordinates data flow between agents
    - Manages workflow execution
    - Generates comprehensive reports
    - Handles error management
    """
    
    def __init__(self):
        """Initialize the Supervisor and all agents"""
        self.data_agent = DataAgent()
        self.analysis_agent = AnalysisAgent()
        self.forecast_agent = ForecastAgent()
        self.recommender_agent = RecommenderAgent()
        
        self.execution_log = []
        self.results = {}
        
    def log_event(self, event: str, status: str = 'info'):
        """Log execution events"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'event': event,
            'status': status
        }
        self.execution_log.append(log_entry)
        print(f"[{timestamp}] [{status.upper()}] {event}")
        
    def run_analysis_pipeline(self, data_source: str = None, use_sample: bool = True) -> Dict:
        """
        Execute the complete analysis pipeline
        
        Args:
            data_source: Path to data file (if not using sample)
            use_sample: Whether to use generated sample data
            
        Returns:
            Dict: Complete analysis results
        """
        try:
            self.log_event("Starting analysis pipeline")
            
            # Step 1: Data Loading
            self.log_event("Step 1: Loading data...")
            if use_sample:
                data = self.data_agent.generate_sample_data(n_records=1000)
                self.log_event("Sample data generated successfully", "success")
            else:
                data = self.data_agent.load_data(data_source)
                self.log_event("Data loaded from file", "success")
            
            if data is None:
                self.log_event("Failed to load data", "error")
                return {}
            
            # Step 2: Data Cleaning
            self.log_event("Step 2: Cleaning and preprocessing data...")
            cleaned_data = self.data_agent.clean_data()
            data_summary = self.data_agent.get_summary()
            self.log_event("Data cleaning completed", "success")
            
            # Step 3: Statistical Analysis
            self.log_event("Step 3: Performing statistical analysis...")
            self.analysis_agent.set_data(cleaned_data)
            
            metrics = self.analysis_agent.calculate_metrics()
            product_analysis = self.analysis_agent.analyze_by_product()
            region_analysis = self.analysis_agent.analyze_by_region()
            trends = self.analysis_agent.analyze_trends()
            correlations = self.analysis_agent.correlation_analysis()
            segments = self.analysis_agent.segment_customers()
            insights = self.analysis_agent.get_insights()
            
            self.log_event("Statistical analysis completed", "success")
            
            # Step 4: Forecasting
            self.log_event("Step 4: Generating forecasts...")
            self.forecast_agent.set_data(cleaned_data)
            
            revenue_forecast = self.forecast_agent.forecast_revenue(periods=30)
            seasonal_analysis = self.forecast_agent.seasonal_analysis()
            
            self.log_event("Forecasting completed", "success")
            
            # Step 5: Recommendations
            self.log_event("Step 5: Generating recommendations...")
            self.recommender_agent.set_analysis_results(metrics)
            
            recommendations = self.recommender_agent.generate_recommendations(cleaned_data)
            opportunities = self.recommender_agent.identify_opportunities(cleaned_data)
            risks = self.recommender_agent.assess_risks(cleaned_data)
            action_plan = self.recommender_agent.create_action_plan(cleaned_data)
            
            self.log_event("Recommendations generated", "success")
            
            # Compile results
            self.results = {
                'timestamp': datetime.now().isoformat(),
                'data_summary': data_summary,
                'analysis': {
                    'metrics': metrics,
                    'product_analysis': product_analysis,
                    'region_analysis': region_analysis,
                    'trends': trends,
                    'correlations': correlations,
                    'segments': segments,
                    'insights': insights
                },
                'forecasting': {
                    'revenue_forecast': revenue_forecast,
                    'seasonal_analysis': seasonal_analysis
                },
                'recommendations': {
                    'recommendations': recommendations,
                    'opportunities': opportunities,
                    'risks': risks,
                    'action_plan': action_plan
                }
            }
            
            self.log_event("Analysis pipeline completed successfully", "success")
            
            return self.results
            
        except Exception as e:
            self.log_event(f"Error in pipeline: {str(e)}", "error")
            return {}
    
    def get_executive_summary(self) -> Dict:
        """
        Generate executive summary of results
        
        Returns:
            Dict: Executive summary
        """
        if not self.results:
            return {'error': 'No results available. Run pipeline first.'}
        
        summary = {
            'report_timestamp': self.results.get('timestamp'),
            'key_metrics': self.results.get('analysis', {}).get('metrics', {}),
            'top_insights': self.results.get('analysis', {}).get('insights', [])[:5],
            'top_recommendations': self.results.get('recommendations', {}).get('recommendations', [])[:3],
            'forecast_summary': {
                'method': self.results.get('forecasting', {}).get('revenue_forecast', {}).get('method'),
                'periods': self.results.get('forecasting', {}).get('revenue_forecast', {}).get('periods')
            },
            'risks_identified': len(self.results.get('recommendations', {}).get('risks', [])),
            'opportunities_identified': len(self.results.get('recommendations', {}).get('opportunities', []))
        }
        
        return summary
    
    def export_results(self, filename: str = 'analysis_results.json') -> str:
        """
        Export results to JSON file
        
        Args:
            filename: Output filename
            
        Returns:
            str: File path
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            self.log_event(f"Results exported to {filename}", "success")
            return filename
        except Exception as e:
            self.log_event(f"Error exporting results: {str(e)}", "error")
            return None
    
    def get_execution_log(self) -> List[Dict]:
        """Get the execution log"""
        return self.execution_log
    
    def print_report(self):
        """Print a formatted analysis report"""
        if not self.results:
            print("No results available. Run pipeline first.")
            return
        
        print("\n" + "="*80)
        print("COFFEE ANALYTICS - COMPREHENSIVE REPORT")
        print("="*80)
        
        # Executive Summary
        summary = self.get_executive_summary()
        print("\nEXECUTIVE SUMMARY")
        print("-" * 80)
        print(f"Report Generated: {summary['report_timestamp']}")
        print(f"\nKey Metrics:")
        for key, value in summary['key_metrics'].items():
            print(f"  • {key}: {value}")
        
        # Insights
        print(f"\nKey Insights:")
        for insight in summary['top_insights']:
            print(f"  • {insight}")
        
        # Recommendations
        print(f"\nTop Recommendations:")
        for i, rec in enumerate(summary['top_recommendations'], 1):
            print(f"  {i}. [{rec.get('priority')}] {rec.get('recommendation')}")
            print(f"     Action: {rec.get('action')}")
        
        # Risks & Opportunities
        print(f"\nRisks & Opportunities:")
        print(f"  • Risks Identified: {summary['risks_identified']}")
        print(f"  • Opportunities Identified: {summary['opportunities_identified']}")
        
        print("\n" + "="*80 + "\n")


# Example usage
if __name__ == "__main__":
    # Initialize supervisor
    supervisor = Supervisor()
    
    # Run the complete analysis pipeline with sample data
    results = supervisor.run_analysis_pipeline(use_sample=True)
    
    # Print the report
    supervisor.print_report()
    
    # Export results
    supervisor.export_results('coffee_analytics_report.json')
    
    # Print execution log
    print("\nExecution Log:")
    for log in supervisor.get_execution_log():
        print(f"  {log}")
