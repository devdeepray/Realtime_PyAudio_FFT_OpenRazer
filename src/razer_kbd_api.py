import openrazer.client
import sys

class RazerKbd:
    def __init__(self, device_idx):
        try:
            self.kbd = openrazer.client.DeviceManager().devices[device_idx]
        except Exception as e:
            sys.exit('Failed to initialize OpenRazer device: ' + str(e))
    
        self.ncols = self.kbd.fx.advanced.cols
        self.nrows = self.kbd.fx.advanced.rows
    
    def Cols(self):
        return self.ncols
    
    def Rows(self):
        return self.nrows
    
    def DrawBar(self, x, level, color):
        for j in range(1, min(level, self.nrows) + 1):
            self.kbd.fx.advanced.matrix[self.nrows - j, x] = color
    
    def ClearDrawBuffer(self):
        self.kbd.fx.advanced.matrix.reset()
    
    def Update(self):
        self.kbd.fx.advanced.draw()

    def ClearAndUpdate(self):
        self.ClearDrawBuffer()
        self.Update()
