def grade_classifier(marks):
    if marks >= 90:
        return 'Distinction'
    elif marks >= 60:
        return 'Pass'
    else:
        return 'Fail'

print(grade_classifier(92))
print(grade_classifier(89))
print(grade_classifier(59))
print(grade_classifier(60))
print(grade_classifier(90))

scores = [45,72,91,60,38,85]

for score in scores:
    print(grade_classifier(score))

iterator = 0
while iterator < len(scores):
    print(grade_classifier(scores[iterator]))
    iterator += 1