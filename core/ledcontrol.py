import re, time, sys, pigpio

gpio = pigpio.pi()

# Our RGB to RPi pinout
R = 27
G = 22
B = 17

INTERVAL = 0.1
TRANSITION_STEPS = 20
LED_OPS = {
    'set_decimal': None,
    'set_hex': None,
    'transition': None,
}

re_rgb_hex = r'#*([A-Fa-f0-9]{1,2})([A-Fa-f0-9]{1,2})([A-Fa-f0-9]{1,2})'

class InvalidHexString(Exception): pass
class InvalidDutyCycle(Exception): pass

class RGB:



    pin_r = -1
    pin_g = -1
    pin_b = -1

    transitioning = False



    def __init__(self, r_pin, g_pin, b_pin):
        self.pin_r = int(r_pin)
        self.pin_g = int(g_pin)
        self.pin_b = int(b_pin)
        self.setup()


    def setup(self):
        LED_OPS['set_decimal'] = self.set_decimal
        LED_OPS['set_hex'] = self.set_hex
        LED_OPS['transition_decimal'] = self.transition_decimal



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
            raise InvalidDutyCycle("The duty cycle %s parmeter is invalid.  It should be between 0 and 255" % cycle)

        gpio.set_PWM_frequency(pin, 60)
        return gpio.set_PWM_dutycycle(pin, cycle)


    def _nextval(self, startv, currentv, endv, step):
        """ Figure out what the next step is """

        # are we there yet?
        if startv <= currentv <= endv \
            or endv <= currentv <= startv:
            
            # Not sure about this math...
            nxt = currentv + step

            # We don't want to go over 255 or under 0
            return self._normalize_decimal(nxt)

        return currentv



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

        # Look for a properly formatted hex string
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

        # Get the start values of the transition
        start_r = self._get_pin(self.pin_r)
        start_g = self._get_pin(self.pin_g)
        start_b = self._get_pin(self.pin_b)

        # Get the destination values
        end_r = r
        end_g = g
        end_b = b

        # Figure out what each 'step' we want to take is
        difstep_r = round((end_r - start_r) / TRANSITION_STEPS)
        difstep_g = round((end_g - start_g) / TRANSITION_STEPS)
        difstep_b = round((end_b - start_b) / TRANSITION_STEPS)

        # signal that we're transitioning
        self.transitioning = True

        while self.transitioning:

            # What is the current PWM setting?
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

            # are we done?  if so, we'll shut down the loop
            if current_r == end_r and current_g == end_g and current_b == end_b:
                self.transitioning = False

            # wait, so all of this isn't instantaneous
            time.sleep(INTERVAL)
