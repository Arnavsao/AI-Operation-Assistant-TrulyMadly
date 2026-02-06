# AI Operations Assistant

A multi-agent AI system that accepts natural language tasks, plans execution steps, calls real APIs, and returns structured results. Built for the TrulyMadly GenAI Intern assignment.

## 🏗️ Architecture

This system implements a **multi-agent architecture** with three specialized agents:

### 1. **Planner Agent**
- Analyzes natural language input using LLM
- Creates structured execution plans with tool selection
- Uses Google Gemini with JSON schema instructions for structured outputs
- Validates tool availability and parameter requirements

### 2. **Executor Agent**
- Executes planned steps sequentially
- Calls appropriate API tools with parameters
- Implements retry logic for failed API requests
- Handles errors gracefully with fallback mechanisms

### 3. **Verifier Agent**
- Validates execution results using LLM
- Assesses output quality and completeness
- Formats final structured response
- Provides quality scores and improvement suggestions

### Agent Flow
```
User Task → Planner → Execution Plan → Executor → Results → Verifier → Final Output
```

## 🛠️ Integrated APIs

1. **GitHub API** (`github_search`)
   - Search repositories by query
   - Get stars, forks, language, and descriptions
   - Sort by stars, forks, or update date

2. **OpenWeatherMap API** (`get_weather`)
   - Current weather for any city
   - Temperature, humidity, wind speed
   - Support for metric/imperial units

3. **News API** (`get_news`)
   - Latest news articles by topic or category
   - Categories: business, technology, sports, entertainment, health, science
   - Returns title, source, author, and publication date

## 📋 Prerequisites

- Python 3.8 or higher
- API Keys (see Setup Instructions)

## 🚀 Setup Instructions

### 1. Clone or Download Repository
```bash
cd trulymadly
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: Google Gemini API Key (FREE!)
GEMINI_API_KEY=AIza-your-gemini-key-here

# Required: OpenWeatherMap API Key (free tier available)
OPENWEATHER_API_KEY=your-openweather-key-here

# Required: News API Key (free tier available)
NEWS_API_KEY=your-newsapi-key-here

# Optional: GitHub Token (increases rate limits)
GITHUB_TOKEN=ghp_your-github-token-here
```

#### Getting API Keys:

- **Google Gemini**: https://aistudio.google.com/app/apikey (100% FREE, no credit card!)
- **OpenWeatherMap**: https://openweathermap.org/api (free tier: 1000 calls/day)
- **News API**: https://newsapi.org/register (free tier: 100 requests/day)
- **GitHub** (optional): https://github.com/settings/tokens

### 5. Run the Application
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## 📝 Example Prompts

### 1. GitHub Repository Search
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the top 5 Python machine learning repositories on GitHub"}'
```

### 2. Weather Information
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get the current weather in Mumbai and Bangalore"}'
```

### 3. News Search
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find the latest news about artificial intelligence"}'
```

### 4. Multi-Tool Task
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Search for React repositories on GitHub and get weather in San Francisco"}'
```

### 5. Complex Query
```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Get technology news, find top JavaScript projects, and check weather in New York"}'
```

## 🌐 API Endpoints

### `GET /`
Returns API information and example tasks

### `GET /health`
Health check endpoint showing system status

### `GET /tools`
Lists all available tools with descriptions and parameters

### `POST /execute`
Execute a natural language task

**Request Body:**
```json
{
  "task": "Your natural language task here"
}
```

**Response:**
```json
{
  "task_summary": "Summary of the task",
  "status": "success|partial|failed",
  "results": {
    "github_search": [...],
    "get_weather": [...],
    "get_news": [...]
  },
  "metadata": {
    "total_steps": 3,
    "successful_steps": 3,
    "failed_steps": 0,
    "quality_score": 9,
    "verification": {...}
  },
  "execution_plan": {
    "steps": [...],
    "expected_output": "..."
  }
}
```

## 🧪 Testing the System

### Using cURL
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test tools listing
curl http://localhost:8000/tools

# Execute a task
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Find top 3 Python repos"}'
```

### Using Browser
1. Navigate to `http://localhost:8000` for API documentation
2. Visit `http://localhost:8000/docs` for interactive Swagger UI
3. Use the interactive interface to test endpoints

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/execute",
    json={"task": "Get weather in London and find news about climate change"}
)

print(response.json())
```

## 📁 Project Structure

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

## 🔍 How It Works

1. **User submits a task** via POST request to `/execute`
2. **Planner Agent** uses Google Gemini to analyze the task and create a structured plan:
   - Breaks down task into steps
   - Selects appropriate tools
   - Defines parameters for each tool
3. **Executor Agent** runs each step:
   - Calls the specified tool with parameters
   - Implements retry logic for API failures
   - Collects results from each step
4. **Verifier Agent** validates the output:
   - Uses LLM to assess quality and completeness
   - Checks for missing data
   - Formats final structured response
5. **System returns** complete results with metadata

## ⚠️ Known Limitations & Tradeoffs

### Limitations
1. **Sequential Execution**: Steps run sequentially, not in parallel
   - Tradeoff: Simpler implementation, easier debugging
   - Future: Could implement parallel execution for independent steps

2. **API Rate Limits**: Free tier APIs have request limits
   - GitHub: 60 requests/hour (unauthenticated), 5000/hour (with token)
   - OpenWeatherMap: 1000 calls/day
   - News API: 100 requests/day
   - Mitigation: Implement caching (future enhancement)

3. **No Response Caching**: Same queries make fresh API calls
   - Tradeoff: Always fresh data vs. API quota usage
   - Future: Add Redis/in-memory caching with TTL

4. **Fixed Retry Count**: Only 2 retries per failed step
   - Tradeoff: Balance between reliability and speed
   - Future: Configurable retry policies

5. **LLM Costs**: Each task uses 2-3 LLM calls (planning + verification)
   - Using Google Gemini 1.5 Flash - **100% FREE!**
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

## 🚀 Future Enhancements

With more time, the following improvements could be made:

1. **Caching Layer**
   - Cache API responses with TTL
   - Reduce API calls and costs
   - Faster response times

2. **Parallel Execution**
   - Execute independent steps concurrently
   - Reduce total execution time

3. **Cost Tracking**
   - Track LLM token usage per request
   - Monitor API call costs
   - Budget alerts

4. **More Tools**
   - Database queries
   - Email sending
   - File operations
   - Web scraping

5. **Web UI**
   - Interactive frontend with Streamlit or React
   - Real-time execution progress
   - Result visualization

6. **Persistent Storage**
   - Save execution history
   - Analytics dashboard
   - User sessions

## 🧑‍💻 Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (if implemented)
pytest tests/
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 📄 License

This project is created for the TrulyMadly GenAI Intern assignment.

## 👤 Author

**Arnav Sao**
- Assignment: GenAI Intern - TrulyMadly
- Submission Date: February 2026

---

## ✅ Assignment Checklist

- [x] Multi-agent design (Planner, Executor, Verifier)
- [x] LLM with structured outputs (Google Gemini with Pydantic models)
- [x] At least 2 real third-party APIs (GitHub, Weather, News)
- [x] Complete end-to-end execution
- [x] No hardcoded responses
- [x] Runs locally with one command (`uvicorn main:app`)
- [x] README with setup instructions
- [x] Environment variables documented (.env.example)
- [x] Architecture explanation
- [x] List of integrated APIs
- [x] 3-5 example prompts
- [x] Known limitations and tradeoffs
# AI-Operation-Assistant--TrulyMadly
# AI-Operation-Assistant--TrulyMadly-
# AI-Operation-Assistant-TrulyMadly
# AI-Operation-Assistant-TrulyMadly
