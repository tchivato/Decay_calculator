


<<<CONTENTS>>>

1. Introduction
2. Setup
3. Operation
4. Troubleshooting
5. References



1. Introduction:

Veenstra's VDC-404 dose calibrator does not have a decay function, operator must use formulas or decay tables to calculate decay.

The Raspberry pi serves as a computer programmed to see in real time the isotope and activity value from the dose calibrator, accept a new time introduced by the operator and show in a display the resulting activity at said time. This eases the operator tasks and reduces errors.

It is programmed for the following isotopes: 99mTc, 123I, 131I, 67Ga, 90Y, 51Cr, 111In and 18F.




2. Setup:

Material list:
-Veenstra VDC-404 dose calibrator:
-Raspberry pi with case. Preferred model is the Zero WH (size and price).
-Micro USB 5V 2.5A power supply.
-Micro SD class 10 card with at least 8 GB loaded with Raspbian.
-Female to female dupont cables:

-Male to female RS232 DB9 null modem cable, without handshake. Male RS232 to male USB, preferably with FTDI chipset.
OR
-Male RS232 to TTL (only option for Raspberry Zero).

-Male to male or female to female RS232 adaptors if the former connectors are not the specified gender.
-USB keypad.
-16x2 LCD with I2C interface.

Boot up the Raspberry pi and enable serial and I2C interface in the configuration menu. 

Install the necessary python 3 modules (1).

Copy the decay.py script into pi directory and modify bashrc to make it run on boot.(2)

Connect the LCD and the RS232 cable or adapter following the schematic provided.

Connect the keypad and the power supply.

Set the RS232 option in the dose calibrator to "PC" and connect it to the Raspberry.




3. Operation:

Boot the Raspberry and wait for the script to load.

Since it has no battery the Raspberry will ask the user to update the time whenever it its switched off. Input time as hhmm and <intro>.

LCD will show the dose calibrator information: isotope, activity, units and real time in lower right corner.

Operator may introduce a new reference time as hhmm. The program will calculate the resulting activity and display it in the LCD. The new time introduced will show up in the upper right corner of the LCD.

The reference time can be changed again at will. If the keypad is not used in several minutes the display is turned off until a key is pressed.

NOTES:
-The only input accepted by the Raspberry is the time to calculate the decay. Other functions must be done from the dose calibrator itself (changing isotope, units etc).
-Decay is only calculated on the present day, between 00:00 and 24:00. It can calculate forward and backwards in time.
-It is important to check if the real time is accurate so the calculated activity is correct. Pressing <-> allows the user to readjust the real time.
-It is advisable not to turn off the Raspberry unless necessary to prevent data corruption on the SD card. Advanced users may modify log writing on the Raspberry to reduce the card wearing over time.(3)  




4. Troubleshooting:

The 9 pins RS232 cable must be null modem without handshake (just pins 2 and 3 crossed over and pin 5 to ground). Most widespread cables are parallel and will not work since both the dose calibrator and the Raspberry are terminals. It is also not compatible with partial or total handshake, they will cause the dose calibrator to reset.

If there is a malfunction, check that all connections are tight and reset the Raspberry.

If the LCD is blank, adjust its potentiometer to change the contrast.

Most common cause of hardware failure is SD card corruption. Format the card if needed and set it up again or change it for a new card.

As a last option, change the Raspberry.




5. References:

-Veenstra VDC-404 user manual.
-https://github.com/raspberrypi/documentation/blob/master/installation/README.md
-https://github.com/raspberrypi/documentation/blob/master/linux/README.md

(1)Use pip3 to install the following modules: pyserial, rplcd, smbus. https://help.dreamhost.com/hc/en-us/articles/115000699011-Using-pip3-to-install-Python3-modules
(2)Run on boot (bashrc): http://www.knight-of-pi.org/options-for-autostarting-raspberry-pi-programs-init-d-bashrc-and-cron/
(3)Read only mode: http://hallard.me/raspberry-pi-read-only/

tchivato@hotmail.com




<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Dose calibrator decay calculator</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Tomás Chivato</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/tchivato/Decay_calculator" rel="dct:source">https://github.com/tchivato/Decay_calculator</a>.
