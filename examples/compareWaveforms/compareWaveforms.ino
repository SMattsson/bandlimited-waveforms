/*
  From repo:
  https://github.com/SMattsson/bandlimited-waveforms/examples

  This program compares the built in squarewave and a bandlimited lookup table
  in the AudioSynthWaveform object in the Teensy Audio Library

  Headphones is recommended for critical listening.
  You'll hear that the original has some distortion in it. That's because of aliasing.
  You can read more about it here: 
  https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem#Aliasing

  The lookup table from the square_table.h uses 65536 bytes
*/

#include <Arduino.h>
#include <Audio.h>
#include "square_table.h"
#define A4 69
AudioOutputI2S          output;
AudioSynthWaveform      waveform_bandlimited;
AudioSynthWaveform      waveform;
AudioMixer4             mixer1;
AudioControlSGTL5000    sgtl5000_1;

AudioConnection         patchCord1(waveform, 0, mixer1, 0);
AudioConnection         patchCord2(waveform, 0, mixer1, 1);
AudioConnection         patchCord3(waveform_bandlimited, 0, mixer1, 2);
AudioConnection         patchCord4(waveform_bandlimited, 0, mixer1, 3);
AudioConnection         patchCord5(mixer1, 0, output, 0);
AudioConnection         patchCord6(mixer1, 0, output, 1);

void setup() {
  AudioMemory(20);
  Serial.begin(9600);
  
  /* Mute all channels in the mixer */
  for (unsigned int i = 0; i < 4; i++) {
    mixer1.gain(i, 0.0);
  }
  
  waveform.begin(WAVEFORM_SQUARE);
  waveform.amplitude(0.3);
  
  waveform_bandlimited.begin(WAVEFORM_ARBITRARY);
  waveform_bandlimited.amplitude(0.3);

  sgtl5000_1.enable();    /* Comment/delete this line if you aren't using Teensy audio adapter */
  sgtl5000_1.volume(0.2); /* Comment/delete this line if you aren't using Teensy audio adapter */
}

void loop() {
  for (int note = A4; note < 90; note += 5) {
    playOriginalSquare();
    delay(800);
    playBandlimitedSquare();
    delay(800);
    setNote(note);
  }
}

void playOriginalSquare() {
  /* Mute the bandlimited and unmute the original */
  mixer1.gain(0, 1.0);
  mixer1.gain(1, 1.0);
  mixer1.gain(2, 0.0);
  mixer1.gain(3, 0.0);
  Serial.println("Original square waveform playing");
}

void playBandlimitedSquare() {
  /* Mute the original and unmute the bandlimited */
  mixer1.gain(0, 0.0);
  mixer1.gain(1, 0.0);
  mixer1.gain(2, 1.0);
  mixer1.gain(3, 1.0);
  Serial.println("Bandlimited square waveform playing");
}

void setNote(int note) {
  AudioNoInterrupts();
  /* Convert midi note number to frequency. */
  float freq = pow(2.0, (note - 69.0) / 12.0) * 440.0;
  
  /* To use the bandlimited waveform correctly, index of the array in the squareTable
     must be the same as the note number */
  waveform_bandlimited.arbitraryWaveform(squareTable[note], 172);
  waveform_bandlimited.frequency(freq);
  
  /* With the built in waveform, only frequency is needed */ 
  waveform.frequency(freq);
  AudioInterrupts();
}