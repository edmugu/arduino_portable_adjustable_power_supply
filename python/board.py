# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 2021

Controls the board.

EXAMPLE: 
        python board.py --port=COM3
        
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


class Board(object):
    """
    It controls the Arduino_Adjustable_Power_Supply module
    """

    version = "0.1"
    arduino_vcc = 5.0

    v_to_i = 1.0 / (100 * 0.1)
    pins = [
        {"num": 0, "name": "Iin", "scale": v_to_i, "cur_pin": True, "value": None},
        {"num": 1, "name": "Vin", "scale": 4.56, "cur_pin": False, "value": None},
        {"num": 2, "name": "Vup", "scale": 13.74, "cur_pin": False, "value": None},
        {"num": 3, "name": "Vout", "scale": 13.74, "cur_pin": False, "value": None},
        {"num": 4, "name": "Iout", "scale": v_to_i, "cur_pin": True, "value": None},
        {"num": 5, "name": "Vdown", "scale": 31.09, "cur_pin": False, "value": None},
    ]

    def __init__(self, port="COM3"):
        print("\nboard.py version %s" % self.version)
        self.board = pyfirmata.Arduino(port)
        print("the board's firmware is version %s.%s" % self.board.firmware_version)

        # Enabling the IO
        it = pyfirmata.util.Iterator(self.board)
        it.start()
        for p in self.pins:
            self.board.analog[p["num"]].enable_reporting()
        time.sleep(0.1)

    def read_voltage(self, read_retries=99, verbose=True):
        """
        It reads the voltage of all the stages of the unit
        """
        if verbose:
            print("reading the raw voltages\n")
        for p in filter(lambda x: x["cur_pin"] == False, self.pins):
            p["value"] = self.board.analog[p["num"]].read()
            for _ in range(read_retries):
                if p["value"] is not None:
                    vcc_percent = p["value"] * 100
                    p["value"] = p["value"] * self.arduino_vcc
                    if verbose:
                        print(
                            "Read %#04.1f%% of VCC on pin a%s (= %3.2f Volts)"
                            % (vcc_percent, p["num"], p["value"])
                        )
                    break
            if p["value"] is None:
                if verbose:
                    print(
                        "Read NONE on pin a%s [this might be a bug on the board's FW. run again]"
                        % p
                    )
        if verbose:
            print("\nCalculating the voltages on the board")
        for p in filter(lambda x: x["cur_pin"] == False, self.pins):
            if p["value"] is not None:
                p["value"] = p["value"] * p["scale"]
                if verbose:
                    print("%9s is %#05.2f Volts" % (p["name"], p["value"]))

    def read_current(self, read_retries=99, verbose=True):
        """
        It reads the current going in and out
        """
        if verbose:
            print("reading the raw voltages\n")
        for p in filter(lambda x: x["cur_pin"] == True, self.pins):
            p["value"] = self.board.analog[p["num"]].read()
            for _ in range(read_retries):
                if p["value"] is not None:
                    vcc_percent = p["value"] * 100
                    p["value"] = p["value"] * self.arduino_vcc
                    if verbose:
                        print(
                            "Read %#04.1f%% of VCC on pin a%s (= %3.2f Volts)"
                            % (vcc_percent, p["num"], p["value"])
                        )
                    break
            if p["value"] is None:
                if verbose:
                    print(
                        "Read NONE on pin a%s [this might be a bug on the board's FW. run again]"
                        % p
                    )

        if verbose:
            print("\nCalculating the voltages on the board")
        for p in filter(lambda x: x["cur_pin"] == True, self.pins):
            if p["value"] is not None:
                p["value"] = p["value"] * p["scale"]
                if verbose:
                    print("%9s is %#07.2f miliAmps" % (p["name"], p["value"] * 1000))

    def calculate_load(self, read_retries=99, verbose=True):
        self.read_voltage(read_retries, verbose=False)
        self.read_current(read_retries, verbose=False)
        if verbose:
            print("Calculating the load on the output\n")

        pvout = list(filter(lambda x: x["name"] == "Vout", self.pins))[0]["value"]
        piout = list(filter(lambda x: x["name"] == "Iout", self.pins))[0]["value"]

        if (pvout is None) or (piout is None):
            print("had issues reading voltage or current")
            return
        ans = pvout / piout
        if verbose:
            print("Rload is %05.2f\n" % ans)


if __name__ == "__main__":
    fire.Fire(Board)
