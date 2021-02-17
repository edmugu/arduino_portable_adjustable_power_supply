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


arduino_vcc = 5.0
pin_list = ["3", "2", "1"]
pin_name = {"3": "Vout", "2": "Vstep_up", "1": "Vin"}
pin_scale = {"Vout": 13.38, "Vstep_up": 13.38, "Vin": 3}


print("\nread_voltage.py version %s" % version)
print("FOR HELP TYPE tools_read_voltage.py --help\n\n")

from pyfirmata import Arduino, util


def read_voltage(port="COM3"):
    """
    It reads the voltage expecified by 'arduion_port'. 
    EXAMPLE: 
        python tools_read_voltage.py --arduion_port COM3
    """
    print("trying to connect to arduino on %s" % port)
    board = Arduino(port)
    board.digital[13].write(1)
    print("connected succesfully!")
    print("the board firmware is version %s.%s" % board.firmware_version)

    print("Enabling the IO \n")
    it = util.Iterator(board)
    it.start()

    a = {}
    for p in pin_list:
        board.analog[int(p)].enable_reporting()
    time.sleep(0.1)

    print("reading the raw voltages\n")
    for p in pin_list:
        a[p] = board.analog[int(p)].read()
        for read_tries in range(99):
            if a[p] is not None:
                vcc_percent = a[p]
                a[p] = a[p] * arduino_vcc
                print("Read %3.2f percent of VCC on pin a%s (= %3.2f Volts)" % (vcc_percent, p, a[p]))
                break

        if a[p] is None:
            print("Read NONE on pin a%s" % p)

    print("\nCalculating the voltage on the board")
    for p in pin_list:
        if a[p] is not None:
            tmp = a[p] * pin_scale[pin_name[p]]
            print("%9s is %#05.2f Volts" % (pin_name[p], tmp))


if __name__ == "__main__":
    fire.Fire(read_voltage)
