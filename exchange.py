"""Script to generate guest list for MCR exchange dinners."""
import numpy as np
import random
from csv import reader
import sys
import platform

exchange_titles = {'Brasenose', 'GTC'}
if len(sys.argv) != 2:
    print('Running in example mode.')
    print('Using "exchange_test_responses.csv"')
    filename = "exchange_test_responses.csv"
else:
    filename = sys.argv[1]
print(filename)


def both_legs(x):
    """People who can attend both legs."""
    if (x[0] + x[1] == 2):
        return 1
    else:
        return 0


def any_legs(x):
    """People who can attend one leg."""
    if (x[0] + x[1] > 0):
        return 1
    else:
        return 0


for dinner in exchange_titles:
    print('Diners for ' + dinner)
    names = []
    emails = []
    dietary = []
    home = []
    away = []
    never = []
    with open(filename, 'r') as f:
        next(f)
        for l in reader(f):
            fields = l
            # fields = l.strip().split(',');
            names.append(fields[1])
            emails.append(fields[2])
            never.append("No" in fields[-2])
            dietary.append(fields[-3])
            # fields = l.strip().split('"');
            fields = fields[3]

            home.append(dinner + ' Home' in fields)
            away.append(dinner + ' Away' in fields)

    # This script was originally written in Python 2. However, in Python 3, the
    # behaviour of the zip() and map() functions changed. The code below takes
    # this into account and implements the old Python 2 behaviour even if it is
    # run in Python 3.
    python_version = int(platform.python_version()[0])
    if python_version == 2:
        legs = zip(home, away)
        both = np.array(map(both_legs, legs))
        skip = np.array(map(any_legs, legs))
    elif python_version == 3:
        legs = []
        both = []
        skip = []
        for i, v in enumerate(home):
            legs.append((home[i], away[i]))
            both.append(both_legs([home[i], away[i]]))
            skip.append(any_legs([home[i], away[i]]))
        both = np.array(both)
        skip = np.array(skip)
    else:
        raise ValueError('The Python version is neither 2 nor 3')
    both_score = 1
    never_score = 5
    scores = np.array(skip) * (1 + both_score * np.array(both) +
                               never_score * np.array(never))

    scores = scores.tolist()
    for i in range(len(names)):
        print((names[i], scores[i], emails[i], never[i], home[i], away[i],
               dietary[i]))
    print('\n')

    bag = []
    bounds = []
    total = 0
    for n in range(len(names)):
        x = scores[n]
        bag += [names[n]] * x
        bounds = bounds + [total + x]
        total += x

    diners = []
    while len(bag) > 0:
        draw = random.randint(1, len(bag)) - 1
        i = 0
        diners = diners + [bag[draw]]
        bag[:] = [x for x in bag if x != diners[-1]]

    print('Order for ' + dinner + ' (' +
          str(len([s for s in scores if s != 0])) + ')')
    print('name,never,home,away,dietary')
    for d in diners:
        index = names.index(d)
        print(d + ',' + str(scores[index]) + ',' + str(never[index]) + ',' +
              ('Home' if home[index] else '') + ',' +
              ('Away' if away[index] else '') + ',' + dietary[index])
    print('\n\n')
