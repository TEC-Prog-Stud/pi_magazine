import RPi.GPIO as GPIO
import time, sys, pygame

trigger_pin_left = 8
echo_pin_left = 7
trigger_pin_right = 18
echo_pin_right = 23

green = (0,255,0)
orange = (255,255,0)
red = (255,0,0)
white = (255,255,255)
black = (0, 0, 0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin_left, GPIO.OUT)
GPIO.setup(echo_pin_left, GPIO.IN)
GPIO.setup(trigger_pin_right, GPIO.OUT)
GPIO.setup(echo_pin_right, GPIO.IN)

def send_trigger_pulse(pin):
    GPIO.output(pin, True)
    time.sleep(0.0001)
    GPIO.output(pin, False)

def wait_for_echo(pin, value, timeout):
    count = timeout
    while GPIO.input(pin) != value and count > 0:
        count -= 1

def get_distance(trigger_pin, echo_pin):
    send_trigger_pulse(trigger_pin)
    wait_for_echo(echo_pin, True, 10000)
    start = time.time()
    wait_for_echo(echo_pin, False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len / 0.000058
    return (int(distance_cm))
    
def colour_for_distance(distance):
    if distance < 30:
        return red
    if distance < 100:
        return orange
    else:
        return green
    
pygame.init()
size = width, height = 800, 600
offset = width / 8

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 50)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            GPIO.cleanup() 
            sys.exit()
        
    left_distance = get_distance(trigger_pin_left, echo_pin_left)
    right_distance = get_distance(trigger_pin_right, echo_pin_right)
    
    screen.fill(white)
    pygame.draw.rect(screen, colour_for_distance(left_distance), (offset, 0, width / 4, left_distance*5))
    pygame.draw.rect(screen, colour_for_distance(right_distance), (width / 2 + offset, 0, width / 4, right_distance*5))
    left_label = myfont.render(str(left_distance)+" cm", 1, black)
    screen.blit(left_label, (offset + 10, height/2))
    right_label = myfont.render(str(right_distance)+" cm", 1, black)
    screen.blit(right_label, (width/2 + offset + 10, height/2))
    pygame.display.update()
    time.sleep(0.1)

