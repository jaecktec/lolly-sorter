# main.py -- put your code here!
import time
import hardware
import math

colors = {
    'YELLOW': (112, 101, 90),
    'RED':  (124, 81, 98),
    'ORANGE': (127, 87, 90),
    'BLUE': (94, 95, 122),
    'GREEN': (108, 105, 99),
    'PURPLE': (111, 87, 114),
    'BROWN': (113, 95, 104),
    'EMPTY': (82, 103, 125)
}

trays = {
    'YELLOW': 0,
    'RED':  1,
    'ORANGE': 2,
    'BLUE': 3,
    'PURPLE': 4,
    'GREEN': 5,
    'BROWN': 6
}


def find_closest_color(measurement):
    global colors
    min_distance = float('inf')
    closest_color = None
    
    for color_name, color_rgb in colors.items():
        r_diff = measurement[0] - color_rgb[0]
        g_diff = measurement[1] - color_rgb[1]
        b_diff = measurement[2] - color_rgb[2]
        
        distance = math.sqrt(r_diff**2 + g_diff**2 + b_diff**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    
    return (min_distance, closest_color)


def sort_n(n: int):
    for i in range(n):
        hardware.collect()
        measurement = hardware.measure()
        (distance, closest) = find_closest_color(measurement)
        print(f"detected color {closest} with distance {distance}")
        if(closest == 'EMPTY'): 
            break
        hardware.deposit(trays[closest])

def measure_n(n: int):
    for i in range(n):
        print(hardware.measure())