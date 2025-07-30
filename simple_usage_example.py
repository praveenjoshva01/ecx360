# SIMPLE USAGE EXAMPLE FOR YOUR EXISTING NOTEBOOK
# Copy this after your clustering analysis

# Assuming you already have your clustered dataframe 'df' with the 'Cluster' column
# from your existing analysis

# 1. FIRST - Install required packages if not already installed
# !pip install plotly

# 2. IMPORT THE ENHANCED FUNCTIONS (copy the entire enhanced analysis code above first)

# 3. SIMPLE EXECUTION - Just run this:
print("🚀 Generating enhanced visualizations for ECLearnix hackathon...")

# Generate all charts
figures = generate_all_visualizations(df)

# Display each chart
print("\n📊 Displaying User Journey Funnel...")
figures['funnel'].show()

print("\n🔥 Displaying Cluster Engagement Heatmap...")
figures['cluster_heatmap'].show()

print("\n🗺️ Displaying Regional Performance Dashboard...")
figures['regional_dashboard'].show()

print("\n⚠️ Displaying Churn Risk Analysis...")
figures['churn_risk'].show()

print("\n💰 Displaying Marketing ROI Analysis...")
figures['marketing_roi'].show()

print("\n💵 Displaying Business Impact Calculator...")
figures['business_impact'].show()

print("\n✅ All visualizations ready for your presentation!")

# 4. OPTIONAL - Save charts as HTML files for sharing
print("\n💾 Saving charts as HTML files...")
for name, fig in figures.items():
    fig.write_html(f"eclearnix_{name}.html")
    print(f"   ✅ Saved: eclearnix_{name}.html")

print("\n🎉 Complete! You now have 6 powerful visualizations for your hackathon submission!")

# 5. GENERATE INSIGHTS SUMMARY
print("\n📋 QUICK INSIGHTS FOR YOUR PRESENTATION:")
print("=" * 50)

# Cluster insights
cluster_summary = df.groupby('Cluster').agg({
    'User_ID': 'count',
    'Churn': 'mean',
    'Time_Spent_Total_Minutes': 'mean'
}).round(2)

for cluster in cluster_summary.index:
    users = cluster_summary.loc[cluster, 'User_ID']
    churn = cluster_summary.loc[cluster, 'Churn'] * 100
    time_spent = cluster_summary.loc[cluster, 'Time_Spent_Total_Minutes']
    
    print(f"📊 Cluster {cluster}: {users} users, {churn:.1f}% churn, {time_spent:.0f} min avg time")

# Platform source insights
platform_summary = df.groupby('Platform_Source')['App_Installed'].mean().sort_values(ascending=False)
print(f"\n🥇 Best Platform: {platform_summary.index[0]} ({platform_summary.iloc[0]:.1%} install rate)")
print(f"🥈 Second Best: {platform_summary.index[1]} ({platform_summary.iloc[1]:.1%} install rate)")

# Regional insights
regional_summary = df.groupby('Region')['User_ID'].count().sort_values(ascending=False)
print(f"\n🌍 Largest Region: {regional_summary.index[0]} ({regional_summary.iloc[0]} users)")
print(f"🎯 Growth Opportunity: {regional_summary.index[-1]} ({regional_summary.iloc[-1]} users)")

print("\n🚀 Use these insights in your presentation slides!")