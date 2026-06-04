import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="Unemployment Analysis Dashboard",
    layout="wide"
)

# ---------------------------------------
# TITLE
# ---------------------------------------

st.title("📊 Unemployment Analysis Dashboard")

st.markdown("""
This dashboard analyzes unemployment trends in India using Python and Streamlit.
""")

# ---------------------------------------
# LOAD DATASET
# ---------------------------------------

df = pd.read_csv("Unemployment.csv")

# Rename Columns

df.columns = [
    'States',
    'Date',
    'Frequency',
    'Estimated Unemployment Rate',
    'Estimated Employed',
    'Estimated Labour Participation Rate',
    'Region'
]

# Convert Date Column

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# ---------------------------------------
# SIDEBAR FILTER
# ---------------------------------------

st.sidebar.header("🔍 Filter Options")

selected_state = st.sidebar.selectbox(
    "Select State",
    sorted(df['States'].dropna().astype(str).unique())
)

# Filter Data

state_data = df[df['States'] == selected_state]

# ---------------------------------------
# SHOW DATA
# ---------------------------------------

st.subheader(f"📄 Dataset for {selected_state}")

st.dataframe(state_data)

# ---------------------------------------
# KPI METRICS
# ---------------------------------------

avg_unemployment = state_data['Estimated Unemployment Rate'].mean()

max_unemployment = state_data['Estimated Unemployment Rate'].max()

avg_labour = state_data['Estimated Labour Participation Rate'].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Unemployment",
    f"{avg_unemployment:.2f}%"
)

col2.metric(
    "Highest Unemployment",
    f"{max_unemployment:.2f}%"
)

col3.metric(
    "Labour Participation",
    f"{avg_labour:.2f}%"
)

# ---------------------------------------
# LINE CHART
# ---------------------------------------

st.subheader("📈 Unemployment Trend Over Time")

fig1, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(
    state_data['Date'],
    state_data['Estimated Unemployment Rate'],
    marker='o'
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Unemployment Rate")
ax1.set_title(f"Unemployment Trend in {selected_state}")

plt.xticks(rotation=45)

st.pyplot(fig1)

# ---------------------------------------
# BAR CHART
# ---------------------------------------

st.subheader("📊 Monthly Employment")

fig2, ax2 = plt.subplots(figsize=(12, 5))

ax2.bar(
    state_data['Date'],
    state_data['Estimated Employed']
)

ax2.set_xlabel("Date")
ax2.set_ylabel("Estimated Employed")
ax2.set_title(f"Employment in {selected_state}")

plt.xticks(rotation=45)

st.pyplot(fig2)

# ---------------------------------------
# PIE CHART
# ---------------------------------------

st.subheader("🥧 Employment Distribution")

latest_data = state_data.tail(1)

labels = ['Employed', 'Unemployment']

sizes = [
    latest_data['Estimated Employed'].values[0],
    latest_data['Estimated Unemployment Rate'].values[0]
]

fig3, ax3 = plt.subplots()

ax3.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90
)

ax3.axis('equal')

st.pyplot(fig3)

# ---------------------------------------
# HEATMAP
# ---------------------------------------

st.subheader("🔥 Correlation Heatmap")

numeric_df = state_data.select_dtypes(include='number')

fig4, ax4 = plt.subplots(figsize=(8, 5))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap='coolwarm',
    ax=ax4
)

st.pyplot(fig4)

# ---------------------------------------
# REGION ANALYSIS
# ---------------------------------------

st.subheader("🌍 Region-wise Average Unemployment")

region_data = df.groupby('Region')['Estimated Unemployment Rate'].mean()

fig5, ax5 = plt.subplots(figsize=(10, 5))

region_data.sort_values().plot(
    kind='bar',
    ax=ax5
)

ax5.set_xlabel("Region")
ax5.set_ylabel("Average Unemployment Rate")
ax5.set_title("Region-wise Unemployment Analysis")

st.pyplot(fig5)

# ---------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------

st.subheader("⬇ Download Filtered Data")

csv = state_data.to_csv(index=False)

st.download_button(
    label="Download CSV File",
    data=csv,
    file_name='filtered_unemployment_data.csv',
    mime='text/csv'
)

# ---------------------------------------
# INSIGHTS
# ---------------------------------------

st.subheader("📌 Key Insights")

st.write("✅ COVID-19 caused a major rise in unemployment.")

st.write("✅ Some states consistently show higher unemployment rates.")

st.write("✅ Labour participation influences employment trends.")

st.write("✅ Seasonal patterns are visible in unemployment data.")

st.success("Dashboard Loaded Successfully ✅")