# RTSIMU: Real-Time Simulation tool for IMU sensors


## Software Description

This software allows the analysis of upper body movements using Inertial Measurement Units (IMUs). The software converts the raw data from the IMUs into quaternions, a unique measure of orientation relative to the Earth, and then into angles of movement. A biomechanical model of the upper body was created to simulate movement and calculate relevant angles, such as abduction, flexion, rotation, and elevation of both shoulders. The open-source tool OpenSim was used to visualize and evaluate the movements in real-time. The developed system provides a novel approach to analyzing worker movements and could help improve work safety and productivity.


## Getting started

This section explains how to use the software developed.

### Dependencies 

To run the software you need `python 3.8` and `Opensim 4.4`.

To install the required packages:

```python
pip install -r requirements.txt
```

### Run the software

Run the motion simulation software in real time:

```python
python rtsimu/main.py
```


## What's included

In this software, mainly two libraries are used for processing the inertial sensor data: Fusion from XioTechnologies (https://github.com/xioTechnologies/Fusion) and OpenSim from SimTK (https://simtk.org/home/opensim/). Fusion is a sensor fusion library for Inertial Measurement Units (IMUs) optimised for embedded systems and employ an Altitude and Heading Reference System (AHRS). The AHRS algorithm combines gyroscope, accelerometer, and magnetometer data collected from sensors into a single measurement of orientation relative to the Earth. The OpenSim is used to simulate and analyze movement in real-time through a musculoskeletal model of the upper body.

## Display of movements in real time

To visualize the upper body movements in real time just change in the file with the directory `rtsimu/config/opensim/config.yaml` the variable `visualize: True`.

## CodeOcean capsule

To check this software running you can access the codeocean capsule via: 

``` cmd
https://www.10.24433/CO.4852020.v1
```


## Authors

- Paula Dias EPMQ, CCG ZGDV Institute, Guimarães, Portugal<br/>
- Arthur Matta EPMQ, CCG ZGDV Institute, Guimarães, Portugal<br/>
- André Pilastri EPMQ, CCG ZGDV Institute, Guimarães, Portugal<br/>
- Luís Miguel Matos ALGORITMI/LASI, Dep. Information Systems, University of Minho, Guimarães,Portugal <br/>
- Paulo Cortez ALGORITMI/LASI, Dep. Information Systems, University of Minho, Guimarães, Portugal <br/>


## Copyright and license

Distributed under the MIT License. See `LICENSE` for more information.


## Suggestions and feedback

Any feedback will be appreciated.
For questions and other suggestions contact paulacdias2000@gmail.com <br/>
Found any bugs? Post Them on the GitHub page of the project!