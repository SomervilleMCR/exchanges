import numpy as np
import random
from csv import reader
import sys


if(len(sys.argv) != 2):
	print('No valid exchange diners csv provided.')
	exit(1)

exchange_titles = {'Brasenose' , 'GTC'}
filename = sys.argv[1]
print(filename)

def both_legs(x):
	if (x[0]+x[1] == 2):
		return 1
	else:
		return 0

def any_legs(x):
	if (x[0]+x[1] > 0):
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
	# with open('Trinity/Trinity 2018 Exchange Dinners (Responses) - Form Responses 1.csv', 'r') as f:
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

	legs = zip(home, away)
	both = np.array(map(both_legs, legs))
	skip = np.array(map(any_legs, legs))

	both_score = 1
	never_score = 5
	scores = np.array(skip) * (1 + both_score * np.array(both) + never_score * np.array(never))

	scores = scores.tolist()
	for i in range(len(names)):
		print((names[i], scores[i], emails[i], never[i], home[i], away[i],dietary[i]))
	print('\n')

	bag = []
	bounds = []
	total = 0
	for n in range(len(names)):
		x = scores[n]
		bag += [names[n]]*x
		bounds = bounds + [total + x]
		total += x

	diners = []
	while len(bag) > 0:
		draw = random.randint(1,len(bag)) - 1
		i = 0
		diners = diners + [bag[draw]]
		bag[:] = [x for x in bag if x != diners[-1]]

	print('Order for ' + dinner + ' (' + str(len([s for s in scores if s != 0])) + ')')
	print('name,never,home,away,dietary')
	for d in diners:
		index = names.index(d)
		print d + ',' + str(scores[index]) + ',' + str(never[index]) + ',' + ('Home' if home[index] else '') + ',' +  ('Away' if away[index] else '') + ',' + dietary[index]
	print('\n\n')
