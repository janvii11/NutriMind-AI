def estimate_portion(confidence):

    if confidence >= 90:
        return 1.0

    elif confidence >= 80:
        return 0.85

    elif confidence >= 70:
        return 0.70

    else:
        return 0.60