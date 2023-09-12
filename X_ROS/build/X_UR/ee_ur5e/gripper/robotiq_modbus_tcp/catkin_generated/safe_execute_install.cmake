execute_process(COMMAND "/home/prakash/CosMic_RAYs_X-main/X_ROS/build/X_UR/ee_ur5e/gripper/robotiq_modbus_tcp/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/prakash/CosMic_RAYs_X-main/X_ROS/build/X_UR/ee_ur5e/gripper/robotiq_modbus_tcp/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
