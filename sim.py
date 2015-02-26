import simpy
from model import *

env = simpy.Environment()

weapons = []
radars = []
ships = []
uavs = []

max_detection_range = 60

weapons.append(Weapon(env, rate=10, lethality=0.05))
radars.append(Radar(env, period=2, ranges=[max_detection_range, 20], p_detect=[0.2, 0.8]))
ships.append(Ship(env, pos=[0,0], speed=2, weapons=weapons, radars=radars))
uavs.append(Uav(env, pos=[100,0], speed=10, lethality=0.8, target=ships[0]))

print uavs
