def grade_classifier(score: float) -> str:
    try:
        score = float(score)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"score must be a number, got {score!r}") from exc

    if score < 0:
        raise ValueError("score cannot be negative")

    if score >= 90:
        return "Distinction"
    if score >= 60:
        return "Pass"
    return "Fail"


test_scores = [92, 89, 59, 60, 90]
for s in test_scores:
    print(f"score = {s} -> {grade_classifier(s)}")


scores = [45, 72, 91, 60, 38, 85]
for score in scores:
    print(f"score = {score} -> {grade_classifier(score)}")