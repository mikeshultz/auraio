import configparser, threading, importlib, queue
from core.ledcontrol import LED_OPS
from core.alert import LEDAlert, OPS_MSG

main_config = configparser.ConfigParser()
main_config.read('auraio.ini')

# Often used conf
DEBUG = main_config['default'].get('debug', False)

plugin_config = configparser.ConfigParser()
plugin_config.read('plugins.ini')

threads = []
auraioq = queue.Queue(255)
alert = LEDAlert(main_config['ledalert']['pin_r'], main_config['ledalert']['pin_g'], main_config['ledalert']['pin_b'])

# Get the plugins we're working with
for sect in plugin_config.sections():

    plugin = None

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

try:

    while True:

        if auraioq.qsize() > 0:

            # Get the operation and arguments
            op,args = auraioq.get()

            # See if the operation exists in LED_OPS
            if LED_OPS.get(op):
                # Run it
                LED_OPS[op](*args)

            # Check the alert ops as well
            elif OPS_MSG.get(op):
                OPS_MSG[op](*args)

            else: 
                # log warning
                print("Warning: LED Operation does not exist.")

except KeyboardInterrupt:
    # log here
    # Shutdown threads
    for t in threads:
        if t.is_alive():
            print('TODO: Thread cleanup')

except Exception as e:
    raise e