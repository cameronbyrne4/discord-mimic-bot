import sys
print("Python Path:")
print("\n".join(sys.path))
print("\nTrying to import OpenAI...")

try:
    from openai import OpenAI
    print("OpenAI import successful!")
    
    client = OpenAI(
        api_key="test",
        base_url="https://api.deepseek.com"
    )
    print("Client creation successful!")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
    print(f"Error occurred in: {__file__}") 