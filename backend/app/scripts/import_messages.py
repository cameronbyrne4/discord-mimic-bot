import sys
import os
import json
# Add the parent directory to Python path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.imessage_parser import iMessageParser

def main():
    # Make sure message_query.json is in the same directory as this script
    parser = iMessageParser()
    try:
        result = parser.export_message_query()
        print(result)
        
        # After export, display some basic statistics
        if os.path.exists('message_query.json'):
            with open('message_query.json', 'r') as f:
                messages = json.load(f)
            print(f"\nTotal messages processed: {len(messages)}")
            print("Sample message:")
            if messages:
                print(json.dumps(messages[0], indent=2))
    except Exception as e:
        print(f"Error during export: {e}")

if __name__ == "__main__":
    main()