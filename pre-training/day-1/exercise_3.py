user_input = int(input('Enter a number between 1-12: '))

while user_input < 1 or user_input > 12:
    user_input = int(input('Enter a number between 1-12: '))

for i in range(1,11):
    print(f'{user_input:>2} * {i:>2} = {user_input * i:>3}')

for x in range(1, 13):
    for y in range(1, 11):
        print(f'{x:>2} * {y:>2} = {x * y:>3}')