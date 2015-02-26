import random
import simpy

class Uav(object):

    # This is the explicit initializer.
    # We can add convenience initializers based on default parameter sets later.
    def __init__(self, env, pos, speed, lethality, target):
        self.env = env
        self.pos = pos
        self.speed = speed
        self.lethality = lethality
        self.target = target

        self.action = env.process(self.blow_up_ship())

    def blow_up_ship(self):
            try:
                dist_to_ship = sum((self.pos-self.target.pos)**2)**(0.5)
                # Still need to correct for non-zero ship speed
                yield self.env.timeout(dist_to_ship/self.speed)
                print "I blew up the ship! " + str(self.env.now)
            except simpy.Interrupt:
                # if the UAV is shot down we can cancel the ship impact
                print "I think I was shot down..."
                pass

class Weapon(object):
    def __init__(self, env, rate, lethality):
        self = simpy.PriorityResource(env, capacity=1)
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
        self.radars = radars


