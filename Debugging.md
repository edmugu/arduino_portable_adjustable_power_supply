---
title: Debugging
has_children: no
nav_order: 30
---

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

