''' Tests '''

import unittest
from unittest import mock
import asyncio

from asyncsector import AsyncSector

def AsyncMock(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro

def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

class TestCreate(unittest.TestCase):
    
    @mock.patch('asyncsector.AsyncSector.login', new=AsyncMock(return_value=True))
    def test_create_login_success(self):
        async_sector = _run(AsyncSector.create(None, None, None, None))
        AsyncSector.login.mock.assert_called_once()
        self.assertIsInstance(async_sector, AsyncSector)

    @mock.patch('asyncsector.AsyncSector.login', new=AsyncMock(return_value=False))
    def test_create_login_fail(self):
        async_sector = _run(AsyncSector.create(None, None, None, None))
        AsyncSector.login.mock.assert_called_once()
        self.assertIsNone(async_sector)


