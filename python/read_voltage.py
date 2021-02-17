# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 18:30:09 2021

It reads the voltage on the analog pins A2-A3 which are connected to the 
voltage rails.

EXAMPLE: 
        python tools_read_voltage.py --arduion_port=COM3
        
REQUIREMENTS: 
    python 3.7+
    pyfirmata  (to talk to the arduino)
    fire (to create command line tool)

@author: Eduardo Munoz
@email: edmugu@protonmail.com
"""
import pyfirmata
import fire
import time

version = "0.1"

scale = 13.38
arduino_vcc = 5.0
port_list = ["3", "2", "1"]
name_list = {"3": "Vout", "2": "Vstep_up", "1": "Vin"}


print("\ntools_read_voltage.py version %s" % version)
print("FOR HELP TYPE tools_read_voltage.py --help\n\n")

from pyfirmata import Arduino, util


def read_voltage(arduino_port="COM3"):
    """
    It reads the voltage expecified by 'arduion_port'. 
    EXAMPLE: 
        python tools_read_voltage.py --arduion_port COM3
    """
    print("trying to connect to arduino on %s" % arduino_port)
    board = Arduino(arduino_port)
    board.digital[13].write(1)
    print("connected succesfully!")
    print("the board firmware is version %s.%s" % board.firmware_version)

    print("Enabling the IO \n")
    it = util.Iterator(board)
    it.start()

    a = {}
    for p in port_list:
        board.analog[int(p)].enable_reporting()
    time.sleep(0.1)

    print("reading the raw voltages\n")
    for p in port_list:
        a[p] = board.analog[int(p)].read()
        for read_tries in range(99):
            if a[p] is not None:
                a[p] = a[p] * arduino_vcc
                print("Read %3.3f Volts on pin a%s" % (a[p], p))
                break

        if a[p] is None:
            print("Read NONE on pin a%s" % p)

    print("\nCalculating the voltage on the board")
    for p in port_list:
        if a[p] is not None:
            tmp = a[p] * scale
            print("%s is %3.3f" % (name_list[p], tmp))


if __name__ == "__main__":
    fire.Fire(read_voltage)
