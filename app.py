
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

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
    # External Sector
    "BM.GSR.TOTL.CD": "Balance of payments, current account, goods, services and primary income (BoP, US$)",
    "BN.CAB.XOKA.CD": "Current account balance (BoP, US$)",
    "BX.GSR.TOTL.CD": "Exports of goods and services (BoP, US$)",
    "BX.TRF.PWKR.CD.DT": "Personal remittances, received (US$)",
    # FDI & Portfolio
    "BX.KLT.DINV.CD.WD": "Foreign direct investment, net inflows (US$)",
    "BX.PEF.TOTL.CD.WD": "Portfolio equity, net inflows (US$)",
    # Debt Indicators
    "DT.DOD.DECT.CD": "External debt stocks, total (US$)",
    "DT.DOD.DECT.GN.ZS": "External debt stocks (% of GNI)",
    "DT.DOD.DIMF.CD": "Use of IMF credit (US$)",
    "DT.DOD.DLXF.CD": "Long-term external debt (US$)",
    "DT.DOD.DPNG.CD": "Multilateral debt (US$)",
    "DT.DOD.DPPG.CD": "Public and publicly guaranteed debt (US$)",
    "DT.DOD.DSTC.CD": "Short-term debt (US$)",
    "DT.DOD.DSTC.ZS": "Short-term debt (% of total external debt)",
    "DT.DOD.DSTC.XP.ZS": "Short-term debt (% of exports)",
    "DT.DOD.DSTC.IR.ZS": "Short-term debt (% of international reserves)",
    "DT.DOD.MIBR.CD": "IBRD loans and IDA credits (US$)",
    "DT.DOD.MIDA.CD": "IDA total (US$)",
    "DT.DOD.MWBG.CD": "World Bank debt outstanding (US$)",
    "DT.DOD.PVLX.CD": "Present value of external debt (US$)",
    "DT.DOD.PVLX.EX.ZS": "Present value of external debt (% of exports of goods and services)",
    # Debt Service
    "DT.TDS.DIMF.CD": "Debt service paid to IMF (US$)",
    "DT.TDS.DPPF.XP.ZS": "Public and publicly guaranteed debt service (% of exports)",
    "DT.TDS.DPPG.CD": "Public and publicly guaranteed debt service (US$)",
    "DT.TDS.DPPG.GN.ZS": "Public and publicly guaranteed debt service (% of GNI)",
    "DT.TDS.DPPG.XP.ZS": "Public and publicly guaranteed debt service (% of exports)",
    "DT.TDS.MLAT.CD": "Multilateral debt service (US$)",
    "DT.TDS.MLAT.PG.ZS": "Multilateral debt service (% of government revenue)",
    "DT.TDS.DECT.CD": "Total debt service, external (US$)",
    "DT.TDS.DECT.EX.ZS": "Total debt service (% of exports of goods and services)",
    "DT.TDS.DECT.GN.ZS": "Total debt service (% of GNI)",
    # Debt Liabilities
    "DT.NFL.BLAT.CD": "Debt liabilities, total (US$)",
    "DT.NFL.BOND.CD": "Bond debt, total (US$)",
    "DT.NFL.DPNG.CD": "Multilateral debt liabilities (US$)",
    "DT.NFL.IMFN.CD": "IMF debt liabilities (US$)",
    "DT.NFL.MIBR.CD": "IBRD loans (US$)",
    "DT.NFL.MIDA.CD": "IDA credits (US$)",
    "DT.NFL.MLAT.CD": "Multilateral debt liabilities (US$)",
    "DT.NFL.MOTH.CD": "Other debt liabilities (US$)",
    "DT.NFL.NIFC.CD": "Not included in foreign currency debt (US$)",
    "DT.NFL.OFFT.CD": "Official creditors (US$)",
    "DT.NFL.PBND.CD": "Public bonds (US$)",
    "DT.NFL.PCBK.CD": "Public commercial bank debt (US$)",
    "DT.NFL.PCBO.CD": "Other public bank debt (US$)",
    "DT.NFL.PROP.CD": "Private sector debt, other (US$)",
    "DT.NFL.PRVT.CD": "Private debt (US$)",
    "DT.NFL.PNGB.CD": "Private non-guaranteed bonds (US$)",
    "DT.NFL.PNGC.CD": "Private non-guaranteed commercial debt (US$)",
    # Grants / ODA
    "BX.GRT.EXTA.CD.WD": "Grants (excluding technical cooperation, US$)",
    "BX.GRT.TECH.CD.WD": "Grants (technical cooperation, US$)",
    "DT.ODA.ODAT.CD": "Official Development Assistance, total (US$)",
    "DT.ODA.ODAT.GN.ZS": "Official Development Assistance (% of GNI)",
    "DT.ODA.ODAT.PC.ZS": "Official Development Assistance per capita (US$)",
    # Financial / Reserves
    "FI.RES.TOTL.DT.ZS": "Total reserves (% of total external debt)",
    "FI.RES.TOTL.MO": "Total reserves in months of imports",
    "FI.RES.TOTL.CD": "Total reserves (US$)",
    # GNP
    "NY.GNP.MKTP.CD": "Gross National Product (current US$)"
}

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Indicator Name'] = df['Indicator Code'].map(indicator_names).fillna(df['Indicator Code'])
        df['Value_Billions'] = df['Value'] / 1e9
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data('ec4c40221073bbdf6f75b6c6127249c3_20240905_173222.csv')

if df.empty:
    st.error("⚠️ Could not load the data file. Please ensure the CSV file is in the correct location.")
    st.stop()

# Initialize session state for storing clicked data
if 'clicked_pie_slice' not in st.session_state:
    st.session_state.clicked_pie_slice = None

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

# -------------------- INTERACTIVE FEATURE 1: TIME PERIOD FOCUS --------------------
st.markdown("### 🎯 **Visual 1: Line Chart**")
st.markdown("*Focus on specific time periods to analyze debt patterns during different economic phases*")

# Get available years for range selection
min_year = int(df['refPeriod'].min())
max_year = int(df['refPeriod'].max())

# Create predefined periods with economic context
periods = {
    "🏛️ Post-2019 Crisis (2019-2023)": (2019, 2023),
    "💰 Pre-Crisis Stability (2010-2018)": (2010, 2018), 
    "🌍 Global Financial Crisis Impact (2007-2012)": (2007, 2012),
    "📈 Economic Growth Era (2000-2008)": (2000, 2008),
    "🏗️ Post-War Reconstruction (1990-2000)": (1990, 2000),
    "🔍 Custom Period": "custom"
}

selected_period = st.radio(
    "Choose Time Period to Analyze:",
    options=list(periods.keys()),
    index=0,
    help="Select a predefined economic period or choose custom to set your own range"
)

if selected_period == "🔍 Custom Period":
    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("Start Year", min_value=min_year, max_value=max_year, value=2010)
    with col2:
        end_year = st.number_input("End Year", min_value=min_year, max_value=max_year, value=max_year)
    year_range = (start_year, end_year)
else:
    year_range = periods[selected_period]

# -------------------- VISUALIZATION 1 (now the line chart): DEBT EVOLUTION IN SELECTED LEBANON PERIOD --------------------
st.markdown("### 📈 Lebanon's Debt Pattern During Selected Period")

key_debt_indicators = ["External debt stocks, total (US$)", "Long-term external debt (US$)", "Short-term debt (US$)"]
period_data = df[
    (df['refPeriod'] >= year_range[0]) & 
    (df['refPeriod'] <= year_range[1]) &
    (df['Indicator Name'].isin(key_debt_indicators))
]

if not period_data.empty:
    fig1 = px.line(
        period_data, 
        x='refPeriod', 
        y='Value_Billions', 
        color='Indicator Name',
        title=f"Lebanon's Debt During: {year_range[0]} - {year_range[1]} (Billions USD)",
        markers=True,
        line_shape='spline'
    )
    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Value (Billions USD)",
        hovermode='x unified',
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    fig1.update_traces(line=dict(width=3), marker=dict(size=8))
    st.plotly_chart(fig1, use_container_width=True)
    
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
        if "Post-2019 Crisis" in selected_period:
            st.write("💥 **Lebanon Context**: Banking crisis, currency collapse, economic meltdown, political instability")
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
            
        duration = year_range[1] - year_range[0] + 1
        st.write(f"📅 **Duration**: {duration} years")
        data_points = len(period_data['refPeriod'].unique())
        st.write(f"📈 **Data Points**: {data_points} years")

    period_name = selected_period.replace("🏛️ ", "").replace("💰 ", "").replace("🌍 ", "").replace("📈 ", "").replace("🏗️ ", "").replace("🔍 ", "")
    st.markdown(f"""
    **📊 Analysis of Lebanon's Debt During {period_name}:**
    This period analysis reveals specific patterns in Lebanon's debt accumulation during {period_name.lower()}. The chart shows how external debt evolved during this crucial phase of Lebanon's economic history, with long-term debt consistently representing the largest component of external obligations. The growth rates and volatility statistics provide insights into the pace of debt accumulation and economic stability during this period. Lebanon's debt trajectory during this time reflects the underlying economic policies, external shocks, and political decisions that shaped the country's fiscal position. Understanding these period-specific patterns is crucial for comprehending how Lebanon reached its current debt crisis and identifying the structural factors that need to be addressed in any sustainable solution.
    """)

else:
    st.warning("No data available for the selected time period.")

st.markdown("#### 💡 Key Insights for Selected Period")
if not period_data.empty:
    total_debt_data = period_data[period_data['Indicator Name'] == 'External debt stocks, total (US$)']
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

# -------------------- INTERACTIVE FEATURE 2: YEAR SELECTOR --------------------
st.markdown("---")
st.markdown("### 🎯 **Visual 2: Pie Chart**")
st.markdown("*Select a specific year to analyze Lebanon's debt evolution over time*")
st.markdown("*<small>💡 **Click on a pie chart slice below** to view details about that specific debt component.</small>*", unsafe_allow_html=True)

available_years = sorted(df['refPeriod'].unique())
selected_year = st.selectbox(
    "Choose Year for Analysis:",
    options=available_years,
    index=len(available_years)-5 if len(available_years) >= 5 else 0,
    help="Select a year to see Lebanon's debt trends and economic context",
    key="year_selector"
)

year_data = df[df['refPeriod'] == selected_year]

# -------------------- VISUALIZATION 2 (now the interactive pie chart): LEBANON'S DEBT EVOLUTION --------------------
st.markdown("### 📈 Lebanon's External Debt Evolution Over Time")

# Define key debt indicators for composition
debt_composition_indicators = [
    "External debt stocks, total (US$)",
    "Multilateral debt (US$)",
    "Public and publicly guaranteed debt (US$)",
    "World Bank debt outstanding (US$)",
    "Public commercial bank debt (US$)",
    "Other public bank debt (US$)",
    "Private sector debt, other (US$)",
    "Private debt (US$)",
    "Private non-guaranteed commercial debt (US$)"
]

composition_data = year_data[year_data['Indicator Name'].isin(debt_composition_indicators)]

# Only show Key Insights section (remove the first pie chart)
st.markdown("#### 💡 Key Insights")
if not composition_data.empty:
    total_debt = composition_data['Value_Billions'].sum()
    largest_component = composition_data.loc[composition_data['Value_Billions'].idxmax()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>Total Debt</h4>
            <h2>${total_debt:.1f}B</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
        <strong>Largest Component:</strong><br>
        {largest_component['Indicator Name']}<br>
        <strong>${largest_component['Value_Billions']:.1f}B</strong>
        ({largest_component['Value_Billions']/total_debt*100:.1f}% of total)
        </div>
        """, unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    if not composition_data.empty:
        fig2 = px.pie(
            composition_data,
            values="Value_Billions",
            names="Indicator Name",
            title=f"Debt Composition in {selected_year} (Billions USD)",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(
            font=dict(size=12),
            showlegend=True,
            height=500
        )
        
        # Use plotly_events to make the pie chart clickable
        clicked_data = plotly_events(fig2, click_event=True, key="pie_chart_events")

        # If a slice is clicked, store its name in session state
        if clicked_data:
            clicked_slice_index = clicked_data[0]['pointIndex']
            clicked_name = composition_data['Indicator Name'].iloc[clicked_slice_index]
            st.session_state.clicked_pie_slice = clicked_name
            
        st.plotly_chart(fig2, use_container_width=True)
        
        # Display information about the clicked slice
        if st.session_state.clicked_pie_slice:
            st.markdown(f"#### **You clicked on:** {st.session_state.clicked_pie_slice}")
            selected_component_data = composition_data[composition_data['Indicator Name'] == st.session_state.clicked_pie_slice]
            
            if not selected_component_data.empty:
                value = selected_component_data['Value_Billions'].iloc[0]
                st.write(f"**Value:** ${value:.2f} Billion")
                
        else:
            st.markdown("<p style='text-align: center;'>Click on a pie slice to see details!</p>", unsafe_allow_html=True)
    else:
        st.warning("No debt composition data available for the selected year.")

with col2:
    if not composition_data.empty:
        st.markdown("#### 📊 Additional Analysis")
        
        # Calculate public vs private debt
        public_debt_categories = [
            "Public and publicly guaranteed debt (US$)",
            "Multilateral debt (US$)",
            "World Bank debt outstanding (US$)",
            "Public commercial bank debt (US$)",
            "Other public bank debt (US$)"
        ]
        
        private_debt_categories = [
            "Private debt (US$)",
            "Private sector debt, other (US$)",
            "Private non-guaranteed commercial debt (US$)"
        ]
        
        public_debt = composition_data[
            composition_data['Indicator Name'].isin(public_debt_categories)
        ]['Value_Billions'].sum()
        
        private_debt = composition_data[
            composition_data['Indicator Name'].isin(private_debt_categories)
        ]['Value_Billions'].sum()
        
        public_pct = (public_debt / total_debt * 100) if total_debt > 0 else 0
        private_pct = (private_debt / total_debt * 100) if total_debt > 0 else 0
        
        st.markdown(f"""
        <div class="insight-box">
        <strong>🏛️ Public Sector Debt:</strong><br>
        ${public_debt:.1f}B ({public_pct:.1f}%)<br><br>
        <strong>🏢 Private Sector Debt:</strong><br>
        ${private_debt:.1f}B ({private_pct:.1f}%)
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

# -------------------- RAW DATA FRAME --------------------
st.markdown("---")
st.markdown("### 📋 **Raw Data**")
st.markdown("*Expand the section below to view the full, unfiltered data frame.*")

with st.expander("View Raw Data"):
    st.dataframe(df)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>📊 External Debt Interactive Dashboard | Built with Streamlit & Plotly</p>
    <p>💡 Use the interactive features above to explore debt patterns and generate insights</p>
</div>
""", unsafe_allow_html=True)
