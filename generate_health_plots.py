#!/usr/bin/env python3
"""
Generate health and fitness visualizations for the Boulder diary.
- Daily steps bar chart (last 14 days) from data/steps.csv
- Cumulative running distance line chart from data/running.csv  
- Heart rate variability trend from data/hrv.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import sys
import numpy as np

def load_and_filter_data(data_file, required_columns, days=14):
    """Load CSV data and filter to last N days."""
    if not os.path.exists(data_file):
        print(f"Warning: {data_file} not found - skipping")
        return None
    
    try:
        df = pd.read_csv(data_file)
    except Exception as e:
        print(f"Error reading {data_file}: {e}")
        return None
    
    # Validate required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"Error: {data_file} must contain columns: {missing_cols}")
        return None
    
    # Convert date column to datetime
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        print(f"Error parsing dates in {data_file}: {e}")
        return None
    
    # Sort by date
    df = df.sort_values('date')
    
    # Filter to last N days
    today = datetime.now()
    cutoff_date = today - timedelta(days=days)
    df_filtered = df[df['date'] >= cutoff_date]
    
    if df_filtered.empty:
        print(f"No recent data found in {data_file}")
        return None
        
    return df_filtered
def generate_steps_plot():
    """Generate steps per day bar chart for the last 14 days."""
    
    df = load_and_filter_data('data/steps.csv', ['date', 'steps'], 14)
    if df is None:
        return False
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Create bar chart
    bars = plt.bar(df['date'], df['steps'], 
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
    for bar, value in zip(bars, df['steps']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + max(df['steps']) * 0.01,
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
    total_steps = df['steps'].sum()
    avg_steps = df['steps'].mean()
    max_steps = df['steps'].max()
    min_steps = df['steps'].min()
    
    print(f"\nSteps Summary for last 14 days:")
    print(f"Total steps: {total_steps:,}")
    print(f"Average daily steps: {avg_steps:,.0f}")
    print(f"Maximum daily steps: {max_steps:,}")
    print(f"Minimum daily steps: {min_steps:,}")
    
    plt.close()
    return True


def generate_running_plot():
    """Generate cumulative running distance plot."""
    
    df = load_and_filter_data('data/running.csv', ['date', 'distance_km'], 30)  # Show more data for cumulative
    if df is None:
        return False
    
    # Calculate cumulative distance
    df = df.sort_values('date')
    df['cumulative_km'] = df['distance_km'].cumsum()
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Create line plot with markers
    plt.plot(df['date'], df['cumulative_km'], 
             color='forestgreen', linewidth=2.5, marker='o', markersize=4)
    
    # Fill area under the curve
    plt.fill_between(df['date'], df['cumulative_km'], alpha=0.3, color='forestgreen')
    
    # Customize the plot
    plt.title('Cumulative Running Distance', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Distance (km)', fontsize=12)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Add grid for better readability
    plt.grid(alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Add annotation for total distance
    total_distance = df['cumulative_km'].iloc[-1]
    plt.annotate(f'Total: {total_distance:.1f} km', 
                xy=(df['date'].iloc[-1], total_distance),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8),
                fontsize=11, fontweight='bold')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    output_file = 'stats/plots/cumulative_running.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Plot saved to {output_file}")
    
    # Print summary statistics
    total_km = df['distance_km'].sum()
    avg_distance = df['distance_km'].mean()
    max_distance = df['distance_km'].max()
    days_run = len(df)
    
    print(f"\nRunning Summary:")
    print(f"Total distance: {total_km:.1f} km")
    print(f"Average per run: {avg_distance:.1f} km")
    print(f"Longest run: {max_distance:.1f} km")
    print(f"Days with runs: {days_run}")
    
    plt.close()
    return True


def generate_hrv_plot():
    """Generate heart rate variability trend plot."""
    
    df = load_and_filter_data('data/hrv.csv', ['date', 'rmssd'], 30)
    if df is None:
        return False
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Create line plot with trend
    plt.plot(df['date'], df['rmssd'], 
             color='crimson', linewidth=2, marker='o', markersize=3, alpha=0.8)
    
    # Add trend line
    x_numeric = mdates.date2num(df['date'])
    z = np.polyfit(x_numeric, df['rmssd'], 1)
    p = np.poly1d(z)
    plt.plot(df['date'], p(x_numeric), 
             color='darkred', linestyle='--', linewidth=2, alpha=0.7, label='Trend')
    
    # Calculate rolling average (7-day)
    if len(df) >= 7:
        df['rolling_avg'] = df['rmssd'].rolling(window=7, center=True).mean()
        plt.plot(df['date'], df['rolling_avg'], 
                 color='orange', linewidth=2.5, alpha=0.8, label='7-day average')
    
    # Customize the plot
    plt.title('Heart Rate Variability (RMSSD) Trend', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('RMSSD (ms)', fontsize=12)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.xticks(rotation=45)
    
    # Add grid and legend
    plt.grid(alpha=0.3, linestyle='-', linewidth=0.5)
    plt.legend()
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    output_file = 'stats/plots/hrv_trend.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Plot saved to {output_file}")
    
    # Print summary statistics
    avg_hrv = df['rmssd'].mean()
    std_hrv = df['rmssd'].std()
    max_hrv = df['rmssd'].max()
    min_hrv = df['rmssd'].min()
    
    # Calculate trend (positive = improving, negative = declining)
    trend_slope = z[0] if len(df) > 1 else 0
    trend_direction = "improving" if trend_slope > 0 else "declining" if trend_slope < 0 else "stable"
    
    print(f"\nHRV Summary:")
    print(f"Average RMSSD: {avg_hrv:.1f} ± {std_hrv:.1f} ms")
    print(f"Range: {min_hrv:.1f} - {max_hrv:.1f} ms")
    print(f"Trend: {trend_direction}")
    
    plt.close()
    return True


def main():
    """Generate all available plots."""
    print("Generating health and fitness plots...")
    
    # Ensure output directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('stats/plots', exist_ok=True)
    
    plots_generated = 0
    
    # Generate steps plot
    if generate_steps_plot():
        plots_generated += 1
    
    # Generate running plot
    if generate_running_plot():
        plots_generated += 1
    
    # Generate HRV plot  
    if generate_hrv_plot():
        plots_generated += 1
    
    if plots_generated == 0:
        print("No plots were generated. Please ensure data files exist:")
        print("- data/steps.csv (columns: date, steps)")
        print("- data/running.csv (columns: date, distance_km)")
        print("- data/hrv.csv (columns: date, rmssd)")
        sys.exit(1)
    else:
        print(f"\nSuccessfully generated {plots_generated} plot(s)")


if __name__ == "__main__":
    main()