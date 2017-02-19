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
            # default to good
            highest_status = 0

            # go through each check and look for the highest(worst) status
            for check in jason:

                if self.debug and check['check']['status'] > 0:
                    print('Found a problem with client %s' % check['client'])

                if check['check']['status'] > highest_status:
                    highest_status = check['check']['status']

            if highest_status == 0:
                self.q.put(('good'))
            elif highest_status == 1:
                self.q.put(('warn'))
            elif highest_status == 2:
                self.q.put(('bad'))
            else:
                self.q.put(('unknown'))

            if self.q:
                self.q.put(('transition_decimal', color))



    def run(self):
        """ Kick it off """
        print('Starting sensu checks.')

        self.running = True

        while self.running:

            self.checkResults()

            time.sleep(self.interval)
