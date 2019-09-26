''' Helpers '''

import datetime
import asyncio

import async_timeout

import re

async def get_json(request):
    '''
    Takes a asyncio response and returns the resulting json
    '''

    try:
        with async_timeout.timeout(20):
            async with request as response:
                if response.status == 426:
                    result = await response.text()
                    raise Exception("Error from api: %s" % result)
                elif 'json' in response.headers.get('content-type'):
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

def find_version(string):
    '''
    Takes an html output and returns version string, if found
    '''

    r=re.search('v\d+_\d+_\d+',string)
    return r.group(0) if r else None
