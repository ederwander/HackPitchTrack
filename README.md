# HackPitchTrack

Therefore, I wrote this code as a proof of concept of the equations used in the Pitch Track of the original patent `US5973252 - Pitch Detection and Intonation Correction Aparatus and Method` (Antares -> Autotune method to extract pitch)

For basic monophonic sounds, it works a little well, but will need to check for errors with periods out of range (TO-DO)...

Yes, it is just a concept to prove that the original patent equations work, it is an autocorrelation variant, they certainly need to be improved, but it is obvious there are many secrets not revealed in the patent lol

OK, `Python` makes me nervous when I percieve how slow the loops are, so I needed to vectorize to gain speed and skip some loops, maybe the equations are not so easy to see in the coded file ...

# FUN

This code is purely python, the demo is just for fun, you will get all Pitch from one .wav file and build sines, for now just use mono and monophonic sounds inputs

The only dependency on the example file is the use of `numpy` and  `pyaudio` to play

Video that show its working https://youtu.be/fsPOWzNtaXQ, yeah you will see/listen that the Pitch Track fails some frequencies at the end lol, seems an old R2d2 ...

