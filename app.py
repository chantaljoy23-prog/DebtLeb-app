
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------- PAGE CONFIG --------------------
st.set_page_config(layout="wide", page_title="External Debt Interactive Dashboard", page_icon="💰")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
    }
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background: rgba(255,255,255,0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 1rem 0;
    }
    .metric-container {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- INDICATOR NAME MAPPING --------------------
indicator_names = {
    "DT.DOD.DECT.CD": "Total External Debt",
    "DT.DOD.DLXF.CD": "Long-term External Debt", 
    "DT.DOD.DSTC.CD": "Short-term Debt",
    "DT.DOD.DPPG.CD": "Public and Publicly Guaranteed Debt",
    "DT.DOD.DPNG.CD": "Multilateral Debt",
    "DT.DOD.MWBG.CD": "World Bank Debt",
    "DT.TDS.DECT.CD": "Total Debt Service",
    "DT.TDS.DPPG.CD": "Public Debt Service",
    "NY.GNP.MKTP.CD": "Gross National Product",
    "FI.RES.TOTL.CD": "Total Reserves",
    "BX.GSR.TOTL.CD": "Exports of Goods and Services"
}

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Indicator Name'] = df['Indicator Code'].map(indicator_names).fillna(df['Indicator Code'])
        # Convert values to billions for better readability
        df['Value_Billions'] = df['Value'] / 1e9
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data
df = load_data('ec4c40221073bbdf6f75b6c6127249c3_20240905_173222.csv')

if df.empty:
    st.error("⚠️ Could not load the data file. Please ensure the CSV file is in the correct location.")
    st.stop()

# -------------------- DASHBOARD HEADER --------------------
st.markdown('<h1 class="main-header">💰 External Debt Interactive Dashboard</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<h3>📊 Lebanon's External Debt Analysis Dashboard</h3>
<p>This interactive dashboard analyzes Lebanon's external debt patterns from 1970-2023, providing insights into the country's debt crisis. 
The visualizations demonstrate that Lebanon's debt problems are primarily driven by public sector borrowing rather than private sector or banking sector excesses. 
Use the interactive features below to explore Lebanon's debt evolution across different economic periods and years.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- INTERACTIVE FEATURE 1: YEAR SELECTOR --------------------
st.markdown("### 🎯 **Interactive Feature 1: Year Selection**")
st.markdown("*Select a specific year to analyze Lebanon's debt evolution over time*")

# Get available years
available_years = sorted(df['refPeriod'].unique())
selected_year = st.selectbox(
    "Choose Year for Analysis:",
    options=available_years,
    index=len(available_years)-5 if len(available_years) >= 5 else 0,
    help="Select a year to see Lebanon's debt trends and economic context"
)

# Filter data for selected year
year_data = df[df['refPeriod'] == selected_year]

# -------------------- VISUALIZATION 1: LEBANON'S DEBT EVOLUTION --------------------
st.markdown("### 📈 Lebanon's External Debt Evolution Over Time")

# Define key debt indicators for composition
debt_composition_indicators = [
    "Long-term External Debt",
    "Short-term Debt", 
    "Public and Publicly Guaranteed Debt",
    "Multilateral Debt"
]

composition_data = year_data[year_data['Indicator Name'].isin(debt_composition_indicators)]

col1, col2 = st.columns([2, 1])

with col1:
    if not composition_data.empty:
        fig1 = px.pie(
            composition_data, 
            values="Value_Billions", 
            names="Indicator Name",
            title=f"Debt Composition in {selected_year} (Billions USD)",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        fig1.update_layout(
            font=dict(size=12),
            showlegend=True,
            height=500
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No debt composition data available for the selected year.")

with col2:
    st.markdown("#### 💡 Key Insights")
    if not composition_data.empty:
        total_debt = composition_data['Value_Billions'].sum()
        largest_component = composition_data.loc[composition_data['Value_Billions'].idxmax()]
        
        st.markdown(f"""
        <div class="metric-container">
            <h4>Total Debt</h4>
            <h2>${total_debt:.1f}B</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-box">
        <strong>Largest Component:</strong><br>
        {largest_component['Indicator Name']}<br>
        <strong>${largest_component['Value_Billions']:.1f}B</strong>
        ({largest_component['Value_Billions']/total_debt*100:.1f}% of total)
        </div>
        """, unsafe_allow_html=True)

# -------------------- INTERACTIVE FEATURE 2: TIME PERIOD FOCUS --------------------
st.markdown("---")
st.markdown("### 🎯 **Interactive Feature 2: Time Period Analysis**")
st.markdown("*Focus on specific time periods to analyze debt patterns during different economic phases*")

# Get available years for range selection
min_year = int(df['refPeriod'].min())
max_year = int(df['refPeriod'].max())

# Create predefined periods with economic context
periods = {
    "📈 Recent Decade (2014-2023)": (2014, 2023),
    "🏛️ Post Financial Crisis (2010-2015)": (2010, 2015), 
    "💥 Financial Crisis Era (2007-2012)": (2007, 2012),
    "🌟 Early 2000s Growth (2000-2007)": (2000, 2007),
    "🔍 Custom Period": "custom"
}

selected_period = st.radio(
    "Choose Time Period to Analyze:",
    options=list(periods.keys()),
    index=0,
    help="Select a predefined economic period or choose custom to set your own range"
)

# Handle custom period selection
if selected_period == "🔍 Custom Period":
    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("Start Year", min_value=min_year, max_value=max_year, value=2010)
    with col2:
        end_year = st.number_input("End Year", min_value=min_year, max_value=max_year, value=max_year)
    year_range = (start_year, end_year)
else:
    year_range = periods[selected_period]

# -------------------- VISUALIZATION 2: DEBT EVOLUTION IN SELECTED LEBANON PERIOD --------------------
st.markdown("### 📈 Lebanon's Debt Pattern During Selected Period")

# Fixed debt indicators for comparison
key_debt_indicators = ["Total External Debt", "Long-term External Debt", "Short-term Debt"]
period_data = df[
    (df['refPeriod'] >= year_range[0]) & 
    (df['refPeriod'] <= year_range[1]) &
    (df['Indicator Name'].isin(key_debt_indicators))
]

if not period_data.empty:
    # Create line chart
    fig3 = px.line(
        period_data, 
        x='refPeriod', 
        y='Value_Billions', 
        color='Indicator Name',
        title=f"Lebanon's Debt During: {year_range[0]} - {year_range[1]} (Billions USD)",
        markers=True,
        line_shape='spline'
    )
    
    fig3.update_layout(
        xaxis_title="Year",
        yaxis_title="Value (Billions USD)",
        hovermode='x unified',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    fig3.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig3, use_container_width=True)
    
    # Period-specific analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Period Statistics")
        for indicator in key_debt_indicators:
            indicator_data = period_data[period_data['Indicator Name'] == indicator]
            if not indicator_data.empty:
                avg_value = indicator_data['Value_Billions'].mean()
                volatility = indicator_data['Value_Billions'].std()
                st.write(f"**{indicator.replace(' External', '')}**")
                st.write(f"Average: ${avg_value:.1f}B")
                st.write(f"Volatility: {volatility:.1f}")
                st.write("---")
    
    with col2:
        st.markdown("#### 📈 Growth Rates")
        for indicator in key_debt_indicators:
            indicator_data = period_data[period_data['Indicator Name'] == indicator].sort_values('refPeriod')
            if len(indicator_data) >= 2:
                start_val = indicator_data['Value_Billions'].iloc[0]
                end_val = indicator_data['Value_Billions'].iloc[-1]
                total_growth = ((end_val - start_val) / start_val * 100) if start_val != 0 else 0
                years = year_range[1] - year_range[0]
                annual_growth = ((end_val / start_val) ** (1/years) - 1) * 100 if start_val > 0 and years > 0 else 0
                
                direction = "📈" if total_growth > 0 else "📉" if total_growth < 0 else "➡️"
                st.write(f"**{indicator.replace(' External', '')}**")
                st.write(f"{direction} Total: {total_growth:+.1f}%")
                st.write(f"Annual: {annual_growth:+.1f}%")
                st.write("---")
    
    with col3:
        st.markdown("#### 🇱🇧 Lebanon Context")
        period_name = selected_period.split(' ', 1)[1] if selected_period != "🔍 Custom Period" else f"Custom ({year_range[0]}-{year_range[1]})"
        
        # Add Lebanon-specific contextual insights based on period
        if "Post-2019 Crisis" in selected_period:
            st.write("💥 **Lebanon Context**: Banking crisis, currency collapse, economic meltdown, political instability (includes 2018 pre-crisis year for comparison)")
        elif "Pre-Crisis Stability" in selected_period:
            st.write("💰 **Lebanon Context**: Relative stability, high public debt, banking sector confidence before 2019 crisis")
        elif "Global Financial Crisis" in selected_period:
            st.write("🌍 **Lebanon Context**: Resilience during global crisis, continued borrowing, pre-crisis confidence")
        elif "Economic Growth Era" in selected_period:
            st.write("📈 **Lebanon Context**: Post-war reconstruction completion, economic growth, increased foreign investment")
        elif "Post-War Reconstruction" in selected_period:
            st.write("🏗️ **Lebanon Context**: Massive reconstruction spending, Solidere project, rapid debt accumulation")
        else:
            st.write(f"📊 **Analysis Period**: {year_range[0]} to {year_range[1]}")
            
        # Show period duration
        duration = year_range[1] - year_range[0] + 1
        st.write(f"📅 **Duration**: {duration} years")
        
        # Show data availability
        data_points = len(period_data['refPeriod'].unique())
        st.write(f"📈 **Data Points**: {data_points} years")

    # Analysis paragraph for period chart
    period_name = selected_period.replace("🏛️ ", "").replace("💰 ", "").replace("🌍 ", "").replace("📈 ", "").replace("🏗️ ", "").replace("🔍 ", "")
    st.markdown(f"""
    **📊 Analysis of Lebanon's Debt During {period_name}:**
    This period analysis reveals specific patterns in Lebanon's debt accumulation during {period_name.lower()}. The chart shows how external debt evolved during this crucial phase of Lebanon's economic history, with long-term debt consistently representing the largest component of external obligations. The growth rates and volatility statistics provide insights into the pace of debt accumulation and economic stability during this period. Lebanon's debt trajectory during this time reflects the underlying economic policies, external shocks, and political decisions that shaped the country's fiscal position. Understanding these period-specific patterns is crucial for comprehending how Lebanon reached its current debt crisis and identifying the structural factors that need to be addressed in any sustainable solution.
    """)

else:
    st.warning("No data available for the selected time period.")

# Show period comparison summary
st.markdown("#### 💡 Key Insights for Selected Period")
if not period_data.empty:
    total_debt_data = period_data[period_data['Indicator Name'] == 'Total External Debt']
    if not total_debt_data.empty:
        max_debt_year = total_debt_data.loc[total_debt_data['Value_Billions'].idxmax(), 'refPeriod']
        max_debt_value = total_debt_data['Value_Billions'].max()
        min_debt_year = total_debt_data.loc[total_debt_data['Value_Billions'].idxmin(), 'refPeriod']
        min_debt_value = total_debt_data['Value_Billions'].min()
        
        st.markdown(f"""
        <div class="insight-box">
        <strong>🔝 Peak Debt:</strong> ${max_debt_value:.1f}B in {max_debt_year}<br>
        <strong>🔽 Lowest Debt:</strong> ${min_debt_value:.1f}B in {min_debt_year}<br>
        <strong>📊 Range:</strong> ${max_debt_value - min_debt_value:.1f}B difference
        </div>
        """, unsafe_allow_html=True)

# -------------------- CONTEXTUAL INFORMATION --------------------
st.markdown("---")
st.markdown("### 📚 About the Data & Methodology")

with st.expander("ℹ️ Data Sources and Definitions"):
    st.markdown("""
    **Data Source**: World Bank International Debt Statistics
    
    **Key Definitions**:
    - **Total External Debt**: All debt owed to nonresidents repayable in currency, goods, or services
    - **Long-term External Debt**: Debt that has an original or extended maturity of more than one year
    - **Short-term Debt**: Debt that has an original maturity of one year or less
    - **Public and Publicly Guaranteed Debt**: External obligations of public debtors and external obligations of private debtors that are guaranteed by a public entity
    
    **Interactive Features**:
    1. **Year Selection**: Choose specific years to analyze Lebanon's debt composition and identify public vs private sector responsibility
    2. **Lebanon Economic Periods**: Select from key periods in Lebanon's economic history (Post-2019 Crisis, Pre-Crisis Stability, Post-War Reconstruction, etc.) to understand how debt evolved during different phases
    """)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>📊 External Debt Interactive Dashboard | Built with Streamlit & Plotly</p>
    <p>💡 Use the interactive features above to explore debt patterns and generate insights</p>
</div>
""", unsafe_allow_html=True)
