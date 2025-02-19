import sys
import os

# Add the parent directory to Python path so we can import our app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.imessage_parser import iMessageParser

def main():
    parser = iMessageParser()
    try:
        result = parser.export_my_messages()
        print(result)
        
        # After export, analyze the messages
        if os.path.exists('my_messages.json'):
            print("\nExport successful! You can now customize the analysis in:")
            print("app/services/ai_service.py in these methods:")
            print("- _extract_common_phrases")
            print("- _analyze_emoji_usage")
            print("- _create_style_prompt")
    except Exception as e:
        print(f"Error during export: {e}")

if __name__ == "__main__":
    main()