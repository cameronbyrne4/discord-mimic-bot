import unittest
from unittest.mock import patch, MagicMock
from backend.app.services.ai_service import AIService

class TestAIService(unittest.TestCase):

    @patch('backend.app.services.ai_service.OpenAI')
    def setUp(self, mock_openai):
        self.ai_service = AIService()
        self.ai_service.openai_client = mock_openai

    def test_get_response(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        self.ai_service._try_openai = MagicMock(return_value=mock_response)

        response = self.ai_service.get_response("Hello", "user_id")
        self.assertEqual(response, "Test response")

    def test_create_style_prompt(self):
        message = "What's up?"
        history_context = "Previous messages"
        prompt = self.ai_service._create_style_prompt(message, history_context)
        self.assertIn(message, prompt)
        self.assertIn(history_context, prompt)

if __name__ == '__main__':
    unittest.main()
