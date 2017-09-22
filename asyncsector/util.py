import datetime
import asyncio
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

