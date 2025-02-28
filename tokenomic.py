import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="EDITH Tokenomics Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for elegant, minimal styling
st.markdown("""
<style>
    /* Modern fonts and styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main container styling */
    .stApp {
        background: #111111 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: white !important;
        font-weight: 500 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Container styling */
    .element-container {
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    
    /* Chart container styling */
    .stPlotlyChart {
        background: rgba(30, 30, 30, 0.3) !important;
        border-radius: 8px;
        padding: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(30, 30, 30, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        color: white !important;
    }
    
    /* Text styling */
    .stMarkdown {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Reduce padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(30, 30, 30, 0.3);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        height: 100%;
        margin-bottom: 1rem;
    }
    .info-title {
        font-size: 1.1rem;
        color: white;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .info-content {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
    }
    .highlight {
        color: white;
        font-weight: 500;
    }
    
    /* Table styling */
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    .comparison-table th {
        background: rgba(50, 50, 50, 0.5);
        color: white;
        padding: 0.75rem;
        text-align: left;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .comparison-table td {
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.7);
    }
    .comparison-table tr:nth-child(even) {
        background: rgba(40, 40, 40, 0.3);
    }
    .comparison-table tr:hover {
        background: rgba(60, 60, 60, 0.3);
    }
    
    /* KPI card styling */
    .kpi-card {
        background: rgba(30, 30, 30, 0.3);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        height: 100%;
    }
    .kpi-title {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 500;
        color: white;
        margin-bottom: 0.5rem;
    }
    .kpi-subtitle {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.5);
    }
    
    /* Mitigation strategy card */
    .mitigation-card {
        background: rgba(30, 30, 30, 0.3);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 1rem;
    }
    .mitigation-title {
        font-size: 1.1rem;
        color: white;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .mitigation-content {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# Title with minimal styling
st.markdown("""
    <h1 style='text-align: center; color: white; font-size: 2rem; font-weight: 500; margin-bottom: 1.5rem;'>
        EDITH (ED) Tokenomics Dashboard
    </h1>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
    <p style='color: rgba(255, 255, 255, 0.7); font-size: 1rem; text-align: center; margin-bottom: 2rem;'>
        This dashboard presents a comprehensive view of the EDITH (ED) tokenomics design, including 
        allocations, vesting schedules, fundraising details, and supply metrics.
    </p>
""", unsafe_allow_html=True)

# Data for Tokenomics
total_supply = 1_000_000_000  # 1 billion tokens

# Token Allocation Distribution (percentages)
allocation_dist = {
    "Sales": 15,  # Aggregate for Private Sale (3%), VC (6%), Launchpad (6%)
    "Team": 10,
    "Advisors": 5,
    "Treasury": 20,
    "Community & Ecosystem": 48,
    "Exchange & Liquidity": 2
}

# Break down Sales into subcategories for vesting
sales_breakdown = {
    "Private Sale": 3,  # 3% of total supply
    "VC Round": 6,  # 6% of total supply
    "Launchpad": 6   # 6% of total supply
}

# Private Sale tiers
private_sale_tiers = {
    ">$10K": {"allocation": 10_000_000, "vesting_period": 12, "tge": 5, "monthly_unlock": 791_667},
    "$5K-$10K": {"allocation": 10_000_000, "vesting_period": 6, "tge": 5, "monthly_unlock": 1_583_333},
    "$0-$5K": {"allocation": 10_000_000, "vesting_period": 4, "tge": 5, "monthly_unlock": 2_375_000}
}

# Vesting and Unlock Schedules (in months, percentages unlocked over time)
vesting_schedule = {
    "Private Sale": {"tge": 5, "vesting_period": 12, "cliff": 0},  # 5% at TGE, 95% over 12 months (tiered)
    "VC Round": {"tge": 5, "vesting_period": 18, "cliff": 6},  # 5% at TGE, 6-month cliff, 95% over 18 months
    "Launchpad": {"tge": 25, "vesting_period": 4, "cliff": 0},  # 25% at TGE, 75% over 4 months
    "Team": {"tge": 0, "vesting_period": 108, "cliff": 12},  # 0% at TGE, 12-month cliff, 100% over 108 months
    "Advisors": {"tge": 0, "vesting_period": 108, "cliff": 12},  # 0% at TGE, 12-month cliff, 100% over 108 months
    "Treasury": {"tge": 5, "vesting_period": 108, "cliff": 12},  # 5% at TGE, 12-month cliff, 95% over 108 months
    "Community & Ecosystem": {"tge": 5, "vesting_period": 240, "cliff": 0},  # 5% at TGE, activity-based (placeholder: 500K ED/month)
    "Exchange & Liquidity": {"tge": 10, "vesting_period": 18, "cliff": 0}  # 10% at TGE, 90% over 18 months
}

# Investor Rounds Data
investor_rounds = {
    "Private Sale": {"tokens": 30_000_000, "price_per_token": 0.01, "amount_raised": 300_000, "fdv": 10_000_000},
    "VC Round": {"tokens": 60_000_000, "price_per_token": 0.015, "amount_raised": 900_000, "fdv": 15_000_000},
    "Launchpad": {"tokens": 60_000_000, "price_per_token": 0.02, "amount_raised": 1_200_000, "fdv": 20_000_000}
}

# Projected market cap and token price at Month 48
market_cap_month_48 = 500_000_000  # $500M

# Token allocations dictionary for reference
allocations = {
    "Private Sale": 30_000_000, "VC Round": 60_000_000, "Launchpad": 60_000_000,
    "Team": 100_000_000, "Advisors": 50_000_000, "Treasury": 200_000_000,
    "Community & Ecosystem": 480_000_000, "Exchange & Liquidity": 20_000_000
}

# Function to calculate monthly unlocks for Private Sale with tiers
def calculate_private_sale_unlocks(month, tiers):
    if month == 0:
        # TGE unlock (5% of each tier)
        return sum([tier["allocation"] * tier["tge"] / 100 for tier in tiers.values()])
    
    monthly_unlock = 0
    for tier_name, tier in tiers.items():
        if month <= tier["vesting_period"]:
            monthly_unlock += tier["monthly_unlock"]
    
    return monthly_unlock

# Function to calculate monthly unlocks for each category
def calculate_monthly_unlock(category, month, allocations, vesting_schedule):
    tokens = allocations[category]
    schedule = vesting_schedule[category]
    tge_percent = schedule["tge"] / 100
    vesting_period = schedule["vesting_period"]
    cliff = schedule["cliff"]
    
    if month == 0:
        return tokens * tge_percent
    elif month <= cliff:
        return 0
    elif month <= vesting_period + cliff:
        if category == "VC Round" and month == cliff + 1:
            # For VC Round with cliff, first month after cliff includes delayed unlocks
            monthly_amount = tokens * (1 - tge_percent) / vesting_period
            delayed_unlocks = monthly_amount * cliff
            return monthly_amount + delayed_unlocks
        elif category == "Treasury" and month == cliff + 1:
            # For Treasury with cliff, linear vesting after cliff
            monthly_amount = tokens * (1 - tge_percent) / vesting_period
            return monthly_amount
        elif category == "Exchange & Liquidity":
            # For Exchange & Liquidity
            monthly_amount = tokens * (1 - tge_percent) / vesting_period
            return monthly_amount
        elif category == "Community & Ecosystem":
            # Activity-based distribution - simulated worker activity
            if month <= 2:
                return 0  # No unlocks in first 2 months after TGE
            else:
                # Start with 500,000 tokens per month from month 3
                return 500_000
        else:
            monthly_amount = tokens * (1 - tge_percent) / vesting_period
            return monthly_amount
    else:
        return 0

# Function to calculate circulating and unlocked supply over time based on vesting schedules
def calculate_supplies(allocations, vesting_schedule, private_sale_tiers, months=48):
    months_range = np.arange(months + 1)
    circulating_supply = np.zeros(len(months_range))
    
    for month in months_range:
        total_unlocked = 0
        for category, tokens in allocations.items():
            if category == "Private Sale":
                total_unlocked += calculate_private_sale_unlocks(month, private_sale_tiers)
            else:
                total_unlocked += calculate_monthly_unlock(category, month, allocations, vesting_schedule)
        circulating_supply[month] = (total_unlocked / total_supply) * 100
    
    # For simplicity, assume unlocked supply equals circulating supply
    return circulating_supply, circulating_supply

# Calculate circulating supply
circulating, unlocked = calculate_supplies(allocations, vesting_schedule, private_sale_tiers)

# Function to calculate supply shocks (month-to-month percentage changes)
def calculate_supply_shocks(circulating_supply):
    shocks = [0]  # TGE has no prior month
    for i in range(1, len(circulating_supply)):
        if circulating_supply[i-1] > 0:
            shock = ((circulating_supply[i] - circulating_supply[i-1]) / circulating_supply[i-1]) * 100
        else:
            shock = 0
        shocks.append(shock)
    return shocks

# Calculate supply shocks
monthly_shocks_calculated = calculate_supply_shocks(circulating)

# Calculate detailed monthly unlocks for the first 12 months
detailed_unlocks = []
for month in range(13):  # 0 to 12 months
    month_data = {"Month": month}
    total_unlocked = 0
    
    # Calculate unlocks for each category
    for category in allocations.keys():
        if category == "Private Sale":
            category_unlocked = calculate_private_sale_unlocks(month, private_sale_tiers)
        else:
            category_unlocked = calculate_monthly_unlock(category, month, allocations, vesting_schedule)
        
        month_data[category] = category_unlocked
        total_unlocked += category_unlocked
    
    month_data["Total Unlocked"] = total_unlocked
    month_data["Circulating %"] = (total_unlocked / total_supply) * 100
    detailed_unlocks.append(month_data)

# Convert to DataFrame for easier manipulation
unlock_df = pd.DataFrame(detailed_unlocks)

# Display EDITH tokenomics overview
st.markdown("## EDITH (ED) Tokenomics Overview")

# Create a clean layout with columns for the overview
overview_cols = st.columns(4)

# Calculate actual TGE circulating supply
tge_circulating = circulating[0]
tge_tokens = (tge_circulating / 100) * total_supply

with overview_cols[0]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Supply</div>
        <div class="kpi-value">1,000,000,000</div>
        <div class="kpi-subtitle">ED Tokens</div>
    </div>
    """, unsafe_allow_html=True)

with overview_cols[1]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Initial Circulating Supply</div>
        <div class="kpi-value">{tge_circulating:.1f}%</div>
        <div class="kpi-subtitle">{tge_tokens:,.0f} ED at TGE</div>
    </div>
    """, unsafe_allow_html=True)

with overview_cols[2]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Total Fund Raise</div>
        <div class="kpi-value">$2,400,000</div>
        <div class="kpi-subtitle">From Private Sale, VC, and Launchpad</div>
    </div>
    """, unsafe_allow_html=True)

with overview_cols[3]:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Fully Diluted Valuation</div>
        <div class="kpi-value">$20,000,000</div>
        <div class="kpi-subtitle">At Launchpad price ($0.02/ED)</div>
    </div>
    """, unsafe_allow_html=True)

# Create a clean layout with columns
col1, col2 = st.columns(2)

# --- ALLOCATION DISTRIBUTION PIE CHART ---
with col1:
    st.markdown("### Token Allocation")
    
    # Create a minimal, elegant pie chart
    colors = [
        '#E0E0E0', '#CCCCCC', '#BBBBBB', '#AAAAAA',
        '#999999', '#888888'
    ]
    
    fig_allocation = go.Figure(data=[go.Pie(
        labels=list(allocation_dist.keys()),
        values=list(allocation_dist.values()),
        hole=0.7,
        marker=dict(
            colors=colors,
            line=dict(color='rgba(0, 0, 0, 0)', width=0)
        ),
        textfont=dict(size=12, color='white'),
        textposition='outside',
        textinfo='percent',
        hovertemplate="<b>%{label}</b><br>" +
                      "Allocation: %{percent}<br>" +
                      "Amount: %{value}M tokens<extra></extra>"
    )])
    
    fig_allocation.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.05,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300
    )
    
    st.plotly_chart(fig_allocation, use_container_width=True)
    
    # Add detailed info for Sales category
    st.markdown("**Sales Breakdown:**")
    sales_cols = st.columns(3)
    with sales_cols[0]:
        st.markdown(f"Private Sale: **{sales_breakdown['Private Sale']}%**")
    with sales_cols[1]:
        st.markdown(f"VC Round: **{sales_breakdown['VC Round']}%**")
    with sales_cols[2]:
        st.markdown(f"Launchpad: **{sales_breakdown['Launchpad']}%**")

# --- CIRCULATION VS UNLOCKS CHART ---
with col2:
    st.markdown("### Supply Metrics")
    
    # Enhanced Circulation vs Unlocks chart
    fig_supply = go.Figure()
    
    # Add markers at key points
    key_months = [0, 1, 2, 3, 4, 5, 6, 7, 12, 24, 36, 48]
    
    # Add traces with proper formatting
    fig_supply.add_trace(go.Scatter(
        x=list(range(49)),
        y=circulating,
        mode='lines+markers',
        name='Circulating Supply',
        line=dict(color='#FFFFFF', width=2),
        marker=dict(
            size=[8 if m in key_months else 0 for m in range(49)],
            color='#FFFFFF'
        ),
        fill='tozeroy',
        fillcolor='rgba(255,255,255,0.05)',
        hovertemplate="Month %{x}<br>Circulating: %{y:.1f}%<extra></extra>"
    ))
    
    # Calculate monthly growth rates for annotations
    monthly_growth_rates = []
    for i in range(1, 6):
        if circulating[i-1] > 0:
            growth_rate = ((circulating[i] - circulating[i-1]) / circulating[i-1]) * 100
        else:
            growth_rate = 0
        monthly_growth_rates.append(growth_rate)
    
    # Add annotations for key points
    for i, month in enumerate(key_months):
        if month == 0:
            # Show initial supply
            fig_supply.add_annotation(
                x=month,
                y=circulating[month],
                text=f"Initial: {circulating[month]:.1f}%",
                showarrow=False,
                yshift=10,
                font=dict(size=10, color='#FFFFFF')
            )
        elif 1 <= month <= 5:
            # Show growth rate for months 1-5
            fig_supply.add_annotation(
                x=month,
                y=circulating[month],
                text=f"+{monthly_growth_rates[month-1]:.1f}%",
                showarrow=False,
                yshift=10,
                font=dict(size=10, color='#FFFFFF')
            )
        elif month > 5 and month < len(circulating):
            # Show circulating supply for later months
            fig_supply.add_annotation(
                x=month,
                y=circulating[month],
                text=f"{circulating[month]:.1f}%",
                showarrow=False,
                yshift=10,
                font=dict(size=10, color='#FFFFFF')
            )
    
    fig_supply.update_layout(
        xaxis=dict(
            title="Months",
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            dtick=6  # Show ticks every 6 months
        ),
        yaxis=dict(
            title="Supply (%)",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
            bgcolor='rgba(0,0,0,0)'
        ),
        hovermode='x unified',
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    
    st.plotly_chart(fig_supply, use_container_width=True)

# --- INVESTOR ROUNDS CHART ---
st.markdown("### Investment Metrics")
col3, col4 = st.columns(2)

with col3:
    # Enhanced Investor Rounds chart
    round_names = list(investor_rounds.keys())
    prices = [data["price_per_token"] for data in investor_rounds.values()]
    amounts_raised = [data["amount_raised"] / 1_000 for data in investor_rounds.values()]  # Convert to thousands
    
    fig_rounds = go.Figure()
    
    # Add price per token bars
    fig_rounds.add_trace(go.Bar(
        x=round_names,
        y=prices,
        name='Price per Token ($)',
        marker_color='rgba(170,170,170,0.7)',
        hovertemplate="<b>%{x}</b><br>" +
                      "Price: $%{y:.3f}<extra></extra>",
        text=[f"${p:.3f}" for p in prices],
        textposition='auto',
        textfont=dict(color='white', size=10)
    ))
    
    # Add amount raised bars
    fig_rounds.add_trace(go.Bar(
        x=round_names,
        y=amounts_raised,
        name='Amount Raised ($K)',
        marker_color='rgba(255,255,255,0.7)',
        hovertemplate="<b>%{x}</b><br>" +
                      "Raised: $%{y:.0f}K<extra></extra>",
        text=[f"${a:.0f}K" for a in amounts_raised],
        textposition='auto',
        textfont=dict(color='white', size=10)
    ))
    
    fig_rounds.update_layout(
        xaxis=dict(
            title="Round",
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title="Value",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False
        ),
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    
    st.plotly_chart(fig_rounds, use_container_width=True)

with col4:
    # Enhanced FDV chart with minimal design
    fdv_values = [data["fdv"] / 1_000_000 for data in investor_rounds.values()]  # In millions
    
    fig_fdv = go.Figure()
    
    # Horizontal bar chart for FDV
    fig_fdv.add_trace(go.Bar(
        y=round_names,
        x=fdv_values,
        orientation='h',
        marker=dict(
            color='rgba(255,255,255,0.7)',
            line=dict(color='rgba(0,0,0,0)', width=0)
        ),
        hovertemplate="<b>%{y}</b><br>" +
                      "FDV: $%{x:.1f}M<extra></extra>",
        text=[f"${v:.1f}M" for v in fdv_values],
        textposition='auto',
        textfont=dict(color='white', size=10)
    ))
    
    fig_fdv.update_layout(
        title=dict(
            text="Fully Diluted Valuation (FDV)",
            font=dict(size=16, color='white'),
            x=0,
            y=0.95
        ),
        xaxis=dict(
            title="FDV ($M)",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(t=30, b=0, l=0, r=0),
        height=300
    )
    
    st.plotly_chart(fig_fdv, use_container_width=True)

# --- PRIVATE SALE TIERS SECTION ---
st.markdown("### Private Sale Investment Tiers")

# Create a bar chart for Private Sale tiers
tier_names = list(private_sale_tiers.keys())
tier_allocations = [tier["allocation"] / 1_000_000 for tier in private_sale_tiers.values()]  # Convert to millions
tier_vesting = [tier["vesting_period"] for tier in private_sale_tiers.values()]

fig_tiers = go.Figure()

# Add allocation bars
fig_tiers.add_trace(go.Bar(
    x=tier_names,
    y=tier_allocations,
    name='Allocation (M Tokens)',
    marker_color='rgba(255,255,255,0.7)',
    hovertemplate="<b>%{x}</b><br>" +
                  "Allocation: %{y:.1f}M tokens<extra></extra>",
    text=[f"{a:.1f}M" for a in tier_allocations],
    textposition='auto',
    textfont=dict(color='white', size=10)
))

# Add vesting period bars
fig_tiers.add_trace(go.Bar(
    x=tier_names,
    y=tier_vesting,
    name='Vesting Period (Months)',
    marker_color='rgba(170,170,170,0.7)',
    hovertemplate="<b>%{x}</b><br>" +
                  "Vesting: %{y} months<extra></extra>",
    text=[f"{v} mo" for v in tier_vesting],
    textposition='auto',
    textfont=dict(color='white', size=10)
))

fig_tiers.update_layout(
    title="Private Sale Tiers",
    xaxis=dict(
        title="Investment Tier",
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title="Value",
        showgrid=True,
        gridcolor='rgba(255,255,255,0.05)',
        zeroline=False
    ),
    barmode='group',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=10),
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(t=30, b=0, l=0, r=0),
    height=300
)

st.plotly_chart(fig_tiers, use_container_width=True)

# --- DETAILED UNLOCK SCHEDULE TABLE ---
st.markdown("### Detailed Monthly Unlock Schedule (TGE to Month 12)")

# Format the DataFrame for display
formatted_unlock_df = unlock_df.copy()
formatted_unlock_df["Month"] = formatted_unlock_df["Month"].apply(lambda x: f"Month {x}")
for category in allocations.keys():
    formatted_unlock_df[category] = formatted_unlock_df[category].apply(lambda x: f"{x:,.0f}")
formatted_unlock_df["Total Unlocked"] = formatted_unlock_df["Total Unlocked"].apply(lambda x: f"{x:,.0f}")
formatted_unlock_df["Circulating %"] = formatted_unlock_df["Circulating %"].apply(lambda x: f"{x:.2f}%")

# Display the unlock schedule table
st.dataframe(
    formatted_unlock_df,
    hide_index=True,
    use_container_width=True
)

# --- SUPPLY SHOCK CHART ---
st.markdown("### Supply Shocks")

# Monthly supply shocks chart
fig_shocks = go.Figure(go.Bar(
    x=list(range(1, 13)),  # Months 1-12
    y=monthly_shocks_calculated[1:13],
    marker_color=['rgba(255,100,100,0.7)' if x > 5 else 'rgba(255,255,255,0.7)' for x in monthly_shocks_calculated[1:13]],
    hovertemplate="Month %{x}<br>Shock: %{y:.1f}%<extra></extra>"
))
fig_shocks.add_hline(y=5, line_dash="dash", line_color="rgba(255,100,100,0.3)", annotation_text="High Risk (>5%)", annotation_position="top right")
fig_shocks.update_layout(
    title="Monthly Supply Shocks (First 12 Months)",
    xaxis_title="Month",
    yaxis_title="Supply Change (%)",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=300
)
st.plotly_chart(fig_shocks, use_container_width=True)

# --- SUPPLY SHOCK TABLE ---
st.markdown("### Supply Shock Table (First 12 Months)")

# Calculate monthly unlocks and supply shocks
shock_data = []
for i in range(13):
    if i == 0:
        tokens = unlock_df.iloc[i]["Total Unlocked"]
        pct = unlock_df.iloc[i]["Circulating %"]
        shock = "-"  # No shock for TGE
    else:
        prev_tokens = unlock_df.iloc[i-1]["Total Unlocked"]
        tokens = unlock_df.iloc[i]["Total Unlocked"]
        pct = unlock_df.iloc[i]["Circulating %"]
        monthly_unlock = tokens - prev_tokens
        shock = ((tokens - prev_tokens) / prev_tokens) * 100 if prev_tokens > 0 else 0
        shock = f"{shock:.2f}%"
    
    shock_data.append({
        "Month": f"Month {i}",
        "Circulating Supply (Tokens)": f"{tokens:,.0f}",
        "Circulating Supply (%)": f"{pct:.2f}%",
        "Monthly Unlock (Tokens)": f"{tokens if i == 0 else tokens - unlock_df.iloc[i-1]['Total Unlocked']:,.0f}",
        "Supply Shock (%)": shock
    })

# Convert to DataFrame and display
shock_df = pd.DataFrame(shock_data)
st.dataframe(
    shock_df,
    hide_index=True,
    use_container_width=True
)

# --- VESTING SCHEDULES SECTION ---
st.markdown("### Vesting Schedules")

# Create a visual representation of vesting schedules
vesting_data = pd.DataFrame([
    {'Category': 'Private Sale (>$10K)', 'TGE (%)': 5, 'Cliff (months)': 0, 'Vesting (months)': 12},
    {'Category': 'Private Sale ($5K-$10K)', 'TGE (%)': 5, 'Cliff (months)': 0, 'Vesting (months)': 6},
    {'Category': 'Private Sale ($0-$5K)', 'TGE (%)': 5, 'Cliff (months)': 0, 'Vesting (months)': 4},
    {'Category': 'VC Round', 'TGE (%)': 5, 'Cliff (months)': 6, 'Vesting (months)': 18},
    {'Category': 'Launchpad', 'TGE (%)': 25, 'Cliff (months)': 0, 'Vesting (months)': 4},
    {'Category': 'Team', 'TGE (%)': 0, 'Cliff (months)': 12, 'Vesting (months)': 108},
    {'Category': 'Advisors', 'TGE (%)': 0, 'Cliff (months)': 12, 'Vesting (months)': 108},
    {'Category': 'Treasury', 'TGE (%)': 5, 'Cliff (months)': 12, 'Vesting (months)': 108},
    {'Category': 'Community & Ecosystem', 'TGE (%)': 5, 'Cliff (months)': 0, 'Vesting (months)': 240},
    {'Category': 'Exchange & Liquidity', 'TGE (%)': 10, 'Cliff (months)': 0, 'Vesting (months)': 18},
])

# Create a horizontal bar chart for vesting schedules
fig_vesting = go.Figure()

# Add bars for vesting periods
for i, row in vesting_data.iterrows():
    # Calculate total duration (cliff + vesting)
    total_duration = row['Cliff (months)'] + row['Vesting (months)']
    
    # Add TGE marker
    fig_vesting.add_trace(go.Bar(
        y=[row['Category']],
        x=[row['TGE (%)']],
        name='TGE',
        orientation='h',
        marker=dict(color='rgba(0, 200, 100, 0.7)'),
        text=[f"{row['TGE (%)']}% at TGE"],
        textposition='auto',
        hovertemplate="<b>%{y}</b><br>TGE: %{x}%<extra></extra>",
        showlegend=False
    ))
    
    # Add cliff period if > 0
    if row['Cliff (months)'] > 0:
        fig_vesting.add_trace(go.Bar(
            y=[row['Category']],
            x=[row['Cliff (months)']],
            name='Cliff',
            orientation='h',
            marker=dict(color='rgba(255, 100, 100, 0.7)'),
            text=[f"{row['Cliff (months)']} mo cliff"],
            textposition='auto',
            hovertemplate="<b>%{y}</b><br>Cliff: %{x} months<extra></extra>",
            showlegend=False
        ))
    
    # Add vesting period
    fig_vesting.add_trace(go.Bar(
        y=[row['Category']],
        x=[row['Vesting (months)']],
        name='Vesting',
        orientation='h',
        marker=dict(color='rgba(255, 255, 255, 0.7)'),
        text=[f"{row['Vesting (months)']} mo vesting"],
        textposition='auto',
        hovertemplate="<b>%{y}</b><br>Vesting: %{x} months<extra></extra>",
        showlegend=False
    ))

fig_vesting.update_layout(
    title="Vesting Schedules",
    xaxis=dict(
        title="Duration (Months)",
        showgrid=True,
        gridcolor='rgba(255,255,255,0.05)',
        zeroline=False
    ),
    yaxis=dict(
        title="",
        showgrid=False,
        zeroline=False,
        categoryorder='array',
        categoryarray=vesting_data['Category'].tolist()[::-1]
    ),
    barmode='stack',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=400,
    margin=dict(l=200)
)

st.plotly_chart(fig_vesting, use_container_width=True)

# --- MITIGATION STRATEGIES SECTION ---
st.markdown("### Supply Shock Mitigation Strategies")

mitigation_cols = st.columns(2)

with mitigation_cols[0]:
    st.markdown("""
    <div class="mitigation-card">
        <div class="mitigation-title">Staking Program</div>
        <div class="mitigation-content">
            <p>A staking program will be implemented to incentivize long-term holding and reduce circulating supply:</p>
            <ul>
                <li><strong>Launch:</strong> Month 1</li>
                <li><strong>APY:</strong> 15-25% (variable based on lock duration)</li>
                <li><strong>Lock Options:</strong> 3, 6, 12 months</li>
                <li><strong>Target:</strong> 30-40% of circulating supply staked</li>
                <li><strong>Impact:</strong> Potential to reduce Month 1 shock from 19.23% to ~10%</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with mitigation_cols[1]:
    st.markdown("""
    <div class="mitigation-card">
        <div class="mitigation-title">Buyback & Burn Program</div>
        <div class="mitigation-content">
            <p>A portion of protocol revenue will be allocated to token buybacks and burns:</p>
            <ul>
                <li><strong>Allocation:</strong> 25% of protocol revenue</li>
                <li><strong>Frequency:</strong> Monthly burns</li>
                <li><strong>Trigger:</strong> Automatic during high supply shock months (>5%)</li>
                <li><strong>Transparency:</strong> Public dashboard tracking all burns</li>
                <li><strong>Long-term Goal:</strong> Burn up to 10% of total supply over 5 years</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Additional mitigation strategies
st.markdown("""
<div class="mitigation-card">
    <div class="mitigation-title">Activity-Based Community & Ecosystem Distribution</div>
    <div class="mitigation-content">
        <p>The Community & Ecosystem allocation (48% of total supply) will be distributed based on actual network activity rather than a fixed schedule:</p>
        <ul>
            <li><strong>Worker Rewards:</strong> Distributed based on actual work completed on the network</li>
            <li><strong>Governance Participation:</strong> Rewards for active governance participation</li>
            <li><strong>Developer Grants:</strong> Milestone-based distribution to ecosystem developers</li>
            <li><strong>Cap:</strong> Maximum monthly distribution of ~2M ED (0.2% of total supply)</li>
            <li><strong>Impact:</strong> Ensures token distribution aligns with actual network growth</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CONCLUSION ---
st.markdown("## Conclusion")

st.markdown("""
<p style='color: rgba(255, 255, 255, 0.7); font-size: 1rem; text-align: center; margin-bottom: 2rem;'>
    The EDITH (ED) tokenomics design balances the needs of early investors, the team, and the community. 
    With tiered private sale vesting, strategic VC cliff periods, and activity-based community distribution, 
    the token supply growth is carefully managed to support long-term price stability while enabling 
    sufficient liquidity for a healthy market.
</p>
""", unsafe_allow_html=True)
