import configparser, threading, importlib, queue
from core.ledcontrol import LED_OPS, RGB

main_config = configparser.ConfigParser()
main_config.read('auraio.ini')

plugin_config = configparser.ConfigParser()
plugin_config.read('plugins.ini')

threads = []
ledop_queue = queue.Queue(255)

# Get the plugins we're working with
for sect in plugin_config.sections():

    plugin = None

    try:
        plugin = importlib.import_module('app', 'plugins.' + sect)
    except ImportError as e:
        if main_config['debug']:
            print(e)
        print('Error importing %s' % sect)

    if plugin:
        new_thread = threading.Thread(target = plugin, name = sect, kwargs = plugin_config[sect])
        new_thread.daemon = True
        new_thread.start()
        threads.append(new_thread)

try:
    while True:

        if ledop_queue.qsize() > 0:

            # Get the operation and arguments
            op,args = q.get()

            # See if the operation exists
            if LED_OPS.get(op):
                # Run it
                LED_OPS[op](*args)
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