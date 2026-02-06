# 🚀 Quick Start Guide

Get the AI Operations Assistant running in 5 minutes!

## Step 1: Install Dependencies (1 min)

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Get API Keys (2-3 mins)

You need 3 API keys (all have free tiers):

### 1. OpenAI API Key (Required)
- Go to: https://platform.openai.com/api-keys
- Create account if needed
- Click "Create new secret key"
- Copy the key (starts with `sk-`)

### 2. OpenWeatherMap API Key (Required)
- Go to: https://openweathermap.org/api
- Sign up for free account
- Go to API keys section
- Copy your API key

### 3. News API Key (Required)
- Go to: https://newsapi.org/register
- Sign up for free account
- Copy your API key from dashboard

### 4. GitHub Token (Optional)
- Go to: https://github.com/settings/tokens
- Generate new token (classic)
- Select `public_repo` scope
- Copy the token

## Step 3: Configure Environment (30 seconds)

```bash
# Copy example file
cp .env.example .env

# Edit .env and paste your API keys
nano .env  # or use any text editor
```

Your `.env` should look like:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENWEATHER_API_KEY=xxxxxxxxxxxxx
NEWS_API_KEY=xxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx  # optional
```

## Step 4: Verify Setup (30 seconds)

```bash
python test_setup.py
```

This will check:
- ✓ All environment variables are set
- ✓ All dependencies are installed
- ✓ All APIs are accessible

## Step 5: Run the Server (10 seconds)

```bash
uvicorn main:app --reload
```

You should see:
```
AI Operations Assistant - Multi-Agent System
============================================================
Server starting on http://0.0.0.0:8000

Available tools: github_search, get_weather, get_news
LLM Model: gpt-4o-mini
```

## Step 6: Test It! (1 min)

### Option A: Use the example client
```bash
# In a new terminal
python example_client.py
```

### Option B: Use curl
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find top 3 Python repos on GitHub"}'
```

### Option C: Use browser
Open http://localhost:8000/docs for interactive API documentation

## 🎉 You're Done!

The system is now running and ready to accept tasks.

## Example Tasks to Try

1. **GitHub Search**
   ```json
   {"task": "Find the top 5 Python machine learning repositories"}
   ```

2. **Weather Check**
   ```json
   {"task": "Get weather in Mumbai, Delhi, and Bangalore"}
   ```

3. **News Search**
   ```json
   {"task": "Find latest news about artificial intelligence"}
   ```

4. **Multi-Tool Task**
   ```json
   {"task": "Search for React repos and get weather in San Francisco"}
   ```

5. **Complex Query**
   ```json
   {"task": "Get tech news, find popular JavaScript projects, and check weather in New York"}
   ```

## Troubleshooting

### "OPENAI_API_KEY environment variable is required"
- Make sure `.env` file exists in project root
- Check that API key is correctly set in `.env`
- Restart the server after editing `.env`

### "Could not connect to server"
- Make sure server is running: `uvicorn main:app --reload`
- Check that port 8000 is not in use
- Try: `uvicorn main:app --port 8001`

### API errors (404, 401, etc.)
- Verify API keys are correct
- Check API quotas (free tiers have limits)
- Wait a few minutes and try again

### Import errors
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

## Need Help?

1. Check `README.md` for detailed documentation
2. Run `python test_setup.py` to diagnose issues
3. Check server logs for error messages
4. Verify API keys are valid and have quota remaining

---

**Total Setup Time: ~5 minutes**

Happy testing! 🚀
