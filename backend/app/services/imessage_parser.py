import json
from datetime import datetime

class iMessageParser:
    def __init__(self):
        self.input_file = 'app/scripts/my_1000_messages.json'

    def parse_exported_messages(self, limit=1000):
        """Parse messages from exported JSON file"""
        try:
            with open(self.input_file, 'r') as f:
                messages = json.load(f)
        except FileNotFoundError:
            print(f"Error: The file {self.input_file} was not found.")
            return []  # Return an empty list or handle as needed
        except json.JSONDecodeError:
            print(f"Error: The file {self.input_file} is not a valid JSON.")
            return []  # Return an empty list or handle as needed
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []  # Return an empty list or handle as needed
        
        # Process messages
        processed_messages = []
        for msg in messages:
            if msg.get('text'):  # Only include messages with text
                processed_messages.append({
                    'content': msg['text'],
                    'timestamp': self._convert_apple_time(msg['date']),
                    'is_from_me': bool(msg['is_from_me']),
                    'contact': msg.get('id', 'unknown')
                })
        
        # Sort by timestamp and limit
        processed_messages = sorted(
            processed_messages, 
            key=lambda x: x['timestamp'], 
            reverse=True
        )[:limit]
        
        return processed_messages
        
    def _convert_apple_time(self, apple_time):
        """Convert Apple's timestamp to ISO format"""
        if apple_time:
            # Convert Apple's timestamp (seconds from 2001-01-01) to Unix timestamp
            unix_timestamp = apple_time/1e9 + 978307200
            return datetime.fromtimestamp(unix_timestamp).isoformat()
        return None

    def export_message_query(self, output_file='message_query.json'):
        """Export processed messages to a new JSON file"""
        try:
            message_query = self.parse_exported_messages()
            
            with open(output_file, 'w') as f:
                json.dump(message_query, f, indent=2)
                
            return f"Exported {len(message_query)} messages to {output_file}"
            
        except Exception as e:
            return f"Error exporting messages: {e}"