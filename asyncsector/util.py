import datetime
import asyncio
import sys

import aiohttp



async def get_json(request):
    '''
    Takes a asyncio response and returns the resulting json
    '''
    with aiohttp.Timeout(20):
        response = await request
    
    with aiohttp.Timeout(20):
        try:
            # other statements

            if 'json' in response.headers.get('content-type'):
                return (await response.json())
            else:
                print((await response.text()))

        finally:
            if sys.exc_info()[0] is not None:
                # on exceptions, close the connection altogether
                response.close()
                result = None
            else:
                result = await response.release()

        return result


def get_time(time):
    '''
    Converts from Sector Alarms time format to a proper time string
    '''
    unix_timestamp = time.split('(')[1][:-2]
    date = datetime.datetime.fromtimestamp(int(unix_timestamp) / 1000)
    return date.isoformat()

