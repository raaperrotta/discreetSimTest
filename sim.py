import simpy
import numpy as n
from model import *

def iterate():
    env = simpy.Environment()

    weapons = []
    radars = []
    ships = []
    uavs = []

    max_detection_range = 60.

    weapons.append(Weapon(env, rate=10., lethality=0.01))
    weapons.append(Weapon(env, rate=0.25, lethality=0.2))

    radars.append(Radar(env, period=2., ranges=[max_detection_range, 20.], p_detect=n.array([0.2, 0.8])))

    ships.append(Ship(env, pos=n.array([0.,0.]), speed=0., weapons=weapons, radars=radars))

    uavs.append(Uav(env, pos=n.array([100.,0.]), speed=10, lethality=0.8, target=ships[0]))
    uavs.append(Uav(env, pos=n.array([110.,0.]), speed=10, lethality=0.8, target=ships[0]))

    weapons[0].action = env.process(weapons[0].shoot_uav(uavs[0]))
    weapons[1].action = env.process(weapons[1].shoot_uav(uavs[1]))

    print " "
    print uavs
    print "%s, " % (uav for uav in uavs)
    print weapons

    env.run()
    return 0

# The iterator that calls each iteration and handles the results
num_runs = 10.
num_fail = 0
for ii in range(10):
    num_fail += iterate()

risk = num_fail/num_runs
print "Hit " + str(100.*risk) + "% of the time."
