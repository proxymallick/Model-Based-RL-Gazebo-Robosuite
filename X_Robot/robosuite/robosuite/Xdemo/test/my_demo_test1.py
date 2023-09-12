import robosuite as suite
from robosuite.controllers import load_controller_config
from robosuite.controllers.controller_factory import reset_controllers
from robosuite.utils import observables
from robosuite.utils.input_utils import *
from robosuite.robots import Bimanual
import imageio
import numpy as np
import robosuite.utils.macros as macros
macros.IMAGE_CONVENTION = "opencv"
options = {
    'env_name': 'EElab_test2',
    "robots": "UR5e"
}
controller_name = "JOINT_VELOCITY"
options["controller_configs"] = suite.load_controller_config(default_controller=controller_name)

action_dim = 6
num_test_steps = 6
test_value = 1
steps_per_action = 75
steps_per_rest = 75



env = suite.make(
    **options,
    has_renderer=False,
    has_offscreen_renderer=True,
    ignore_done=True,
    # control_freq=100,
    use_camera_obs=True,
    use_object_obs=True, 
    camera_names='Labviewer',
    camera_heights=512,
    camera_widths=512,
    # has_offscreen_renderer=True,
)

# obs = {
#     'robot0_joint_pos_cos': None,
#     'robot0_joint_pos_sin': None,
#     'robot0_joint_vel': None,
#     'robot0_eef_pos': None,
#     'robot0_eef_quat': None,
#     'robot0_gripper_qpos': None,
#     'robot0_gripper_qvel': None,
#     'cubeA_pos': None,
#     'cubeA_quat': None,
#     'cubeB_pos': None,
#     'cubeB_quat': None,
#     'gripper_to_cubeA': None,
#     'gripper_to_cubeB': None,
#     'cubeA_to_cubeB': None,
# }

obs = env.reset()
print(obs)
ndim = env.action_dim
# print('env.action_dim = ', env.action_dim)
# o = list(obs['robot0_proprio-state']) + list(obs['object-state'])
# print('length of o = ', len(o))
# env.viewer.set_camera(camera_id=3)
writer = imageio.get_writer("/home/xhnfly/Cosmic_rays_X/X_Robot/robosuite/robosuite/demos/video/video_my2.mp4", fps=100)
frames = []
# To accommodate for multi-arm settings (e.g.: Baxter), we need to make sure to fill any extra action space
# Get total number of arms being controlled
n = 0
gripper_dim = 0
for robot in env.robots:
    gripper_dim = robot.gripper["right"].dof if isinstance(robot, Bimanual) else robot.gripper.dof
    # print("gripper_dim=", gripper_dim)
    
    n += int(robot.action_dim / (action_dim + gripper_dim))
    print('n = ', n)

# Define neutral value
neutral = np.zeros(action_dim + gripper_dim)
print("neutral=", neutral)
# Keep track of done variable to know when to break loop
count = 0
# Loop through controller space

action = neutral.copy()
for i in range(100):
    action[count] = test_value
    # print("action[count]=", action[count])
    total_action = np.tile(action, n)
    # print('total_action = ', total_action)
    obs, reward, done, _  = env.step(total_action)
    frame = obs["Labviewer_image"]
    
    writer.append_data(frame)
    print("Saving frame #{}".format(i))
    if i == 100:
        count += 1
    # env.render()
    if done:
        break




# Shut down this env before starting the next test
writer.close()
