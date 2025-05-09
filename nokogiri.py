import pretty_midi
import numpy as np
import scipy.io.wavfile as wavfile

def sawtooth_wave(frequency, fs, duration):
    t = np.arange(int(fs * duration))
    period = fs / frequency
    t = t % period
    t = 2 * t / period - 1
    return t

midi_data = pretty_midi.PrettyMIDI('/Users/tachibananoyushou/Downloads/basic_pitch_transcription (2).mid')

fs = 44100
duration = midi_data.get_end_time()

total_samples = int(fs * duration)
samples = np.zeros(total_samples)

for instrument in midi_data.instruments:
    for note in instrument.notes:
        start_sample = int(note.start * fs)
        end_sample = int(note.end * fs)
        frequency = pretty_midi.note_number_to_hz(note.pitch)
        note_duration = note.end - note.start
        t = sawtooth_wave(frequency, fs, note_duration)
        t_samples = len(t)
        # のこぎり波の長さがノートの長さより短い場合、残りをゼロで埋める
        if t_samples < (end_sample - start_sample):
            t = np.concatenate([t, np.zeros((end_sample - start_sample - t_samples))])
        samples[start_sample:end_sample] += t

samples /= np.max(np.abs(samples))

wavfile.write('output_sawtooth.wav', fs, samples)
