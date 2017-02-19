from core.ledcontrol import RGB

OPS_MSG = {
    'good': None,
    'warn': None,
    'bad': None,
}

# Th
R = 27
G = 22
B = 17

class LEDAlert:

    control = None

    def __init__(self, pin_r, pin_g, pin_b):
        self.control = RGB(pin_r, pin_g, pin_b)

    def setup(self):
        OPS_MSG['good'] = self.good
        OPS_MSG['warn'] = self.warn
        OPS_MSG['bad'] = self.bad

    def good(self): 
        """ Everything is swell """

        if self.control:
            # Set LEDs to green
            self.control.transition_decimal(0, 255, 0)

    def warn(self): 
        """ Everything could be better """

        if self.control:
            # Set LEDs to yellow
            self.control.transition_decimal(0, 255, 255)

    def bad(self): 
        """ Everything sucks hard """

        if self.control:
            # Set LEDs to yellow
            self.control.transition_decimal(255, 0, 0)