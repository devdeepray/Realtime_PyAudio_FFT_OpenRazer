import numpy as np
import time, sys, math
import pygame
from collections import deque
from src.utils import Button
from matplotlib import cm
import openrazer.client

class Spectrum_Visualizer:
    """
    The Spectrum_Visualizer visualizes spectral FFT data using a simple PyGame GUI
    """
    def __init__(self, ear, kbd):
        self.ear = ear

        self.kbd = kbd


        self.cm = cm.inferno

        self.toggle_history_mode()

        self.fast_bar_colors = [list((255*np.array(self.cm(i))[:3]).astype(int)) for i in np.linspace(0,255,self.ear.n_frequency_bins).astype(int)]
        self.fast_bar_colors = self.fast_bar_colors[::-1]

        self.frequency_bin_max_energies  = np.zeros(self.ear.n_frequency_bins)
        self.frequency_bin_energies = self.ear.frequency_bin_energies

        #Fixed init params:
        self.start_time = None
        self.vis_steps  = 0
        self.fps_interval = 10
        self.fps = 0
        self._is_running = False

    def toggle_history_mode(self):

        self.decay_speed        = 0.06
        self.avg_energy_height  = 0.4


        #Configure the bars:
        self.fast_bars = []
        for i in range(self.ear.n_frequency_bins):
            fast_bar = None
            self.fast_bars.append(fast_bar)

    def start(self):
        print("Starting spectrum visualizer...")
        assert(len(self.frequency_bin_energies) == self.kbd.Cols())

        self._is_running = True

    def stop(self):
        print("Stopping spectrum visualizer...")
        # Clear keyboard
        self._is_running = False

    def toggle_display(self):
        '''
        This function can be triggered to turn on/off the display
        '''
        if self._is_running: self.stop()
        else: self.start()

    def update(self):
        if np.min(self.ear.bin_mean_values) > 0:
            self.frequency_bin_energies = self.avg_energy_height * self.ear.frequency_bin_energies / self.ear.bin_mean_values


        if self.start_time is None:
           self.start_time = time.time()

        self.vis_steps += 1

        if self.vis_steps%self.fps_interval == 0:
            self.fps = self.fps_interval / (time.time()-self.start_time)
            self.start_time = time.time()

        self.plot_bars()

        self.kbd.Update()


    def plot_bars(self):
        bars, new_slow_features = [], []
        local_height = self.kbd.Rows()
        feature_values = self.frequency_bin_energies[::-1]

        for i in range(len(self.frequency_bin_energies)):
            feature_value = feature_values[i] * local_height
            self.fast_bars[i] = int(feature_value)


        self.kbd.ClearDrawBuffer()
        for i, fast_bar in enumerate(self.fast_bars):
            self.kbd.DrawBar(len(self.fast_bars) - i - 1, fast_bar, self.fast_bar_colors[i])

