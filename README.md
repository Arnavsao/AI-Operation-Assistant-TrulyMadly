# AI Operations Assistant

A multi-agent AI system that accepts natural language tasks, plans execution steps, calls real APIs, and returns structured results. Built for the TrulyMadly GenAI Intern assignment.

## Architecture

This system implements a **mandatory multi-agent architecture** with three specialized agents:

### 1. Planner Agent
- Converts natural language input into structured execution plans
- Uses Google Gemini LLM with JSON schema constraints
- Selects appropriate tools and defines parameters for each step
- Validates tool availability before execution

### 2. Executor Agent
- Executes planned steps sequentially
- Calls real third-party APIs with proper error handling
- Implements retry logic for failed API requests (up to 2 retries)
- Collects results from each step

### 3. Verifier Agent
- Validates execution results using LLM
- Assesses output quality and completeness
- Checks for missing or incorrect data
- Formats final structured response with quality scores

### Agent Flow
```
User Task → Planner (LLM) → Execution Plan → Executor (APIs) → Results → Verifier (LLM) → Final Output
```

## Integrated APIs

This system integrates with **three real third-party APIs**:

1. **GitHub API**
   - Search repositories by query
   - Retrieve stars, forks, language, and descriptions
   - Sort by stars, forks, or update date

2. **OpenWeatherMap API**
   - Get current weather for any city
   - Temperature, humidity, wind speed, conditions
   - Support for metric/imperial units

3. **News API**
   - Fetch latest news articles by topic or category
   - Categories: business, technology, sports, entertainment, health, science
   - Returns title, source, author, and publication date

## Project Structure

```
ai_ops_assistant/
├── agents/
│   ├── __init__.py
│   ├── planner.py      # Planner Agent - Creates execution plans
│   ├── executor.py     # Executor Agent - Runs steps and calls tools
│   └── verifier.py     # Verifier Agent - Validates and formats results
├── tools/
│   ├── __init__.py
│   ├── base.py         # Base tool interface
│   ├── github_tool.py  # GitHub API integration
│   ├── weather_tool.py # OpenWeatherMap API integration
│   └── news_tool.py    # News API integration
├── llm/
│   ├── __init__.py
│   └── client.py       # Google Gemini LLM client with structured outputs
├── main.py             # FastAPI application and orchestration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- API Keys (see below)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Add your API keys to `.env`:

```env
# Google Gemini API Key (FREE - no credit card required!)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenWeatherMap API Key (free tier available)
OPENWEATHER_API_KEY=your_openweather_key_here

# News API Key (free tier available)
NEWS_API_KEY=your_newsapi_key_here

# GitHub Token (optional - increases rate limits)
GITHUB_TOKEN=your_github_token_here
```

#### Getting API Keys:

- **Google Gemini**: https://aistudio.google.com/app/apikey (100% FREE, no credit card!)
- **OpenWeatherMap**: https://openweathermap.org/api (free tier: 1000 calls/day)
- **News API**: https://newsapi.org/register (free tier: 100 requests/day)
- **GitHub** (optional): https://github.com/settings/tokens

### 3. Run the Application

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## Usage

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and examples |
| `/health` | GET | Health check endpoint |
| `/tools` | GET | List available tools |
| `/execute` | POST | Execute a natural language task |
| `/docs` | GET | Interactive Swagger UI documentation |

### Example Requests

#### 1. GitHub Repository Search
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the top 5 Python machine learning repositories on GitHub"}'
```

#### 2. Weather Information
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get the current weather in Mumbai and Delhi"}'
```

#### 3. News Search
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the latest news about artificial intelligence"}'
```

#### 4. Multi-Tool Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in London and find latest technology news"}'
```

### Interactive Testing

Visit `http://localhost:8000/docs` for an interactive Swagger UI where you can test all endpoints.

## LLM Usage

### Planner Agent
- **Prompt**: Constrained to JSON schema using Pydantic models
- **Model**: Google Gemini (`models/gemini-flash-latest`)
- **Output**: Structured execution plan with steps and tool selections
- **Temperature**: 0.3 (low for consistent planning)

### Verifier Agent
- **Prompt**: Validates output quality and schema compliance
- **Model**: Google Gemini (`models/gemini-flash-latest`)
- **Output**: Quality assessment and formatted final response
- **Temperature**: 0.5 (moderate for balanced verification)

## Error Handling

- **API Failures**: Automatic retry up to 2 times with exponential backoff
- **Partial Data**: Graceful fallback when some steps succeed and others fail
- **Missing Tools**: Clear error messages when requested tool doesn't exist
- **Rate Limits**: Proper error handling for API quota exceeded scenarios

## Sample Response

```json
{
  "task_summary": "Get the current weather in Mumbai",
  "status": "success",
  "results": {
    "get_weather": [{
      "city": "Mumbai",
      "country": "IN",
      "temperature": 25.99,
      "feels_like": 25.99,
      "humidity": 50,
      "conditions": "smoke",
      "wind_speed": 0,
      "units": "°C"
    }]
  },
  "metadata": {
    "total_steps": 1,
    "successful_steps": 1,
    "failed_steps": 0,
    "quality_score": 8
  },
  "execution_plan": {
    "steps": [{
      "step_number": 1,
      "tool": "get_weather",
      "description": "Retrieve current weather for Mumbai",
      "parameters": {"city": "Mumbai", "units": "metric"}
    }]
  }
}
```

## Known Limitations & Tradeoffs

### Limitations
1. **Sequential Execution**: Steps run sequentially, not in parallel
   - Tradeoff: Simpler implementation, easier debugging
   - Future: Could implement parallel execution for independent steps

2. **API Rate Limits**: Free tier APIs have request limits
   - GitHub: 60 requests/hour (unauthenticated), 5000/hour (with token)
   - OpenWeatherMap: 1000 calls/day
   - News API: 100 requests/day

3. **No Response Caching**: Same queries make fresh API calls
   - Tradeoff: Always fresh data vs. API quota usage
   - Future: Add Redis/in-memory caching with TTL

4. **Fixed Retry Count**: Only 2 retries per failed step
   - Tradeoff: Balance between reliability and speed

5. **LLM Costs**: Each task uses 2-3 LLM calls (planning + verification)
   - Using Google Gemini - **100% FREE!**
   - No credit card required, 1,500 requests/day free tier

### Design Tradeoffs

1. **Structured Outputs vs. Prompt Engineering**
   - Chose: Google Gemini with JSON schema instructions
   - Benefit: Free, reliable JSON outputs with proper prompting
   - Advantage: No cost, no credit card needed

2. **FastAPI vs. Streamlit**
   - Chose: FastAPI for API-first design
   - Benefit: Easy integration, testable, scalable
   - Tradeoff: No built-in UI (but Swagger docs provided)

3. **Synchronous vs. Async Execution**
   - Chose: Synchronous for simplicity
   - Benefit: Easier to debug and understand
   - Tradeoff: Lower throughput under load

## Improvements With More Time

1. **Caching Layer**
   - Cache API responses with TTL to reduce API calls and costs
   - Faster response times for repeated queries

2. **Parallel Tool Execution**
   - Execute independent steps concurrently
   - Reduce total execution time significantly

3. **Cost Tracking**
   - Track LLM token usage per request
   - Monitor API call costs and budget alerts

4. **More Tools**
   - Database queries, email sending, file operations, web scraping
   - Expand capabilities with additional API integrations

5. **Web UI**
   - Interactive frontend with real-time execution progress
   - Result visualization and history tracking

## Technical Details

- **Framework**: FastAPI with async support
- **LLM**: Google Gemini (free tier, no credit card)
- **Structured Outputs**: Pydantic models for type safety
- **Error Handling**: Comprehensive try-catch with retries
- **Documentation**: Auto-generated Swagger UI
- **CORS**: Enabled for frontend integration

## Assignment Compliance

✅ **Multi-agent architecture** (Planner, Executor, Verifier)  
✅ **LLM-powered reasoning** (Google Gemini with structured outputs)  
✅ **Real API integrations** (GitHub, Weather, News)  
✅ **Runnable locally** (`uvicorn main:app --reload`)  
✅ **No monolithic prompts** (Separate agent prompts)  
✅ **Proper project structure** (agents/, tools/, llm/)  
✅ **Complete documentation** (README, .env.example, API docs)  
✅ **Working demo** (Swagger UI + curl examples)  

## Author

**Arnav Sao**  
GenAI Intern Assignment - TrulyMadly  
February 2026

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# 3. Run the server
uvicorn main:app --reload

# 4. Test it
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get weather in Mumbai"}'

# Or visit http://localhost:8000/docs for interactive testing
```

**Note**: Google Gemini API is completely FREE and requires no credit card!
