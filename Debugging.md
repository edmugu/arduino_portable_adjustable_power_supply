---
title: Debugging
has_children: no
nav_order: 30
---

# Debugging Process
## Bug 1: The voltage of the first stage does not go above vin
After checking that the enable pin was high and that the switching output was doing what it was suppose to be doing, I decided to replace the switch. However, it still showed the same behavior. Vout would reach >30 Volts then it would drop to Vin. Then I checked my sma units on a eval board and they work. At that moment, I started to investigate the second most complicated unit on the first stage, the diode. Then it was clear that the issue was that I installed the diode backwards. However the silkscreen and schematics had the diode on the right orientation. Which meant that the footprint pads of the diode were swapped. 



![board bring up](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/picture%20of%20bringup.PNG  "board bring up")



## Bug 2: The output of the final stage was stuck at 1.8 Volts
Note that the feed back to the last two stages can be selected between a "fixed" voltage divided that would allow the output go all the way to 27 volts. Or it can be selected to be the dynamic feedback circuit that would keep the voltage of the last two stages close to each other. The circuit worked fine when the fixed voltage divider was used however it got stuck at 1.8 volts when it was switch to the dynamic feedback. At that moment, the feedback circuit was set to have 0.8 Volts difference between the two stages. And indeed there was a 0.8 volt difference between the stages. So I though that may be if I raised the difference to 5 volts it would work. Luckily, it did and after looking for an explanation I noted that the linear regulator needed at least 3 volts difference between its output and its input. 
	
## Bug 3: The output can only drive <1 mA before it starts to struggle. 
I believed this is due to the sma capacitors. However I noted that this issue went away if I lowered the voltage the minimum voltage of 1.2V and then raised to the wanted voltage. So it seems that the step-down switch and regulator had issues if the initial load was too much. So I decided to make prototype out of evaluation boards to check this behavior because my board already had a compromising rework on the schottky diodes. When I characterized the prototype it was only able to output 5 Watts when the design should have had been able to handle >10 Watts. 

A few notes on the prototype: 
	(1) the evaluation board of the step down circuit is for the LMR14006 component but it has the same pin out as the AOZ1282. So the unit was swapped.
	(2) the wires used are size AWG 20 and they are able to handle 1.5 amps, this should not be limiting factor, yet. 
	
![prototype out of eval boards](https://raw.githubusercontent.com/edmugu/arduino_adjustable_power_supply/master/documentation/snippets/debugging.PNG  "prototype out of eval boards")


