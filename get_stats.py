import sys, data
from collections import defaultdict

goals = []

f = open('strategy.txt', 'r')
for line in f.readlines():
    # form = '{} to {}; Cost: {}'.format(goal.hero_name, goal.level, cost)
    ss = line[:-1].split()
    name = ' '.join(ss[:-4])
    level = int(ss[-3][:-1])
    cost = float(ss[-1])
    goals.append((name, level, cost))


names_idx = {u['name']:i for i,u in enumerate(data.heroes)}

h = int(sys.argv[1])
stats = defaultdict(int)
for (name, lvl, cost) in goals[:h]:
    stats[name] = lvl

stats = stats.items()
stats.sort(key=lambda x:names_idx[x[0]])

for name, level in stats:
    print name, level
