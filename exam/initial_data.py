from random import randint
import json
d = []
for difficulty in xrange(1, 11):
    for i in xrange(100):
        d.append(dict(model="exam.Question", pk=difficulty*100+i, fields=dict(text="Difficulty %d Question %d" % (difficulty, i), difficulty=difficulty,
                 option_1="Difficulty %d Question %d Option 1" % (difficulty, i),
                 option_2="Difficulty %d Question %d Option 2" % (difficulty, i),
                 option_3="Difficulty %d Question %d Option 3" % (difficulty, i),
                 option_4="Difficulty %d Question %d Option 4" % (difficulty, i),
                 correct_option=randint(1, 4)
                 )))

with open('initial_data.json', 'w') as f:
    f.write(json.dumps(d, indent=4))
