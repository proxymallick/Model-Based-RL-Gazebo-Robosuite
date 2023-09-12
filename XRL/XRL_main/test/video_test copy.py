from typing import Dict, List, Optional, Tuple
import gym
from PIL import Image

from pyvirtualdisplay import Display
Display().start()

def render_episode(env: gym.Env): 

  screen = env.render(mode='rgb_array')
  im = Image.fromarray(screen)
  images = [im]
  s_next = env.reset()

  for i in range(1000):

      s_next, reward, done, _ = env.step(env.action_space.sample())

      screen = env.render(mode='rgb_array')
      images.append(Image.fromarray(screen))

      if done:
        break

  return images

if __name__ =='__main__':
  # server_model('server')
  env = gym.make("CartPole-v1")
  env.reset()


  # Save GIF image
  images = render_episode(env)
  image_file = 'cartpole-v1_py.gif'
  # loop=0: loop forever, duration=1: play each frame for 1ms
  images[1].save(
      image_file, save_all=True, append_images=images[1:], loop=0, duration=1)
  print(images[0])