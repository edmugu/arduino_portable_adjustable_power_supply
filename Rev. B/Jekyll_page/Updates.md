---
layout: default
title: Rev. B Updates
nav_order: 2
parent: Rev. B
---

After debugging the Rev A board, I noted that at the moment there was no IC sold in Digi key that could output over >13 amps **with the same package** [check page "Rev. A / Design Flaws" page for explanation ] . That is when I realized that voltage controllers are more upgradeable than voltage regulators. The reason is that a voltage regulator is a voltage controller WITH a power transistor and current sense mechanism. So if you want to upgrade your voltage controller power supply to handle more power you just have to update the power transistor and/or current sense mechanism.  And if you want to upgrade a voltage regulator, you just hope there is a IC with the same package that meets your requirements. 

Also, while design Rev A board, I did not realized that the final linear voltage regular used **LM317** is very inefficient since it requires at least 3-volts difference between the input and the output. That is when I can with the **MIC5157** voltage controller. 



