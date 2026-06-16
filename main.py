#!/usr/bin/env python
"""
Main entry point for the Coffee Analytics Copilot
"""

import sys
import argparse
from pathlib import Path

from supervisor import Supervisor


def main():
    """
    Main function to run the Coffee Analytics system
    """
    parser = argparse.ArgumentParser(
        description='Coffee Analytics Copilot - Multi-Agent Data Analysis System'
    )
    
    parser.add_argument(
        '--data',
        type=str,
        help='Path to data file (CSV, Excel, or JSON)',
        default=None
    )
    
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Use generated sample data (default)',
        default=True
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file for results (JSON format)',
        default='coffee_analytics_report.json'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress console output',
        default=False
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'text', 'both'],
        help='Output format',
        default='both'
    )
    
    args = parser.parse_args()
    
    # Initialize supervisor
    print("\n" + "="*80)
    print("COFFEE ANALYTICS COPILOT")
    print("Multi-Agent Data Analysis System")
    print("="*80 + "\n")
    
    supervisor = Supervisor()
    
    # Determine data source
    use_sample = args.sample or args.data is None
    data_source = args.data if not use_sample else None
    
    if use_sample:
        print("Using generated sample data...\n")
    else:
        print(f"Loading data from: {args.data}\n")
    
    # Run analysis pipeline
    results = supervisor.run_analysis_pipeline(
        data_source=data_source,
        use_sample=use_sample
    )
    
    if not results:
        print("\nError: Analysis pipeline failed. Check logs above.")
        return 1
    
    # Output results
    if args.format in ['text', 'both']:
        if not args.quiet:
            supervisor.print_report()
    
    if args.format in ['json', 'both']:
        output_path = supervisor.export_results(args.output)
        if output_path and not args.quiet:
            print(f"Results exported to: {output_path}\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
