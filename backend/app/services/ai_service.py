import os
import aiohttp
import sys
from typing import Optional, List
from dotenv import load_dotenv
from openai import OpenAI

try:
    print("Debug: Attempting to import OpenAI...")
    from openai import OpenAI
    print("Debug: OpenAI import successful!")
except Exception as e:
    print(f"Debug: Import error: {type(e).__name__}: {str(e)}")
    raise

class AIService:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Debug prints
        print("Environment variables loaded:")
        print(f"DEEPSEEK_API_KEY exists: {bool(os.getenv('DEEPSEEK_API_KEY'))}")
        print(f"DEEPSEEK_API_KEY starts with: {os.getenv('DEEPSEEK_API_KEY')[:10]}...")
        
        # self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        # Initialize OpenAI client (DeepSeek commented out for now)
        self.openai_client = OpenAI(
            api_key=self.openai_api_key
        )
        # self.deepseek_client = OpenAI(
        #     api_key=self.deepseek_api_key,
        #     base_url="https://api.deepseek.com"
        # )

    async def get_response(self, message: str, user_id: str) -> str:
        try:
            # Try OpenAI first
            response = await self._try_openai(message)
            return response
        except Exception as e:
            print(f"OpenAI error: {e}")
            # print("Falling back to DeepSeek...")
            # # Fallback to DeepSeek (commented out for now)
            # try:
            #     response = await self._try_deepseek(message)
            #     return response
            # except Exception as e:
            #     print(f"DeepSeek error: {e}")
            return "Sorry, I encountered an error with the AI service."

    # async def _try_deepseek(self, message: str) -> str:
    #     response = self.deepseek_client.chat.completions.create(
    #         model="deepseek-chat",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant"},
    #             {"role": "user", "content": message},
    #         ],
    #         stream=False
    #     )
    #     return response.choices[0].message.content

    async def _try_openai(self, message: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": message},
            ],
            stream=False
        )
        return response.choices[0].message.content
    '''
    async def get_gif(self, query: str) -> Optional[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.giphy.com/v1/gifs/search',
                params={
                    'api_key': self.giphy_api_key,
                    'q': query,
                    'limit': 1
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['data']:
                        return data['data'][0]['images']['original']['url']
        return None
        '''