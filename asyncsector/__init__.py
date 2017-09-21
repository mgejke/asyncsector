'''
    Asynchronous package for Sector Alarm
'''

import asyncio
import datetime
import sys

import aiohttp



@asyncio.coroutine
def get_json(request):
    '''
    Takes a asyncio response and returns the resulting json
    '''
    with aiohttp.Timeout(20):
        response = yield from request
        try:
            # other statements

            if 'json' in response.headers.get('content-type'):
                return (yield from response.json())
            else:
                print((yield from response.text()))

        finally:
            if sys.exc_info()[0] is not None:
                # on exceptions, close the connection altogether
                response.close()
                result = None
            else:
                result = yield from response.release()

    return result


def get_time(time):
    '''
    Converts from Sector Alarms time format to a proper time string
    '''
    unix_timestamp = time.split('(')[1][:-2]
    date = datetime.datetime.fromtimestamp(int(unix_timestamp) / 1000)
    return date.isoformat()


class AsyncSector(object):
    ''' Class to interact with sector alarm webpage '''

    Base = 'https://mypagesapi.sectoralarm.net/'
    Login = 'User/Login'
    Alarm = 'Panel/GetOverview'
    Temperatures = 'Panel/GetTempratures/{}'
    History = 'Panel/GetPanelHistory/{}'
    Arm = 'Panel/ArmPanel'

    @classmethod
    @asyncio.coroutine
    def create(cls, session, alarm_id, username, password):
        ''' factory '''
        self = AsyncSector(session, alarm_id, username, password)
        logged_in = yield from self.login()

        return self if logged_in else None

    def __init__(self, session, alarm_id, username, password):
        self._alarm_id = alarm_id
        self._session = session
        self._auth = {'userID': username, 'password': password}

    @asyncio.coroutine
    def login(self):

        with aiohttp.Timeout(10):
            response = yield from self._session.post(
                AsyncSector.Base + AsyncSector.Login, data=self._auth)

            if response.status == 200:
                result = yield from response.text()
                if 'frmLogin' in result:
                    return False
                return True

        return False

    @asyncio.coroutine
    def get_status(self):
        '''
        Fetches the status of the alarm
        '''
        request = self._session.post(
            AsyncSector.Base + AsyncSector.Alarm,
            data={'PanelId': self._alarm_id})

        return (yield from get_json(request))

    @asyncio.coroutine
    def get_temperatures(self):
        '''
        Fetches a list of all temperature sensors
        '''
        request = self._session.get(
            AsyncSector.Base + AsyncSector.Temperatures.format(self._alarm_id))

        return (yield from get_json(request))

    @asyncio.coroutine
    def get_history(self):
        '''
        Fetches the alarm event log/history
        '''
        request = self._session.get(AsyncSector.Base +
                                    AsyncSector.History.format(self._alarm_id))

        return (yield from get_json(request))

    @asyncio.coroutine
    def alarm_toggle(self, state, code=None):
        data = {
            'ArmCmd': state,
            'PanelCode': code,
            'HasLocks': False,
            'id': self._alarm_id
        }

        request = self._session.post(
            AsyncSector.Base + AsyncSector.Arm, data=data)

        result = yield from get_json(request)
        if 'status' in result and result['status'] == 'success':
            return True

        return False

    @asyncio.coroutine
    def alarm_disarm(self, code=None):
        return (yield from self.alarm_toggle('Disarm', code=code))

    @asyncio.coroutine
    def alarm_arm_home(self, code=None):
        return (yield from self.alarm_toggle('Partial', code=code))

    @asyncio.coroutine
    def alarm_arm_away(self, code=None):
        return (yield from self.alarm_toggle('Total', code=code))

