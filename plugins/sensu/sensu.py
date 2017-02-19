import time, requests

class AuraioSensu:

    debug = False
    server = ''
    interval = -1

    running = True

    def __init__(self, *args, **kwargs):
        print('Initializing sensu plugin.')
        self.debug = kwargs.get('debug', False)
        self.server = kwargs.get('baseurl', 'http://127.0.0.1:4567')
        self.interval = int(kwargs.get('interval', 30))

        # auraio components
        self.q = kwargs.get('auraioq')

        self.run()



    def _request(self, endpoint):
        """ Submit HTTP request and return json """

        r = requests.get(self.server + endpoint)

        if r.status_code == 200:
            #log 
            return r.json()
        else:
            print("Odd response from Sensu.  Code %s." % r.status_code)
            return None



    def checkResults(self):
        """ Check Sensu's check results """

        jason = self._request('/results')

        if not jason:
            print('Error: No JSON received from Sensu?')
        else:
            for check in jason:
                if check['check']['status'] > 0:
                    print('Found a problem with client %s' % check['client'])
                    if self.q:
                        self.q.put(('transition_decimal', [255,0,0]))



    def run(self):
        """ Kick it off """
        print('Starting sensu checks.')

        self.running = True

        while self.running:

            self.checkResults()

            time.sleep(self.interval)
