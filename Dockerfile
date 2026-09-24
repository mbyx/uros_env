FROM osrf/ros:humble-desktop-full

RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    python3-colcon-common-extensions \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/uros_ws

RUN git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup \
    && apt-get update \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -y \
    && . /opt/ros/humble/setup.sh \
    # Build everything
    && colcon build \
    && . install/local_setup.sh \
    && ros2 run micro_ros_setup create_agent_ws.sh \
    && ros2 run micro_ros_setup build_agent.sh \
    # Clean up intermediate source files to keep the image small, leaving 'install/' intact
    && rm -rf build/ log/ src/ \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc \
    && echo "source /root/uros_ws/install/local_setup.bash" >> /root/.bashrc
    
WORKDIR /root/workspace
