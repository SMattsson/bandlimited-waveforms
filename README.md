

# Bandlimited waveforms for Teensy audio library

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [TODO](#todo)
* [Status](#status)

## General info
This is an open source tool developed in Python that can generate lookup tables to be used with the
Teensy Audio Library. The tool generates header files that can be included in your project to play
the standard waveforms bandlimited (without harmonic frequencies above 22.05kHz).

Using these will result in a clearer tone with less distortion, but at the cost of higher flash usage.
Try out the test code compareWaveform.ino found in the examples folder for a comparison between
bandlimited and non-bandlimited square waves.

If you just want the header files that you can include in your project, get them from the generated_headers folder.

## Setup
To run this script you'll need to have Python 3.x installed.
For usage see the code examples below or run the script with the command python3 `python3 blwftal --help`

## Code Examples
To generate a lookup table for a square wave execute:
`python3 blwftal --square`
It will generate a header file square_table.h that you can include in your Teensy audio library project
who utilizes about 65k of flash

To make a lookup table that uses less flash execute:
`python3 blwftal --square --compact`
This will make a header that utilizes half the flash space of the previous one, about 32k.

Take a look in the examples folder for example how to implement with the Teensy Audio Library.

## TODO
* Add other basic waveforms other than square and saw wave
* Add an example on how to use a lookup table with the --compact option
* Add an example on how to make a pulse wave with a variable duty cycle
* Add more generated headers that are ready for use
* Add sound examples.

## Status
Project is: _in progress_
