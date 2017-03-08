from .sensu import AuraioSensu

def app(*args, **kwargs):
    """ Run the plugin """
    print('starting sensu.app')
    plugin = AuraioSensu(*args, **kwargs)