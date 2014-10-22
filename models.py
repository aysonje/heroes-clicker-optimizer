class Representable(object):
    def __repr__(self):
        result = {}
        for attr in self.__represent__:
            result[attr] = getattr(self, attr)
        return repr(result)

class Achievement(Representable):
    __represent__ = ['name', 'bonus']

    def __init__(self, name, bonus):
        self.name = name
        self.bonus = bonus


class Goal(Representable):
    __represent__ = ['hero_name', 'level', 'upgrade']

    def __init__(self, hero_name, level, upgrade=None):
        self.hero_name = hero_name
        self.level = level
        self.upgrade = upgrade
        if self.upgrade.level > self.level:
            self.level = self.upgrade.level


class Upgrade(Representable):
    __represent__ = ['level', 'bonus', 'type']

    def __init__(self, type, level, bonus, cost):
        self.level = level
        self.bonus = bonus
        self.cost = cost
        self.type = type

    def is_global(self):
        return self.type == 'global' or self.type == 'gold'


class Hero(Representable):
    __represent__ = ['name', 'level', 'upgrades']

    def __init__(self, name, base_damage, base_cost):
        self.level = 0
        self.name = name
        self.base_damage = base_damage
        self.base_cost = base_cost
        self.upgrades = []

    def _clone(self):
        clone = Hero(self.name, self.base_damage, self.base_cost)
        clone.level = self.level
        clone.upgrades = self.upgrades[:]
        return clone

    def _price_to_level(self, level):
        return self.base_cost*(1.07**self.level - 1.07**level) / (-0.07)

    def fork(self, goal):
        # Goal has been matched in one instance
        if (self.level > goal.level) and (goal.upgrade in self.upgrades):
            return 0, self
        clone = self._clone()
        cost = 0
        if self.level < goal.level:
            cost += clone._price_to_level(goal.level)
            clone.level = goal.level
        if goal.upgrade is not None:
            cost += goal.upgrade.cost
            clone.upgrades.append(goal.upgrade)
        return cost, clone

    def compute_personal_multiplier(self):
        multiplier = 1.00
        for upgrade in self.upgrades:
            if not upgrade.is_global():
                multiplier *= upgrade.bonus
        return multiplier

    def compute_global_multiplier(self):
        multiplier = 1.00
        for upgrade in self.upgrades:
            if upgrade.is_global():
                multiplier *= upgrade.bonus
        return multiplier

    def compute_raw_damage(self):
        return self.base_damage * self.level

    def compute_upgraded_damage(self):
        return self.compute_personal_multiplier() * self.compute_raw_damage()


class Universe(object):
    def __init__(self, achievements, heroes):
        self.achievements = achievements
        self.heroes = dict((h.name,h) for h in heroes)

    def compute_global_multiplier(self):
        multiplier = 1.00
        for achievement in self.achievements:
            multiplier *= achievement.bonus
        for hero in self.heroes.itervalues():
            multiplier *= hero.compute_global_multiplier()
        return multiplier

    def compute_damage(self):
        global_multiplier = self.compute_global_multiplier()
        total_damage = 0.0
        for hero in self.heroes.itervalues():
            total_damage += hero.compute_upgraded_damage()
        return 1e-5 + global_multiplier * total_damage

    def _clone(self):
        clone = Universe(self.achievements, self.heroes.values())
        return clone

    def fork(self, goal):
        clone = self._clone()
        hero = clone.heroes[goal.hero_name]
        cost, fork = hero.fork(goal)
        clone.heroes[goal.hero_name] = fork
        return cost, clone
