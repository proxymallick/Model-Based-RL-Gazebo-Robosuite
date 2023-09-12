import sys
sys.path.append("/home/xhnfly/Cosmic_rays_X/XRL/")

import XRL_main

env = XRL_main.make('Reacher-v2')

env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()