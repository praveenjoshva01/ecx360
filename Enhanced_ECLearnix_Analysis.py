# Enhanced ECLearnix Data Analytics - Hackathon Submission
# Additional Visualizations and Analysis for Round 2

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Load your existing clustered dataset
# df = pd.read_csv('your_clustered_data.csv')  # Replace with your actual file

# =============================================================================
# 1. ADVANCED USER JOURNEY FUNNEL ANALYSIS
# =============================================================================

def create_user_journey_funnel(df):
    """Create an interactive funnel showing user journey progression"""
    
    # Calculate funnel metrics
    total_users = len(df)
    app_installed = df['App_Installed'].sum()
    first_login = df['First_Login_Completed'].sum()
    event_registered = df['Registered_for_Event'].sum()
    course_completed = df['Course_Completed'].sum()
    
    # Create funnel data
    funnel_data = {
        'Stage': ['Total Users', 'App Installed', 'First Login', 'Event Registered', 'Course Completed'],
        'Count': [total_users, app_installed, first_login, event_registered, course_completed],
        'Percentage': [100, (app_installed/total_users)*100, (first_login/total_users)*100, 
                      (event_registered/total_users)*100, (course_completed/total_users)*100]
    }
    
    fig = go.Figure(go.Funnel(
        y = funnel_data['Stage'],
        x = funnel_data['Count'],
        textposition = "inside",
        textinfo = "value+percent initial",
        opacity = 0.65,
        marker = {"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
                 "line": {"width": [4, 2, 2, 3, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
        connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}}
    ))
    
    fig.update_layout(
        title="ECLearnix User Journey Funnel Analysis",
        font_size=12,
        height=600
    )
    
    return fig

# =============================================================================
# 2. CLUSTER-BASED ENGAGEMENT HEATMAP
# =============================================================================

def create_cluster_engagement_heatmap(df):
    """Create heatmap showing engagement patterns by cluster and user characteristics"""
    
    # Create cluster summary
    cluster_summary = df.groupby(['Cluster', 'User_Type']).agg({
        'Time_Spent_Total_Minutes': 'mean',
        'Course_Completed': 'mean',
        'Feedback_Rating': 'mean',
        'Saved_Event_Count': 'mean'
    }).round(2)
    
    # Pivot for heatmap
    engagement_matrix = cluster_summary['Time_Spent_Total_Minutes'].unstack()
    
    fig = px.imshow(engagement_matrix, 
                    labels=dict(x="User Type", y="Cluster", color="Avg Time Spent (min)"),
                    title="Average Engagement Time by Cluster and User Type",
                    color_continuous_scale='RdYlBu_r')
    
    fig.update_layout(height=500)
    return fig

# =============================================================================
# 3. REGIONAL PERFORMANCE DASHBOARD
# =============================================================================

def create_regional_dashboard(df):
    """Create comprehensive regional analysis dashboard"""
    
    # Regional metrics
    regional_stats = df.groupby('Region').agg({
        'User_ID': 'count',
        'App_Installed': 'mean',
        'Course_Completed': 'mean',
        'Churn': 'mean',
        'Time_Spent_Total_Minutes': 'mean',
        'Feedback_Rating': 'mean'
    }).round(3)
    
    # Create subplot dashboard
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('User Distribution by Region', 'Course Completion Rate by Region',
                       'Churn Rate by Region', 'Average Engagement Time by Region'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # User distribution
    fig.add_trace(
        go.Bar(x=regional_stats.index, y=regional_stats['User_ID'], 
               name="Users", marker_color='skyblue'),
        row=1, col=1
    )
    
    # Course completion
    fig.add_trace(
        go.Bar(x=regional_stats.index, y=regional_stats['Course_Completed'], 
               name="Completion Rate", marker_color='lightgreen'),
        row=1, col=2
    )
    
    # Churn rate
    fig.add_trace(
        go.Bar(x=regional_stats.index, y=regional_stats['Churn'], 
               name="Churn Rate", marker_color='salmon'),
        row=2, col=1
    )
    
    # Engagement time
    fig.add_trace(
        go.Bar(x=regional_stats.index, y=regional_stats['Time_Spent_Total_Minutes'], 
               name="Avg Time", marker_color='gold'),
        row=2, col=2
    )
    
    fig.update_layout(height=700, title_text="Regional Performance Analysis Dashboard")
    return fig

# =============================================================================
# 4. PREDICTIVE CHURN RISK SCORING
# =============================================================================

def create_churn_risk_analysis(df):
    """Create churn risk analysis visualization"""
    
    # Calculate risk scores (simplified for demo)
    df['Risk_Score'] = (
        (df['Days_Since_Last_Activity'] / df['Days_Since_Last_Activity'].max()) * 0.4 +
        (1 - df['Time_Spent_Total_Minutes'] / df['Time_Spent_Total_Minutes'].max()) * 0.3 +
        (1 - df['Course_Completed']) * 0.3
    ) * 100
    
    # Risk categories
    df['Risk_Category'] = pd.cut(df['Risk_Score'], 
                                bins=[0, 25, 50, 75, 100], 
                                labels=['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'])
    
    # Create risk distribution by cluster
    risk_dist = df.groupby(['Cluster', 'Risk_Category']).size().unstack(fill_value=0)
    
    fig = px.bar(risk_dist, 
                 title="Churn Risk Distribution by User Cluster",
                 labels={'value': 'Number of Users', 'variable': 'Risk Category'},
                 color_discrete_sequence=['green', 'yellow', 'orange', 'red'])
    
    fig.update_layout(height=500)
    return fig

# =============================================================================
# 5. MARKETING CHANNEL ROI ANALYSIS
# =============================================================================

def create_marketing_roi_analysis(df):
    """Analyze marketing channel effectiveness"""
    
    # Marketing channel performance
    channel_perf = df.groupby('Platform_Source').agg({
        'User_ID': 'count',
        'App_Installed': 'mean',
        'First_Login_Completed': 'mean',
        'Course_Completed': 'mean',
        'Time_Spent_Total_Minutes': 'mean',
        'Churn': 'mean'
    }).round(3)
    
    # Calculate composite score
    channel_perf['Effectiveness_Score'] = (
        channel_perf['App_Installed'] * 0.2 +
        channel_perf['First_Login_Completed'] * 0.3 +
        channel_perf['Course_Completed'] * 0.3 +
        (1 - channel_perf['Churn']) * 0.2
    ) * 100
    
    # Create bubble chart
    fig = px.scatter(channel_perf.reset_index(), 
                     x='User_ID', 
                     y='Effectiveness_Score',
                     size='Time_Spent_Total_Minutes',
                     hover_name='Platform_Source',
                     title="Marketing Channel Performance Analysis",
                     labels={'User_ID': 'Total Users Acquired', 
                            'Effectiveness_Score': 'Channel Effectiveness Score'})
    
    fig.update_layout(height=500)
    return fig

# =============================================================================
# 6. PERSONALIZATION OPPORTUNITY MATRIX
# =============================================================================

def create_personalization_matrix(df):
    """Create matrix showing personalization opportunities"""
    
    # Calculate metrics for matrix
    user_segments = df.groupby(['User_Type', 'Department']).agg({
        'Course_Completed': 'mean',
        'Time_Spent_Total_Minutes': 'mean',
        'Churn': 'mean',
        'User_ID': 'count'
    }).round(3)
    
    # Create bubble chart for opportunity matrix
    user_segments_reset = user_segments.reset_index()
    user_segments_reset['Opportunity_Score'] = (
        user_segments_reset['Course_Completed'] * 
        (1 - user_segments_reset['Churn']) * 
        user_segments_reset['Time_Spent_Total_Minutes'] / 100
    )
    
    fig = px.scatter(user_segments_reset,
                     x='Course_Completed',
                     y='Time_Spent_Total_Minutes',
                     size='User_ID',
                     color='Churn',
                     hover_data=['User_Type', 'Department'],
                     title="Personalization Opportunity Matrix",
                     labels={'Course_Completed': 'Course Completion Rate',
                            'Time_Spent_Total_Minutes': 'Average Time Spent'},
                     color_continuous_scale='RdYlGn_r')
    
    fig.update_layout(height=600)
    return fig

# =============================================================================
# 7. ENGAGEMENT TIMELINE ANALYSIS
# =============================================================================

def create_engagement_timeline(df):
    """Simulate and visualize user engagement over time"""
    
    # Simulate timeline data based on clusters
    np.random.seed(42)
    timeline_data = []
    
    for cluster in df['Cluster'].unique():
        cluster_size = len(df[df['Cluster'] == cluster])
        base_engagement = df[df['Cluster'] == cluster]['Time_Spent_Total_Minutes'].mean()
        
        for week in range(1, 13):  # 12 weeks
            # Simulate engagement trends
            if cluster == 0:  # At-risk learners
                engagement = base_engagement * (0.9 ** (week/4)) + np.random.normal(0, 10)
            elif cluster == 1:  # Loyal champions
                engagement = base_engagement * (1.1 ** (week/6)) + np.random.normal(0, 15)
            else:  # Course completers
                engagement = base_engagement * np.sin(week/2) * 0.2 + base_engagement + np.random.normal(0, 12)
            
            timeline_data.append({
                'Week': week,
                'Cluster': f'Cluster {cluster}',
                'Avg_Engagement': max(0, engagement),
                'User_Count': cluster_size
            })
    
    timeline_df = pd.DataFrame(timeline_data)
    
    fig = px.line(timeline_df, 
                  x='Week', 
                  y='Avg_Engagement', 
                  color='Cluster',
                  title="Projected User Engagement Timeline by Cluster",
                  labels={'Avg_Engagement': 'Average Engagement (minutes)'})
    
    fig.update_layout(height=500)
    return fig

# =============================================================================
# 8. ADVANCED CLUSTER PROFILING
# =============================================================================

def create_cluster_profile_radar(df):
    """Create radar chart for cluster profiling"""
    
    # Calculate normalized metrics for each cluster
    cluster_profiles = df.groupby('Cluster').agg({
        'App_Installed': 'mean',
        'First_Login_Completed': 'mean',
        'Course_Completed': 'mean',
        'Newsletter_Subscribed': 'mean',
        'Registered_for_Event': 'mean',
        'Feedback_Rating': lambda x: x.mean()/5,  # Normalize to 0-1
        'Time_Spent_Total_Minutes': lambda x: x.mean()/x.max()  # Normalize
    }).round(3)
    
    # Create radar chart
    categories = ['App Usage', 'Login Completion', 'Course Completion', 
                 'Newsletter', 'Event Registration', 'Satisfaction', 'Time Investment']
    
    fig = go.Figure()
    
    colors = ['red', 'green', 'blue']
    cluster_names = ['At-Risk Learners', 'Loyal Champions', 'Course Completers']
    
    for i, cluster in enumerate(cluster_profiles.index):
        values = cluster_profiles.loc[cluster].values.tolist()
        values += values[:1]  # Complete the circle
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=f'{cluster_names[i]} (Cluster {cluster})',
            line_color=colors[i]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="User Cluster Behavioral Profiles",
        height=600
    )
    
    return fig

# =============================================================================
# 9. BUSINESS IMPACT CALCULATOR
# =============================================================================

def create_business_impact_calculator():
    """Create business impact visualization"""
    
    # Current vs Projected metrics
    scenarios = {
        'Current State': {
            'Users': 100000,
            'Churn_Rate': 0.32,
            'Avg_Revenue_Per_User': 2500,
            'Marketing_Efficiency': 0.15
        },
        'With Our Solution': {
            'Users': 100000,
            'Churn_Rate': 0.22,  # 10% reduction
            'Avg_Revenue_Per_User': 3000,  # Improved engagement
            'Marketing_Efficiency': 0.25   # Better targeting
        },
        'Scaled (1M Users)': {
            'Users': 1000000,
            'Churn_Rate': 0.20,
            'Avg_Revenue_Per_User': 3000,
            'Marketing_Efficiency': 0.30
        }
    }
    
    # Calculate metrics
    results = []
    for scenario, metrics in scenarios.items():
        retained_users = metrics['Users'] * (1 - metrics['Churn_Rate'])
        annual_revenue = retained_users * metrics['Avg_Revenue_Per_User']
        marketing_roi = metrics['Marketing_Efficiency'] * annual_revenue
        
        results.append({
            'Scenario': scenario,
            'Retained_Users': retained_users,
            'Annual_Revenue_Crores': annual_revenue / 10000000,  # Convert to crores
            'Marketing_ROI_Crores': marketing_roi / 10000000
        })
    
    results_df = pd.DataFrame(results)
    
    # Create comparison chart
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=['Retained Users', 'Annual Revenue (₹ Crores)', 'Marketing ROI (₹ Crores)'],
        specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]]
    )
    
    colors = ['lightcoral', 'lightblue', 'lightgreen']
    
    for i, col in enumerate(['Retained_Users', 'Annual_Revenue_Crores', 'Marketing_ROI_Crores']):
        fig.add_trace(
            go.Bar(x=results_df['Scenario'], y=results_df[col], 
                   marker_color=colors[i], showlegend=False),
            row=1, col=i+1
        )
    
    fig.update_layout(height=500, title_text="Business Impact Analysis")
    return fig

# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

def generate_all_visualizations(df):
    """Generate all enhanced visualizations"""
    
    print("🚀 Generating Enhanced ECLearnix Analytics Dashboard...")
    print("=" * 60)
    
    # Store all figures
    figures = {}
    
    print("📊 1. Creating User Journey Funnel...")
    figures['funnel'] = create_user_journey_funnel(df)
    
    print("🔥 2. Creating Cluster Engagement Heatmap...")
    figures['cluster_heatmap'] = create_cluster_engagement_heatmap(df)
    
    print("🗺️ 3. Creating Regional Performance Dashboard...")
    figures['regional_dashboard'] = create_regional_dashboard(df)
    
    print("⚠️ 4. Creating Churn Risk Analysis...")
    figures['churn_risk'] = create_churn_risk_analysis(df)
    
    print("💰 5. Creating Marketing ROI Analysis...")
    figures['marketing_roi'] = create_marketing_roi_analysis(df)
    
    print("🎯 6. Creating Personalization Opportunity Matrix...")
    figures['personalization_matrix'] = create_personalization_matrix(df)
    
    print("📈 7. Creating Engagement Timeline...")
    figures['engagement_timeline'] = create_engagement_timeline(df)
    
    print("🕸️ 8. Creating Cluster Profile Radar...")
    figures['cluster_radar'] = create_cluster_profile_radar(df)
    
    print("💵 9. Creating Business Impact Calculator...")
    figures['business_impact'] = create_business_impact_calculator()
    
    print("✅ All visualizations generated successfully!")
    print("\n🎉 Ready for your hackathon presentation!")
    
    return figures

# =============================================================================
# USAGE EXAMPLE
# =============================================================================

"""
# To use this code with your dataset:

# 1. Load your data
df = pd.read_csv('your_clustered_dataset.csv')

# 2. Generate all visualizations
figures = generate_all_visualizations(df)

# 3. Display individual charts
figures['funnel'].show()
figures['cluster_heatmap'].show()
figures['regional_dashboard'].show()
# ... and so on

# 4. Save charts for presentation
for name, fig in figures.items():
    fig.write_html(f"eclearnix_{name}.html")
    fig.write_image(f"eclearnix_{name}.png", width=1200, height=600)
"""

# Additional helper functions for statistical insights
def generate_insights_summary(df):
    """Generate key insights summary for presentation"""
    
    insights = {
        'total_users': len(df),
        'churn_rate_by_cluster': df.groupby('Cluster')['Churn'].mean().to_dict(),
        'top_platform_sources': df.groupby('Platform_Source')['App_Installed'].mean().sort_values(ascending=False).head(3).to_dict(),
        'regional_gaps': df.groupby('Region')['Course_Completed'].mean().to_dict(),
        'engagement_leaders': df.groupby('User_Type')['Time_Spent_Total_Minutes'].mean().sort_values(ascending=False).head(3).to_dict()
    }
    
    return insights

# Statistical significance testing
def validate_cluster_differences(df):
    """Validate that cluster differences are statistically significant"""
    from scipy import stats
    
    clusters = df['Cluster'].unique()
    significant_features = []
    
    for feature in ['Time_Spent_Total_Minutes', 'Course_Completed', 'Churn']:
        cluster_groups = [df[df['Cluster'] == c][feature] for c in clusters]
        f_stat, p_value = stats.f_oneway(*cluster_groups)
        
        if p_value < 0.05:
            significant_features.append(feature)
    
    return significant_features

print("🎯 Enhanced ECLearnix Analysis Code Ready!")
print("📊 This code provides 9 advanced visualizations for your hackathon submission")
print("🚀 Use generate_all_visualizations(df) to create all charts at once!")