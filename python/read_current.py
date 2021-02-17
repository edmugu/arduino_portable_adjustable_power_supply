# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:16:01 2021

It reads the voltage on the analog pins A1 A4 which are connected to the 
Current sensing amps.

EXAMPLE: 
        python read_current.py --arduion_port=COM3
        
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
pin_list = ["0", "4"]
pin_name = {"0": "Iin", "4": "Iout"}

Rsense = 0.1
gain = 100
scale = 1.0 / gain  # this is the voltage on the sense resistor before it is amplified
scale = scale / Rsense  # This is the current going through Rsense


print("\nread_current.py version %s" % version)
print("FOR HELP TYPE tools_read_voltage.py --help\n\n")

from pyfirmata import Arduino, util


def read_current(port="COM3"):
    """
    It reads the current expecified by 'port'. 
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
                vcc_percent = a[p] * 100
                a[p] = a[p] * arduino_vcc
                print(
                    "Read %#04.1f%% of VCC on pin a%s (= %3.2f Volts)"
                    % (vcc_percent, p, a[p])
                )
                break

        if a[p] is None:
            print("Read NONE on pin a%s [this might be a bug on the board's FW. run again]" % p)

    print("\nCalculating the Currents on the board")
    for p in pin_list:
        if a[p] is not None:
            tmp = a[p] * scale * 1000
            print("%9s is %#07.02f miliAmps" % (pin_name[p], tmp))


if __name__ == "__main__":
    fire.Fire(read_current)
