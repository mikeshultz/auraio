#!/bin/python
# -*- coding: utf-8 -*-

import os, sys, configparser, threading, importlib, queue, collections
from core.ledcontrol import LED_OPS
from core.alert import LEDAlert, OPS_MSG

DIR = os.path.dirname(os.path.realpath(__file__))
auraioini = os.path.join(DIR, 'auraio.ini')
pluginsini = os.path.join(DIR, 'plugins.ini')

if not os.path.isfile(auraioini):
    print("Error: auraio.ini not found at %s." % auraioini)
    sys.exit(1)
if not os.path.isfile(pluginsini):
    print("Error: plugins.ini not found at %s." % pluginsini)
    sys.exit(1)

main_config = configparser.ConfigParser()
main_config.read(auraioini)

# Often used conf
DEBUG = main_config['default'].get('debug', False)

plugin_config = configparser.ConfigParser()
plugin_config.read(pluginsini)

threads = []
auraioq = queue.Queue(255)
alert = LEDAlert(main_config['ledalert']['pin_r'], main_config['ledalert']['pin_g'], main_config['ledalert']['pin_b'])

# Get the plugins we're working with
for sect in plugin_config.sections():

    plugin_app = None

    try:
        plugin_module = importlib.import_module('plugins.' + sect)
        plugin_app = getattr(plugin_module, 'app')
    except ImportError as e:
        if DEBUG:
            print(e)
        print('Error importing %s' % 'plugins.' + sect + '.app')

    if plugin_app:
        if DEBUG:
            print('Starting new thread for %s' % sect)
        extra_kwargs = {'auraioq': auraioq}
        new_thread = threading.Thread(target = plugin_app, name = sect, kwargs = dict(**plugin_config[sect], **extra_kwargs))
        new_thread.daemon = True
        new_thread.start()
        threads.append(new_thread)

def shutdown_clean(self, signum, frame):
    """ Clean shutdown """

    # log here
    # Shutdown threads
    for t in threads:
        if t.is_alive():
            print('TODO: Thread cleanup')

    # TODO: turn all LEDs off
    print('Shutting down.')

def main():

    signal.signal(signal.SIGTERM, shutdown_clean)

    try:

        while True:

            if auraioq.qsize() > 0:

                # Get the operation and arguments
                op,args = auraioq.get()

                # Check the alert ops as well
                if OPS_MSG.get(op):
                    if args and isinstance(args, collections.Iterable):
                        OPS_MSG[op](*args)
                    elif not args:
                        OPS_MSG[op]()
                    else:
                        OPS_MSG[op](args)

                # See if the operation exists in LED_OPS
                elif LED_OPS.get(op):
                    if args and isinstance(args, collections.Iterable):
                        LED_OPS[op](*args)
                    elif not args:
                        LED_OPS[op]()
                    else:
                        LED_OPS[op](args)

                else: 
                    # log warning
                    print("Warning: Operation '%s' does not exist. Valid operations are: %s" % (op, {**LED_OPS, **OPS_MSG}))

    except Exception as e:
        raise e

if __name__ == '__main__':
    main()