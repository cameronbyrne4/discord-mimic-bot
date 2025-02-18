import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

class MessageService:
    def __init__(self):
        load_dotenv()
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is not set")
            
        # Create a new client and connect to the server
        self.client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise  # Raise the exception to handle it further up if needed

        self.db = self.client.ai_friend_db

    async def save_message(self, user_id: str, message: str, response: str):
        chat_history = {
            'user_id': user_id,
            'message': message,
            'response': response,
            'timestamp': datetime.utcnow()
        }
        self.db.chat_history.insert_one(chat_history)

    async def get_chat_history(self, user_id: str, limit: int = 50):
        cursor = self.db.chat_history.find(
            {'user_id': user_id}
        ).sort('timestamp', -1).limit(limit)
        return list(cursor)

    def get_scheduled_messages(self):
        current_hour = datetime.utcnow().hour
        return list(self.db.scheduled_messages.find({
            'hour': current_hour
        }))

    def add_scheduled_message(self, message_data: dict):
        self.db.scheduled_messages.insert_one(message_data)

    def import_message_history(self, user_id: str, messages: list):
        if messages:
            formatted_messages = []
            for msg in messages:
                formatted_msg = {
                    'user_id': user_id,
                    'message': msg.get('content', ''),
                    'timestamp': datetime.fromisoformat(msg.get('timestamp', datetime.utcnow().isoformat())),
                    'source': 'import'
                }
                formatted_messages.append(formatted_msg)
            
            if formatted_messages:
                self.db.imported_history.insert_many(formatted_messages)