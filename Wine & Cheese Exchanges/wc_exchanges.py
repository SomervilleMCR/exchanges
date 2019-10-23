"""Script for choosing guests on MCR wine & cheese exchanges."""
import numpy as np
import random
from csv import reader
import sys
import platform
import re


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

# GET THE NAMES OF THE COLLEGES YOU ARE EXCHANGING WITH
exchange_titles = []
with open(filename, 'r') as f:
    # SKIP OVER THE FIRST ROW OF THE SPREADSHEET
    next(f)
    # FOR EACH REMAINING ROW IN THE SPREADSHEET, EXTRACT THE INFORMATION
    for row in reader(f):
        # FIND THE INDICES OF THE STARTS OF THE COLLEGES' NAMES
        idx_starts_1 = [-2]
        idx_starts_2 = [m.start() for m in re.finditer(',', row[3])]
        idx_starts = idx_starts_1 + idx_starts_2
        # FIND THE INDICES OF THE ENDS OF THE COLLEGES' NAMES
        idx_ends_1 = [m.start() for m in re.finditer('Home', row[3])]
        idx_ends_2 = [m.start() for m in re.finditer('Away', row[3])]
        idx_ends = idx_ends_1 + idx_ends_2
        idx_ends.sort()
        # FOR EACH COLLEGE NAME, ADD IT TO THE LIST
        for i, v in enumerate(idx_starts):
            idx_start = idx_starts[i]
            idx_end = idx_ends[i]
            college = row[3][idx_start + 2:idx_end - 1]
            exchange_titles.append(college)
# REMOVE DUPLICATES FROM THE LIST
exchange_titles = list(set(exchange_titles))

for exchange in exchange_titles:
    print('Diners for ' + exchange)
    names = []
    home = []
    away = []
    # emails = []  # NOT RELEVANT FOR WC EXCHANGES
    # dietary = []  # NOT RELEVANT FOR WC EXCHANGES
    # never = []  # NOT RELEVANT FOR WC EXCHANGES
    with open(filename, 'r') as f:
        # SKIP OVER THE FIRST ROW OF THE SPREADSHEET
        next(f)
        # FOR EACH REMAINING ROW IN THE SPREADSHEET, EXTRACT THE INFORMATION
        for row in reader(f):
            names.append(row[1])
            # emails.append(row[2])  # NOT RELEVANT FOR WC EXCHANGES
            # never.append("No" in row[-2])  # NOT RELEVANT FOR WC EXCHANGES
            # dietary.append(row[-3])  # NOT RELEVANT FOR WC EXCHANGES
            attendance = row[3]
            home.append(exchange + ' Home' in attendance)
            away.append(exchange + ' Away' in attendance)

    # THIS SCRIPT WAS ORIGINALLY WRITTEN IN PYTHON 2. HOWEVER, IN PYTHON 3, THE
    # BEHAVIOUR OF THE zip() AND map() FUNCTIONS CHANGES. THE CODE BELOW TAKES
    # THIS INTO ACCOUNT AND IMPLEMENTS THE OLD PYTHON 2 BEHAVIOUR EVEN IF IT IS
    # RUN IN PYTHON 3.
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
    # never_score = 5  # NOT RELEVANT FOR WC EXCHANGES
    scores = np.array(skip) * (1 + both_score * np.array(both))

    scores = scores.tolist()
    for i in range(len(names)):
        print((names[i], scores[i], home[i], away[i]))

    print('')

    # PUT ALL THE NAMES INTO A VIRTUAL BAG
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

    # DRAW THE NAMES OF THE DINERS OUT OF THE VIRTUAL BAG
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

    # EXPORT THE NAMES OF THE PEOPLE WHO HAVE MADE IT ONTO THE EXCHANGE READY
    # TO BE COPY-PASTED INTO AN EMAIL
    with open('{}.txt'.format(exchange), 'w') as f:
        for diner in diners:
            f.write(diner + '\n')
