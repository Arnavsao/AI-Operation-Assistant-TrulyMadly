# ✅ Setup Complete! Next Steps

## Dependencies Installed Successfully! 🎉

All Python packages are now installed in your virtual environment.

---

## What to Do Now

### 1. Get Your API Keys (10 minutes)

You need 3 API keys (all have FREE tiers):

#### **Google Gemini** (100% FREE - No Credit Card!)
1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

#### **OpenWeatherMap** (FREE tier)
1. Go to: **https://openweathermap.org/api**
2. Sign up
3. Get API key from dashboard

#### **News API** (FREE tier)
1. Go to: **https://newsapi.org/register**
2. Sign up
3. Get API key from dashboard

#### **GitHub Token** (Optional)
1. Go to: **https://github.com/settings/tokens**
2. Generate new token
3. Select `public_repo` scope

---

### 2. Add Keys to .env File

Your `.env` file is already open in your editor. Add your keys:

```env
# Google Gemini API Key (required - FREE!)
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub Personal Access Token (optional - increases rate limits)
GITHUB_TOKEN=ghp_your_github_token_here

# OpenWeatherMap API Key (required)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# News API Key (required)
NEWS_API_KEY=your_news_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

---

### 3. Test Your Setup

Once you have your API keys in `.env`, run:

```bash
source venv/bin/activate
python test_setup.py
```

You should see:
```
✓ GEMINI_API_KEY: AIza... (Google Gemini API key for LLM (FREE!))
✓ OPENWEATHER_API_KEY: ... (OpenWeatherMap API key)
✓ NEWS_API_KEY: ... (News API key)

✓ Google Gemini API: Connected
✓ OpenWeatherMap API: Connected
✓ News API: Connected
✓ GitHub API: Connected
```

---

### 4. Run the Server

```bash
source venv/bin/activate
uvicorn main:app --reload
```

You should see:
```
============================================================
AI Operations Assistant - Multi-Agent System
============================================================
Server starting on http://0.0.0.0:8000

Available tools: github_search, get_weather, get_news
LLM Model: Google gemini-1.5-flash
============================================================
```

---

### 5. Test It!

In a **new terminal**:

```bash
cd /Users/arnavsao/Desktop/trulymadly
source venv/bin/activate
python example_client.py
```

Or use curl:
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find top 3 Python repos on GitHub"}'
```

Or open in browser:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Quick Commands Reference

```bash
# Activate virtual environment (always do this first!)
source venv/bin/activate

# Test setup
python test_setup.py

# Run server
uvicorn main:app --reload

# Test with example client (in new terminal)
python example_client.py

# Deactivate virtual environment (when done)
deactivate
```

---

## Troubleshooting

### "command not found: python"
Use `python3` or activate the virtual environment first:
```bash
source venv/bin/activate
```

### "ModuleNotFoundError"
Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not valid"
- Check you copied the full key
- Make sure no extra spaces in `.env`
- Gemini keys start with `AIza`

---

## You're Almost Done!

1. ✅ Virtual environment created
2. ✅ Dependencies installed
3. ⏳ Get API keys (10 min)
4. ⏳ Add to .env file
5. ⏳ Test and run!

**Next**: Get your Gemini API key from https://aistudio.google.com/app/apikey

It's FREE and takes 2 minutes! 🚀
