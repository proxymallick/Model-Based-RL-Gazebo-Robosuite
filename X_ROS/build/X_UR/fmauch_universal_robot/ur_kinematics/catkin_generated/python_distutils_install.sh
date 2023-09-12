#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/prakash/CosMic_RAYs_X-main/X_ROS/src/X_UR/fmauch_universal_robot/ur_kinematics"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/prakash/CosMic_RAYs_X-main/X_ROS/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/prakash/CosMic_RAYs_X-main/X_ROS/install/lib/python2.7/dist-packages:/home/prakash/CosMic_RAYs_X-main/X_ROS/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/prakash/CosMic_RAYs_X-main/X_ROS/build" \
    "/usr/bin/python2" \
    "/home/prakash/CosMic_RAYs_X-main/X_ROS/src/X_UR/fmauch_universal_robot/ur_kinematics/setup.py" \
     \
    build --build-base "/home/prakash/CosMic_RAYs_X-main/X_ROS/build/X_UR/fmauch_universal_robot/ur_kinematics" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/prakash/CosMic_RAYs_X-main/X_ROS/install" --install-scripts="/home/prakash/CosMic_RAYs_X-main/X_ROS/install/bin"
