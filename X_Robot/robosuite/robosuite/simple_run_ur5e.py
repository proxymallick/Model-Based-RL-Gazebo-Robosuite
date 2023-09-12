import robosuite as suite
from robosuite.controllers import load_controller_config
from robosuite.controllers.controller_factory import reset_controllers
from robosuite.utils import observables
from robosuite.utils.input_utils import *
from robosuite.robots import Bimanual
import torch
# Load the desired controller configuration
controller_config = load_controller_config(default_controller="OSC_POSE")

options = {
    'env_name': 'EElab_test2',
    "robots": "UR5e"
}
controller_name = "JOINT_VELOCITY"
options["controller_configs"] = suite.load_controller_config(default_controller=controller_name)
'''
options = {
    'env_name': 'Door',
    "robots": "UR5e"
}
controller_name = "JOINT_VELOCITY"
options["controller_configs"] = suite.load_controller_config(default_controller=controller_name)
'''
env = suite.make(
    **options,
    has_renderer=False,
    has_offscreen_renderer=True,
    ignore_done=True,
    use_camera_obs=False,

)

test_env = suite.make(
    **options,
    has_renderer=False,
    has_offscreen_renderer=True,
    ignore_done=True,
    use_camera_obs=False,

)


video_env = suite.make(
    **options,
    has_renderer=False,
    has_offscreen_renderer=True,
    ignore_done=True,
    use_camera_obs=True,
    use_object_obs=True
)

frame = []
device= torch.device("cuda" if torch.cuda.is_available() else "cpu")
print('device = ', device)

# Reset the environment
obs = env.reset()

# Define a simple controller function to move the robot arm
def simple_controller(obs):
    # Set the desired end effector position
    target_pos = [0.5, 0.0, 0.5]
    # Set the desired joint angles
    target_joint_angles = env.robot.arm.inverse_kinematics(target_pos)

    # Set the action command to move the robot arm
    action = {
        "arm": target_joint_angles,
        "gripper": env.robot.gripper.format_action(0.0),  # Keep gripper closed
    }

    return action

# Run the simulation for 1000 steps
for i in range(1000):
    # Get the current observation from the environment
    obs = env._get_observation()

    # Call the simple controller function to get the action command
    action = simple_controller(obs)

    # Step the environment with the action command
    obs, reward, done, info = env.step(action)

    # Render the visualization
    env.render()
