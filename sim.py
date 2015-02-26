import simpy
import numpy as n
from model import *

env = simpy.Environment()

weapons = []
radars = []
ships = []
uavs = []

max_detection_range = 60.

weapons.append(Weapon(env, rate=10., lethality=0.05))
radars.append(Radar(env, period=2., ranges=[max_detection_range, 20.], p_detect=n.array([0.2, 0.8])))
ships.append(Ship(env, pos=n.array([0.,0.]), speed=0., weapons=weapons, radars=radars))
uavs.append(Uav(env, pos=n.array([100.,0.]), speed=10, lethality=0.8, target=ships[0]))

env.run(until=100)
