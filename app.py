import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

# Import functions from the project structure
from data.fetch import fetch_and_normalize_data
from indicators.rsi_stoch import calculate_momentum_indicators
from indicators.ma_cross import calculate_trend_indicators
from scoring.signal import aggregate_signals
from ui.charts import create_candlestick_chart
from ui.meter import render_buy_sell_meter

# --- APP CONFIGURATION ---
st.set_page_config(page_title="MVP Stock Analyzer", layout="wide", initial_sidebar_state="expanded")
st.title("📈 Technical Indicator Aggregator MVP")
st.markdown("⚠️ This is NOT financial advice. It is a technical indicator aggregation tool.")

# --- 1. USER INPUT (Sidebar) ---
st.sidebar.header('Data Input Layer')

# Ticker Input
ticker_symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL)", 'MSFT').upper()

# Timeframe Selector
today = date.today()
timeframe_map = {
    '1 Year': relativedelta(years=1),
    '6 Months': relativedelta(months=6),
    '3 Months': relativedelta(months=3),
}
timeframe_option = st.sidebar.selectbox('Timeframe', list(timeframe_map.keys()))

start_date = today - timeframe_map.get(timeframe_option, relativedelta(years=1))
end_date = today

st.sidebar.markdown(f"Pulling data from **{start_date}** to **{end_date}**.")

# --- 2. DATA FETCHING ---

@st.cache_data(ttl=3600) # Cache for 1 hour
def load_data(ticker, start, end):
    return fetch_and_normalize_data(ticker, str(start), str(end))
    
if ticker_symbol:
    data_df = load_data(ticker_symbol, start_date, end_date)

    # Check 1: Did yfinance return an empty DataFrame?
    if data_df.empty:
        st.error(f"Could not retrieve data for ticker: **{ticker_symbol}** or the specified dates. Please check the symbol and ensure trading data exists for the timeframe.")
        # Stop execution here if no data was returned
        st.stop()
        
    # Check 2: Do we have at least one row of data to calculate metrics?
    if len(data_df) < 1:
        st.error(f"Data for **{ticker_symbol}** was fetched, but contains no trading days.")
        st.stop()

    # --- 3. INDICATOR ENGINE ---
    
    # Calculate all indicators. These functions now handle internal checks for sufficient data (e.g., 200 days)
    momentum_signals = calculate_momentum_indicators(data_df)
    trend_signals = calculate_trend_indicators(data_df)
    
    # Combine all indicator results
    all_indicators = {**momentum_signals, **trend_signals}

    # --- 4. SIGNAL SCORING ENGINE ---
    signal_data = aggregate_signals(all_indicators)
    
    # --- MAIN PAGE DISPLAY ---
    
    # Overview Header
    st.subheader(f"Analysis for **{ticker_symbol}**")
    
    # This line is now safe because we checked len(data_df) >= 1
    latest_close = data_df['close'].iloc[-1] 
    st.markdown(f"**Latest Close Price:** ${latest_close:.2f}")

    # Buy/Sell Meter and Breakdown
    render_buy_sell_meter(signal_data)
    
    st.markdown("---")
    
    # --- 5. CANDLESTICK CHART ---
    st.subheader("Price Visualization")
    
    # Get the latest price and the range for the chart title
    first_date = data_df['date'].iloc[0].strftime('%Y-%m-%d')
    last_date = data_df['date'].iloc[-1].strftime('%Y-%m-%d')

    chart_fig = create_candlestick_chart(data_df, ticker_symbol)
    st.plotly_chart(chart_fig, use_container_width=True) 

    st.markdown("---")
    
    # --- 6. EXPLAINABILITY (Indicator Breakdown) ---
    st.subheader("🔍 Signal Breakdown")
    
    # Prepare data for the breakdown table
    breakdown_list = []
    for key, value in signal_data['breakdown'].items():
        breakdown_list.append({
            "Indicator": key,
            "Signal": value["label"],
            "Score": f"{value['score']:.2f}",
            "Weighted Contribution": f"{value['weighted_score']:.3f}"
        })
        
    breakdown_df = pd.DataFrame(breakdown_list)
    st.table(breakdown_df.set_index('Indicator'))

    st.markdown("---")
    st.caption(f"Raw Data points used: {len(data_df)}")
        
else:
    st.info("Please enter a stock ticker symbol in the sidebar to begin analysis.")
