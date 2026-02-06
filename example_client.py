"""
Example client script to demonstrate AI Operations Assistant usage
"""
import requests
import json
import time

# API endpoint
BASE_URL = "http://localhost:8000"

def print_response(response_data):
    """Pretty print the response"""
    print("\n" + "=" * 80)
    print("RESPONSE")
    print("=" * 80)
    print(json.dumps(response_data, indent=2))
    print("=" * 80 + "\n")

def execute_task(task: str):
    """Execute a task and print the response"""
    print(f"\n📝 Task: {task}")
    print("⏳ Processing...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/execute",
            json={"task": task},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Status: {data['status']}")
            print(f"📊 Quality Score: {data['metadata']['quality_score']}/10")
            print(f"📈 Steps: {data['metadata']['successful_steps']}/{data['metadata']['total_steps']} successful")
            print_response(data)
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

def main():
    """Run example tasks"""
    print("\n" + "=" * 80)
    print("AI Operations Assistant - Example Client")
    print("=" * 80)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server returned unexpected status")
            return
    except:
        print("❌ Server is not running. Please start it first:")
        print("   uvicorn main:app --reload")
        return
    
    # Example tasks
    examples = [
        "Find the top 3 Python machine learning repositories on GitHub",
        "Get the current weather in Mumbai and Delhi",
        "Find latest news about artificial intelligence",
        "Search for React repositories and get weather in San Francisco",
        "Get technology news and find popular JavaScript projects"
    ]
    
    print("\n📋 Available Example Tasks:")
    for i, task in enumerate(examples, 1):
        print(f"  {i}. {task}")
    
    print("\n" + "-" * 80)
    
    # Run first example
    print("\n🚀 Running Example 1...")
    execute_task(examples[0])
    
    # Ask user if they want to run more
    print("\n" + "-" * 80)
    print("\nTo run other examples, modify this script or use curl:")
    print("\ncurl -X POST http://localhost:8000/execute \\")
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"task": "Your task here"}\'')
    print("\nOr visit http://localhost:8000/docs for interactive API documentation")
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()
