from robosuite.models import MujocoWorldBase
from robosuite.models.robots import UR5e
from robosuite.models.grippers import gripper_factory
from robosuite.models.arenas import EETable
from robosuite.models.mounts import mount_factory
from robosuite.models.objects import BallObject
from robosuite.utils.mjcf_utils import new_joint
from mujoco_py import MjSim, MjViewer
from robosuite.models.arenas import TableArena

import robosuite as suite
from robosuite.controllers import load_controller_config
from robosuite.utils.input_utils import *
from robosuite.robots import Bimanual


world = MujocoWorldBase()
mujoco_robot = UR5e()

# ################# Gripper ######################

gripper = gripper_factory('Robotiq140Gripper')
mujoco_robot.add_gripper(gripper)


# ################# Mount ########################

# mount = mount_factory('RethinkMinimalMount')
mount = mount_factory('ELabMount')
mujoco_robot.add_mount(mount)

mujoco_robot.set_base_xpos([1.5, -0.9, 0])
world.merge(mujoco_robot)

# ################# Arena ########################

mujoco_arena = EETable()
mujoco_arena.set_origin([2, 0, 0])
world.merge(mujoco_arena)

# ################# Environement Task #################

sphere = BallObject(
    name="sphere",
    size=[0.04],
    rgba=[0, 0.5, 0.5, 1]).get_obj()
sphere.set('pos', '2.5 0.1 1.0')
world.worldbody.append(sphere)


# ################## Build MuJoCo Model ###############

model = world.get_model(mode="mujoco_py")

sim = MjSim(model)
viewer = MjViewer(sim)
viewer.vopt.geomgroup[0] = 0 # disable visualization of collision mesh


# ################### Start Main ######################

for i in range(10000):
  sim.data.ctrl[:] = 0
  sim.step()
  viewer.render()






if __name__ == "__main__":

    # Create dict to hold options that will be passed to env creation call
    options = {}


    # Choose environment and add it to options
    options["env_name"] = choose_environment()

    # If a multi-arm environment has been chosen, choose configuration and appropriate robot(s)
    if "TwoArm" in options["env_name"]:
        # Choose env config and add it to options
        options["env_configuration"] = choose_multi_arm_config()

        # If chosen configuration was bimanual, the corresponding robot must be Baxter. Else, have user choose robots
        if options["env_configuration"] == 'bimanual':
            options["robots"] = 'Baxter'
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

    # Choose controller
    controller_name = choose_controller()

    # Load the desired controller
    options["controller_configs"] = suite.load_controller_config(default_controller=controller_name)

    # Define the pre-defined controller actions to use (action_dim, num_test_steps, test_value)
    controller_settings = {
        "OSC_POSE":         [6, 6, 0.1],
        "OSC_POSITION":     [3, 3, 0.1],
        "IK_POSE":          [6, 6, 0.01],
        "JOINT_POSITION":   [joint_dim, joint_dim, 0.2],
        "JOINT_VELOCITY":   [joint_dim, joint_dim, 1],
        "JOINT_TORQUE":     [joint_dim, joint_dim, 0.25]
    }

    # Define variables for each controller test
    action_dim = controller_settings[controller_name][0]
    num_test_steps = controller_settings[controller_name][1]
    test_value = controller_settings[controller_name][2]

    # Define the number of timesteps to use per controller action as well as timesteps in between actions
    steps_per_action = 75
    steps_per_rest = 75

    # Help message to user
    print()
    print("Press \"H\" to show the viewer control panel.")

    # initialize the task
    env = suite.make(
        **options,
        has_renderer=True,
        has_offscreen_renderer=False,
        ignore_done=True,
        use_camera_obs=False,
        horizon=(steps_per_action + steps_per_rest) * num_test_steps,
        control_freq=20,
    )
    
    env.reset()
    env.viewer.set_camera(camera_id=0)

    # To accommodate for multi-arm settings (e.g.: Baxter), we need to make sure to fill any extra action space
    # Get total number of arms being controlled
    n = 0
    gripper_dim = 0
    for robot in env.robots:
        print(robot)
        gripper_dim = robot.gripper["right"].dof if isinstance(robot, Bimanual) else robot.gripper.dof
        n += int(robot.action_dim / (action_dim + gripper_dim))

    # Define neutral value
    neutral = np.zeros(action_dim + gripper_dim)

    # Keep track of done variable to know when to break loop
    count = 0
    # Loop through controller space
    while count < num_test_steps:
        action = neutral.copy()
        for i in range(steps_per_action):
            if controller_name in {'IK_POSE', 'OSC_POSE'} and count > 2:
                # Set this value to be the scaled axis angle vector
                vec = np.zeros(3)
                vec[count - 3] = test_value
                action[3:6] = vec
            else:
                action[count] = test_value
            total_action = np.tile(action, n)
            env.step(total_action)
            env.render()
        for i in range(steps_per_rest):
            total_action = np.tile(neutral, n)
            env.step(total_action)
            env.render()
        count += 1

    # Shut down this env before starting the next test
    env.close()
