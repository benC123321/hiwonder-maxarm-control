# hiwonder-maxarm-control
This repository provides tools to control the hiwonder maxarm 4dof robot arm from a linux SBC.

This provides tools to compile a runtime executable that will run on:
    - Raspberry Pi 5

The executable exposes the following interfaces for commanding the arm:
    - gRPC (over wifi or ethernet)
