SCAM_KEYWORDS = {
    "otp": 30,
    "pin": 30,
    "password": 30,
    "urgent": 15,
    "click": 25,
    "verify account": 25,
    "send money": 25,
    "blocked": 20,
    "lottery": 30,
    "prize": 25,
}


def analyze_scam(text: str):
    print("NEW SCAM SERVICE RUNNING")
    lowered = text.lower()

    matched = [
        word for word in SCAM_KEYWORDS
        if word in lowered
    ]

    score = min(
        sum(SCAM_KEYWORDS[word] for word in matched),
        100,
    )

    if score >= 60:
        risk_level = "HIGH"
    elif score >= 20:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    warnings = [
        f"Suspicious phrase detected: {word}"
        for word in matched
    ]

    if risk_level == "HIGH":
        message = "High scam risk. Do not share OTP, PIN, passwords, or send money."
    elif risk_level == "MEDIUM":
        message = "Be careful and verify the sender before taking action."
    else:
        message = "No major scam indicators detected."

    return {
        "risk_level": risk_level,
        "score": score,
        "warnings": warnings,
        "message": message,
    }