import streamlit as st

def render_buy_sell_meter(signal_data: dict):
    """
    Renders the Buy/Sell Strength Meter using Streamlit components.
    
    Args:
        signal_data: The dictionary output from the signal scoring engine.
    """
    final_score = signal_data['final_score']
    final_label = signal_data['final_label']
    
    # Normalize score from [-1.0, 1.0] to a percentage [0, 100]
    normalized_progress = int((final_score + 1) / 2 * 100)

    st.subheader("Buy ↔ Sell Meter")
    
    # Use a customized progress bar/metric display for the score
    if final_label in ["Strong Buy", "Buy"]:
        color = "🟢"
    elif final_label in ["Strong Sell", "Sell"]:
        color = "🔴"
    else:
        color = "🟡"

    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f"## {color} **{final_label}**")
        st.metric(label="Aggregated Score", value=f"{final_score:.2f} / 1.00")

    with col2:
        st.markdown("**Strength Meter (0% = Strong Sell, 100% = Strong Buy)**")
        st.progress(normalized_progress)
        
        # Display a helpful message explaining the signal
        if final_label == "Strong Buy":
            st.success("All indicators are pointing towards strong upside momentum and trend strength.")
        elif final_label == "Strong Sell":
            st.error("Multiple indicators signal strong downside momentum and trend weakness.")
        elif final_label == "Neutral":
            st.info("The aggregated signal is mixed or waiting for confirmation.")
        else:
            st.write(f"The indicators suggest a **{final_label}** position.")
            
    st.markdown("---")
