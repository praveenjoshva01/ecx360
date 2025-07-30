# ECLearnix Interactive Dashboard - Flask App
# Copy this code to create a web dashboard for your hackathon demo

from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.utils
import json

app = Flask(__name__)

# Sample data for demo (replace with your actual data)
def create_sample_data():
    """Create sample data for demo purposes"""
    import numpy as np
    np.random.seed(42)
    
    data = {
        'User_ID': range(1000),
        'Cluster': np.random.choice([0, 1, 2], 1000, p=[0.6, 0.2, 0.2]),
        'Platform_Source': np.random.choice(['Social Media', 'Website', 'Email', 'WhatsApp', 'LinkedIn'], 1000),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
        'User_Type': np.random.choice(['Student', 'Professional', 'Faculty'], 1000),
        'Churn': np.random.choice([0, 1], 1000, p=[0.68, 0.32]),
        'Time_Spent_Total_Minutes': np.random.normal(120, 50, 1000),
        'Course_Completed': np.random.choice([0, 1], 1000, p=[0.7, 0.3]),
        'App_Installed': np.random.choice([0, 1], 1000, p=[0.4, 0.6])
    }
    
    return pd.DataFrame(data)

# Load your data (replace this with your actual data loading)
df = create_sample_data()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/cluster_analysis')
def cluster_analysis():
    """API endpoint for cluster analysis data"""
    
    cluster_summary = df.groupby('Cluster').agg({
        'User_ID': 'count',
        'Churn': 'mean',
        'Time_Spent_Total_Minutes': 'mean',
        'Course_Completed': 'mean'
    }).round(3)
    
    # Create cluster comparison chart
    fig = px.bar(
        x=cluster_summary.index,
        y=cluster_summary['Churn'],
        title="Churn Rate by User Cluster",
        labels={'x': 'Cluster', 'y': 'Churn Rate'},
        color=cluster_summary['Churn'],
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=400)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': graphJSON,
        'summary': cluster_summary.to_dict()
    })

@app.route('/api/regional_analysis')
def regional_analysis():
    """API endpoint for regional analysis"""
    
    regional_stats = df.groupby('Region').agg({
        'User_ID': 'count',
        'Churn': 'mean',
        'Course_Completed': 'mean'
    }).round(3)
    
    # Create regional chart
    fig = px.bar(
        x=regional_stats.index,
        y=regional_stats['User_ID'],
        title="User Distribution by Region",
        labels={'x': 'Region', 'y': 'Number of Users'},
        color=regional_stats['User_ID']
    )
    
    fig.update_layout(height=400)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': graphJSON,
        'stats': regional_stats.to_dict()
    })

@app.route('/api/platform_analysis')
def platform_analysis():
    """API endpoint for platform source analysis"""
    
    platform_stats = df.groupby('Platform_Source').agg({
        'User_ID': 'count',
        'App_Installed': 'mean',
        'Course_Completed': 'mean'
    }).round(3)
    
    # Create platform effectiveness chart
    fig = px.scatter(
        platform_stats.reset_index(),
        x='App_Installed',
        y='Course_Completed',
        size='User_ID',
        hover_name='Platform_Source',
        title="Platform Source Effectiveness",
        labels={'App_Installed': 'App Install Rate', 'Course_Completed': 'Course Completion Rate'}
    )
    
    fig.update_layout(height=400)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': graphJSON,
        'stats': platform_stats.to_dict()
    })

@app.route('/api/business_impact')
def business_impact():
    """API endpoint for business impact analysis"""
    
    # Calculate current vs improved metrics
    current_churn = df['Churn'].mean()
    improved_churn = current_churn * 0.7  # 30% improvement
    
    scenarios = {
        'Current': {
            'Users': 100000,
            'Churn_Rate': current_churn,
            'Revenue': 100000 * (1 - current_churn) * 2500
        },
        'Improved': {
            'Users': 100000,
            'Churn_Rate': improved_churn,
            'Revenue': 100000 * (1 - improved_churn) * 3000
        }
    }
    
    # Create impact chart
    scenarios_df = pd.DataFrame(scenarios).T
    scenarios_df['Revenue_Crores'] = scenarios_df['Revenue'] / 10000000
    
    fig = px.bar(
        x=scenarios_df.index,
        y=scenarios_df['Revenue_Crores'],
        title="Revenue Impact Analysis",
        labels={'x': 'Scenario', 'y': 'Annual Revenue (₹ Crores)'},
        color=scenarios_df['Revenue_Crores']
    )
    
    fig.update_layout(height=400)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({
        'chart': graphJSON,
        'scenarios': scenarios
    })

# HTML Template (save this as templates/dashboard.html)
dashboard_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>ECLearnix Analytics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }
        .header { text-align: center; color: #2E7D9A; margin-bottom: 30px; }
        .dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .chart-container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .metrics { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .metric-item { display: inline-block; margin: 10px 20px; text-align: center; }
        .metric-value { font-size: 24px; font-weight: bold; color: #2E7D9A; }
        .metric-label { color: #666; }
        .loading { text-align: center; color: #666; padding: 40px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 ECLearnix Analytics Dashboard</h1>
        <p>Data-Driven Insights for Scaling to 1M+ Users</p>
    </div>
    
    <div class="metrics" id="metrics">
        <div class="metric-item">
            <div class="metric-value" id="total-users">100K</div>
            <div class="metric-label">Total Users</div>
        </div>
        <div class="metric-item">
            <div class="metric-value" id="churn-rate">32%</div>
            <div class="metric-label">Churn Rate</div>
        </div>
        <div class="metric-item">
            <div class="metric-value" id="revenue">₹17 Cr</div>
            <div class="metric-label">Annual Revenue</div>
        </div>
        <div class="metric-item">
            <div class="metric-value" id="potential">₹23 Cr</div>
            <div class="metric-label">Potential Revenue</div>
        </div>
    </div>
    
    <div class="dashboard-grid">
        <div class="chart-container">
            <div id="cluster-chart" class="loading">Loading cluster analysis...</div>
        </div>
        
        <div class="chart-container">
            <div id="regional-chart" class="loading">Loading regional analysis...</div>
        </div>
        
        <div class="chart-container">
            <div id="platform-chart" class="loading">Loading platform analysis...</div>
        </div>
        
        <div class="chart-container">
            <div id="impact-chart" class="loading">Loading business impact...</div>
        </div>
    </div>
    
    <script>
        // Load cluster analysis
        fetch('/api/cluster_analysis')
            .then(response => response.json())
            .then(data => {
                Plotly.newPlot('cluster-chart', JSON.parse(data.chart).data, JSON.parse(data.chart).layout);
            });
        
        // Load regional analysis
        fetch('/api/regional_analysis')
            .then(response => response.json())
            .then(data => {
                Plotly.newPlot('regional-chart', JSON.parse(data.chart).data, JSON.parse(data.chart).layout);
            });
        
        // Load platform analysis
        fetch('/api/platform_analysis')
            .then(response => response.json())
            .then(data => {
                Plotly.newPlot('platform-chart', JSON.parse(data.chart).data, JSON.parse(data.chart).layout);
            });
        
        // Load business impact
        fetch('/api/business_impact')
            .then(response => response.json())
            .then(data => {
                Plotly.newPlot('impact-chart', JSON.parse(data.chart).data, JSON.parse(data.chart).layout);
            });
    </script>
</body>
</html>
'''

# Create templates directory and save HTML
import os
if not os.path.exists('templates'):
    os.makedirs('templates')

with open('templates/dashboard.html', 'w') as f:
    f.write(dashboard_html)

if __name__ == '__main__':
    print("🚀 Starting ECLearnix Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("💡 Use this for your hackathon demo!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# USAGE INSTRUCTIONS:
"""
1. Save this code as 'dashboard_app.py'
2. Install Flask: pip install flask pandas plotly
3. Run: python dashboard_app.py
4. Open browser to: http://localhost:5000
5. Show this dashboard during your hackathon presentation!

The dashboard includes:
- Live metrics display
- Interactive cluster analysis chart
- Regional performance visualization
- Platform source effectiveness analysis
- Business impact projections

Perfect for demonstrating your data-driven approach!
"""