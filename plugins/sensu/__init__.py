from .sensu import AuraioSensu

def app(*args, **kwargs):
    """ Run the plugin """
    plugin = AuraioSensu(*args, **kwargs)