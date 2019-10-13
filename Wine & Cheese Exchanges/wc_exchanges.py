"""Script for choosing guests on MCR wine & cheese exchanges."""
import numpy as np
import random
from csv import reader
import sys
import platform


#
# FUNCTION DEFINITIONS
#
def both_legs(x):
    """When someone can attend both legs of the exchange."""
    if (x[0]+x[1] == 2):
        return 1
    else:
        return 0


def any_legs(x):
    """When someone can attend one leg of the exchange."""
    if (x[0]+x[1] > 0):
        return 1
    else:
        return 0


#
# SCRIPT
#
if(len(sys.argv) != 2):
    filename = 'wc_exchange_test_responses.csv'
    print('No valid exchange diners csv provided.')
    print('Will continue with the example file which is:')
    print(filename)
elif len(sys.argv) == 2:
    filename = sys.argv[1]
    print(filename)
exchange_titles = {'Magdalen', 'Kellogg'}

for exchange in exchange_titles:
    print('Diners for ' + exchange)
    names = []
    home = []
    away = []
    # emails = []  # Not relevant for wc exchanges
    # dietary = []  # Not relevant for wc exchanges
    # never = []  # Not relevant for wc exchanges
    with open(filename, 'r') as f:
        next(f)  # Skip over the first row of the spreadsheet
        # For each remaining row in the spreadsheet, extract the information
        for row in reader(f):
            names.append(row[1])
            # emails.append(row[2])  # Not relevant for wc exchanges
            # never.append("No" in row[-2])  # Not relevant for wc exchanges
            # dietary.append(row[-3])  # Not relevant for wc exchanges
            attendance = row[2]
            home.append(exchange + ' Home' in attendance)
            away.append(exchange + ' Away' in attendance)

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
    both_score = 5
    # never_score = 5  # Not relevant for wc exchanges
    scores = np.array(skip) * (1 + both_score * np.array(both))

    scores = scores.tolist()
    for i in range(len(names)):
        print((names[i], scores[i], home[i], away[i]))

    print('')

    # Put all the names into a virtual bag
    bag = []
    bounds = []
    total = 0
    for n in range(len(names)):
        x = scores[n]
        bag += [names[n]]*x
        bounds = bounds + [total + x]
        total += x

    # Draw the names of the diners out of the virtual bag
    diners = []
    while len(bag) > 0:
        draw = random.randint(1, len(bag)) - 1
        diners = diners + [bag[draw]]
        bag[:] = [x for x in bag if x != diners[-1]]

    # Print the names of the diners you have draw out of the bag
    num_scores = len([s for s in scores if s != 0])
    print('Order for ' + exchange + ' (' + str(num_scores) + ')')
    print('name,home,away')
    for d in diners:
        index = names.index(d)
        print(d +
              ',' + str(scores[index]) +
              ',' + ('Home' if home[index] else '') +
              ',' + ('Away' if away[index] else '')
              )

    print('\n\n')

    # Export the names of the people who have made it onto the exchange ready
    # to be copy-pasted into an email
    with open('{}.txt'.format(exchange), 'w') as f:
        for diner in diners:
            f.write(diner + '\n')
