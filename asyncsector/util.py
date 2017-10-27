''' Helpers '''

import datetime
import asyncio

import async_timeout


async def get_json(request):
    '''
    Takes a asyncio response and returns the resulting json
    '''

    try:
        with async_timeout.timeout(20):
            async with request as response:

                if 'json' in response.headers.get('content-type'):
                    return await response.json()
                else:
                    print(await response.text())

    except asyncio.TimeoutError:
        pass

    return None


def get_time(time):
    '''
    Converts from Sector Alarms time format to a proper time string
    '''
    unix_timestamp = time.split('(')[1][:-2]
    date = datetime.datetime.fromtimestamp(int(unix_timestamp) / 1000)
    return date.isoformat()
