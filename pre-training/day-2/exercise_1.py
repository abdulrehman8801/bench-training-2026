def word_frequency(sentence):
    words = sentence.lower().split(' ')
    dict = {}
    for word in words:
        count = words.count(word)
        dict.update({ word: count })
    return dict

sentence = 'python is fun and python is easy to learn i like learning python because python is powerful practice makes coding better and practice improves skills coding in python every day makes practice easier learning coding and practicing python makes coding fun'

x = word_frequency(sentence)

sorted_x_by_count = dict(sorted(x.items(), key=lambda item: item[1], reverse=True))

converted_to_list = list(sorted_x_by_count.items())

it = 0
while it < 5:
    print(converted_to_list[it])
    it+=1