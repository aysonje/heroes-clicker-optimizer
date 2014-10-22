def create_heroic_goals(hero):
    goals = []
    for upgrade in hero.upgrade_options:
        goal = Goal(hero, upgrade.level, upgrade)
        goals.append(goals)

    for level in range(200, 2001, 25):
        goal = Goal(hero, level)
        goals.append(goal)

    return goals
