#!/usr/bin/env python3
"""
Generate a vertical bar chart showing walked steps per day for the last 14 days.
Reads from data/steps.csv and saves plot to stats/plots/steps_per_day.png.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import sys

def generate_steps_plot():
    """Generate steps per day bar chart for the last 14 days."""
    
    # Check if data file exists
    data_file = 'data/steps.csv'
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found")
        sys.exit(1)
    
    # Read the CSV file
    try:
        df = pd.read_csv(data_file)
    except Exception as e:
        print(f"Error reading {data_file}: {e}")
        sys.exit(1)
    
    # Validate required columns
    if 'date' not in df.columns or 'steps' not in df.columns:
        print("Error: CSV file must contain 'date' and 'steps' columns")
        sys.exit(1)
    
    # Convert date column to datetime
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        print(f"Error parsing dates: {e}")
        sys.exit(1)
    
    # Sort by date
    df = df.sort_values('date')
    
    # Filter to last 14 days
    today = datetime.now()
    fourteen_days_ago = today - timedelta(days=14)
    df_filtered = df[df['date'] >= fourteen_days_ago]
    
    if df_filtered.empty:
        print("No data found for the last 14 days")
        sys.exit(1)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Create bar chart
    bars = plt.bar(df_filtered['date'], df_filtered['steps'], 
                   color='steelblue', alpha=0.7, width=0.8)
    
    # Customize the plot
    plt.title('Daily Steps - Last 14 Days', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Steps', fontsize=12)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=45)
    
    # Add value labels on top of bars
    for bar, value in zip(bars, df_filtered['steps']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + max(df_filtered['steps']) * 0.01,
                f'{int(value):,}', ha='center', va='bottom', fontsize=9)
    
    # Format y-axis to show thousands with comma separators
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Ensure output directory exists
    os.makedirs('stats/plots', exist_ok=True)
    
    # Save the plot
    output_file = 'stats/plots/steps_per_day.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Plot saved to {output_file}")
    
    # Print summary statistics
    total_steps = df_filtered['steps'].sum()
    avg_steps = df_filtered['steps'].mean()
    max_steps = df_filtered['steps'].max()
    min_steps = df_filtered['steps'].min()
    
    print(f"\nSummary for last 14 days:")
    print(f"Total steps: {total_steps:,}")
    print(f"Average daily steps: {avg_steps:,.0f}")
    print(f"Maximum daily steps: {max_steps:,}")
    print(f"Minimum daily steps: {min_steps:,}")
    
    plt.close()

if __name__ == "__main__":
    generate_steps_plot()