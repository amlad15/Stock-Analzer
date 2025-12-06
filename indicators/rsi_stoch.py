import pandas as pd
import pandas_ta as ta
import numpy as np

def calculate_momentum_indicators(df: pd.DataFrame) -> dict:
    """
    Calculates RSI and Stochastic RSI and assigns a score and label.
    
    Args:
        df: Normalized DataFrame containing 'close' column.
        
    Returns:
        A dictionary containing the score and label for each indicator.
    """
    df_temp = df.copy()
    
    # --- 1. Calculate Indicators ---
    # pandas-ta documentation: df.ta.rsi(length=14)
    df_temp.ta.rsi(length=14, append=True)
    
    # pandas-ta documentation: df.ta.stoch(k=14, d=3, smooth_k=3)
    df_temp.ta.stoch(k=14, d=3, append=True)
    
    # Get the latest values
    latest_rsi = df_temp['RSI_14'].iloc[-1]
    latest_stoch_k = df_temp['STOCHk_14_3_3'].iloc[-1]
    
    results = {}

    # --- 2. RSI Signal Scoring (Range: -1.0 to +1.0) ---
    rsi_score = 0.0
    rsi_label = "Neutral"
    
    if latest_rsi < 30:
        rsi_score = 0.8  # Strong Bullish
        rsi_label = "Oversold (Bullish)"
    elif 30 <= latest_rsi < 50:
        rsi_score = 0.2  # Slight Bullish
        rsi_label = "Slight Bullish"
    elif 50 <= latest_rsi < 70:
        rsi_score = -0.2 # Slight Bearish
        rsi_label = "Slight Bearish"
    elif latest_rsi >= 70:
        rsi_score = -0.8 # Strong Bearish
        rsi_label = "Overbought (Bearish)"
    
    results['RSI'] = {"score": rsi_score, "label": rsi_label}

    # --- 3. Stochastic RSI Signal Scoring (Range: -1.0 to +1.0) ---
    stoch_score = 0.0
    stoch_label = "Neutral"

    if latest_stoch_k < 20:
        stoch_score = 1.0  # Strong Buy Signal
        stoch_label = "Oversold Extreme (Strong Buy)"
    elif latest_stoch_k > 80:
        stoch_score = -1.0 # Strong Sell Signal
        stoch_label = "Overbought Extreme (Strong Sell)"
    
    results['Stoch_RSI'] = {"score": stoch_score, "label": stoch_label}
    
    return results
