
class AuraioSensu:

    debug = False

    def __init__(self, *args, **kwargs):
        print('Checking for sensu debug setting...')
        print(kwargs['debug'])
        self.debug = kwargs['debug']