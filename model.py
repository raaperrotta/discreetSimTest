import random
import numpy as n
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
        self.aggressors = []

        self.action = env.process(self.blow_up_ship())

    def __str__(self):
        return "Uav_" + str(id(self))

    def blow_up_ship(self):
            try:
                dist_to_ship = n.linalg.norm(self.pos-self.target.pos)
                # Still need to correct for non-zero ship speed
                yield self.env.timeout(dist_to_ship/self.speed)
                print "%s hit %s at %.2f" % (self, self.target, self.env.now)
                # self.env.exit(1)
            except simpy.Interrupt:
                # if the UAV is shot down we can cancel the ship impact
                # everyone can stop shooting at this uav now
                for weapon in self.aggressors:
                    weapon.action.interrupt()

class Weapon(object):
    def __init__(self, env, rate, lethality):
        # self = simpy.PriorityResource(env, capacity=1)
        self.env = env
        self.rate = rate
        self.lethality = lethality

    def __str__(self):
        return "Wpn_" + str(id(self))

    def shoot_uav(self,uav):
        uav.aggressors.append(self)
        period = 1./self.rate
        time_to_kill = period
        while random.random() > self.lethality:
            time_to_kill += period
        try:
            yield self.env.timeout(time_to_kill)
            uav.aggressors.remove(self)
            uav.action.interrupt()
            print "%s shot-down %s at %.2f" % (self, uav, self.env.now)
        except simpy.Interrupt:
            pass


class Radar(object):
    def __init__(self, env, period, ranges, p_detect):
        self.env = env
        self.period = period
        self.ranges = ranges
        self.p_detect = p_detect

    def __str__(self):
        return "Rdr_" + str(id(self))

        """
        self.action = env.process(self.search())

    def search(self):
        pass
"""

class Ship(object):
    def __init__(self, env, pos, speed, weapons, radars):
        self.env = env
        self.pos = pos
        self.speed = speed
        self.weapons = weapons
        self.radars = radars

    def __str__(self):
        return "Shp_" + str(id(self))

class World(object):
    def __init__(self,weapons,radars,ships,uavs): # will add weather later
        self.weapons = weapons
        self.radars = radars
        self.ships = ships
        self.uavs = uavs
