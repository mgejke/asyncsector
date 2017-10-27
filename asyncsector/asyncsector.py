import asyncio

import aiohttp
from .util import get_json

class AsyncSector(object):
    ''' Class to interact with sector alarm webpage '''

    Base = 'https://mypagesapi.sectoralarm.net/'
    Login = 'User/Login'
    Alarm = 'Panel/GetOverview'
    Temperatures = 'Panel/GetTempratures/{}'
    History = 'Panel/GetPanelHistory/{}'
    Arm = 'Panel/ArmPanel'

    @classmethod 
    async def create(cls, session, alarm_id, username, password):
        ''' factory '''
        self = AsyncSector(session, alarm_id, username, password)
        logged_in = await self.login()

        return self if logged_in else None

    def __init__(self, session, alarm_id, username, password):
        self._alarm_id = alarm_id
        self._session = session
        self._auth = {'userID': username, 'password': password}

    async def login(self):

        with aiohttp.Timeout(10):
            response = await self._session.post(
                AsyncSector.Base + AsyncSector.Login, data=self._auth)

            if response.status == 200:
                result = await response.text()
                if 'frmLogin' in result:
                    return False
                return True

        return False

    async def get_status(self):
        '''
        Fetches the status of the alarm
        '''
        request = self._session.post(
            AsyncSector.Base + AsyncSector.Alarm,
            data={'PanelId': self._alarm_id})

        return (await get_json(request))

    async def get_temperatures(self):
        '''
        Fetches a list of all temperature sensors
        '''
        request = self._session.get(
            AsyncSector.Base + AsyncSector.Temperatures.format(self._alarm_id))

        return (await get_json(request))

    async def get_history(self):
        '''
        Fetches the alarm event log/history
        '''
        request = self._session.get(AsyncSector.Base +
                                    AsyncSector.History.format(self._alarm_id))

        return (await get_json(request))

    async def alarm_toggle(self, state, code=None):
        data = {
            'ArmCmd': state,
            'PanelCode': code,
            'HasLocks': False,
            'id': self._alarm_id
        }

        request = self._session.post(
            AsyncSector.Base + AsyncSector.Arm, data=data)

        result = await get_json(request)
        if 'status' in result and result['status'] == 'success':
            return True

        return False

    async def alarm_disarm(self, code=None):
        return (await self.alarm_toggle('Disarm', code=code))

    async def alarm_arm_home(self, code=None):
        return (await self.alarm_toggle('Partial', code=code))

    async def alarm_arm_away(self, code=None):
        return (await self.alarm_toggle('Total', code=code))
