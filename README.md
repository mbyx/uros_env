# uros_env
A Dockerfile and environment for running ROS2 and MicroROS, with all tools available.

### Running
Run the following to start the build (only builds first run) and then run the docker image:
```
$ ./run.sh
```
If you want to open multiple terminals within the same container, open a new terminal, then run:
```
$ ./run_alt.sh
```
When the container opens, all the contents of uros2_ws will be available inside the container.
To run MicroROS, if connected via UART/Serial, run:
```
$ ./run_agent_serial.sh /dev/ttyUSB0
```
