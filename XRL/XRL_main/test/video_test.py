from typing import Dict, List, Optional, Tuple
import gym
from PIL import Image


# display = Display(visible=1, size=(400, 300))

class video_rec:
    def __init__ (self, video_loc=True):
        self.video_loc = video_loc
        if self.video_loc:
            from pyvirtualdisplay import Display
            Display().start()
            print('Video local = True')

    def same_video(self):
        screen = env.render(mode='rgb_array')
        im = Image.fromarray(screen)
        images = [im]
        s_next = env.reset()

        for i in range(1000):

            s_next, reward, done, _ = env.step(action_step)

            screen = env.render(mode='rgb_array')
            images.append(Image.fromarray(screen))
            

            if done:
                break

        return images


    def play_video(self):
        screen = env.render(mode='rgb_array')
        im = Image.fromarray(screen)
        images = [im]
        s_next = env.reset()

        for i in range(1000):

            s_next, reward, done, _ = env.step(action_step)

            screen = env.render(mode='rgb_array')
            images.append(Image.fromarray(screen))
            

            if done:
                break

        return images

            
    def render_episode(self, self.env: gym.Env, action_step): 
        if self.video_loc == True:
          self.same_video()
        else:


        return images


if __name__ =='__main__':
  video_loc = True
  env = gym.make("Hopper-v2")
  env.reset()


  # Save GIF image
  images = video_rec.render_episode(env, False)
  image_file = 'cartpole-v2_py.gif'
  # loop=0: loop forever, duration=1: play each frame for 1ms
  images[0].save(
      image_file, save_all=True, append_images=images[1:], loop=0, duration=1)
  env.close()