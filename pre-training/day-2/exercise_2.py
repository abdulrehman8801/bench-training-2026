def calculate_average(scores):
    total = 0
    for score in scores:
        total += score
    return total / len(scores)

def class_topper(students):
    return max(students, key=lambda s: calculate_average(s['scores']))

def get_grade(scores):
    avg = calculate_average(scores)
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'


x = [
    {'name': 'a', 'scores': [30,40,80,90], 'subject': 'math'},
    {'name': 'b', 'scores': [40,80,90], 'subject': 'eng'},
    {'name': 'c', 'scores': [40,80,90,100], 'subject': 'urdu'},
    {'name': 'd', 'scores': [40,70,88,100], 'subject': 'comp'},
    {'name': 'e', 'scores': [30,70,58,95], 'subject': 'phy'}
]

is_top_scorer = class_topper(x)

for student in x:
    name = student['name']
    scores = student['scores']
    avg = calculate_average(scores)
    grade = get_grade(scores)

    is_top = student == is_top_scorer
    print(f"{'*** TOP *** ' if is_top else ''}{name} | {avg:.2f} | {grade}")

y = sorted(x, key=lambda s: calculate_average(s['scores']), reverse=True)
print(y)
