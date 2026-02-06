# ✅ System Testing Guide

## Your System is WORKING! 🎉

Based on the logs, your system successfully processed requests. Here's how to test it properly.

---

## 🚀 Quick Start

### 1. Start the Server

```bash
cd /Users/arnavsao/Desktop/trulymadly
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
LLM Model: Google models/gemini-flash-latest
============================================================
```

---

## 📋 Manual Testing Methods

### Method 1: Swagger UI (EASIEST!)

1. **Open browser**: http://localhost:8000/docs
2. **Click** on `POST /execute`
3. **Click** "Try it out"
4. **Enter** your task in the JSON:
   ```json
   {
     "task": "Get weather in Mumbai and Delhi"
   }
   ```
5. **Click** "Execute"
6. **See** the results below!

---

### Method 2: Using curl (Terminal)

```bash
# Test 1: Weather (WORKING!)
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Mumbai and Delhi"}'

# Test 2: News (WORKING!)
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find latest technology news"}'

# Test 3: Combined
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in London and find AI news"}'
```

---

### Method 3: Python Script

```bash
# Use the example client
source venv/bin/activate
python example_client.py
```

Or create your own:

```python
import requests

response = requests.post(
    "http://localhost:8000/execute",
    json={"task": "Get weather in Paris"}
)

print(response.json())
```

---

## ✅ Working Examples

### Example 1: Weather Query
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Mumbai"}'
```

**Expected Response:**
```json
{
  "task_summary": "Get the current weather information for Mumbai.",
  "status": "success",
  "results": {
    "get_weather": [{
      "city": "Mumbai",
      "temperature": 25.99,
      "humidity": 50,
      "conditions": "smoke"
    }]
  }
}
```

### Example 2: News Query
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find latest AI news"}'
```

### Example 3: Multi-Tool Query
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Tokyo and find technology news"}'
```

---

## 🔍 Health Check

```bash
# Check if server is running
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "agents": ["planner", "executor", "verifier"],
  "tools": ["github_search", "get_weather", "get_news"],
  "llm_model": "models/gemini-flash-latest"
}
```

---

## 📊 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/tools` | GET | List available tools |
| `/execute` | **POST** | Execute a task (main endpoint) |
| `/docs` | GET | Swagger UI (interactive docs) |

---

## ❌ Common Errors & Fixes

### Error 1: "405 Method Not Allowed"
**Problem**: Using GET instead of POST on `/execute`

**Fix**: Use POST method:
```bash
# ❌ Wrong
curl http://localhost:8000/execute

# ✅ Correct
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "your task"}'
```

### Error 2: "404 Not Found" for `/api/jobs/`
**Problem**: Trying to access non-existent endpoint

**Fix**: Use correct endpoints (see table above)

### Error 3: GitHub 401 Unauthorized
**Problem**: GitHub token not configured

**Fix**: Either:
1. **Skip GitHub** - Use weather and news only
2. **Add token** - Get from https://github.com/settings/tokens

### Error 4: "429 RESOURCE_EXHAUSTED"
**Problem**: Hit Gemini rate limit

**Fix**: Wait 20 seconds and try again

---

## 🎯 Test Checklist

Run these tests to verify everything works:

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. List tools
curl http://localhost:8000/tools

# 3. Weather test
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Mumbai"}'

# 4. News test
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find latest AI news"}'

# 5. Multi-tool test
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in London and find technology news"}'
```

**Expected**: All should return 200 OK with JSON responses

---

## 📱 Browser Testing

### Option 1: Swagger UI (Recommended)
1. Open: http://localhost:8000/docs
2. Interactive interface with "Try it out" buttons
3. See request/response examples
4. Test all endpoints easily

### Option 2: Main Page
1. Open: http://localhost:8000
2. See API information and examples

---

## 🐛 Debugging

### Check Server Logs
The terminal running `uvicorn` shows:
- ✅ `[PLANNER] Created plan with X steps` - Good!
- ✅ `[EXECUTOR] Step 1/1 ✓` - Success!
- ✅ `[COMPLETE] Task finished with status: success` - Perfect!
- ❌ `[ERROR] Task execution failed` - Check the error message

### Check API Response
```bash
# Add -v for verbose output
curl -v -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Mumbai"}'
```

---

## 📝 Example Session

```bash
# Terminal 1: Start server
cd /Users/arnavsao/Desktop/trulymadly
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Test
source venv/bin/activate

# Test 1: Health
curl http://localhost:8000/health
# ✅ Should return: {"status": "healthy", ...}

# Test 2: Weather
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Mumbai"}'
# ✅ Should return weather data

# Test 3: News
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find latest technology news"}'
# ✅ Should return news articles
```

---

## 🎉 Success Indicators

You know it's working when you see:

1. **Server logs show**:
   ```
   [PLANNER] Created plan with 1 steps
   [EXECUTOR] Step 1/1 ✓
   [COMPLETE] Task finished with status: success
   INFO: 127.0.0.1 - "POST /execute HTTP/1.1" 200 OK
   ```

2. **Response includes**:
   ```json
   {
     "status": "success",
     "results": { ... },
     "metadata": {
       "successful_steps": 1,
       "failed_steps": 0
     }
   }
   ```

---

## 🚀 Ready for Submission!

Your system is working! The logs show:
- ✅ LLM (Gemini) working
- ✅ Weather API working
- ✅ News API working
- ✅ Multi-agent system working
- ✅ Structured outputs working

**Next**: Push to GitHub and submit!

---

## 📞 Quick Reference

**Server**: http://localhost:8000
**Docs**: http://localhost:8000/docs
**Health**: http://localhost:8000/health

**Main Endpoint**: `POST /execute`
**Request Format**:
```json
{
  "task": "your natural language task here"
}
```

**Working Tasks**:
- "Get weather in [city]"
- "Find latest [topic] news"
- "Get weather in [city] and find [topic] news"

---

Good luck! 🎉
