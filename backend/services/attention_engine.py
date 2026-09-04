def calculate_attention_score(
    price_change_percent: float,
    volume_change_percent: float = 0,
    volume_ratio: float = 0,
    news_count: int = 0
):
    score = 0
    reasons = []

    # =============================================
    # PRICE MOVEMENT
    # =============================================

    if abs(price_change_percent) >= 5:
        score += 40
        reasons.append("Significant price movement")

    elif abs(price_change_percent) >= 2:
        score += 25
        reasons.append("Notable price movement")

    elif abs(price_change_percent) >= 1:
        score += 10
        reasons.append("Small price movement")

    # =============================================
    # VOLUME ACTIVITY
    # =============================================

    if volume_ratio >= 2:
        score += 35
        reasons.append(
            f"Unusually high trading volume ({volume_ratio:.1f}x normal)"
        )

    elif volume_ratio >= 1.5:
        score += 20
        reasons.append(
            f"Higher than normal trading volume ({volume_ratio:.1f}x normal)"
        )

    elif volume_ratio >= 1.2:
        score += 10
        reasons.append(
            f"Increased trading volume ({volume_ratio:.1f}x normal)"
        )

    # =============================================
    # NEWS
    # =============================================

    if news_count >= 3:
        score += 25
        reasons.append(
            f"{news_count} new news events"
        )

    elif news_count > 0:
        score += 10
        reasons.append(
            f"{news_count} new news event"
        )

    # =============================================
    # FINAL SCORE
    # =============================================

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"

    elif score >= 40:
        level = "MEDIUM"

    else:
        level = "LOW"

    # =============================================
    # EXPLANATION
    # =============================================

    if reasons:
        explanation = " combined with ".join(reasons) + "."

    else:
        explanation = "No significant changes detected."

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
        "explanation": explanation
    }