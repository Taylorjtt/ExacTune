import serial
import struct
import os
import plotting
import numpy as np
import threading
import time
import random
import math
import sys
clear = lambda: os.system('cls')
ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM4"
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

try:
    ser.open()
except  Exception:
    print ("Error Opening Serial Port")
if ser.isOpen():
    try:
        ser.flushInput();
        ser.flushOutput();
    except Exception as err:
        print("error communicating {0}".format(err))
def plot():
    plt = plotting.DynamicPlotterNumpy(sampleinterval=0.005, timewindow=10.)
    @plt.data_wrapper
    def data_gen():
        if ser.isOpen():
            try:
                data = ser.read(3)
                unpacked = struct.unpack('!BBB', data)
                aCurr = unpacked[0] | (unpacked[1] & 0x0F) << 8
                bCurr = (unpacked[2] << 4) | ((unpacked[1] & 0xF0) >> 4)
                PhaseACurrentInAmps = (aCurr - 2048) * 0.0080566
                PhaseBCurrentInAmps = (bCurr - 2048) * 0.0080566
                return np.array([PhaseACurrentInAmps, PhaseBCurrentInAmps])
            except Exception as err:
                print("error communicating {0}".format(err))


        # Define the thread
    th = threading.Thread(target=data_gen)
    th.daemon = True

        # Finally when the set-up is ready, start everything
    th.start() # Start thread
    plt.run()  # Start plotting

if __name__ == '__main__':
    plot()