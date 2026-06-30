import requests
import json

def test_ollama():
    """Test if Ollama is working locally"""
    
    # Test 1: Check if Ollama is running
    print("Test 1: Checking if Ollama is running...")
    try:
        response = requests.get("http://localhost:11434/api/tags")
        print(f"✓ Ollama is running")
        print(f"  Available models: {[m['name'] for m in response.json()['models']]}")
    except Exception as e:
        print(f"✗ Ollama is not running: {e}")
        return
    
    # Test 2: Simple generation test with smaller model
    print("\nTest 2: Testing simple generation with llama3 (smaller)...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": "Say 'Hello World' in one word",
                "stream": False
            },
            timeout=60
        )
        result = response.json()
        print(f"✓ Generation successful")
        print(f"  Response: {result.get('response', 'No response')}")
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        print("  Trying llama3.3 with longer timeout...")
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.3",
                    "prompt": "Say 'Hello World' in one word",
                    "stream": False
                },
                timeout=120
            )
            result = response.json()
            print(f"✓ Generation successful with llama3.3")
            print(f"  Response: {result.get('response', 'No response')}")
        except Exception as e2:
            print(f"✗ llama3.3 also failed: {e2}")
            return
    
    # Test 3: Chat completion test
    print("\nTest 3: Testing chat completion...")
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [
                    {"role": "user", "content": "What is 2+2?"}
                ],
                "stream": False
            },
            timeout=30
        )
        result = response.json()
        print(f"✓ Chat completion successful")
        print(f"  Response: {result.get('message', {}).get('content', 'No response')}")
    except Exception as e:
        print(f"✗ Chat completion failed: {e}")
        return
    
    print("\n✓ All tests passed! Ollama is working correctly.")

if __name__ == "__main__":
    test_ollama()
