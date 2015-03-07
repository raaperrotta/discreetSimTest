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
                
        # Still need to correct for non-zero ship speed
        time_to_ship = self.range_to_target(0)/self.speed
        
        self.reached_ship = env.timeout(time_to_ship)
        self.shot_down = env.event();
        
        self.action = env.process(self.attack())

    def __str__(self):
        return "Uav_" + str(id(self))
    
    def range_to_target(self,time):
        dist_to_ship = n.linalg.norm(self.pos-self.target.pos)
        return dist_to_ship - time*self.speed
        
    def attack(self):
        result = yield self.reached_ship | self.shot_down
        if self.reached_ship in result:
            print "%s hit %s at %.2f" % (self, self.target, self.env.now)
        else: # self.shot_down in result
            print "%s was shot down at %.2f" % (self, self.env.now)
            
            
class Weapon(object):
    def __init__(self, env, rate, lethality, ship):
        self.env = env
        self.rate = rate
        self.lethality = lethality
        self.resource = simpy.Resource(env, capacity=1)
        self.ship = ship
        ship.weapons.append(self)
        
        self.destroyed = env.event()

    def __str__(self):
        return "Wpn_" + str(id(self))

    def shoot_uav(self,uav):
        period = 1./self.rate
        time_to_kill = period
        while random.random() > self.lethality:
            time_to_kill += period

        print "%s engaged %s at %.2f" % (self, uav, self.env.now)
        result = yield self.env.timeout(time_to_kill) | uav.reached_ship
        if uav.reached_ship in result:
            pass
            # the UAV object will handle this case
        else:
            uav.shot_down.succeed()
            print "%s shot-down %s at %.2f" % (self, uav, self.env.now)


class Radar(object):
    def __init__(self, env, period, ranges, p_detect, ship, uavs):
        self.env = env
        self.period = period
        self.ranges = ranges
        self.p_detect = p_detect
        self.ship = ship
        self.uavs = uavs
        ship.radars.append(self)
        
        self.destroyed = env.event()
        
        self.action = []
        for uav in self.uavs:
            self.action.append(env.process(self.search(uav)))

    def __str__(self):
        return "Rdr_" + str(id(self))
    
    def search(self,uav):
        time_to_detect = 0
        detected_uav = self.env.timeout(time_to_detect)
        result = yield self.destroyed | uav.reached_ship | detected_uav
        if detected_uav in result:
            print "%s spotted %s at %.2f" % (self, uav, self.env.now)
            self.env.process(self.ship.alert(uav))
            
class Ship(object):
    def __init__(self, env, pos, speed):
        self.env = env
        self.pos = pos
        self.speed = speed
        self.weapons = []
        self.radars = []

    def __str__(self):
        return "Shp_" + str(id(self))
    
    def alert(self, uav):
        print "%s is aware of %s at %.2f" % (self, uav, self.env.now)
        events = [uav.reached_ship, uav.shot_down]
        for weapon in self.weapons:
            events.append(weapon.resource.request)
            
        result = yield simpy.events.AnyOf(self.env, events)
        if uav.reached_ship in result or uav.shot_down in result:
            print "hi"
        else:
            for weapon in result:
                print weapon
