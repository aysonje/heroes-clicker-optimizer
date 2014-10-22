from models import Hero, Upgrade, Achievement, Universe, Goal
import data, config

answer = open('strategy.txt', 'w')
def pretty_print(goal, dps, cost):
    form = '{} to {}; Cost: {}'.format(goal.hero_name, goal.level, cost)
    print(form)
    answer.write(form+'\n')
    answer.flush()

print('Loading heroes...')
basic_heroes = []
for d in data.heroes:
    hero = Hero(d['name'], d['base_damage'], d['base_cost'])
    basic_heroes.append(hero)

print('Initializing achievements...')
active_achievements = []
for a in data.achievements:
    if a['name'] in config.achievements:
        active_achievements.append( Achievement(a['name'], a['bonus']) )
        print('Activated %s'%a['name'])

print('Creating goals...')
goals = []
for h in data.heroes:
    for u in h['upgrades']:
        upgrade = Upgrade(u['type'], u['level'], u['bonus'], u['cost'])
        upgrade_goal = Goal(h['name'], upgrade.level, upgrade)
        goals.append(upgrade_goal)

    for level in range(200, 2001, 25):
        if level%1000 == 0:
            bonus = 10.00
        else:
            bonus = 4.00
        upgrade = Upgrade('hidden', level, bonus, 0)
        level_goal = Goal(h['name'], level, upgrade)
        goals.append(level_goal)


print('Creating the universe...')
universe = Universe(active_achievements, basic_heroes)

best_dps = None
while len(goals) > 0:
    splits = []
    starting_dps = best_dps or universe.compute_damage()
    best_goodness = None

    for goal in goals:
        cost, fork = universe.fork(goal)
        result_dps = fork.compute_damage()
        try:
            goodness = cost/starting_dps + cost/(result_dps - starting_dps)
        except ZeroDivisionError:
            # This happens when something adds so little value to us
            if cost/last_cost < 1e-4:
                goodness = 0.0 # Too cheap to matter anyway
            else:
                goodness = float('inf')

        if best_goodness is None or goodness < best_goodness:
            best_goodness = goodness
            best_cost = cost
            best_goal = goal
            best_universe = fork
            best_dps = result_dps

    pretty_print(best_goal, best_dps, best_cost)
    goals.remove(best_goal)
    universe = best_universe
    last_cost = best_cost