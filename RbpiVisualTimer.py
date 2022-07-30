from blinkt import set_pixel, clear, set_all, show, NUM_PIXELS, get_pixel, set_brightness, set_clear_on_exit
from random import randint
from multiprocessing import Process
import time


# Constants
MINUTE = 60
COLOR_MAX = 255
STEP = 5

class Timer:
    '''
    A visual timer for the Raspberry pi Blinkt led strip
    
    PROPERTIES
    - Properties should be changed when timer on stop state to have efect on the next start()
    
    brightness:
    Led brightness as a float in the range [0,1]
    
    session_duration:
    Session duration in minutes
    
    change_duration:
    Time between sessions in seconds
    
    timer_version:
    Colors to create the timer gradient 
    1 - Green/Red version
    2 - Blue/Red version
    
    standby_version:
    1 - Random Colors
    2 - Color Loop
    '''
    
    # Leds Brightnes ()
    brightness = 0.1
    
    # Session duration in minutes
    session_duration = 0.5
    
    # Change duration in seconds
    change_duration = 0.5
    
    # Timmer Version
    timer_version = 1
    
    # Standby version
    standby_version = 1
    
    # The process lauched to avoid bloking of the shell
    process = 0
    
    
    def __init__(self):
        set_brightness(self.brightness)
        set_clear_on_exit(True)
        self.process = Process(target = self.randomColors)
        self.process.start()
        print('Timer activated')
        return


    def outSignal(self):
        beginning = int(time.time())
        while(int(time.time())-beginning < self.change_duration/2):
            set_all(COLOR_MAX,0,0)
            show()
            time.sleep(0.3)
            clear()
            show()
            time.sleep(0.3)
        clear()
        show()
        return
    
    
    def inSignal(self,color):
        beginning = int(time.time())
        while(int(time.time())-beginning < self.change_duration/2):
            if color == 2:
                set_all(0,0,COLOR_MAX)
            else:
                set_all(0,COLOR_MAX,0)
            show()
            time.sleep(0.3)
            clear()
            show()
            time.sleep(0.3)
        clear()
        show()
        return
    
    
    def start(self):
        """start a loop of infinite timers"""
        self.process.terminate()
        clear()
        show()
        self.process = Process(target=self.session,args=[self.timer_version])
        self.process.start()
        return
    
    
    def stop(self):
        """Enter standby mode"""
        self.process.terminate()
        clear()
        show()
        if self.standby_version == 2:
            self.process = Process(target = self.colorLoop)
            self.process.start()
        else:
            self.process = Process(target = self.randomColors)
            self.process.start()
        return
     

    def end(self):
        """Clear leds"""
        self.process.terminate()
        clear()
        show()
        return


    def session(self,version):
        """A session of timer loops"""
        while True:
            self.inSignal(version)
            for i in range(NUM_PIXELS):
                if version == 2:
                    set_pixel(i,i*(COLOR_MAX//(NUM_PIXELS-1)),0,COLOR_MAX-(i*(COLOR_MAX//(NUM_PIXELS-1))))
                else:
                    set_pixel(i,i*(COLOR_MAX//(NUM_PIXELS-1)),COLOR_MAX-(i*(COLOR_MAX//(NUM_PIXELS-1))),0)
                show()
                time.sleep((self.session_duration*MINUTE)//NUM_PIXELS)
            self.outSignal()


    def randomColors(self):
        """Random colors on random leds"""
        clear()
        show()
        while True:
            led = randint(0,NUM_PIXELS-1)
            r = randint(0,255)
            g = randint(0,255)
            b = randint(0,255)
            set_pixel(led,r,g,b)
            show()


    def colorLoop(self):
        clear()
        show()
        color = {'red': COLOR_MAX,'green':0,'blue':0}
        self.process = Process()
        for i in range(NUM_PIXELS):
            set_pixel(i,color['red'],color['green'],color['blue'])
        show()
        # Calculate next color
        while True:
            if color['red'] == COLOR_MAX:
                if color['blue'] > 0:
                    color['blue'] -=STEP
                else:
                    if color['green'] < COLOR_MAX:
                        color['green'] +=STEP
                    else:
                        color['red'] -= STEP
            if color['green'] == COLOR_MAX:
                if color['red'] > 0:
                    color['red'] -= STEP
                else:
                    if color['blue'] < COLOR_MAX:
                        color['blue'] += STEP
                    else:
                        color['green'] -= STEP
            if color['blue'] == COLOR_MAX:
                if color['green'] > 0:
                    color['green'] -= STEP
                else:
                    if color['red'] < COLOR_MAX:
                        color['red'] += STEP
                    else:
                        color['blue'] -= STEP
            for i in range(NUM_PIXELS-1):
                pixel = get_pixel(i+1)
                set_pixel(i,pixel[0],pixel[1],pixel[2])
            set_pixel(NUM_PIXELS-1,color['red'],color['green'],color['blue'])
            show()