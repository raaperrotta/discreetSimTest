import simpy
import numpy as n
from model import *

def iterate():
    env = simpy.Environment()

    ships = []
    weapons = []
    radars = []
    uavs = []

    max_detection_range = 60.

    ships.append(Ship(env, pos=n.array([0.,0.]), speed=0.))
    
    # Might want a generator function later
    # At least should have a way to delay/stagger the UAV creation
    uavs.append(Uav(env, pos=n.array([100.,0.]), speed=10, lethality=0.8, target=ships[0]))
    uavs.append(Uav(env, pos=n.array([100.,100.]), speed=10, lethality=0.8, target=ships[0]))
    uavs.append(Uav(env, pos=n.array([110.,0.]), speed=10, lethality=0.8, target=ships[0]))
    uavs.append(Uav(env, pos=n.array([110.,10.]), speed=10, lethality=0.8, target=ships[0]))
    uavs.append(Uav(env, pos=n.array([110.,20.]), speed=10, lethality=0.8, target=ships[0]))
    uavs.append(Uav(env, pos=n.array([110.,30.]), speed=10, lethality=0.8, target=ships[0]))

    radars.append(Radar(env, period=2., ranges=[max_detection_range, 20.], p_detect=n.array([0.2, 0.8]), ship=ships[0], uavs=uavs))
    
    weapons.append(Weapon(env, rate=10., lethality=0.01, ship=ships[0]))
    weapons.append(Weapon(env, rate=0.25, lethality=0.2, ship=ships[0]))
    weapons.append(Weapon(env, rate=2., lethality=0.10, ship=ships[0]))
    # weapons.append(Weapon(env, rate=4., lethality=0.05, ship=ships[0]))

    print " "
    print ships
    print uavs
    print radars
    print weapons
    print " "

    # weapons[0].action = env.process(weapons[0].shoot_uav(uavs[0]))
    # weapons[1].action = env.process(weapons[1].shoot_uav(uavs[1]))
    
    env.run()
    return 0


iterate()

"""
# The iterator that calls each iteration and handles the results
num_runs = 10.
num_fail = 0
for ii in range(10):
    num_fail += iterate()

risk = num_fail/num_runs
print "Hit " + str(100.*risk) + "% of the time."
"""
