import unittest
from unittest.mock import AsyncMock, patch
from backend.app.bot.discord_bot import bot

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):

    @patch('backend.app.bot.discord_bot.ai_service.get_response', new_callable=AsyncMock)
    async def test_chat_command(self, mock_get_response):
        mock_get_response.return_value = "Test response"
        ctx = AsyncMock()
        ctx.send = AsyncMock()

        await bot.get_command('chat')(ctx, message="Hello")
        ctx.send.assert_called_once_with("Test response")

    @patch('backend.app.bot.discord_bot.ai_service.get_response', new_callable=AsyncMock)
    async def test_hello_command(self, mock_get_response):
        ctx = AsyncMock()
        await bot.get_command('hello')(ctx)
        ctx.send.assert_called_once_with('Hello!')

if __name__ == '__main__':
    unittest.main()
