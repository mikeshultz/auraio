from auraio.core.ledcontrol import RGB

OPS_MSG = {
    'good': None,
    'warn': None,
    'bad': None,
    'unknown': None,
}

# Th
R = 27
G = 22
B = 17

class LEDAlert:

    control = None

    def __init__(self, pin_r, pin_g, pin_b, frequency = None):
        self.control = RGB(pin_r, pin_g, pin_b)
        if frequency:
            self.control.set_frequency(frequency)
        self.setup()

    def setup(self):
        OPS_MSG['good'] = self.good
        OPS_MSG['warn'] = self.warn
        OPS_MSG['bad'] = self.bad
        OPS_MSG['unknown'] = self.unknown

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

    def unknown(self): 
        """ Everything is odd """

        if self.control:
            # Set LEDs to blue
            self.control.transition_decimal(0, 0, 255)
