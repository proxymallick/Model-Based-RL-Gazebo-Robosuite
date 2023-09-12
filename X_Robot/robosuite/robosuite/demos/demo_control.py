"""
This demo script demonstrates the various functionalities of each controller available within robosuite.

For a given controller, runs through each dimension and executes a perturbation "test_value" from its
neutral (stationary) value for a certain amount of time "steps_per_action", and then returns to all neutral values
for time "steps_per_rest" before proceeding with the next action dim.

    E.g.: Given that the expected action space of the Pos / Ori (OSC_POSE) controller (without a gripper) is
    (dx, dy, dz, droll, dpitch, dyaw), the testing sequence of actions over time will be:

        ***START OF DEMO***
        ( dx,  0,  0,  0,  0,  0, grip)     <-- Translation in x-direction      for 'steps_per_action' steps
        (  0,  0,  0,  0,  0,  0, grip)     <-- No movement (pause)             for 'steps_per_rest' steps
        (  0, dy,  0,  0,  0,  0, grip)     <-- Translation in y-direction      for 'steps_per_action' steps
        (  0,  0,  0,  0,  0,  0, grip)     <-- No movement (pause)             for 'steps_per_rest' steps
        (  0,  0, dz,  0,  0,  0, grip)     <-- Translation in z-direction      for 'steps_per_action' steps
        (  0,  0,  0,  0,  0,  0, grip)     <-- No movement (pause)             for 'steps_per_rest' steps
        (  0,  0,  0, dr,  0,  0, grip)     <-- Rotation in roll (x) axis       for 'steps_per_action' steps
        (  0,  0,  0,  0,  0,  0, grip)     <-- No movement (pause)             for 'steps_per_rest' steps
        (  0,  0,  0,  0, dp,  0, grip)     <-- Rotation in pitch (y) axis      for 'steps_per_action' steps
        (  0,  0,  0,  0,  0,  0, grip)     <-- No movement (pause)             for 'steps_per_rest' steps
        (  0,  0,  0,  0,  0, dy, grip)     <-- Rotation in yaw (z) axis        for 'steps_per_action' steps
        (  0,  0,  0,  0,  0,  0, grip)     <-- No movement (pause)             for 'steps_per_rest' steps
        ***END OF DEMO***

    Thus the OSC_POSE controller should be expected to sequentially move linearly in the x direction first,
        then the y direction, then the z direction, and then begin sequentially rotating about its x-axis,
        then y-axis, then z-axis.

Please reference the documentation of Controllers in the Modules section for an overview of each controller.
Controllers are expected to behave in a generally controlled manner, according to their control space. The expected
sequential qualitative behavior during the test is described below for each controller:

* OSC_POSE: Gripper moves sequentially and linearly in x, y, z direction, then sequentially rotates in x-axis, y-axis,
            z-axis, relative to the global coordinate frame
* OSC_POSITION: Gripper moves sequentially and linearly in x, y, z direction, relative to the global coordinate frame
* IK_POSE: Gripper moves sequentially and linearly in x, y, z direction, then sequentially rotates in x-axis, y-axis,
            z-axis, relative to the local robot end effector frame
* JOINT_POSITION: Robot Joints move sequentially in a controlled fashion
* JOINT_VELOCITY: Robot Joints move sequentially in a controlled fashion
* JOINT_TORQUE: Unlike other controllers, joint torque controller is expected to act rather lethargic, as the
            "controller" is really just a wrapper for direct torque control of the mujoco actuators. Therefore, a
            "neutral" value of 0 torque will not guarantee a stable robot when it has non-zero velocity!

"""

import robosuite as suite
from robosuite.controllers import load_controller_config
from robosuite.robots import Bimanual
from robosuite.utils.input_utils import *

if __name__ == "__main__":

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

    # Choose controller
    controller_name = choose_controller()

    # Load the desired controller
    options["controller_configs"] = suite.load_controller_config(default_controller=controller_name)

    # Define the pre-defined controller actions to use (action_dim, num_test_steps, test_value)
    controller_settings = {
        "OSC_POSE": [6, 6, 0.1],
        "OSC_POSITION": [3, 3, 0.1],
        "IK_POSE": [6, 6, 0.01],
        "JOINT_POSITION": [joint_dim, joint_dim, 0.2],
        "JOINT_VELOCITY": [joint_dim, joint_dim, -0.1],
        "JOINT_TORQUE": [joint_dim, joint_dim, 0.25],
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
    print('Press "H" to show the viewer control panel.')

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
        gripper_dim = robot.gripper["right"].dof if isinstance(robot, Bimanual) else robot.gripper.dof
        n += int(robot.action_dim / (action_dim + gripper_dim))

    # Define neutral value
    neutral = np.zeros(action_dim + gripper_dim)

    # Keep track of done variable to know when to break loop
    count = 0
    import torch
    # Set the device to CPU
    device = torch.device("cpu")
    act=[torch.Tensor([ 0.0056,  0.0088,  0.0041, -0.0196,  0.0318,  0.0571, -0.0213], device=device), 
        torch.Tensor([ 0.0072,  0.0174,  0.0155, -0.0142,  0.0314,  0.0644, -0.0250], device=device), 
        torch.Tensor([ 0.0105,  0.0098,  0.0013, -0.0352,  0.0362,  0.0726, -0.0136], device=device), 
        torch.Tensor([-0.0859,  0.9599, -0.1526,  0.7142, -0.7654, -0.4575, -0.1924],device=device),
        torch.Tensor([ 0.9379,  0.8099, -0.4069,  0.9840, -0.5012, -0.7882,  0.9019],device=device), 
        torch.Tensor([ 0.0222, -0.0113,  0.0070, -0.0278,  0.0469,  0.0983, -0.0294],device=device), 
        torch.Tensor([-0.6993,  0.1166, -0.1432,  0.8463, -0.7898,  0.9651,  0.7509],device=device), 
        torch.Tensor([ 0.8086, -0.1013, -0.6988,  0.1877,  0.0752, -0.6032,  0.2061],device=device), 
        torch.Tensor([-0.4980, -0.8692, -0.1736,  0.1549, -0.0070, -0.6744, -0.2569],device=device),
        torch.Tensor([-0.7246,  0.2981,  0.7121, -0.8136,  0.5074,  0.3804,  0.7333],device=device), 
        torch.Tensor([-0.0044,  0.0087,  0.0068,  0.0011,  0.0439,  0.0870, -0.0187],device=device), 
        torch.Tensor([ 0.8305, -0.6940,  0.9806, -0.8814, -0.8822,  0.6465,  0.5532],device=device), 
        torch.Tensor([ 0.0135, -0.0154,  0.0162, -0.0319,  0.0514,  0.0762, -0.0252],device=device), 
        torch.Tensor([ 0.0095,  0.0081,  0.0254, -0.0023,  0.0521,  0.0687, -0.0063], device=device), 
        torch.Tensor([ 0.0149, -0.0034, -0.0068, -0.0371,  0.0315,  0.0860, -0.0123], device=device), 
        torch.Tensor([ 0.0245, -0.0133,  0.0085, -0.0075,  0.0582,  0.0831, -0.0191],device=device), 
        torch.Tensor([ 0.1396, -0.0016,  0.2254,  0.4455,  0.3278,  0.5242, -0.7074],device=device), 
        torch.Tensor([-0.1422, -0.1287, -0.7492, -0.6580,  0.8380, -0.0847, -0.0551],device=device), 
        torch.Tensor([-0.0010,  0.0225,  0.0193, -0.0460,  0.0465,  0.0715, -0.0418],device=device), 
        torch.Tensor([ 0.0283, -0.0028,  0.0214, -0.0092,  0.0324,  0.0658, -0.0111],device=device) ]
        # Loop through controller space
    while count < num_test_steps:
        import pdb
        '''for i in range(steps_per_rest):
            pdb.set_trace()
            env.step(act[i])
            env.render()'''
        action = neutral.copy()
        for i in range(steps_per_action):
            if controller_name in {"IK_POSE", "OSC_POSE"} and count > 2:
                # Set this value to be the scaled axis angle vector
                vec = np.zeros(3)
                vec[count - 3] = test_value
                
                action[3:6] = vec
            else:
                action[count] = test_value
            
            
            total_action = np.tile(action, n)
            pdb.set_trace()
            env.step(np.array(act[i]))
            env.render()
        '''for i in range(steps_per_rest):
            total_action = np.tile(neutral, n)
            env.step(total_action)
            env.render()'''
        count += 1

    # Shut down this env before starting the next test
    env.close()
