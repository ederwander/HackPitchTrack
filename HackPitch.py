#Crazy F0 return
#Eng Eder de Souza - ederwander
from struct import pack
import wave
import numpy as np
import math
import pyaudio
import sys


#Here are all the math equations described in patent
def GetPitch(frame, maxP, minP):
    minimum=np.Inf
    periodo = -1
    for pos in range(minP, maxP):
        nolag=frame[0:(maxP*2)-pos]
        onelag=frame[pos:maxP*2]
        twolag=frame[np.round(np.arange(pos*2, (maxP*2)*2, 2))]
        H=np.sum((nolag * onelag)-(onelag * twolag))
        E=np.sum((nolag**2)-(twolag**2))
        V=E-(2.0*H)
        if V<minimum and V <= (np.finfo(np.float32).eps * E):
            minimum=V
            periodo=pos;
    return periodo;


#its is just for fun ;)
def BuildSine(F, phase):
    phaseInc = 2.0*np.pi*F/Fs;
    signal2=[]
    for i in range(0, frameSize):
        signal2.append(np.sin(phase))
        phase = phase + phaseInc;
    #place the phaser between the 0 and 2pi range
    phase = np.mod(phase, 2.0*np.pi);
    return signal2, phase



spf = wave.open('teste.wav','r');


# If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

Fs = spf.getframerate();
signal = spf.readframes(-1);

intsignal = np.frombuffer(signal, dtype=np.int16)
floatsignal  = np.float32(intsignal) / (1<<15)


# Initialize PyAudio
pyaud = pyaudio.PyAudio()


# Open stream
stream = pyaud.open(format =  pyaudio.paFloat32,
               channels = spf.getnchannels(),
               rate = spf.getframerate(),
               output = True)


phase=0.0;
signal2=[];
frameSize=1<<12;
minF = 50
maxF = 900
     
minP = int(Fs/maxF);
maxP = int(Fs/minF);


if frameSize < maxP:
	frameSize = maxP

lastP0=Fs/minF

hiSine=[]

print("Collecting Pitch and build a Sine Melody...")

for i in range(0, len(floatsignal), frameSize):

    if i+frameSize > len(floatsignal):
        break

    chunk = (floatsignal[i:i+frameSize])
    P0=GetPitch(chunk, maxP, minP)
    if Fs/P0 > maxF:
        P0=lastP0
    hi, phase=BuildSine((Fs/P0), phase)
    hiSine=np.concatenate([hiSine, hi])
    

    '''
    #I tryed play inside this loop but I get clicks sometimes, than lets append all Sine Sounds to play later
    out = pack("%df"%len(hi), *(hi))
    stream.write(out)
    '''

    lastP0=P0;

print("Done ...")

print("Playing...")

out = pack("%df"%len(hiSine), *(hiSine))
stream.write(out)
