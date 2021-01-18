import RPi.GPIO as GPIO
import os, sys, configparser, threading, json, time, logging,  logging.handlers
from datetime import datetime
from gpiozero import CPUTemperature

LOG_FILENAME = r"/home/pi/fancontrol/fancontrol.log"
CFG_FILE = r"/home/pi/fancontrol/fancontrol.cfg"

# defaults settings
LOG_LEVEL = 0 # UNSET
FAN_PIN = 15
PWM_FREQ = 25
INTERVAL = 5
ON_THRESOLD = 30
TEMPS = [ 1000 ]
SPEEDS = [ 100 ]

#def getTemp():
#    using vcgencmd measure_temp
#    output = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True)
#    temp_str = output.stdout.decode()
#    try:
#        return float(temp_str.split("=")[1].split("\'")[0])
#    except (IndexError, ValueError):
#        raise RuntimeError("Can\'t retrive cpu temp")

def getTemp(): 
    # using gpiozero
    # need: pip install gpiozero
    cpu = CPUTemperature()
    return cpu.temperature

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def loadConfig():
    global FAN_PIN
    global PWM_FREQ
    global INTERVAL
    global ON_THRESOLD
    global LOG_LEVEL
    global logger
    tmp = safe_cast(cfg.get("Settings", "LOG_LEVEL"), int, 0)
    if (tmp != 0):
        LOG_LEVEL = tmp
        logger.setLevel(LOG_LEVEL)
    else:
        logger.warning("Invalid value for 'LOG_VALUE'. Use default")
    tmp = safe_cast(cfg.get("Settings", "GPIO_PIN"), int, 0)
    if (tmp != 0):
        FAN_PIN = tmp
    else:
        logger.warning("Invalid value for 'GPIO_PIN'. Use default")
    tmp = safe_cast(cfg.get("Settings", "PWM_FREQ"), int, 0)
    if (tmp != 0):
        PWM_FREQ = tmp
    else:
        logger.warning("Invalid value for 'PWM_FREQ'. Use default")
    tmp = safe_cast(cfg.get("Settings", "INTERVAL"), int, 0)
    if (tmp != 0):
        INTERVAL = tmp
    else:
        logger.warning("Invalid value for 'INTERVAL'. Use default")
    tmp = safe_cast(cfg.get("Settings", "ON_THRESOLD"), int, 0)
    if (tmp != 0):
        ON_THRESOLD = tmp
    else:
        logger.warning("Invalid value for 'ON_THRESOLD'. Use default")

def loadTemperatures():
    global TEMPS
    global SPEEDS
    global logger
    try:
        TEMPS = json.loads(cfg.get("Temperatures", "Temps"))
    except:
        logger.warning("Invalid value for 'Temps'. Use default")
    try:
        SPEEDS = json.loads(cfg.get("Temperatures", "Speeds"))
    except:
        logger.warning("Invalid value for 'Speeds'. Use default")

def checkTemp():
        # vars
        global ON_THRESOLD
        global TEMPS
        global SPEEDS
        global fanRunning
        global logger
        global fan
        global prevDC
        currDC = 100                # fall back
        currTemp = int(getTemp())   # get temperature

        # switch on/off depending by ON_THRESOLD
        if currTemp >= ON_THRESOLD and not fanRunning:
            logger.info("FAN --> ON")
            fan.start(100)
            prevDC = 100
            fanRunning = True
        elif currTemp < ON_THRESOLD and fanRunning:
            logger.info("FAN --> OFF")
            fan.stop()
            prevDC = 0
            currDC = 0
            fanRunning = False

        # if running, set DutyCycle
        if fanRunning:
            for i in range(0, len(TEMPS) - 1):
                if currTemp < TEMPS[i]:
                    currDC = SPEEDS[i]
                    break

            if (currDC != prevDC):
                logger.info(f"CHANGE DUTY-CYCLE: {prevDC} --> {currDC}  ({currTemp}°C)")
                fan.ChangeDutyCycle(100)
                time.sleep(1)
                fan.ChangeDutyCycle(currDC)
                prevDC = currDC

            logger.debug(f"CPU TEMP: {currTemp}°C FAN: {fanRunning} ({currDC})")
        else:
            logger.debug(f"CPU TEMP: {currTemp}°C FAN: {fanRunning}")

try:
    prevDC = 0
    fanRunning = False
    cleanupGPIO = False
    # setup log
    logger = logging.getLogger("FanByTempLog")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=3)
    logger.addHandler(handler)
    logger.info(f'{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} Service startup ...')

    # load config file
    if os.path.exists(CFG_FILE):
        logger.debug(f"Loading settings from '{CFG_FILE}'")
        cfg = configparser.RawConfigParser()
        cfg.read(CFG_FILE)
        # load Settings
        loadConfig()
        # load currTemperatures
        loadTemperatures()
    else:
        logger.debug("No settings file. Use defaults.")    

    # setup GPIO
    logger.debug(f"Setup GPIO (PIN {FAN_PIN})")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, 25)
    cleanupGPIO = True
    
    # start work
    logger.info("Service running ...")
    checkTemp()
    while True:
        # not run every INTERVAL but almost
        thread = threading.Timer(INTERVAL, checkTemp)  
        thread.daemon = True # stop if the program exits
        thread.start()
        thread.join()

except Exception as e:
    logger.critical(f"Exception: {str(e)}")
finally:
    logger.info(f"Service stopped. {cleanupGPIO}")
    if cleanupGPIO:
        GPIO.cleanup()
