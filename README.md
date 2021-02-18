# [Arduino Adjustable Power Supply](https://edmugu.github.io/arduino_adjustable_power_supply/)

![3d view of pcb file](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/3d%20view.PNG "Power Supply")

## Abstract

This project is based on the [LT journal's Article from Keith Szolusha](https://github.com/edmugu/arduino_portable_adjustable_power_supply/blob/master/documentation/LTJournal-Bench_Supply.pdf). On which he discussed how to design a clean power supply. But this design is augmented by making it controllable by an Arduino. ***Use Cases Include*: motor controller, high power wireless communication, and benchtop supply.**



## Intro

This portable power supply should be able to be powered by multiple kinds of batteries from AA to Car batteries. But the main target battery is a USB power bank. Most USB power banks can deliver 12W @ 5Volts. Hence this power supply will deliver 10 Watts at its output to accommodate the inefficiencies of the power stages of this design. And because the default use case will be to power a 50-ohm load, the maximum voltage at the output should be greater than 22.36 Volts to deliver 10 Watts.

On the original design by Szolusha, there are 4 modules. (1)  a switching regulator that steps down a 10-40V input to an intermediate voltage that is slightly above the output voltage. (2) Linear regulator that "cleans" the output. (3) The current source sets a reference voltage that is not affected by temperature. And lastly, (4) A current sink that helps the Linear regulator reach low voltages.

We will modify each block to fit our needs, which are to make this portable and usable with any common household batteries. And also to make this friendly to the Arduino and Beaglebone modules there is a secondary supply that is fixed to supply 5V on a USB port. So you can power your Arduino without compromising the main power output.


![logic schematics](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/python/Assets/Arduino-power-supply.png "logic schematics")


## Use cases

Before we design anything, we better set some use cases to come with some characteristics our design must meet.

Input battery

| Use Case   | Voltage [V] | Current [A] | Power [W] | Notes                         |
|------------|-------------|-------------|-----------|-------------------------------|
| AA         | 1.5         | 0.050       | 0.075     | This voltage might be too low |
| 9-Volt     | 9           | 0.111       | N/A       | Forced Power to 1 Watt        |
| CAR        | 12.6        | 0.793       | > 10      |                               |
| Power Bank | 5           | 2.4         | 12        |                               |


Output Use cases


| OUTPUT     | Ideal           | Max            |
|------------|-----------------|----------------|
| Power      | 0.1 Watts       | 11 Watts       |
| Current    | 0.1 Amp         | 1 Amp          |
| Voltage    | 5 Volts         | 23 Volts       |
| LOAD       | 50 Ohms         | NA             |




## Pre-requirements

Input: 	1.0 Volts to 14 Volts

Output:	0-23 Volts

Power:	< 10 Watts [depending on the battery]

Monitors:

	* Voltage, for all the stages of the regulator
	* Current, for the input and output stages

Controls: 	

* Manual, with the help of a potentiometer
* Automatic, with the help of digital resistors
* Enable Switch for each output

Communications:

* I2C
* USB COM port (provided by Arduino with the [Firmata library](https://www.arduino.cc/en/reference/firmata) )

Versions:

* stand-alone
* Arduino addon



## Design Procedure

### (1) Battery Current Monitor stage

The input batteries used might have a current limit (i.e. the maximum current will be 2.4 Amps as the typical use case). This will be done to ensure the life of the battery. So the first step will be to measure the current going into the device. This can be done with a current monitor that has a voltage range from 0 to 14V and can detect <2.4 Amps through a sense resistor. The **INA199**  meets the voltage range requirement and it has an x200 gain.

As for R_sense, it should be less than 1 ohm since it will have up to 2.4 Amps going through it but it should be high enough so we can detect the voltage drop. Therefore, we installed a 100mOhm sense resistor with 4 terminals. We could have picked a smaller resistor but because this will most likely will be read by a cheap Arduino we stuck with that value. Also, to avoid measuring the voltage drop across the solder pads we installed a four-terminal resistor. That way the current monitor can measure the voltage drop on the middle of the resistor.

|        | Voltage      | Notes                     |
| ------ | ------------ | ------------------------- |
| Input  | -0.3 to 26 V |                           |
| Output | Vin - 0.24 V | worse case @ I = 2.4 Amps |

![Schematics of the current monitor](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Current_monitor.PNG "Current Monitor")


### (2) Step-Up stage

Instead of using an expensive step-down/step-up converter that can do all we need, we opted for a cheap two-stage module. So we first need to step-up the voltage above the maximum output voltage [ to account for inefficiencies]. That way we can take any battery as the input, no matter its voltage. The IC **LMR64010 **will be used for this module. Its maximum output voltage is 40V which is well above the wanted 23V output.   And the power output is 40 Watts when the regulator is set to output 40 Volts. However, the battery can limit this stage if the battery itself can't deliver 40 Watts. Also, this IC has the disadvantage of only taking voltages from 2.7V to 14V.  So our requirements can be updated to only take voltages as low as 2.7 Volts.



|        | Voltage     | Current | Notes           |
| ------ | ----------- | ------- | --------------- |
| Input  | 2.7 to 14 V |         |                 |
| Output | <40 V       | <1 A    | ~85% efficiency |

![Schematics of the Step-Up stage](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Step_up.PNG "Step-Up stage")


### (3) Step-Down stage

To be efficient one can use a switching regulator instead of a linear regulator. But on the other hand, one might want a stable clean power supply that a switching regulator can not provide. Hence one has to find the right compromise. In this project, we will use both solutions in series. A switching regulator will efficiently bring down the voltage and the linear regulator will clean its output from any noise the switching regulator might have introduced.

#### (3A) Step-Down switch substage

The previous stage will output a voltage of up to 40 Volts. However, the final output just needs to be above 23 Volts. The IC **AOZ1282CI** is a cheap buck converter that takes up to 36 Volts. And it can step down the voltage from 0.8 V to 85% of the input voltage. So if I want to output 23 Volts  I need at least [Vout = 0.85 Vin OR Vin = 23/.85] 27 Volts. So 36 Volts is good enough to give me some wiggle room. Note that to output voltage should be a bit higher than the final output voltage to count for inefficiencies in the next state. Therefore,  the feedback circuit has to feed on the next substage. Or I can keep this stage to the maximum voltage needed of 27 Volts [ + some wiggle room].



|        | Voltage        | Current | Notes           |
| ------ | -------------- | ------- | --------------- |
| Input  | 4.5 to 36 V    |         |                 |
| Output | 0.8 to 85% Vin | <1.2 A  | efficiency >85% |


![Schematics of the Step-Down Switch](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Step_down_switch.PNG "Step-Down switch")

#### (3B) Step-Down Linear Regulator substage

The second substage is to clean any noise created on the switch buck converter. Now the **LM317**  is an adjustable linear regulator that can output over 1 Amp and can take in up to 40 Volts. Which meets our needs.

|        | Voltage          | Current |
| ------ | ---------------- | ------- |
| Input  | 4.25 to 40 Volts |         |
| Output | 1.25 to 37 Volts | <1.5 A  |

![Schematics of the Step-Down linear regulator](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Step_down_linear.PNG "Step-Down linear regulator")

#### (3C) Feedback to substages

The main challenge is that the voltage of the first substage should be above the output of the second substage. However, if the difference in the voltage between the two is too high, the second stage will have to "overburn" the excess voltage. Making it less inefficient. And on top of that, the final voltage is adjustable. So to tackle this an operational amplifier is used to calculate the voltage difference between the stages. This voltage will be feed to the feedback of the first stage [the switching regulator], which will raise its voltage until its feedback reaches its critical voltage. Hence, the voltage of the switching regulator will be held above the final output. 


![Schematics of the feedback circuit](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/step_down_feedback.PNG "feedback circuit")


### (4) Final Battery Current Monitor stage

This is the final stage of the power supply. By having a current monitor at the begging and the end we can calculate the efficiency of the power supply.



## How to use

The easiest way to monitor voltage is to use the Arduino Firmata library. This can easily be uploaded by the Arduino IDE by opening the example firmata project and uploading it to the Arduino. After that, you can run the /python/read_voltage.py script provided in this repo.

![read_voltage.py.png](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/read_voltage.py.png "read_voltage.py.png")

## Bring up 
While bringing up I noticed a couple of issues that can be fix but should be address on the next version. The first issue noted was that the SMA DIODE footprint was backwards [This is what happens when you use the "free community software" and you are a noob with the tool]. 


![board bring up](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/picture%20of%20bringup.PNG  "board bring up")


