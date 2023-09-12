from robosuite.models import MujocoWorldBase
from robosuite.models.robots import UR5e
from robosuite.models.grippers import gripper_factory
from robosuite.models.arenas import EETable
from robosuite.models.mounts import mount_factory
from robosuite.models.objects import BallObject
from robosuite.utils.mjcf_utils import new_joint
from mujoco_py import MjSim, MjViewer
from robosuite.models.arenas import TableArena

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
    obj_type="visual",
    joints=None,
    rgba=[0, 0.5, 0.5, 1]).get_obj()
sphere.set('pos', '2.5 0.1 1.0')
world.worldbody.append(sphere)


# ################## Build MuJoCo Model ###############

model = world.get_model(mode="mujoco_py")

sim = MjSim(model)
viewer = MjViewer(sim)
viewer.vopt.geomgroup[0] = 0 # disable visualization of collision mesh


# ################### Start Main ######################
print("loop 1 start")
for i in range(10000):
  sim.data.ctrl[:] = 0
  o = sim.step()
  viewer.render()

print("loop 2 start")
sphere.set('pos', '2.5 0.5 1.0')
sim.reset()
for i in range(10000):
  sim.data.ctrl[:] = 0
  o = sim.step()
  viewer.render()


