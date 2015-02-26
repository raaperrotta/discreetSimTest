import random
import simpy

class Uav(object):

    # This is the explicit initializer.
    # We can add convenience initializers based on default parameter sets later.
    def __init__(self, env, pos, speed, lethality, target):
        self.env = env
        self.pos = pos
        self.lethality = lethality
        self.target = target

    """
        self.action = env.process(self.fly())

    def fly(self):
        while True:
            try:
                yield self.env.timeout(10)
            except simpy.Interrupt:
                # if the UAV is shot down we can cancel the ship impact
                return

            self.env.process(self.crash())

    def crash(self):
    """

class Weapon(object):
    def __init__(self, env, rate, lethality):
        self = simpy.PreemptiveResource(env, capacity=1)
        self.env = env
        self.rate = rate
        self.lethality = lethality


class Radar(object):
    def __init__(self, env, period, ranges, p_detect):
        self.env = env
        self.period = period
        self.ranges = ranges
        self.p_detect = p_detect


class Ship(object):
    def __init__(self, env, pos, speed, weapons, radars):
        self.env = env
        self.pos = pos
        self.speed = speed
        self.weapons = weapons
        self.radar = radar


