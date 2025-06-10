#-------------------------------------#
#-------Year 8 STEM Enhancement-------#
#----------Peter Saaksjarvi-----------#
#------------31/01/2024---------------#

from machine import Pin, SPI
import max7219
import utime

# LED matrix setup
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 1)
display.brightness(3)

# Ultrasonic sensor setup
TRIGGER_PIN = 13
ECHO_PIN = 12
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
onboard_led = Pin("LED", Pin.OUT)

# Constants
GOAL_THRESHOLD_DISTANCE = 21
MAX_GOALS = 99
GOAL_DELAY_SECONDS = 1
SPEED_OF_SOUND = 0.0343

# Initialize the scoreboard
score = 0

# LED matrix digit patterns
DIGIT_ZERO = ((1, 1, 1), (1, 0, 1), (1, 0, 1), (1, 0, 1), (1, 1, 1))
DIGIT_ONE = ((0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0))
DIGIT_TWO = ((1, 1, 1), (0, 0, 1), (1, 1, 1), (1, 0, 0), (1, 1, 1))
DIGIT_THREE = ((1, 1, 1), (0, 0, 1), (1, 1, 1), (0, 0, 1), (1, 1, 1))
DIGIT_FOUR = ((1, 0, 1), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 0, 1))
DIGIT_FIVE = ((1, 1, 1), (1, 0, 0), (1, 1, 1), (0, 0, 1), (1, 1, 1))
DIGIT_SIX = ((1, 1, 1), (1, 0, 0), (1, 1, 1), (1, 0, 1), (1, 1, 1))
DIGIT_SEVEN = ((1, 1, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1))
DIGIT_EIGHT = ((1, 1, 1), (1, 0, 1), (1, 1, 1), (1, 0, 1), (1, 1, 1))
DIGIT_NINE = ((1, 1, 1), (1, 0, 1), (1, 1, 1), (0, 0, 1), (0, 0, 1))

DIGIT_PATTERNS = {0: DIGIT_ZERO, 1: DIGIT_ONE, 2: DIGIT_TWO, 3: DIGIT_THREE,
                  4: DIGIT_FOUR, 5: DIGIT_FIVE, 6: DIGIT_SIX, 7: DIGIT_SEVEN,
                  8: DIGIT_EIGHT, 9: DIGIT_NINE}

def show_number(display, number):
    display.fill(0)
    tens, ones = split_digits(number)
    draw_number(display, tens, ones)

def draw_number(display, tens, ones):
    if tens > 0:
        draw_digit(display, tens, 0)
    draw_digit(display, ones, 5)

def draw_digit(display, digit, offset):
    for row, pattern_row in enumerate(DIGIT_PATTERNS.get(digit, ((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)))):
        for col, pixel in enumerate(pattern_row):
            display.pixel(col + offset, row, pixel)

def split_digits(number):
    tens = number // 10 # floor division
    ones = number % 10  # modulo (remainder)
    return tens, ones

def measure_distance():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    
    while echo.value() == 0:
        signaloff = utime.ticks_us()

    while echo.value() == 1:
        signalon = utime.ticks_us()

    timepassed = signalon - signaloff
    distance = (timepassed * SPEED_OF_SOUND) / 2
    #print(distance)
    return distance

# Display initial score
show_number(display, score)
display.show()

#-------------------------------------#
# Main Program
#-------------------------------------#
if __name__ == "__main__":
    # Main  loop
    while True:
        # Perform ultrasonic measurement
        distance = measure_distance()
        #print(distance)
        
        #-------------------------------------#
        # SCORING LOGIC
        #-------------------------------------#
        # if distance is less than the threshold distance
        if distance < GOAL_THRESHOLD_DISTANCE:
            # increase the score to equal score plus one (or two--your choice)
            score = min(score + 1, MAX_GOALS)
            # show the number (using display and score as parameters)
            show_number(display, score)
            # show the display
            display.show()
            # using utime, sleep for a small amount to prevent multiple goals
            utime.sleep(GOAL_DELAY_SECONDS)

            ## If the score equals the maximum goals allowed set scores back equal to zero
            if score == MAX_GOALS:
                score = 0

        # Sleep for a short time before the next measurement
        utime.sleep_ms(50)  # Adjust this to control the counter speed
