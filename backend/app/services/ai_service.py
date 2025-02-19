import os
import aiohttp
import sys
import json
import emoji 
from typing import Optional, List
from dotenv import load_dotenv
from openai import OpenAI
import random  # Make sure to import the random module at the top of your file

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
        # self.giphy_api_key = os.getenv('GIPHY_API_KEY')  # Commented out for now
        self.message_style = self._load_message_style()
        
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

    def _load_message_style(self) -> dict:
        """Load and analyze personal message style from exported data"""
        try:
            with open('message_query.json', 'r') as f:
                messages = json.load(f)
            
            # Extract key characteristics
            style_characteristics = {
                'avg_length': sum(len(m['content']) for m in messages) / len(messages),
                'common_phrases': self._extract_common_phrases(messages),
                'emoji_usage': self._analyze_emoji_usage(messages),
                'example_messages': messages[:100]  # Keep some examples for context
            }
            return style_characteristics
        except FileNotFoundError:
            return {}

    def _extract_common_phrases(self, messages: List[dict]) -> List[str]:
        """Extract commonly used phrases from messages"""
        if not messages or not all('content' in msg for msg in messages):
            return []
        # Add your custom phrase analysis here
        phrases = {
            # Hard coding to boost the stats of some phrases that I know Cameron says
            "oh hell nah": 1,
            "what the balls": 1,
            "aight lil bro": 1,
            "shutcho ass up": 1,
            "ohh I see": 1,
        }
        
        for msg in messages:
            content = msg['content'].lower()
            # Example: Track 3-word phrases
            words = content.split()
            for i in range(len(words)-2):
                phrase = " ".join(words[i:i+3])
                phrases[phrase] = phrases.get(phrase, 0) + 1
            for i in range(len(words)-1):  # Adjust for two-word phrases
                phrase = " ".join(words[i:i+2])
                phrases[phrase] = phrases.get(phrase, 0) + 1
        
        # Return most 10 common phrases "what the balls" "oh hell nah"
        return [phrase for phrase, count in 
                sorted(phrases.items(), key=lambda x: x[1], reverse=True)[:10]]

    def _analyze_emoji_usage(self, messages: List[dict]) -> dict:
        """Analyze emoji usage patterns"""
        
        emoji_counts = {}
        
        for msg in messages:
            content = msg['content']
            # Count emojis in message
            for char in content:
                if char in emoji.EMOJI_DATA:
                    emoji_counts[char] = emoji_counts.get(char, 0) + 1
        
        return {
            'most_used': sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'frequency': sum(emoji_counts.values()) / len(messages)
        }

    async def get_response(self, message: str, user_id: str) -> str:
        try:
            # Create a prompt that includes style guidance
            style_prompt = self._create_style_prompt(message)
            
            # Only doing OpenAI, no Deepseek
            response = await self._try_openai(style_prompt)
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

    def _create_style_prompt(self, message: str) -> str:
        """Create a prompt that guides the AI to match your style"""
        if not self.message_style:
            return message
        
        # Must include prompt hard coding for personal background!
        prompt = f"""
        Respond to this message: "{message}"
    
        Character:
        You are texting as a 20 year old Asian boy who goes to UCSB. He is often sarcastic, or responds with vague sounds like "merp". He is not entirely politically correct.

        Use these style characteristics:
        - Typical message length: {self.message_style.get('avg_length', 'natural')} characters
        - Common phrases you use: {', '.join(self.message_style.get('common_phrases', [])[:10])}
        - Emoji usage: {self.message_style.get('emoji_usage', {}).get('frequency', 0)} emojis per message
        - When you make a funny statement or quip, you often send two sobbing emojis or two skull emojis afterwards
        - Do not end sentences with periods. You often forego punctuation.
        - Some of your common greetings are "yo", "sup bro", "wsg", "hallooo"
        - You use colon faces such as :) and :(
        - Use emojis in 1 of 5 messages only (can rng)
        - Answer only in lowercase
        - Do not use commas
        - Limit responses to one sentence
        - For exphasis completely upper case a word, phrase, or sentence. For example a message could be "BRO" or "why the FUCK would i do that"
        - You may curse as often as in the examples, which is pretty often
        - replace "fam" with "bruh"
        

        Example responses in their style:
        {self._format_examples()}
        
        Generate a response that sounds authentic to their voice:
        """
        return prompt

    def _format_examples(self) -> str:
        """Format example messages for the prompt"""
        if not self.message_style or 'example_messages' not in self.message_style:
            return ""
            
        examples = self.message_style['example_messages']
        
        # Print the first 5 random examples for confirmation
        random_examples = random.sample(examples, min(5, len(examples)))  # Get up to 5 random examples
        print("First 5 random examples:")
        for example in random_examples:
            print(f"- {example['content']}")
        
        return "\n".join(f"- {msg['content']}" for msg in examples)

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

    async def _try_openai(self, message: str) -> Optional[str]:
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