import plotly.graph_objects as go
import pandas as pd

def create_candlestick_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Creates an interactive Plotly Candlestick chart.
    """
    # Create the figure
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=f'{ticker} Price'
    )])

    # Customize the layout
    fig.update_layout(
        title=f'{ticker} Price Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False, # Hide the bottom range slider for a cleaner look
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        template="plotly_dark" # Use a modern dark theme
    )

    return fig
