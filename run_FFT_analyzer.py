import argparse
from src.stream_analyzer import Stream_Analyzer
import time
from src.razer_kbd_api import RazerKbd
import atexit


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_device', type=int, default=None, dest='device',
                        help='pyaudio (portaudio) device index')
    parser.add_argument('--razer_dev_idx', type=int, default=0,
                        help='Index for the razer device in openrazer device manager.')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--max_fps', type=int, default=0,
                        help='Maximum updates per second, 0 implies infinite. Use this to reduce CPU usage.')
    return parser.parse_args()

def run_FFT_analyzer():
    args = parse_args()

    kbd = RazerKbd(args.razer_dev_idx)

    atexit.register(kbd.ClearAndUpdate)

    ear = Stream_Analyzer(
        # Pyaudio (portaudio) device index, defaults to first mic input
        device=args.device,
        rate=None,               # Audio samplerate, None uses the default source settings
        FFT_window_size_ms=60,    # Window size used for the FFT transform
        updates_per_second=1000,  # How often to read the audio stream for new data
        smoothing_length_ms=50,    # Apply some temporal smoothing to reduce noisy features
        n_frequency_bins=kbd.Cols(),  # The FFT features are grouped in bins
        verbose=args.verbose,    # Print running statistics (latency, fps, ...)
        height=kbd.Rows(),     # Height, in pixels, of the visualizer device.
        kbd=kbd   # The keyboard used to output the visualization.
    )

    max_fps = args.max_fps  # How often to update the FFT features + display
    last_update = time.time()
    while True:
        if (max_fps != 0):
            if (time.time() - last_update) > (1./max_fps):
                last_update = time.time()
            else:
                time.sleep(last_update + 1./max_fps - time.time())
        
        raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()


if __name__ == '__main__':
    run_FFT_analyzer()
