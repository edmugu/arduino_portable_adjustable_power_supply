# Arduino Adjustable and Portable  Power Supply

## Abstract

This project is based on the LT journal's Article from Keith Szolusha. On which it is discussed on how to design a clean power supply. But this is augmented by making it portable for your Arduino projects. ***Use Cases Include*: motor controller, high power wireless communication, and bench top supply.** 



## Intro 

This portable power supply should be able to be powered by multiple kinds of batteries from AA to Car batteries. But the main target battery is a USB power bank. Most USB power banks can deliver 12W @ 5Volts. Hence this power supply will deliver 10 Watts at its output to accommodate to the inefficiencies of the power stages of this design. And because the default use case will be to power a 50 ohm load [like a conventional antenna], the maximum voltage at the output should be greater than 22.36 Volts. 

On the original design there are 4 modules. (1)  a switching regulator that steps down a 10-40V input to an intermediate voltage that is slightly above the output voltage. (2) Linear regulator that "cleans" the output. (3) Current source that sets a reference voltage that is not affected by temperature. And lastly, (4) A current sink that helps the Linear regulator reach low voltages. 

To make this portable and usable with any battery a boost converter is used to raise the battery voltage to 30 volts. Also to make this friendly to the Arduino and beaglebone modules there is a secondary supply that is fixed to supply 5V on a USB port.



## Use cases

Input battery

```markdown
| Use Case   | Voltage [Volts] | Current [Amps] | Power [Watts] | Notes                 |
|------------|-----------------|----------------|---------------|-----------------------|
| AA         | 1.5             | 0.050          | 0.075         |                       |
| 9-Volt     | 9               | 0.111          | 1             | Forced Power to 1 Watt|
| CAR        | 12.6            | 0.793          | > 10          |                       |
| Power Bank | 5               | 2.4            | 12            |                       |
```



Output Use cases

```markdown
| OUTPUT     | Ideal           | Max            |
|------------|-----------------|----------------|
| Power      | NA              | 11 Watts       |
| Current    | NA              | 1 Amp          |
| Voltage    | NA              | 23 Volts       |
| LOAD       | 50 Ohms         | NA             |
```



## Requirements

Input: 	3 Volts to 14 Volts

Output:	0-23 Volts

Power:	< 10 Watts [depending on the battery]

Monitors: 

	* Voltage, for all the stages of the regulator
	* Current, for the input and output stages
	* able to store measurements on an EEPROM

Controls: 	

* Manual, with the help of potentiometer
* Automatic, with the help of digital resistors
* Power Switch 
* Enable Switch for each output

Communications:

* I2C (for both stand-alone and Arduino addon)
* COM port (for the stand alone)

Versions: 

* stand-alone
* Arduino addon



## Modules

### Battery Current Limiter

The input batteries used might have a current limit (i.e. the maximum current will be 2.4 Amps as the typical use case). This will be done to ensure the life of the battery. So the first step will be to measure the current going in to the device for which one can use a **INA199** current sensor with a 200 gain. Hence, the sense resistor will be [Rsense = (5 Volts / 2.4 Amps) / ( 200 gain) = 10.41 miliOhms].  Note that the **INA199** op-amp has a 100uV offset, which means that the read out will have an error of 20mV that might be able to be handled during calibration. 

Now, to reduce the current an op-amp and a power transistor will be use, such that when the current is above a level the op-amp will tune down the power transistor delivering the device. **LM321LV** and **Si4425FDY** will do nicely. 

### Pre Step-Up

Instead of using a step-down/step-up converter that can do all we need, we opted for a cheap two stage module. We first step-up to the voltage above the maximum output voltage. That way we can take any battery as the input, no matter its voltage. For this module will use the IC **LMR64010**. Its maximum output voltage is 40V which is well above the wanted 23V output. And the power output is 40 Watts when the regulator is set to output 40 Volts. However the battery can limit this stage. To overcome the battery limitation we place a super capacitor to hold energy need for high burst of energy.



### Step-Down

To be efficient one can use a switching regulator instead of a linear regulator. But on the other hand, one might want a stable clean power supply that a switching regulator can not provide. Hence one has to find the right compromise. In this project we will use both solutions on series. A switching regulator will efficiently bring down the voltage and the linear regulator will clean its output from any noise the switching regulator might have introduced. 



Because there will be two outputs, which one is a fixed 5 Volts, there will have to be two switching regulators. To control the adjustable regulator, a digital resistor will be used. The **MCP4017** is a digital POT with I2C control signals and 127 steps. This will control the Feedback line of the regulator controlling its output. **LMR14006** step-down switching regulator works by keeping 0.765 Volts on the feedback pin [which is connected to a voltage divider connected to the output]. As for the fixed 5 Volts, a LMR14006 with a fixed voltage divider that takes 5 volts and divides to 0.765 volts [the wanted voltage on the feedback pin]. 



### Output Stage

The fixed 5 volts noise can be cleaned by the onboard regulator on the Arduino or Beaglebone. But the adjustable voltage will have linear regulator. **LM317** can go all the way to zero volts and it is controlled by a single resistor. To overcome the reference deviation due to temperature one uses another LT3085. 





