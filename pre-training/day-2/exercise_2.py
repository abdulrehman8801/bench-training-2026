from typing import Dict, List

def calculate_average(scores: List[float]) -> float:
    if not scores:
        raise ValueError("scores must be a non-empty list")
    if not all(isinstance(s, (int, float)) for s in scores):
        raise TypeError("all scores must be numbers")
    return sum(scores) / len(scores)

def get_grade(avg: float) -> str:
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"

def class_topper(students: List[Dict]) -> Dict:
    if not students:
        raise ValueError("students must be a non-empty list")
    return max(students, key=lambda s: calculate_average(s["scores"]))

students = [
    {"name": "a", "scores": [30, 40, 80, 90], "subject": "Math"},
    {"name": "b", "scores": [40, 80, 90], "subject": "English"},
    {"name": "c", "scores": [40, 80, 90, 100], "subject": "Urdu"},
    {"name": "d", "scores": [40, 70, 88, 100], "subject": "Computer"},
    {"name": "e", "scores": [30, 70, 58, 95], "subject": "Physics"},
]

topper = class_topper(students)

print("Report (original order):")
for student in students:
    avg = calculate_average(student["scores"])
    grade = get_grade(avg)
    prefix = "*** TOP *** \n" if student is topper else ""
    print(f"{prefix}{student['name']} | {avg:.2f} | {grade}")

print("\nReport (sorted by average):")
sorted_students = sorted(students, key=lambda s: calculate_average(s["scores"]), reverse=True)
for student in sorted_students:
    avg = calculate_average(student["scores"])
    grade = get_grade(avg)
    prefix = "*** TOP *** \n" if student is topper else ""
    print(f"{prefix}{student['name']} | {avg:.2f} | {grade}")
