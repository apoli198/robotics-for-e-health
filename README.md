# Robotics for e-Health

ROS and Python application for the NAO humanoid robot, designed to conduct an interactive sound-reproduction exercise with children.

## Overview

This project implements an interactive activity in which the NAO robot asks a child to reproduce the sound or onomatopoeia associated with a sequence of animals and objects.

The application was conceived as an experimental robotic interaction for the assessment of abilities relevant to autism-oriented clinical tests, including interaction, attention, imitation and sound reproduction.

NAO introduces the activity, pronounces the name and sound of each item, listens to the child's response and uses an external sound-recognition component to verify whether the reproduced sound is correct.

This repository contains the ROS package responsible for:

- controlling the activity workflow;
- interacting with NAO through NAOqi;
- providing text-to-speech and audio playback services;
- triggering sound recognition;
- collecting recognition results;
- managing successful responses, errors and activity termination.

## Purpose

The project investigates the use of a humanoid robot as an interactive interface for exercises involving children.

NAO was selected because its humanoid appearance, limited facial expressiveness and small size can provide a more predictable and less intimidating interaction than a human examiner in some experimental settings.

The software is an academic prototype and is not a validated diagnostic or medical device.

## Activity Workflow

The default activity includes five items:

1. Cow
2. Sheep
3. Car
4. Train
5. Dog

For each item:

1. The operator places or presents the corresponding object.
2. The operator presses Enter to start the step.
3. NAO pronounces the object's name.
4. NAO reproduces its associated sound through text-to-speech.
5. The sound-recognition system starts listening.
6. The child has approximately five seconds to respond.
7. The application waits for recognition processing.
8. The recognized labels are compared with the expected label.

When the answer is correct:

- NAO says `Bravo!`;
- the activity continues with the next item.

When the answer is incorrect or absent:

- the global error counter is increased;
- NAO reports that the response was incorrect;
- the same item is proposed again.

The activity terminates:

- successfully when all items are completed;
- unsuccessfully when three errors have been recorded.

## Default Activity Configuration

The sequence is configured through three parallel text files:

```text
medrob_ws/src/project/names.txt
medrob_ws/src/project/sounds.txt
medrob_ws/src/project/labels.txt
```

### `names.txt`

Contains the Italian names pronounced by NAO:

```text
Mucca
Pecora
Macchina
Treno
Cane
```

### `sounds.txt`

Contains the onomatopoeias pronounced by NAO:

```text
mùùùùùù
bèèèèèè
bruuum bruuum
ciùùùf ciùùùf
bau bau
```

### `labels.txt`

Contains the labels returned by the sound-recognition system:

```text
cow
sheep
car
train
dog
```

The three files must contain the same number of lines and preserve the same ordering.

Additional objects can be added by extending all three files and providing the corresponding recognition classes and training samples in the external sound-recognition package.

## Architecture

The application follows a modular ROS architecture based on nodes, services, publishers and subscribers.

```text
Main application
    |
    +-- Text2SpeechClient
    |       |
    |       +-- ROS service: /tts
    |               |
    |               +-- Text2SpeechNode
    |                       |
    |                       +-- NAOqi ALTextToSpeech
    |
    +-- SoundRecognitionClient
            |
            +-- publishes: /soundrec_trig
            +-- subscribes: /soundrec
                    |
                    +-- external sound-recognition package
```

An additional audio-player service is included for playing audio files through NAO.

## Main Components

### Activity Controller

```text
medrob_ws/src/project/scripts/application.py
```

Controls:

- introductory instructions;
- sequence progression;
- manual operator confirmation;
- response timing;
- recognition-result validation;
- error counting;
- final outcome.

### Sound Recognition Client

```text
medrob_ws/src/project/scripts/sound_recognition_client.py
```

The client:

- publishes a start trigger on `soundrec_trig`;
- subscribes to recognition results on `soundrec`;
- stores the labels received during the current attempt.

The classifier and sound-recognition nodes are external components and are not included in this repository.

### Text-to-Speech Client and Node

```text
medrob_ws/src/project/scripts/text2speech_client.py
medrob_ws/src/project/src/text2speech_node.py
```

The client calls the custom `Text2Speech` ROS service.

The node connects to NAO through the NAOqi `ALTextToSpeech` proxy and instructs the robot to pronounce the requested sentence.

### Audio Player Client and Node

```text
medrob_ws/src/project/scripts/audioplayer_client.py
medrob_ws/src/project/src/audioplayer_node.py
```

These components expose an audio-playback service based on the NAOqi `ALAudioPlayer` proxy.

The main activity currently relies primarily on text-to-speech, but the audio-player module is available for file-based playback.

### ROS Launch File

```text
medrob_ws/src/project/launch/project.launch
```

The launch file starts:

- the text-to-speech node;
- the audio-player node;
- the NAO microphone node;
- the external voice-activity-detection node;
- the external sound-recognition node.

### Custom Services

```text
medrob_ws/src/project/srv/Text2Speech.srv
medrob_ws/src/project/srv/AudioPlayer.srv
```

These service definitions are generated during the Catkin build process.

## Repository Structure

```text
robotics-for-e-health/
├── docs/
│   └── project-report.pdf
├── medrob_ws/
│   └── src/
│       └── project/
│           ├── launch/
│           │   └── project.launch
│           ├── scripts/
│           │   ├── application.py
│           │   ├── application_bak.py
│           │   ├── audioplayer_client.py
│           │   ├── sound_recognition_client.py
│           │   └── text2speech_client.py
│           ├── src/
│           │   ├── audioplayer_node.py
│           │   └── text2speech_node.py
│           ├── srv/
│           │   ├── AudioPlayer.srv
│           │   └── Text2Speech.srv
│           ├── CMakeLists.txt
│           ├── package.xml
│           ├── names.txt
│           ├── sounds.txt
│           └── labels.txt
├── .gitignore
└── README.md
```

## Technologies

- Python
- ROS 1
- Catkin
- NAO robot
- NAOqi Python SDK
- `rospy`
- ROS topics
- ROS services
- Text-to-Speech
- Audio playback
- Sound recognition
- Voice activity detection

## Requirements

The project was developed for an older ROS 1 and NAO environment.

The following components are required:

- Linux environment compatible with ROS 1
- Catkin workspace
- Python 2-compatible ROS installation
- NAO robot
- NAOqi Python SDK
- `nao_nodes` ROS package
- external `sound_recognition` ROS package
- network access to the robot
- trained sound-recognition classes and samples

The repository does not include:

- NAOqi;
- `nao_nodes`;
- the sound-recognition classifier package;
- the trained recognition samples;
- the physical NAO robot environment.

## Installation

Clone the repository:

```bash
git clone https://github.com/apoli198/robotics-for-e-health.git
cd robotics-for-e-health/medrob_ws
```

Add the required external packages to the workspace or make sure they are available in the active ROS environment.

Build the workspace:

```bash
catkin_make
```

Load the generated environment:

```bash
source devel/setup.bash
```

Ensure that the Python nodes and scripts are executable:

```bash
chmod +x src/project/scripts/*.py
chmod +x src/project/src/*.py
```

## Configuration

### Robot Address

The default launch configuration uses:

```text
NAO IP:   10.0.1.236
NAO port: 9559
```

The values can be overridden through environment variables:

```bash
export NAO_IP=192.168.1.100
export NAO_PORT=9559
```

### Dataset File Paths

The current `application.py` contains absolute paths referring to the original development environment:

```text
/home/mivia/Desktop/medrob_ws/src/project/names.txt
/home/mivia/Desktop/medrob_ws/src/project/sounds.txt
/home/mivia/Desktop/medrob_ws/src/project/labels.txt
```

These paths must be replaced before running the application on another machine.

For example, they can be changed to the absolute path of the cloned workspace, or the script can be modified to resolve files relative to its own directory.

## Running the Application

### 1. Start the ROS Master

```bash
roscore
```

### 2. Launch the NAO and Recognition Nodes

In another terminal:

```bash
cd robotics-for-e-health/medrob_ws
source devel/setup.bash
roslaunch project project.launch
```

### 3. Start the Activity

In a third terminal:

```bash
cd robotics-for-e-health/medrob_ws
source devel/setup.bash
rosrun project application.py
```

When requested by the terminal:

1. place or present the required object;
2. press Enter;
3. allow NAO to pronounce the name and sound;
4. let the child reproduce the sound;
5. wait for the recognition result.

## Testing

The original project was evaluated through manually simulated sessions.

The test scenarios included:

- successful sessions without errors;
- successful sessions with one or two errors;
- failed sessions reaching three errors;
- incorrect sounds;
- missing responses;
- unknown sounds.

The original experiments indicated that increasing the number of sound samples per class improved recognition reliability.

An additional `unknown` class was introduced in the sound-recognition system to reduce false positives for sounds that did not belong to any expected object or animal.

The detailed experimental results are available in:

```text
docs/project-report.pdf
```

## Known Limitations

- The project depends on a ROS 1 and Python 2 software stack.
- `application.py` uses `raw_input()`, which is not compatible with Python 3 without modification.
- Dataset paths are hardcoded to the original development machine.
- The default robot IP address is specific to the original laboratory network.
- The sound-recognition package, classifier and training samples are not included.
- `nao_nodes` and the NAOqi SDK must be installed separately.
- The application requires manual keyboard input before the activity and before each object.
- The response timeout and recognition-processing delay are fixed in the source code.
- The number of permitted errors is fixed at three.
- The sequence is not randomized.
- The application does not store a structured clinical report or patient record.
- There is no automated test suite.
- `application_bak.py` is a legacy backup and should not be used as the main entry point.
- `package.xml` still contains placeholder maintainer and license information.
- The prototype has not been clinically validated and must not be used as a diagnostic system.

## Possible Improvements

- Replace absolute paths with ROS package-relative paths.
- Port the application to Python 3 and a more recent ROS environment.
- Move activity parameters to ROS parameters or a YAML configuration file.
- Add configurable timeout and error thresholds.
- Add sequence randomization.
- Store session results in a structured output file.
- Add automated unit and integration tests.
- Package the recognition model and document its training procedure.
- Replace manual keyboard confirmation with a graphical operator interface.
- Update the package metadata and add an explicit license.
- Support modern NAO or alternative social-robotics platforms.

## Contributors

This project was developed by:

- Americo Liguori
- Alessandro Poli
- Luigi Verolla

## Academic Context

The project was developed for the **Robotics for e-Health** course in the Master's Degree in **Information Engineering for Digital Medicine** at the University of Salerno during the 2022/2023 academic year.

The work covered:

- requirements analysis;
- robotic interaction design;
- ROS node and service development;
- NAOqi integration;
- sound-recognition integration;
- interaction testing;
- experimental result analysis.

## Disclaimer

This repository contains an academic research prototype.

It is not a certified medical device, has not undergone clinical validation and must not be used for diagnosis or clinical decision-making.
