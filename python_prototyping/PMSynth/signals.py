import math
import array

import subprocess
import warnings

import numpy as np
import random
from wave import open as open_wave
from bokeh.plotting import figure, output_file, show

PI2 = 2 * math.pi

class WavFileWriter:
    """Writes wav files."""

    def __init__(self, filename='sound.wav', framerate=44100):
        """Opens the file and sets parameters.

        filename: string
        framerate: samples per second
        """
        self.filename = filename
        self.framerate = framerate
        self.nchannels = 1
        self.sampwidth = 2
        self.bits = self.sampwidth * 8
        self.bound = 2**(self.bits-1) - 1

        self.fmt = 'h'
        self.dtype = np.int16

        self.fp = open_wave(self.filename, 'w')
        self.fp.setnchannels(self.nchannels)
        self.fp.setsampwidth(self.sampwidth)
        self.fp.setframerate(self.framerate)

    def write(self, wave):
        """Writes a wave.

        wave: Wave
        """
        zs = wave.quantize(self.bound, self.dtype)
        self.fp.writeframes(zs.tostring())

    def close(self, duration=0):
        """Closes the file.

        duration: how many seconds of silence to append
        """
        if duration:
            self.write(rest(duration))

        self.fp.close()

class Signal():

    # Ability to add one signal to another
    def __add__(self, other):
        if other == 0:
            return self

        return SumSignal(self, other)

    def modulate(self, other, beta):
        if other == 0:
            return self

        return ModSignal(self, other, beta)

    def make_wave(self, dur_s = 1, start_s = 0, framerate = 44100):
        # Generate time vector
        nSamples = round(dur_s * framerate)
        ts_s = start_s + np.arange(nSamples) / framerate

        # Evaluate signal
        ys = self.evaluate(ts_s)

        # Return wave object
        return Wave(ys, ts_s, framerate = framerate)

    def play(self, dur_s = 1, framerate = 44100):
        wave = self.make_wave(dur_s, 0, framerate)
        wave.play()

class SinSignal(Signal):

    def __init__(self, freq_Hz = 440, amp = 1.0):
        self.freq_Hz = freq_Hz
        self.amp = amp
        self.func = np.sin

    def evaluate(self, ts_s, modulation = 0):
        ts_s = np.asarray(ts_s)
        phases = PI2 * self.freq_Hz * ts_s + modulation
        ys = self.amp * self.func(phases)

        return ys

class SquareSignal(Signal):

    def __init__(self, freq_Hz = 440, amp = 1.0):
        self.freq_Hz = freq_Hz
        self.amp = amp

    def evaluate(self, ts_s, modulation = 0):
        ts_s = np.asarray(ts_s)
        cycles = self.freq_Hz * ts_s + modulation
        frac, _ = np.modf(cycles)
        ys = self.amp * np.sign(unbias(frac))

        return ys

class TriangleSignal(Signal):

    def __init__(self, freq_Hz = 440, amp = 1.0):
        self.freq_Hz = freq_Hz
        self.amp = amp

    def evaluate(self, ts_s, modulation = 0):
        ts_s = np.asarray(ts_s)
        cycles = self.freq_Hz * ts_s + modulation
        frac, _ = np.modf(cycles)
        ys = np.abs(frac - 0.5)
        ys = normalize(unbias(ys), self.amp)

        return ys

class SumSignal(Signal):

    def __init__(self, *args):
        self.signals = args

    def evaluate(self, ts_s):
        ts_s = np.asarray(ts_s)

        return sum(sig.evaluate(ts_s) for sig in self.signals)

class ModSignal(Signal):

    def __init__(self, carrier, modulator, beta):
        self.carrier = carrier
        self.modulator = modulator
        self.beta = beta

    def evaluate(self, ts_s, modulation = 0):
        ts_s = np.asarray(ts_s)
        ys_mod = self.beta * self.modulator.evaluate(ts_s)
        ys = self.carrier.evaluate(ts_s, ys_mod + modulation)

        return ys

class SelfModSignal(Signal):

    def __init__(self, carrier, beta):
        self.carrier = carrier
        self.beta = beta

    def evaluate(self, ts_s):
        ts_s = np.asarray(ts_s)
        ys = np.zeros(len(ts_s))
        lastSample = 0.0

        for iSample in range(0, len(ts_s)):
            ys[iSample] = self.carrier.evaluate(ts_s[iSample], self.beta * lastSample)
            lastSample = ys[iSample]

        return ys

class LowPassFilter():

    def __init__(self, Q, fc, framerate = 44100):
        w = PI2 * fc / framerate
        d = 1 / Q
        beta = 0.5 * (1 - 0.5 * d * np.sin(w)) / (1 + 0.5 * d * np.sin(w))
        gamma = (0.5 + beta) * np.cos(w)

        self.a0 = 0.5 * (0.5 + beta - gamma)
        self.a1 = 0.5 + beta - gamma
        self.a2 = self.a0
        self.b1 = -2 * gamma
        self.b2 = 2 * beta

    def transform(self, drySignal, ts_s):
        wetSignal = drySignal

        for i in range(2, len(drySignal)):
            wetSignal[i] = self.a0 * drySignal[i] \
                           + self.a1 * drySignal[i - 1] \
                           + self.a2 * drySignal[i - 2] \
                           - self.b1 * wetSignal[i - 1] \
                           - self.b2 * wetSignal[i - 2]

        return wetSignal

class HiPassFilter():

    def __init__(self, Q, fc, framerate = 44100):
        w = PI2 * fc / framerate
        d = 1 / Q
        beta = 0.5 * (1 - 0.5 * d * np.sin(w)) / (1 + 0.5 * d * np.sin(w))
        gamma = (0.5 + beta) * np.cos(w)

        self.a0 = 0.5 * (0.5 + beta + gamma)
        self.a1 = -(0.5 + beta + gamma)
        self.a2 = self.a0
        self.b1 = -2 * gamma
        self.b2 = 2 * beta

    def transform(self, drySignal, ts_s):
        wetSignal = drySignal

        for i in range(2, len(drySignal)):
            wetSignal[i] = self.a0 * drySignal[i] \
                           + self.a1 * drySignal[i - 1] \
                           + self.a2 * drySignal[i - 2] \
                           - self.b1 * wetSignal[i - 1] \
                           - self.b2 * wetSignal[i - 2]

        return wetSignal

class DelayEffect():

    def __init__(self, delays, attenuations):
        self.delays = np.asarray(delays)
        self.attenuations = np.asarray(attenuations)

    def transform(self, drySignal, ts_s):
        wetSignal = drySignal

        for i in range(0, len(self.delays)):
            dryLength = len(drySignal)
            currDelay = self.delays[i]

            shiftedDry = np.zeros(dryLength)
            shiftedDry[currDelay:] = drySignal[0:dryLength - currDelay]

            wetSignal += self.attenuations[i] * shiftedDry

        return wetSignal

class ChorusEffect():

    def __init__(self, delays, attenuations):
        self.delays = np.asarray(delays)
        self.attenuations = np.asarray(attenuations)

    def transform(self, drySignal, ts_s):
        wetSignal = drySignal
        dryLength = len(drySignal)

        for i in range(0, len(self.delays)):
            currDelay = self.delays[i]
            shiftedDry = np.zeros(dryLength)
            shiftedDry[currDelay:] = self.attenuations[i] * drySignal[0:len(drySignal) - currDelay]
            wetSignal += shiftedDry

        return wetSignal

class Wave():

    def __init__(self, ys, ts=None, framerate=None):
        self.ys = np.asanyarray(ys)
        self.framerate = framerate if framerate is not None else 44100

        if ts is None:
            self.ts = np.arange(len(ys)) / self.framerate
        else:
            self.ts = np.asanyarray(ts)

    def __len__(self):
        return len(self.ys)

    def applyEffect(self, effect):
        self.ys = effect.transform(self.ys, self.ts)

    def quantize(self, bound, dtype):
        return quantize(self.ys, bound, dtype)

    def scale(self, factor):
        self.ys *= factor

    def write(self, filename='sound.wav'):
        print('Writing', filename)
        wfile = WavFileWriter(filename, self.framerate)
        wfile.write(self)
        wfile.close()

    def play(self, filename='sound.wav'):
        self.write(filename)
        play_wave(filename)

    def plot(self):
        TOOLS = "pan, box_zoom, reset"
        output_file("wave.html", title="wave time", mode="cdn")
        p = figure(tools=TOOLS, x_axis_label="time [s]", y_axis_label="amplitude [-]")
        p.line(self.ts, self.ys)
        show(p)

    def normalize(self, amp=1.0):
        """Normalizes the signal to the given amplitude.

        amp: float amplitude
        """
        self.ys = normalize(self.ys, amp=amp)

    def unbias(self):
        """Unbiases the signal.
        """
        self.ys = unbias(self.ys)

    def make_spectrum(self, full=False):
        """Computes the spectrum using FFT.

        returns: Spectrum
        """
        n = len(self.ys)
        d = 1 / self.framerate

        if full:
            hs = np.fft.fft(self.ys)
            fs = np.fft.fftfreq(n, d)
        else:
            hs = np.fft.rfft(self.ys)
            fs = np.fft.rfftfreq(n, d)

        return Spectrum(hs, fs, self.framerate, full)

def quantize(ys, bound, dtype):
    """Maps the waveform to quanta.

    ys: wave array
    bound: maximum amplitude
    dtype: numpy data type of the result

    returns: quantized signal
    """
    if max(ys) > 1 or min(ys) < -1:
        warnings.warn('Warning: normalizing before quantizing.')
        ys = normalize(ys)

    zs = (ys * bound).astype(dtype)
    return zs

def normalize(ys, amp=1.0):
    """Normalizes a wave array so the maximum amplitude is +amp or -amp.

    ys: wave array
    amp: max amplitude (pos or neg) in result

    returns: wave array
    """
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)

def unbias(ys):
    """Shifts a wave array so it has mean 0.

    ys: wave array

    returns: wave array
    """
    return ys - ys.mean()

def play_wave(filename='sound.wav', player='aplay'):
    """Plays a wave file.

    filename: string
    player: string name of executable that plays wav files
    """
    cmd = '%s %s' % (player, filename)
    popen = subprocess.Popen(cmd, shell=True)
    popen.communicate()
