# 🔑 API Keys Setup Guide

This guide will help you get all the required API keys for the AI Operations Assistant.

## Required API Keys

You need **3 API keys** to run this project. All have free tiers!

---

## 1. Google Gemini API Key (Required) - **FREE!**

### What it's for
Powers the LLM for planning and verification

### Free Tier
**Completely FREE** - No credit card required!
- 15 requests per minute
- 1,500 requests per day
- Perfect for this assignment

### How to get it

1. **Go to**: https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click**: "Create API Key"
4. **Select**: "Create API key in new project" (or use existing project)
5. **Copy** the API key (starts with `AIza...`)
6. **Paste** into `.env` file as `GEMINI_API_KEY`

### Important
- Keep this key secret!
- Don't commit it to git
- Monitor usage at: https://aistudio.google.com/app/apikey
- **No credit card needed** - 100% free!

---

## 2. OpenWeatherMap API Key (Required)

### What it's for
Provides current weather data for cities

### Free Tier
- 1,000 API calls per day
- 60 calls per minute
- Current weather data

### How to get it

1. **Go to**: https://openweathermap.org/api
2. **Click**: "Sign Up" (top right)
3. **Fill** the registration form
4. **Verify** your email
5. **Log in** to your account
6. **Go to**: https://home.openweathermap.org/api_keys
7. **Copy** the default API key (or create a new one)
8. **Paste** into `.env` file as `OPENWEATHER_API_KEY`

### Note
- API key activation takes ~10 minutes
- If you get 401 errors, wait a bit longer
- Free tier is more than enough for testing

---

## 3. News API Key (Required)

### What it's for
Fetches latest news articles by topic or category

### Free Tier
- 100 requests per day
- Access to top headlines
- Search by keyword or category

### How to get it

1. **Go to**: https://newsapi.org/register
2. **Fill** the registration form
   - Name
   - Email
   - Password
3. **Select**: "Individual" plan (Free)
4. **Agree** to terms
5. **Submit** the form
6. **Check** your email for confirmation
7. **Log in** at: https://newsapi.org/account
8. **Copy** your API key from the dashboard
9. **Paste** into `.env` file as `NEWS_API_KEY`

### Limitations
- Development use only (free tier)
- 100 requests/day limit
- Perfect for this assignment

---

## 4. GitHub Token (Optional)

### What it's for
Increases GitHub API rate limits from 60 to 5,000 requests/hour

### Free Tier
Unlimited (it's your personal token)

### How to get it

1. **Go to**: https://github.com/settings/tokens
2. **Click**: "Generate new token" → "Generate new token (classic)"
3. **Name it**: "AI Operations Assistant"
4. **Select scopes**: `public_repo` (read access to public repos)
5. **Set expiration**: 30 days (or as needed)
6. **Click**: "Generate token"
7. **Copy** the token (starts with `ghp_...`)
8. **Paste** into `.env` file as `GITHUB_TOKEN`

### Note
- This is optional but recommended
- Without it, you're limited to 60 requests/hour
- With it, you get 5,000 requests/hour

---

## Setting Up Your .env File

Once you have all the keys, create a `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit it with your favorite editor
nano .env
# or
code .env
# or
vim .env
```

Your `.env` should look like this:

```env
# Google Gemini API Key (required - FREE!)
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenWeatherMap API Key (required)
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# News API Key (required)
NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub Token (optional but recommended)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Server Configuration (optional)
HOST=0.0.0.0
PORT=8000
```

---

## Verification

After setting up your `.env` file, verify everything works:

```bash
python test_setup.py
```

This will:
- ✅ Check all environment variables are set
- ✅ Verify all dependencies are installed
- ✅ Test connectivity to all APIs

---

## Troubleshooting

### Google Gemini API Key Issues

**Error**: "API key not valid"
- Make sure you copied the entire key (starts with `AIza`)
- Check for extra spaces or newlines
- Verify the key at: https://aistudio.google.com/app/apikey

**Error**: "Quota exceeded"
- You've used all your free quota (1,500/day)
- Wait 24 hours for quota to reset
- Gemini is completely free, no payment needed!

### OpenWeatherMap Issues

**Error**: "Invalid API key"
- Wait 10-15 minutes after creating the key
- Check you copied the correct key
- Verify at: https://home.openweathermap.org/api_keys

### News API Issues

**Error**: "Your API key is invalid"
- Check you copied the key correctly
- Verify your email address
- Log in to check your key: https://newsapi.org/account

**Error**: "You have made too many requests"
- You've hit the 100/day limit
- Wait 24 hours or upgrade to paid plan

### GitHub Token Issues

**Error**: "Bad credentials"
- Make sure token has `public_repo` scope
- Check token hasn't expired
- Regenerate if needed

---

## Cost Estimates

### For Testing (10-20 requests)
- **Gemini: FREE** (no cost, no credit card needed!)
- Weather: Free (within 1,000/day limit)
- News: Free (within 100/day limit)
- GitHub: Free (within rate limits)

**Total**: **100% FREE** for testing!

### For Production (1,000 requests/day)
- **Gemini: FREE** (within 1,500/day limit)
- Weather: Free or $0 (free tier)
- News: ~$9/month (paid plan needed)
- GitHub: Free

**Gemini Advantage**: No credit card, no billing, completely free! 🎉

---

## Security Best Practices

1. **Never commit `.env` to git**
   - It's in `.gitignore` already
   - Double-check before pushing

2. **Rotate keys regularly**
   - Especially if shared or exposed
   - Easy to regenerate

3. **Use environment variables**
   - Never hardcode keys in code
   - Use `.env` file locally
   - Use secrets manager in production

4. **Monitor usage**
   - Check OpenAI usage dashboard
   - Watch for unexpected spikes
   - Set up billing alerts

---

## Ready to Go!

Once you have all 3 required keys (4 if including GitHub), you're ready to run:

```bash
# Verify setup
python test_setup.py

# Start the server
uvicorn main:app --reload

# Test it
python example_client.py
```

---

## Need Help?

- **Google Gemini**: https://ai.google.dev/docs
- **OpenWeatherMap**: https://openweathermap.org/faq
- **News API**: https://newsapi.org/docs
- **GitHub**: https://docs.github.com/en/authentication

---

**Total Setup Time**: ~10-15 minutes

**Cost**: **100% FREE** (using free tiers)

Good luck! 🚀
