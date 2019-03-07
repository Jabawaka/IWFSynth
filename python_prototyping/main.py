from PMSynth import signals as sg
import numpy as np


pureToneSig_A3 = sg.SinSignal(220, 1.0)
pureToneSig_A4 = sg.SinSignal(440, 1.0)
pureToneSig_A4 = sg.SinSignal(1440, 1.0)
modSig = pureToneSig_A3.modulate(pureToneSig_A4, 1.0)

lopass = sg.LowPassFilter(0.707, 1000)
chorus = sg.ChorusEffect( \
        [13, 17, 19, 23, 29, 31, 37], \
        [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7])

wave = pureToneSig_A3.make_wave(1.0, 0.0, 44100)
wave.applyEffect(chorus)

pureToneSig_A3.play(1.0)
wave.play()
