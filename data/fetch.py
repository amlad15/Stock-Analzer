import yfinance as yf
import pandas as pd

def fetch_and_normalize_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical OHLCV data using yfinance and normalizes the columns.
    
    Args:
        ticker: The stock symbol (e.g., 'AAPL').
        start_date: Start date string (YYYY-MM-DD).
        end_date: End date string (YYYY-MM-DD).
        
    Returns:
        A normalized pandas DataFrame or an empty DataFrame on failure.
    """
    try:
        # 1. Fetch data from yfinance
        # Adding auto_adjust=True to handle split/dividend adjustments cleanly
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        
        if df.empty:
            return pd.DataFrame()

        # 2. Reset index to turn 'Date' into a column named 'date'
        df = df.reset_index()
        
        # 3. Rename and select columns to match the normalized format
        column_mapping = {
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }
        
        # Select and reorder columns
        df = df[list(column_mapping.keys())].rename(columns=column_mapping)
        
        # Ensure 'date' is the correct type
        df['date'] = pd.to_datetime(df['date'])

        return df
        
    except Exception as e:
        # In a real app, you might use logging.error
        # print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()
