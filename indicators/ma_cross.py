import pandas as pd
import pandas_ta as ta
import numpy as np

def calculate_trend_indicators(df: pd.DataFrame) -> dict:
    """
    Calculates EMA/SMA trends and the Golden/Death Cross and assigns a score and label.
    Includes safety checks for minimum data length.
    
    Args:
        df: Normalized DataFrame containing 'close' column.
        
    Returns:
        A dictionary containing the score and label for each indicator.
    """
    df_temp = df.copy()
    
    # Check 1: Minimum Data Length (Need at least 200 rows for MA_200 indicators)
    if len(df_temp) < 200:
        # If not enough data, return Neutral for all trend indicators
        return {
            'EMA_Trend': {"score": 0.0, "label": "Insufficient Data (Need 200+ days)"},
            'SMA_Trend': {"score": 0.0, "label": "Insufficient Data (Need 200+ days)"},
            'MA_Cross': {"score": 0.0, "label": "Insufficient Data (Need 200+ days)"}
        }
        
    # --- 1. Calculate Indicators ---
    # EMAs: 20, 50, 200
    df_temp.ta.ema(length=20, append=True)
    df_temp.ta.ema(length=50, append=True)
    df_temp.ta.ema(length=200, append=True)
    
    # SMAs: 50, 200
    df_temp.ta.sma(length=50, append=True)
    df_temp.ta.sma(length=200, append=True)
    
    # Define expected column names
    EMA_200_COL = 'EMA_200'
    SMA_50_COL = 'SMA_50'
    SMA_200_COL = 'SMA_200'
    
    # Check 2: Ensure pandas-ta created the columns (minimal check for 200 period)
    if EMA_200_COL not in df_temp.columns or SMA_200_COL not in df_temp.columns:
         return {
            'EMA_Trend': {"score": 0.0, "label": "Calculation Error (MA failed)"},
            'SMA_Trend': {"score": 0.0, "label": "Calculation Error (MA failed)"},
            'MA_Cross': {"score": 0.0, "label": "Calculation Error (MA failed)"}
        }

    # Get the latest values
    latest_close = df_temp['close'].iloc[-1]
    latest_ema_20 = df_temp['EMA_20'].iloc[-1]
    latest_ema_50 = df_temp['EMA_50'].iloc[-1]
    latest_ema_200 = df_temp['EMA_200'].iloc[-1]
    
    latest_sma_50 = df_temp['SMA_50'].iloc[-1]
    latest_sma_200 = df_temp['SMA_200'].iloc[-1]

    # Check 3: Ensure values are not NaN
    if pd.isna(latest_ema_200) or pd.isna(latest_sma_200):
        return {
            'EMA_Trend': {"score": 0.0, "label": "Indicator Value NaN"},
            'SMA_Trend': {"score": 0.0, "label": "Indicator Value NaN"},
            'MA_Cross': {"score": 0.0, "label": "Indicator Value NaN"}
        }

    # Check for Cross (using 50 and 200 period SMAs)
    cross_signal = (latest_sma_50 - latest_sma_200)

    results = {}
    
    # --- 2. EMA Trend Scoring (Using 20/50/200 Stack) ---
    ema_score = 0.0
    ema_label = "Neutral"
    
    if latest_close > latest_ema_20 and latest_close > latest_ema_50 and latest_close > latest_ema_200:
        ema_score = 0.8
        ema_label = "Strong Bullish Trend (Price above all EMAs)"
    elif latest_close < latest_ema_200:
        ema_score = -0.8
        ema_label = "Strong Bearish Trend (Price below EMA 200)"
    elif latest_close > latest_ema_50:
        ema_score = 0.4
        ema_label = "Bullish Intermediate Trend"
    elif latest_close < latest_ema_50:
        ema_score = -0.4
        ema_label = "Bearish Intermediate Trend"
        
    results['EMA_Trend'] = {"score": ema_score, "label": ema_label}
    
    # --- 3. SMA Trend Scoring (Using 50/200 Trend) ---
    sma_score = 0.0
    sma_label = "Neutral"
    
    if latest_close > latest_sma_50 and latest_close > latest_sma_200:
        sma_score = 0.6
        sma_label = "Bullish Long-Term Trend"
    elif latest_close < latest_sma_50 and latest_close < latest_sma_200:
        sma_score = -0.6
        sma_label = "Bearish Long-Term Trend"

    results['SMA_Trend'] = {"score": sma_score, "label": sma_label}
    
    # --- 4. Cross Scoring (Golden/Death) ---
    cross_score = 0.0
    cross_label = "Neutral"

    # Compare the current 50/200 SMA relationship
    if cross_signal > 0:
        cross_score = 1.0
        cross_label = "Golden Cross in effect (50 SMA > 200 SMA)"
    elif cross_signal < 0:
        cross_score = -1.0
        cross_label = "Death Cross in effect (50 SMA < 200 SMA)"
    
    results['MA_Cross'] = {"score": cross_score, "label": cross_label}
    
    return results
