''' Start asyncsector '''

import sys
import asyncio
import argparse

import aiohttp

from asyncsector import AsyncSector
from asyncsector.util import get_time

async def async_main(loop):
    '''
    Async main function

    Logs in to Sector Alarm and prints alarm history + temperatures repeatedly with delay.
    '''

    parser = argparse.ArgumentParser(description='Check Sector Alarm status')

    parser.add_argument('alarm_id', type=str, help='ID of your alarm system')
    parser.add_argument('username', type=str,
                        help='Your Sector Alarm username')
    parser.add_argument('password', type=str,
                        help='Your Sector Alarm password')
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--delay', type=int, default=10)
    parser.add_argument('--history', type=int, default=1)

    args = parser.parse_args()

    async with aiohttp.ClientSession(loop=loop) as session:

        alarm = await AsyncSector.create(session,
                                         args.alarm_id, args.username, args.password)

        for i in range(0, args.repeat):

            if i != 0:
                await asyncio.sleep(args.delay)

            history, temperatures = await asyncio.gather(alarm.get_history(),
                                                         alarm.get_temperatures())

            print()

            if history:
                log = history.get('LogDetails', None)
                if log is not None:
                    for entry in log[:args.history]:
                        print(
                            '{:12}{:12}{}'.format(
                                entry['EventType'],
                                entry['User'],
                                get_time(entry['Time'])))
                    print()

            if temperatures:
                for temperature in temperatures:
                    print('{:12}{}'.format(
                        temperature['Label'], temperature['Temprature']))


def main():
    '''
    Synchronous main, bootstraps async main
    '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main(loop))


if __name__ == "__main__":
    sys.exit(main())

