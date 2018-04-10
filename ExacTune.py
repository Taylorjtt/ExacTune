import serial
import struct
import os

clear = lambda: os.system('cls')
ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM4"

try:
    ser.open()
except  Exception:
    print ("Error Opening Serial Port")

if ser.isOpen():
    try:
        ser.flushInput();
        ser.flushOutput();
        while True:
            data = ser.read(3)
            unpacked = struct.unpack('!BBB',data)
            aCurr = unpacked[0] | (unpacked[1] & 0x0F) << 8
            bCurr = (unpacked[2] << 4) | ((unpacked[1] & 0xF0) >> 4)
            PhaseACurrentInAmps = (aCurr - 2048)*0.0080566
            PhaseBCurrentInAmps = (bCurr - 2048) * 0.0080566
            print("Phase A Current: "+str(PhaseACurrentInAmps)+"A")
            print("Phase B Current: " + str(PhaseBCurrentInAmps) + "A")




    except Exception as err:
        print("error communicating {0}".format(err))



