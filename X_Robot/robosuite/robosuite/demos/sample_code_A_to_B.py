import robosuite
from robosuite import load_controller_config, make
from robosuite import make
from robosuite.controllers import load_controller_config
from robosuite.robots import Bimanual
from robosuite.utils.input_utils import *
# Load the robot and environment
controller_config = load_controller_config(default_controller="OSC_POSE")
# initialize the task
# Load the desired controller
# Create dict to hold options that will be passed to env creation call
options = {}

# print welcome info
print("Welcome to robosuite v{}!".format(suite.__version__))
print(suite.__logo__)

# Choose environment and add it to options
options["env_name"] = choose_environment()

# If a multi-arm environment has been chosen, choose configuration and appropriate robot(s)
if "TwoArm" in options["env_name"]:
    # Choose env config and add it to options
    options["env_configuration"] = choose_multi_arm_config()

    # If chosen configuration was bimanual, the corresponding robot must be Baxter. Else, have user choose robots
    if options["env_configuration"] == "bimanual":
        options["robots"] = "Baxter"
    else:
        options["robots"] = []

        # Have user choose two robots
        print("A multiple single-arm configuration was chosen.\n")

        for i in range(2):
            print("Please choose Robot {}...\n".format(i))
            options["robots"].append(choose_robots(exclude_bimanual=True))

# Else, we simply choose a single (single-armed) robot to instantiate in the environment
else:
    options["robots"] = choose_robots(exclude_bimanual=True)

# Hacky way to grab joint dimension for now
joint_dim = 6 if options["robots"] == "UR5e" else 7
controller_name = choose_controller()
options["controller_configs"] = suite.load_controller_config(default_controller=controller_name)
# Define variables for each controller test
controller_settings = {
        "OSC_POSE": [6, 6, 0.1],
        "OSC_POSITION": [3, 3, 0.1],
        "IK_POSE": [6, 6, 0.01],
        "JOINT_POSITION": [joint_dim, joint_dim, 0.2],
        "JOINT_VELOCITY": [joint_dim, joint_dim, -0.1],
        "JOINT_TORQUE": [joint_dim, joint_dim, 0.25],
    }
action_dim = controller_settings[controller_name][0]
num_test_steps = controller_settings[controller_name][1]
test_value = controller_settings[controller_name][2]

# Define the number of timesteps to use per controller action as well as timesteps in between actions
steps_per_action = 75
steps_per_rest = 75
env = make(
    **options,
    has_renderer=True,
    has_offscreen_renderer=False,
    ignore_done=True,
    use_camera_obs=False,
    horizon=(steps_per_action + steps_per_rest) * num_test_steps,
    control_freq=20,
)
'''env = make(
    "UR5e",                  # Robot type
    "PickPlace",               # Environment type
    controller_config=controller_config,
    has_renderer=True,         # Enable graphical visualization
    ignore_done=True           # Continue the episode even if task is completed
)'''
env.reset()
env.viewer.set_camera(camera_id=0)

# Reset the environment
env.reset()
import pdb
pdb.set_trace()
# Get the initial robot joint positions
#initial_joint_positions = env._joint_positions

# Specify the desired end effector position and orientation
target_position = [0.2, 0.3, 0.4]  # [x, y, z] coordinates
target_orientation = [1, 0, 0, 0]  # Quaternion [w, x, y, z]

# Move the end effector to the target position
for _ in range(100):
    # Compute the robot's action based on desired position and orientation
    action = controller_config["position"]["kp"] * (target_position - env._eef_xpos) - \
             controller_config["position"]["kv"] * env._eef_xvel

    # Perform the action in the environment
    obs, reward, done, _ = env.step(action)

    # Check if the target position has been reached
    if abs(env._eef_xpos - target_position).max() < 0.01:
        break
    env.render()

# Print the final joint positions
final_joint_positions = env._joint_positions
#print("Initial Joint Positions:", initial_joint_positions)
print("Final Joint Positions:", final_joint_positions)

# Close the environment
env.close()
