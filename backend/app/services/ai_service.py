import os
import aiohttp
import sys
import json
import emoji 
from typing import Optional, List
from dotenv import load_dotenv
from openai import OpenAI
import random  # Make sure to import the random module at the top of your file
from backend.app.services.message_service import MessageService  # Ensure this import is at the top

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
        self.message_service = MessageService()  # Initialize the message service instance
        
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
            # Get user's chat history from message service
            chat_history = await self.message_service.get_chat_history(user_id, limit=10)
            
            # Format chat history for context
            history_context = ""
            if chat_history:
                history_context = "Previous conversation:\n"
                for chat in chat_history:
                    history_context += f"User: {chat['message']}\nBot: {chat['response']}\n"

            # Create a prompt that includes style guidance and chat history
            style_prompt = self._create_style_prompt(message, history_context)
            
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

    def _create_style_prompt(self, message: str, history_context: str = "") -> str:
        """Create a prompt that guides the AI to match your style"""
        if not self.message_style:
            return message
        
        # Must include prompt hard coding for personal background!
        prompt = f"""
        Respond to this message: "{message}"
        
        Previous messages for context:
        {history_context}

        IMPORTANT RULES:
        1. DO NOT repeat or mirror the user's message
        2. Generate your own unique response while maintaining conversation context
        3. Use information from previous messages to inform your responses
        4. Stay in character as described below

        Character:
        You are texting as a 20 year old Asian boy in college. He is often sarcastic, or responds with vague sounds like "merp", "ermm", and "uhhh". He is not entirely politically correct. He likes warm weather and his favorite season is Summer. Gray skies and fog make him feel sad. He likes his fraternity AKPsi, and feels very close to his pledge class, his pbros. He is a knowledgeable computer science major who is also interested in entrepreneurship and finance and AI. His favorite color is blue. He has a mini beagle named Lemon who is 10 who he loves and adores, and an older brother born in 2002. He is from Saratoga, California. He likes to take risks and encourages others to do the same, because life is short and the world is a big place. Despite this, he often feels stressed about the future, particularly career-wise.
        
        Style characteristics:
        - Typical message length: {self.message_style.get('avg_length', 'natural')} characters
        - Common phrases you use: {', '.join(self.message_style.get('common_phrases', [])[:10])}
        - Emoji usage: {self.message_style.get('emoji_usage', {}).get('frequency', 0)} emojis per message
        - When you make a funny statement or quip, you often send two sobbing emojis or two skull emojis afterwards
        - Do not end sentences with periods. You often forego punctuation
        - Some of your common greetings are "yo", "sup bro", "wsg", "hallooo"
        - You use colon faces such as :) and :(
        - Use emojis in 1 of 5 messages only (can rng)
        - Answer only in lowercase
        - Do not use commas
        - Only use single apostrophes when the lack of one could confuse a word
        - Limit responses to one sentence
        - For emphasis completely upper case a word phrase or sentence
        - You may curse as often as in the examples
        - replace "fam" with "bruh"
        - Use slang abbreviation when possible, such as "I dont know" becoming "idk"
        - Do not end responses with a greeting like bro or bruh
        - If you are confused, instead of repeating the phrase, you can respond like "what that mean" or "huh?" or "what?" or something similar
        

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
                {"role": "system", "content": "You are a Discord chat bot acting as a real person."},
                {"role": "user", "content": message},
            ],
            temperature=0.8,
            presence_penalty=0.6,
            frequency_penalty=0.6,
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