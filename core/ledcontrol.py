import re, time, sys, pigpio

gpio = pigpio.pi()

# Our RGB to RPi pinout
R = 27
G = 22
B = 17

INTERVAL = 0.1
TRANSITION_STEPS = 20

re_rgb_hex = r'#*([A-Fa-f0-9]{1,2})([A-Fa-f0-9]{1,2})([A-Fa-f0-9]{1,2})'

class InvalidHexString(Exception): pass

class RGB:



    pin_r = -1
    pin_g = -1
    pin_b = -1



    def __init__(self, r_pin, g_pin, b_pin):
        self.pin_r = r_pin
        self.pin_g = g_pin
        self.pin_b = b_pin



    def _normalize_decimal(self, dec):
        """ Normalize a decimal value between 0 and 255 """
        if dec < 0:
            dec = 0
        elif dec > 255:
            dec = 255
        return dec


    def _get_pin(self, pin):
        """ Get the value of the pin's dutycycle """

        if type(pin) != type(int()) or pin < 1 or pin > 40:
            raise InvalidGPIOPin("The GPIO pin number provided is invalid. See https://pinout.xyz/ for available GPIO pins")

        return gpio.get_PWM_dutycycle(pin)



    def _set_pin(self, pin, cycle):
        """ Set the pin to its new value """

        # brief sanity checks
        if type(pin) != type(int()) or pin < 1 or pin > 40:
            raise InvalidGPIOPin("The GPIO pin number provided is invalid. See https://pinout.xyz/ for available GPIO pins")
        if type(cycle) != type(int()) or cycle < 0 or cycle > 255:
            raise InvalidGPIOPin("The duty cycle parmeter is invalid.  It should be between 0 and 255")

        return gpio.set_PWM_dutycycle(pin, cycle)


    def _nextval(self, startv, currentv, endv, step):
        """ Figure out what the next step is """
        # are we there yet?
        if start_r <= current_r <= end_r \
            or end_r <= current_r <= start_r:
            
            # Not sure about this math...
            nxt = current_r + step

            if nxt > 255:
                return 255
            else:
                return nxt



    def set_decimal(self, r, g, b):
        """ Set the color of the LED strip using RCB decimal """

        # Normalize the input
        r = self._normalize_decimal(r)
        g = self._normalize_decimal(g)
        b = self._normalize_decimal(b)

        # Set the color
        self._set_pin(self.pin_r, r)
        self._set_pin(self.pin_g, g)
        self._set_pin(self.pin_b, b)



    def set_hex(self, s):
        """ Sets the color value of the LED strip according to a hex 
            string 
        """

        match = re.match(re_rgb_hex, s)

        if not match:
            raise InvalidHexString("Hex string is invalid.")

        # convert to decimal
        red = int(match.group(1), 16)
        green = int(match.group(2), 16)
        blue = int(match.group(3), 16)

        return self.set_decimal(red, green, blue)

    def transition_decimal(self, r, g, b):
        """ Transition to a color """

        start_r = self._get_pin(self.pin_r)
        start_g = self._get_pin(self.pin_g)
        start_b = self._get_pin(self.pin_b)

        end_r = r
        end_g = g
        end_b = b

        difstep_r = (start_r - end_r) / TRANSITION_STEPS
        difstep_g = (start_g - end_g) / TRANSITION_STEPS
        difstep_b = (start_b - end_b) / TRANSITION_STEPS

        transitioning = True

        while transitioning:

            current_r = self._get_pin(self.pin_r)
            current_g = self._get_pin(self.pin_g)
            current_b = self._get_pin(self.pin_b)

            # are we there yet? If not, move to the next step
            if current_r != end_r:
                self._set_pin(self.pin_r, self._nextval(start_r, current_r, end_r, difstep_r))
            if current_g != end_g:
                self._set_pin(self.pin_g, self._nextval(start_g, current_g, end_g, difstep_g))
            if current_b != end_b:
                self._set_pin(self.pin_b, self._nextval(start_b, current_b, end_b, difstep_b))

            if current_r == end_r and curreng_g == end_g and current_b == end_b:
                transitioning = False

            time.sleep(INTERVAL)
