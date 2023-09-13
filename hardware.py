# boot.py -- run on boot-up

from machine import Pin,PWM
from time import sleep,sleep_ms,ticks_ms,ticks_cpu


POS_DEPO_EXIT = 45
POS_DEPO_COLLECT = 95
POS_DEPO_MEASURE = 65

POS_RETREIVE_MIN = 60
POS_RETREIVE_MAX = 104

COLOR_S2 = Pin(0, Pin.OUT)
COLOR_S3 = Pin(4, Pin.OUT)
COLOR_OUT = Pin(2, Pin.IN, Pin.PULL_UP)
COLOR_FREQ_COUNT = 0

servo_1 = PWM(Pin(14, mode=Pin.OUT))
servo_2 = PWM(Pin(12, mode=Pin.OUT))

servo_1.freq(50)
servo_2.freq(50)

def __count_freq(p):
    global COLOR_FREQ_COUNT
    COLOR_FREQ_COUNT += 1

COLOR_OUT.irq(handler=__count_freq, trigger=Pin.IRQ_FALLING)

def __move_servo(servo: PWM, duty: int, delay_ms: int = 500):
    servo.duty(duty)
    sleep_ms(delay_ms)
    servo.duty(0)
    

def collect():
    __move_servo(servo_1, POS_DEPO_COLLECT)
    for _ in range(10):
        __move_servo(servo_1, POS_DEPO_COLLECT + 2, 50)
        __move_servo(servo_1, POS_DEPO_COLLECT - 4, 50)
    __move_servo(servo_1, POS_DEPO_COLLECT)

def measure():
    __move_servo(servo_1, POS_DEPO_MEASURE)
    return read_sensor()
    


def deposit(tray: int):
    
    if(tray == 0): __move_servo(servo_2, 60) 
    elif(tray == 1): __move_servo(servo_2, 70) 
    elif(tray == 2): __move_servo(servo_2, 83) 
    elif(tray == 3): __move_servo(servo_2, 95) 
    elif(tray == 4): __move_servo(servo_2, 106) 
    elif(tray == 5): __move_servo(servo_2, 116) 
    elif(tray == 6): __move_servo(servo_2, 126) 
    else: print(f"we don't have tray {tray}")

    sleep_ms(250)
    __move_servo(servo_1, POS_DEPO_EXIT)

def _read_sensor():
    global COLOR_FREQ_COUNT
    COLOR_FREQ_COUNT = 0
    sleep_ms(100)
    return COLOR_FREQ_COUNT


def read_sensor():
    COLOR_S2.off()
    COLOR_S3.off()
    red = _read_sensor()

    COLOR_S2.on()
    COLOR_S3.on()
    green = _read_sensor()

    COLOR_S2.off()
    COLOR_S3.on()
    blue = _read_sensor()

    total = red + green + blue
    red = red / total
    green = green / total
    blue = blue / total

    red = red * 1.2
    green = green * 1.2
    blue = blue * 1.2

    return (
        int(red * 255),
        int(green * 255),
        int(blue * 255)
    )

