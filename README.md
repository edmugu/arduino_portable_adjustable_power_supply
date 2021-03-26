---
title: Main
has_children: false
nav_order: 1
---


# [Arduino Adjustable Power Supply](https://edmugu.github.io/arduino_adjustable_power_supply/)

![3d view of pcb file](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/3d%20view.PNG "Power Supply")

## Abstract

This project is based on the [LT journal's Article from Keith Szolusha](https://github.com/edmugu/arduino_portable_adjustable_power_supply/blob/master/documentation/LTJournal-Bench_Supply.pdf). In the article, he discussed how to design a clean power supply. However, this design is augmented by making it controllable by an Arduino. Use Cases Include: motor controller, high power wireless communication, and benchtop supply.


## Intro

On the original design by Szolusha, there are four modules. (1) a switching regulator that steps down a 10-40V input to an intermediate voltage that is slightly above the output voltage. (2) Linear regulator that "cleans" the output. (3) The current source sets a reference voltage that is not affected by temperature. Lastly, (4) A current sink that helps the Linear regulator reach low voltages.

We will modify each block to fit our needs, making this portable and usable with any common household batteries. So the base design is shown on the diagram below. The first step is to step-up the voltage of the battery to a usuable voltage we can step down. From there the second step is to step-down the voltage to the wanted voltages like 3.3 Volts, 5.0 Volts and Vout. However, the efficient step-down switches can create "switching ripples" on the output. These ripples aren't a big deal; however, if one needs a very clean supply one could use a inefficient LDO regulator. So will use the step-down switch and regulator to create a clean semi-efficent voltage output as shown on the diagram. 

![logic schematics](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/python/Assets/Arduino-power-supply.png "logic schematics")

The main target battery is a USB power bank. Most USB power banks can deliver 12W @ 5Volts. Hence, this power supply will deliver 10 Watts at its output to accommodate the inefficiencies of the power stages of this design. Since the default use case will be to power a 50-ohm load, the maximum voltage at the output should be greater than 22.36 Volts to deliver 10 Watts.


# Design process
## Use cases
Before we design anything, it is better to set some use cases to come with some characteristics our design must meet.

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
Now that we have all our use cases (and an ideal use case), we can start defining some requirements for our design. 

Input: 	1.0 Volts to 14 Volts

Output:	0-23 Volts

Power:	< 10 Watts [depending on the battery]

Monitors:
	* Voltage, for all the stages of the regulator
	* Current, for the input and output stages

Controls: 	
* Manual, with the help of a potentiometer
* Automatic, with the help of digital resistors

Communications:
* I2C
* USB COM port (provided by Arduino with the [Firmata library](https://www.arduino.cc/en/reference/firmata) )

Versions:
* stand-alone
* Arduino addon



## Design Procedure
### (1) Battery Current Monitor stage
The input batteries used might have a current limit (i.e., the maximum current will be 2.4 Amps as the typical use case). This will be done to ensure the life of the battery. The first step will be to measure the current going into the device. This can be done with a current monitor with a voltage range from 0 to 14V and that can detect <2.4 Amps through a sense resistor. The **INA199** meets the voltage range requirement, and it has a x200 gain.

R_Sense should be less than 1 ohm since it will have up to 1 Amp going through it. However, it should be high enough to detect the voltage drop. Therefore, we installed a 100mOhm sense resistor with four terminals. We could have picked a smaller resistor, but since this will most likely will be read by a cheap Arduino, we stuck with that value. Futher, to avoid measuring the voltage drop across the solder pads, we installed a four-terminal resistor.

|        | Voltage      | Notes                     |
| ------ | ------------ | ------------------------- |
| Input  | -0.3 to 26 V |                           |
| Output | Vin - 0.24 V | worse case @ I = 2.4 Amps |

![Schematics of the current monitor](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Current_monitor.PNG "Current Monitor")


### (2) Step-Up stage
Instead of using an expensive step-down/step-up converter to do all we need, we opted for a cheap two-stage module. We first need to step-up the voltage above the maximum output voltage [ to account for inefficiencies]. That way, we can take any battery as the input, no matter its voltage. The IC **LMR64010** will be used for this module. Its maximum output voltage is 40V, which is well above the wanted 23V output. Its power output is 40 Watts when the regulator is set to output 40 Volts. However, the battery can limit this stage if the battery cannot deliver 40 Watts. Further, this IC has the disadvantage of only taking voltages from 2.7V to 14V. Hence, we can update our requirements only to take voltages as low as 2.7 Volts.

|        | Voltage     | Current | Notes           |
| ------ | ----------- | ------- | --------------- |
| Input  | 2.7 to 14 V |         |                 |
| Output | <40 V       | <1 A    | ~85% efficiency |

![Schematics of the Step-Up stage](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Step_up.PNG "Step-Up stage")


### (3) Step-Down stage

#### (3A) Step-Down switch substage

The previous stage will output a voltage of up to 40 Volts. However, the final output needs to be above 23 Volts. The IC **AOZ1282CI** is a cheap buck converter that takes up to 36 Volts. It can reduce the voltage from 0.8 V to 85% of the input voltage. If I want to output 23 Volts, I need at least [Vout = 0.85 Vin OR Vin = 23/.85] 27 Volts. Hence, 36 Volts is good enough to give me some wiggle room. Note that output voltage should be a bit higher than the final output voltage to count for inefficiencies in the next stage. Therefore, the feedback circuit has to feed on the next substage. Further, I can keep this stage to the maximum voltage needed of 27 Volts [ + some wiggle room].

|        | Voltage        | Current | Notes           |
| ------ | -------------- | ------- | --------------- |
| Input  | 4.5 to 36 V    |         |                 |
| Output | 0.8 to 85% Vin | <1.2 A  | efficiency >85% |


![Schematics of the Step-Down Switch](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Step_down_switch.PNG "Step-Down switch")

#### (3B) Step-Down Linear Regulator substage

The second substage is used to clean any noise created on the step-down switch. Now the **LM317** an adjustable linear regulator that can output over 1 Amp and can take in up to 40 Volts. This meets our needs effectively.

|        | Voltage          | Current |
| ------ | ---------------- | ------- |
| Input  | 4.25 to 40 Volts |         |
| Output | 1.25 to 37 Volts | <1.5 A  |

![Schematics of the Step-Down linear regulator](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/Step_down_linear.PNG "Step-Down linear regulator")

#### (3C) Feedback to substages

The main challenge is that the first substage's voltage should be above the output of the second substage. However, if the difference in the voltage between the two is too high, the second stage will have to "overburn" the excess voltage, making it less efficient. On top of that, the final voltage is adjustable. To tackle this, an operational amplifier is used to calculate the voltage difference between the stages. This voltage will be fed to the second stage [the switching regulator], which will raise its voltage until its feedback reaches its critical voltage. Hence, the voltage of the switching regulator will be held above the final output.


![Schematics of the feedback circuit](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/step_down_feedback.PNG "feedback circuit")


### (4) Final Battery Current Monitor stage

This is the final stage of the power supply. By having a current monitor at the beginning and the end, we can calculate the efficiency of the power supply. Also the feedback voltage of the previous stage takes the drop across this stage by feeding the "final" voltage to linear regulator. 


### (5) Arduino Control 

 To make the design controllable by an Arduino an I2C digital pot was added to the one of the choose able feedback circuits. 


### (6) Price per stage
Current Monitor 	INA199B is about $0.80 ($1.60 for two)
Step-Up Voltage 	LMR64010 is about $1.61
Step-Down Voltage 	AOZ1282CI is about $1.15
Regulator  		LM317 is about $0.60

Main IC cost  		$4.69


![regulator_feedback](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/regulator_feedback.PNG)


# Debugging Process
## Bug 1: The voltage of the first stage does not go above vin
After checking that the enable pin was high and that the switching output was doing what it was suppose to be doing, I decided to relace the switch. However, it still showed the same behaviour. Vout would reach >30 Volts then it would drop to Vin. Then I checked my sma units on a eval board and they work. At that moment, I started to investigate the second most complicated unit on the first stage, the diode. Then it was clear that the issue was that I installed the diode backwards. However the silkscreen and schematics had the diode on the right oritation. Which meant that the footprint pads of the diode were swaped. 

## Bug 2: The output of the final stage was stuck at 1.8 Volts
Note that the feed back to the last two stages can be selected between a "fixed" voltage divided that would allow the output go all the way to 27 volts. Or it can be selected to be the dynamic feedback circuit that would keep the voltage of the last two stages close to each other. The circuit worked fine when the fixed voltage divider was used however it got stuck at 1.8 volts when it was switch to the dynamic feedback. At that moment, the feedback circuit was set to have 0.8 Volts difference between the two stages. And indeed there was a 0.8 volt difference between the stages. So I though that may be if I raised the difference to 5 volts it would work. Luckly, it did and after looking for an explanation I noted that the linear regulator needed at least 3 volts difference between its output and its input. 
	
## Bug 3: The output can only drive <1 mA before it starts to struggle. 
I believed this is due to the sma capacitos. However I noted that this issue went away if I lowered the voltage the mininum voltage of 1.2V and then raised to the wanted voltage. So it seems that the step-down switch and regulator had issues if the initial load was too much. 


![board bring up](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/picture%20of%20bringup.PNG  "board bring up")

## Thermal test
![thermal picture](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/1_watt_thermal.PNG "Thermal picture")


# CLI

The easiest way to monitor voltage is to use the Arduino Firmata library. This can easily be uploaded by the Arduino IDE by opening the firmata project and uploading it to the Arduino. Afterwards, you can run the /python/read_voltage.py script provided in this report.

![read_voltage.py.png](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/read_voltage.py.png "read_voltage.py.png")

## Test validation

To guarantee that the board works and can be massed produced some basic validation test have to be set. These should include software and hardware test, [which are described on the wiki with more details](https://github.com/edmugu/arduino_adjustable_power_supply/wiki/Hardware-Test-procedure)


