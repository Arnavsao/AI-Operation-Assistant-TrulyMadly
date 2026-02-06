"""
Test script to verify the AI Operations Assistant setup
Run this before starting the server to check if everything is configured correctly
"""
import os
import sys
from dotenv import load_dotenv

def check_env_vars():
    """Check if all required environment variables are set"""
    print("=" * 60)
    print("Environment Variables Check")
    print("=" * 60)
    
    load_dotenv()
    
    required_vars = {
        "GEMINI_API_KEY": "Google Gemini API key for LLM (FREE!)",
        "OPENWEATHER_API_KEY": "OpenWeatherMap API key",
        "NEWS_API_KEY": "News API key"
    }
    
    optional_vars = {
        "GITHUB_TOKEN": "GitHub token (optional, increases rate limits)"
    }
    
    all_good = True
    
    print("\nRequired Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  ✓ {var}: {masked} ({description})")
        else:
            print(f"  ✗ {var}: NOT SET ({description})")
            all_good = False
    
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  ✓ {var}: {masked} ({description})")
        else:
            print(f"  - {var}: Not set ({description})")
    
    return all_good

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "=" * 60)
    print("Dependencies Check")
    print("=" * 60)
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "google.genai",
        "requests",
        "dotenv"
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def test_api_connections():
    """Test basic API connectivity"""
    print("\n" + "=" * 60)
    print("API Connectivity Test")
    print("=" * 60)
    
    load_dotenv()
    
    # Test Gemini
    print("\nTesting Google Gemini API...")
    try:
        from google import genai
        from google.genai import types
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        # Simple test call
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents="Say 'OK'"
        )
        if response.text:
            print("  ✓ Google Gemini API: Connected")
        else:
            print("  ✗ Google Gemini API: No response")
    except Exception as e:
        print(f"  ✗ Google Gemini API: {str(e)}")
    
    # Test Weather API
    print("\nTesting OpenWeatherMap API...")
    try:
        import requests
        api_key = os.getenv("OPENWEATHER_API_KEY")
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": "London", "appid": api_key},
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ OpenWeatherMap API: Connected")
        else:
            print(f"  ✗ OpenWeatherMap API: Status {response.status_code}")
    except Exception as e:
        print(f"  ✗ OpenWeatherMap API: {str(e)}")
    
    # Test News API
    print("\nTesting News API...")
    try:
        import requests
        api_key = os.getenv("NEWS_API_KEY")
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={"apiKey": api_key, "country": "us", "pageSize": 1},
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ News API: Connected")
        else:
            print(f"  ✗ News API: Status {response.status_code}")
    except Exception as e:
        print(f"  ✗ News API: {str(e)}")
    
    # Test GitHub API
    print("\nTesting GitHub API...")
    try:
        import requests
        headers = {}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        
        response = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": "python", "per_page": 1},
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            print("  ✓ GitHub API: Connected")
        else:
            print(f"  ✗ GitHub API: Status {response.status_code}")
    except Exception as e:
        print(f"  ✗ GitHub API: {str(e)}")

def main():
    """Run all checks"""
    print("\n🔍 AI Operations Assistant - Setup Verification\n")
    
    # Check environment variables
    env_ok = check_env_vars()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Test API connections
    if env_ok and deps_ok:
        test_api_connections()
    
    # Final summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if env_ok and deps_ok:
        print("\n✓ All checks passed! You can now run:")
        print("  uvicorn main:app --reload")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        if not env_ok:
            print("\n  1. Copy .env.example to .env")
            print("  2. Add your API keys to .env")
        if not deps_ok:
            print("\n  Run: pip install -r requirements.txt")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
