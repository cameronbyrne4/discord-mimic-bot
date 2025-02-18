import sqlite3
import os
import json
from datetime import datetime

class iMessageParser:
    def __init__(self):
        # Default path to iMessage database on macOS
        self.chat_db_path = os.path.expanduser("~/Library/Messages/chat.db")
        
    def extract_messages(self, limit=1000):
        """Extract messages from iMessage database"""
        if not os.path.exists(self.chat_db_path):
            raise FileNotFoundError("iMessage database not found")
            
        # Create a copy of the database to avoid file permission issues
        temp_db = "/tmp/chat_temp.db"
        os.system(f"cp '{self.chat_db_path}' '{temp_db}'")
        
        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            query = """
            SELECT 
                message.text,
                message.date,
                message.is_from_me,
                handle.id
            FROM message 
            LEFT JOIN handle ON message.handle_id = handle.ROWID 
            WHERE message.text IS NOT NULL 
            ORDER BY message.date DESC 
            LIMIT ?
            """
            
            cursor.execute(query, (limit,))
            messages = cursor.fetchall()
            
            # Process messages
            processed_messages = []
            for msg in messages:
                if msg[0]:  # Only include messages with text
                    processed_messages.append({
                        'content': msg[0],
                        'timestamp': self._convert_apple_time(msg[1]),
                        'is_from_me': bool(msg[2]),
                        'contact': msg[3] if msg[3] else 'unknown'
                    })
            
            return processed_messages
            
        finally:
            conn.close()
            os.remove(temp_db)
    
    def _convert_apple_time(self, apple_time):
        """Convert Apple's timestamp to ISO format"""
        if apple_time:
            # Convert Apple's timestamp (seconds from 2001-01-01) to Unix timestamp
            unix_timestamp = apple_time/1e9 + 978307200
            return datetime.fromtimestamp(unix_timestamp).isoformat()
        return None

    def export_my_messages(self, output_file='my_messages.json'):
        """Export only messages sent by me"""
        try:
            all_messages = self.extract_messages()
            my_messages = [msg for msg in all_messages if msg['is_from_me']]
            
            with open(output_file, 'w') as f:
                json.dump(my_messages, f, indent=2)
                
            return f"Exported {len(my_messages)} messages to {output_file}"
            
        except Exception as e:
            return f"Error exporting messages: {e}"