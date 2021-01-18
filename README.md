# Raspberry - PwmFanControl

Phyton script that monitors the temperature and adjusts the speed of the cooling fan.  
For Raspberry and 5V FAN.

Davide Mencarelli - d.mencarelli@outlook.com  
First release: **18/01/2021**  

## Notes

Script for Raspberry Pi  
Required modules: RPi, gpiozero (*pip install gpiozero*)  
The phyton file is **fan_by_pwm.py**  
Script for **Phyton 3.7+**  
Configuration file: **fancontrol.cfg**  
Optional: copy **fancontrol.sh** in **/etc/init.d/** for starting at boot

## Configuration

### LOG_LEVEL

Logging messages which are less severe than level will be ignored (**/fancontrol.log**)  
CRITICAL&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;50  
ERROR&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;40  
WARNING&nbsp;&nbsp;&nbsp;&nbsp;30  
INFO&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;20  
DEBUG&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;10  

### PWM_FREQ

GPIO PWM Frequency

### GPIO_PIN

The GPIO PIN connect to the base of the transistor

### INTERVAL

Each x seconds check the CPU Temperature

### ON_THRESOLD

Above this temperature the FAN starting.  
When under FAN stop.

### Temps and Speed

This two array indicate temperature inteval and fan speed to set.  

Example:  
Temps:  [ 45, 55, 9999 ]  
Speeds: [ 50, 75, 100 ]  

ON_THRESOLD < T < 45 => SPEED 50%  
45 < T < 55&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=> SPEED 75%  
55 < T < 9999&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=> SPEED 100%  

## Eletronic

+5V to the FAN  
GPIO_PIN to the base of 2N222 transistor  
GND to the collector of 2N222 transistor  
Emitter of 2N222 transistor to GND of the FAN  
