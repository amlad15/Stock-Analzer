def aggregate_signals(indicator_results: dict) -> dict:
    """
    Aggregates all indicator scores using defined weights to calculate a final score.
    
    Args:
        indicator_results: A dictionary containing all indicator results, 
                           where each value is {"score": float, "label": str}.
        
    Returns:
        A dictionary containing the final aggregated score and label.
    """
    
    # 1. Example MVP weights (must sum to 1.0)
    weights = {
        "RSI": 0.4,
        "Stoch_RSI": 0.1,
        "EMA_Trend": 0.2,
        "SMA_Trend": 0.2,
        "MA_Cross": 0.1
    }
    
    if round(sum(weights.values()), 3) != 1.0:
        # Emergency check for weight integrity
        raise ValueError("Weights must sum to 1.0")

    final_score = 0.0
    scores_breakdown = {}
    
    # 2. Aggregate Score
    for key, weight in weights.items():
        if key in indicator_results:
            score = indicator_results[key]["score"]
            final_score += score * weight
            scores_breakdown[key] = {
                "score": score,
                "label": indicator_results[key]["label"],
                "weighted_score": round(score * weight, 3)
            }
        else:
            # Handle cases where an indicator might be missing
            scores_breakdown[key] = {"score": 0.0, "label": "N/A", "weighted_score": 0.0}

    # 3. Map Score to Label (Buy / Sell Meter Mapping)
    
    if final_score <= -0.6:
        final_label = "Strong Sell"
        color = "red"
    elif -0.6 < final_score <= -0.2:
        final_label = "Sell"
        color = "orange"
    elif -0.2 < final_score <= 0.2:
        final_label = "Neutral"
        color = "gray"
    elif 0.2 < final_score <= 0.6:
        final_label = "Buy"
        color = "lightgreen"
    elif final_score > 0.6:
        final_label = "Strong Buy"
        color = "green"
    else:
        final_label = "Neutral"
        color = "gray"

    return {
        "final_score": round(final_score, 3), # Final score between -1.0 and +1.0
        "final_label": final_label,
        "color": color,
        "breakdown": scores_breakdown
    }
