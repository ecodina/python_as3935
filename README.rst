Welcome to python_as3935!
=========================

This Python module let’s you control the AS3935 lightning detector. The
board used is the MOD-1016 from
`EmbeddedAdventures <http://www.embeddedadventures.com/as3935_lightning_sensor_module_mod-1016.html>`__.

1. It works with `Pigpio <http://abyz.me.uk/rpi/pigpio/>`__ instead of
   the common `RPi.GPIO <https://pypi.org/project/RPi.GPIO/>`__, in
   order to be able to use it without being root.
2. The communication with the device is done via I2C serial protocol.
3. It allows you to perform every action described in the
   `datasheet <http://www.embeddedadventures.com/datasheets/AS3935_Datasheet_EN_v2.pdf>`__.

To install it from Pypi:

::

   $ pip install as3935

1. Connection of the device
===========================

If using a `40-pin
GPIO <https://www.raspberrypi.org/documentation/usage/gpio/>`__
Raspberry Pi, the device should be connected as follows:

+---------------+--------------------+------------------+
| Pin on AS3935 | Pin name on RPi    | Pin number (BCM) |
+===============+====================+==================+
| Vcc           | 3.3V               | Any              |
+---------------+--------------------+------------------+
| IRQ           | Any available GPIO | e.g. 4           |
+---------------+--------------------+------------------+
| SCL           | Clock              | 3                |
+---------------+--------------------+------------------+
| SDA           | Data               | 2                |
+---------------+--------------------+------------------+
| GND           | Ground             | Any              |
+---------------+--------------------+------------------+

2. Requisites
=============

2.1 Pigpio
----------

Install the Pigpio daemon, either from source or via:

::

   $ sudo apt install pigpio

Configure *Remote GPIO* using (if on Raspbian):

::

   $ sudo raspi-config

Enable the daemon and start it now:

::

   $ sudo systemctl enable pigpiod
   $ sudo systemctl start pigpiod

Install the `Python interface <https://pypi.org/project/pigpio/>`__:

::

   $ pip install pigpio

For further information, visit
`Pigpio’s <http://abyz.me.uk/rpi/pigpio/pigpiod.html>`__ webpage.

2.2 Python
----------

This module has been tested on Python 3.7. It might work on other
versions as well. The only library used, a part from *Pigpio*, is *time*

3. Usage
========

It is very simple to use. Just import it and create a new object with
the configuration you need.

::

   import as3935
   import pigpio
       
   irq_pin_number = 4    # BCM number (code after GPIO)
   bus = 1               # On newer Raspberrys is 1
   address = 0x03        # If using MOD-1016 this is the address

   sensor = as3935.AS3935(irq_pin_number, bus, address)

   # We need to calibrate the sensor first. Use the tuning cap provided
   # or calculate it using sensor.calculate_tuning_cap(*args)
   sensor.full_calibration(12)

   sensor.set_indoors(True)

   # Every time you sense a pulse on IRQ it means there is an
   # interruption request. You can read it like this:
   def irq_callback(gpio, level, tick):
       interruption = sensor.get_interrupt()
       if interruption == as3935.INT_NH:
           print("Noise floor too high")
       elif interruption == as3935.INT_D:
           print("Disturbance detected. Mask it?")
       elif interruption == as3935.INT_L:
           print("Lightning detected!")
           distance = sensor.get_distance()

   try:
       cb = sensor.pi.callback(irq_pin_number, pigpio.RISING_EDGE, irq_callback)
       while True:
           pass
   finally:
       cb.cancel()
       sensor.pi.stop()

This above is a very simple example. Check the full documentation to
learn all the methods you can call.

4. Credits
==========

Created by Eloi Codina during December 2019. There are other Python
modules that allow you to use the AS3935 sensor. However, none of them
use Pigpio It is licensed under the GNU General Public License v3.0
(please read LICENSE.txt)

::

       python_AS3935
       Copyright (C) 2019  Eloi Codina Torras

       This program is free software: you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation, either version 3 of the License, or
       (at your option) any later version.

       This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

       You should have received a copy of the GNU General Public License
       along with this program.  If not, see <https://www.gnu.org/licenses/>.

5. Full documentation
=====================

5.1 Constants (interruptions)
-----------------------------

-  *INT_NH*: noise level too high
-  *INT_D*: man-made disturbance detected
-  *INT_L*: lightning detected

5.2 Class AS3935
----------------

It provides an object to control the AS3935.

-  **irq**: (int) GPIO pin number the IRQ is connected at (BCM number)
-  **bus**: (int, optional) the bus the AS3935 is connected at. Default
   = 1
-  **address**: (int, optional) the address of the AS3935. Default =
   0x03

You can access the following properties from this object:

-  **address**: the address of the AS3935
-  **bus**: the bus of the AS3935
-  **irq**: the GPIO pin number the IRQ is connected at
-  **pi**: pigpio.pi instance. You can communicate with the GPIO with
   this.
-  **i2c_device**: an integer representing the connection with the
   AS3935

5.2.1 Methods
~~~~~~~~~~~~~

5.2.1.1 Cross methods
^^^^^^^^^^^^^^^^^^^^^

::

   read_byte(self, address)
         
        Returns the value of the byte stored at address.
          
         :param address: (int) the address to read from  
         :return: (int) the value of the address  

::

   write_byte(self, address, value)
         
        Writes value at address. Raises ValueError if the value is not correct. It sleeps for 2 ms after writing the value
          
         :param address: (int) the address to write to  :param value: (int) the byte value (between 0x00 and 0xFF) 

::

   full_calibration(self, tuning_cap):  
       
        Performs a full calibration: antenna and RCO  
        
         :param tuning_cap: int: tuning number for the antenna. Can be calculated with self.calculate_tuning_cap() 

5.2.1.3 Operating modes
^^^^^^^^^^^^^^^^^^^^^^^

::

   power_down_mode(self):    
     
      Sets the AS3935 on power down mode (PWD) 

::

   listening_mode(self) 
       
        Sets the AS3935 on listening mode (PWD) 

5.2.1.3 Direct commands
^^^^^^^^^^^^^^^^^^^^^^^

::

   set_default_values(self) 
       
        Sends a direct command to 0x3C to reset to default values. 

::

   calibrate_rco(self)  
       
        Sends a direct command to 0x3D to calibrate the RCO (CALIB_RCO) 

5.2.1.4 AFE and Watchdog
^^^^^^^^^^^^^^^^^^^^^^^^

::

   get_indoors(self)
       
        Checks whether the device is configured to be run indoors. (AFE_GB)  
        
         :return: (bool) whether the device is configured to be run indoors  

::

   set_indoors(self, indoors)
       
        Configures the device to be run indoors or outdoors. (AFE_GB)  
        
         :param indoors: (bool) configure the AS3935 to be run indoors 

::

   get_watchdog_threshold(self)
       
        Returns the watchdog threshold (WDTH)  
        
         :return: (int) the current watchdog threshold  

::

   set_watchdog_threshold(self, value=0b0001):  
         
        Sets the watchdog threshold to value (WDTH). If called without parameters, it sets it to the default configuration. Can raise a ValueError if not 0 <= value <= 0b1111  
        
         :param value: (int, optional) The value to be set. From 0b0000 to 0b1111. Default=0b0001  

5.2.1.5 Noise floor generator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   get_noise_floor(self)
         
        Checks the current noise floor threshold (NF_LEV).  
        
         :return: (int) the current noise floor threshold  

::

   set_noise_floor(self, noise_floor=0b010) 
         
        Sets a new noise floor threshold (NF_LEV). If called without parameters, it sets it to the default configuration. Can raise a ValueError if not 0 <= noise_floor <= 0b111  
       
         :param noise_floor: (int, optional) The value to be set. From 0b000 to 0b111

::

   lower_noise_floor(self, min_noise=0b000)  
         
        Lowers the noise floor threshold by one step (subtracts 1 to the current NF_LEV) if it is currently higher than min_noise. Can raise a ValueError if not 0 <= min_noise <= 0b111  
        
         :param min_noise: (int, optional) the minimum NF_LEV the device should be set at. Default = 0b000  :return: (int) the new noise floor threshold 

::

   raise_noise_floor(self, max_noise=0b111) 
        
        Raises the noise floor threshold by one step (adds 1 to the current NF_LEV) if it is currently lower than max_noise Can raise a ValueError if not 0 <= max_noise <= 0b111  
        
         :param max_noise: (int, optional) the maximum  NF_LEV the device should be set at. Default 0b111  :return: (int) the new noise floor threshold  

#### 5.2.1.6 Signal validation

::

   get_spike_rejection(self) 
       
        Checks the current spike rejection settings (SREJ)  
        
         :return: (int) the current spike rejection setting (SREJ)  

::

   set_spike_rejection(self, value=0b0010)  
       
        Sets a new setting for the spike rejection algorithm (SREJ). If the function is called without any parameter, it sets it to the default value of 0b0010 Can raise a ValueError if not 0 <= value <= 0b1111  
        
        :param value: (int, optional) the value to set SREJ. Default = 0b0010 

5.2.1.7 Energy calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   get_energy(self)  
         
        Checks the last lightning strike's energy calculation. It does not have any physical meaning. (Energy of the Single Lightning *SBYTE)  
        
         :return: (int) last strike's energy 

#### 5.2.1.8 Distance estimation

::

   def get_distance(self)  
        
        Checks the estimation of the last lightning strike's distance in km (DISTANCE).  
        
         :return: (int/None) last strike's distance in km. None if out of range, 0 if overhead  

::

   get_interrupt(self)  
       
        Checks the reason of the interruption (INT). To know what it is, use the constants: INT_NH: noise level too high INT_D: disturber detected INT_L: lightning strike detected  
        
        It sleeps for 2 ms before retrieving the value, as specified at the datasheet.  
        
         :return: (int) the interruption reason  

::

   set_mask_disturber(self, mask_dist)
       
        Sets whether disturbers should be masked (MASK_DIST).  
        
         :param mask_dist: (bool) whether disturbers should be masked 

::

   get_mask_disturber(self)
       
        Checks whether disturbers are currently masked (MASK_DIST).  
        
         :return: (bool) whether disturbers are currently masked  

::

   get_min_strikes(self)
       
        Checks the current configuration of how many strikes AS3935 has to detect in 15 minutes to issue an interrupt (MIN_NUM_LIG). In case of an error, it raises a LookupError  
        
         :return: (int) number of strikes. Possible values: 1, 5, 9, 16

::

   set_min_strikes(self, min_strikes)  
       
        Sets the minumum number of lightning strikes the AS3935 has to detect in 15 minutes to issue an interrupt (MIN_NUM_LIG). Can raise a ValueError if min_strikes is not an accepted value.  
        
         :param min_strikes: (int) min number of strikes to issue an interrupt. Possible values: 1, 5, 9, 16 

::

   clear_lightning_stats(self)
           
        Clears the statistics built up by the lightning distance estimation algorithm (CL_STAT) 

#### 5.2.1.10 Antenna tunning

::

   get_display_lco(self)  
       
        Checks whether the antenna resonance frequency is currently displayed on the IRQ pin (DISP_LCO)  
        
         :return: (bool) whether the antenna resonance frequency is currently displayed

::

   set_display_lco(self, display_lco)  
         
        Sets whether the antenna resonance frequency should be displayed on the IRQ pin(DISP_LCO).  
        
         :param display_lco: (bool) whether the antenna resonance frequency should be displayed 

::

   set_tune_antenna(self, tuning_cap) 
       
        Sets the antenna calibration. It adds or removes internal capacitors according to tuning_cap (TUN_CAP). If tuning_cap is unknown, this could be calculated by calculate_tuning_cap(self, frequency_divisor, tries_frequency) Can raise a ValueError if not 0 <= tuning_cap <= 15  
        
         :param tuning_cap: (int) the number to calibrate the antenna 

::

   calculate_tuning_cap(self, frequency_divisor=16, tries_frequency=3, seconds_try=4)  
       
        Measures the frequency of the LC resonator for every possible tuning_cap and returns the best value. If possible, use the default values for frequency_divisor, tries_frequency and seconds_try. This function takes a long time. It should take about tries_frequency*seconds_try*16 seconds given that there are 16 tuning possibilities.  
        The ideal frequency is of 500 kHz  
        Can raise ValueError if frequency_divisor is not a valid number.  
        
         :param frequency_divisor: (int) the divisor the AS3935 uses to divide the frequency before displaying it on the IRQ 
         :param tries_frequency: (int) number of times the current frequency is calculated during *seconds_try* seconds to calculate an average  
         :param seconds_try: (float) seconds during which pulses on IRQ will be counted to calculate the internal frequency  
         :return: (int) a tuning number between 0 and 15

::

   calculate_resonance_frequency(self, seconds)  
        
        Sets the AS3935 to display the antenna resonance frequency on the IRQ during *seconds* and counts the number of pulses in this time to calculate the internal frequency. To get the real frequency multiply this value by the frequency divisor ratio.
          
         :param seconds: (int) number of seconds while it should count spikes  :return: (int) internal frequency 

::

   get_frequency_division_ratio(self)  
       
        Gets the current frequency division ratio. Number by which the real antenna resonance frequency is divided to display on the IRQ pin (LCO_FDIV). Can raise a LookupError if there is an error checkig the configuration.  
        
         :return: (int) frequency division ratio. Possible numbers: 16, 32, 64, 128  

::

   set_frequency_division_ratio(self, divisor=16)  
       
        Sets a new frequency division ration by which the antenna resonance frequency is divided to display on the IRQ pin (LCO_FDIV).If called with no parameter, it defaults to 16. Can raise a ValueError if *divisor* is not an accepted number.  
        
         :param divisor: (int, optional) frequency divisor ratio. Accepted values = (16, 32, 64, 128). Default = 16 

5.2.1.11 Clock generation
^^^^^^^^^^^^^^^^^^^^^^^^^

::

   get_display_srco(self) 
       
        Checks whether the SRCO frequency is being displayed on the IRQ pin.  
        
         :return: (bool) whether the SRCO frequency is currently displayed 

::

   set_display_srco(self, display_srco) 
       
        Sets whether the SRCO frequency should be displayed on the IRQ pin.  
        
         :param display_srco: (bool) whether the SRCO frequency should be displayed 

::

   get_display_trco(self)  
       
        Checks' whether the TRCO frequency is being displayed on the IRQ pin. 
         
         :return: (bool) whether the TRCO frequency is currently displayed  

::

   set_display_trco(self, display_trco)  
       
        Sets whether the TRCO frequency should be displayed on the IRQ pin. 
    
         :param display_srco: (bool) whether the TRCO frequency should be displayed  

::

   calibrate_trco(self)  
       
        Calibrates the TRCO by sending the direct command CALIB_RCO and toggling the DIS_TRCO bit (low-high-low) 
