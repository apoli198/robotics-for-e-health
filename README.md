# Robotics for e-Health

ROS/Python application developed for the NAO robot to support an interactive sound-recognition test for children.

## Contents

- `medrob_ws/` — ROS workspace containing the application package, nodes, launch files and service definitions.
- `docs/project-report.pdf` — original academic project report.

## Main components

- Interactive test workflow implemented in Python.
- Text-to-speech and audio playback services.
- Sound-recognition client integration.
- ROS launch and package configuration for the NAO-based application.

## Requirements

The project was developed for a ROS environment with access to the NAO robot and the related communication stack. Hardware-specific dependencies and services may be required and are not included in this repository.

## Known limitations

The project depends on the original ROS/NAO execution environment. Paths, robot addresses and external recognition services may need to be configured before execution.

## Academic context

University group project for the Robotics for e-Health course.
