/*
  https://github.com/SMattsson/bandlimited-waveforms/examples

  This program shows how to use a header file generated with the --compact option.
  The --compact option makes the lookup table half the size, 64 rows instead of 128 rows (There is 128 midi notes)

  You can uncomment the line at row 33 in this file to compare it with the built-in squarewave.

  To access the correct table in the table, you simply access the row equal to midinote / 2 instead of midinote.
  To see more describing syntax, see line 61 in this file.

  Headphones is recommened to critical lissening.
  You'll hear that the original has some distortion in it, and that's because of aliasing.
  You can read more about it here 
  https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem#Aliasing

  The lookup table from the square_table_compact.h uses 32768 bytes
*/

#include <Arduino.h>
#include <Audio.h>
#include "square_table_compact.h"

AudioOutputI2S          output;
AudioSynthWaveform      waveform;
AudioControlSGTL5000    sgtl5000_1;
AudioConnection         patchCord3(waveform, 0, output, 0);
AudioConnection         patchCord4(waveform, 0, output, 1);

void setup() {
  AudioMemory(20);
  waveform.begin(WAVEFORM_ARBITRARY);
  //waveform.begin(WAVEFORM_SQUARE); /*Uncomment this line to hear the built in squarewave instead */
  waveform.amplitude(0.3);
  sgtl5000_1.enable();    /* Comment/delete this line if you aren't using Teensy audio adapter */
  sgtl5000_1.volume(0.2); /* Comment/delete this line if you aren't using Teensy audio adapter */
}

int previousMillis;
int interval = 350;
int tones[] = {60,64,67,72,67,64,55,59,62,67,62,59};
int numberOfTones = sizeof(tones)/sizeof(int);
int currentNote = 0;
int pitchMod = 12;

void loop() {
    if (millis() - previousMillis > interval) {
        previousMillis = millis();
        setNote(tones[currentNote % numberOfTones] + pitchMod); /* Input must be between 0 and 127 */
        currentNote++;
    }
}

void setNote(int note) {
  AudioNoInterrupts();
  /* Convert midi note number to frequency. */
  float freq = pow(2.0, (note - 69.0) / 12.0) * 440.0;
  
  /* To use the bandlimited waveform correctly, index of the array in the squareTable
     must be the half the note number rounded down (here with just casting it into int) */
  waveform.arbitraryWaveform(squareTableCompact[int(note / 2)], 172);
  waveform.frequency(freq);
  AudioInterrupts();
}