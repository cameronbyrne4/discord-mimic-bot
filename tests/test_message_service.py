import unittest
from unittest.mock import patch, MagicMock
from backend.app.services.message_service import MessageService

class TestMessageService(unittest.IsolatedAsyncioTestCase):

    @patch('backend.app.services.message_service.MongoClient')
    def setUp(self, mock_mongo_client):
        self.message_service = MessageService()
        self.message_service.client = mock_mongo_client

    @patch('backend.app.services.message_service.datetime')
    async def test_save_message(self, mock_datetime):
        mock_datetime.utcnow.return_value = "2023-01-01T00:00:00Z"
        await self.message_service.save_message("user_id", "Hello", "Response")
        # Check if the message was saved correctly
        self.assertEqual(self.message_service.db.chat_history.insert_one.call_count, 1)

    @patch('backend.app.services.message_service.MongoClient')
    async def test_get_chat_history(self, mock_mongo_client):
        mock_cursor = MagicMock()
        mock_cursor.sort.return_value.limit.return_value = [{'user_id': 'user_id', 'message': 'Hello', 'response': 'Response'}]
        mock_mongo_client.ai_friend_db.chat_history.find.return_value = mock_cursor

        history = await self.message_service.get_chat_history("user_id", limit=10)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['message'], 'Hello')

if __name__ == '__main__':
    unittest.main()
