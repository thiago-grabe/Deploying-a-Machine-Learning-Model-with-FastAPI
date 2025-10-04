# Deployment Guide

This guide covers deploying the Census Income Classification API to cloud platforms. **This project is currently deployed on Render.com**.

## 🌐 Current Deployment

**Live Production URL:** [https://census-income-api-l4cf.onrender.com](https://census-income-api-l4cf.onrender.com)

- **Platform:** Render.com (Free Tier)
- **Status:** ✅ Live and Operational
- **Auto-Deploy:** Enabled from GitHub main branch
- **CI/CD:** Integrated with GitHub Actions

### Quick Test:
```bash
# Test the live API
python query_live_api.py https://census-income-api-l4cf.onrender.com

# Or visit in browser
open https://census-income-api-l4cf.onrender.com
open https://census-income-api-l4cf.onrender.com/docs
```

## Prerequisites

- ✅ Git repository connected to GitHub
- ✅ GitHub Actions CI/CD configured and passing (14 tests)
- ✅ Trained model artifacts (`model.pkl`, `encoder.pkl`, `lb.pkl`) committed to the repository
- ✅ All dependencies in `requirements.txt`

## Primary Option: Deploy to Render (Current Deployment)

### 1. Sign Up for Render

1. Visit [https://render.com](https://render.com)
2. Sign up with your GitHub account (recommended for easier integration)
3. Authorize Render to access your GitHub repositories

### 2. Create a New Web Service

**Step-by-Step:**

1. **Click "New +"** in the top right corner
2. **Select "Web Service"** from the dropdown
3. **Connect Repository:**
   - If first time: Click "Connect GitHub" and authorize
   - Select your repository: `Deploying-a-Machine-Learning-Model-with-FastAPI`
   - Click "Connect"

4. **Configure Service:**
   ```
   Name: census-income-api (or your choice)
   Region: Oregon (US West) or closest to you
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r starter/requirements.txt
   Start Command: cd starter && uvicorn main:app --host=0.0.0.0 --port=$PORT
   ```

5. **Important Notes:**
   - ⚠️ Use `$PORT` (not `8000`) - Render assigns this dynamically
   - ⚠️ Include `cd starter` in start command
   - ✅ Python version is read from `runtime.txt` (3.13.2)

6. **Click "Create Web Service"**

### 3. Deployment Process

**What Happens:**
```
1. Render clones your repository
2. Installs dependencies from starter/requirements.txt
3. Starts your API with uvicorn
4. Provides a URL: https://your-app-name.onrender.com
```

**Typical deployment time:** 3-5 minutes

**Watch the logs in real-time:**
- You'll see dependency installation
- Model files loading
- Server starting
- ✅ "Your service is live" when complete

### 4. Enable Auto-Deploy (Already Configured!)

**Current Configuration:**
- ✅ **Auto-Deploy:** Enabled by default
- ✅ **Branch:** main
- ✅ **GitHub Integration:** Connected
- ✅ **CI/CD:** Waits for GitHub Actions to pass

**How it works:**
```
Push to GitHub → GitHub Actions runs → Tests pass → Render deploys automatically
```

### 5. Verify Your Deployment

**Your Live URLs:**
- **API Root:** https://census-income-api-l4cf.onrender.com
- **API Docs:** https://census-income-api-l4cf.onrender.com/docs
- **OpenAPI Schema:** https://census-income-api-l4cf.onrender.com/openapi.json

**Test Commands:**
```bash
# Test GET endpoint
curl https://census-income-api-l4cf.onrender.com/

# Test with query script
python query_live_api.py https://census-income-api-l4cf.onrender.com

# Open in browser
open https://census-income-api-l4cf.onrender.com
open https://census-income-api-l4cf.onrender.com/docs
```

### 6. Monitor Your Deployment

**View Logs:**
1. Go to Render Dashboard
2. Click on your service
3. Click "Logs" tab
4. See real-time logs

**Useful Log Commands:**
- Filter by time
- Search for errors
- Download logs

### 7. Render Free Tier Notes

**What to Expect:**
- ✅ Sufficient for this project
- ⚠️ Service "spins down" after 15 minutes of inactivity
- ⏱️ First request after inactivity takes ~30 seconds to "wake up"
- ✅ No time limits - runs 24/7
- ✅ SSL certificate included (HTTPS)

**This is normal behavior!** Just wait 30 seconds if the first request is slow.

## Alternative: Deploy to Heroku

**Note:** Heroku removed its free tier in November 2022. You can still use it with a paid plan.

### Quick Heroku Setup (If You Prefer)

```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Or use GitHub integration:
# 1. Go to https://dashboard.heroku.com/
# 2. Click "New" -> "Create new app"
# 3. Connect to GitHub repository
# 4. Enable automatic deploys
```

**Configuration Files (Already Included):**
- `Procfile`: `web: cd starter && uvicorn main:app --host=0.0.0.0 --port=$PORT`
- `runtime.txt`: `python-3.13.2`
- `starter/requirements.txt`: All dependencies

### Verify Heroku Deployment

```bash
# Open app
heroku open

# View logs
heroku logs --tail

# Test API
python starter/query_live_api.py https://your-app-name.herokuapp.com
```

## 📸 Screenshots (Already Captured!)

All required screenshots have been captured and are in `starter/screenshots/`:

### ✅ Completed Screenshots:

1. **continuous_integration.png** ✅
   - GitHub Actions CI passing with all 14 tests
   - Location: GitHub repo → Actions tab

2. **continuous_deployment.png** ✅
   - Render dashboard showing auto-deploy configuration
   - Shows GitHub integration and automatic deployments

3. **example.png** ✅
   - FastAPI docs at: https://census-income-api-l4cf.onrender.com/docs
   - Shows Pydantic model with examples and Field aliases

4. **live_get.png** ✅
   - Browser showing GET request to root
   - URL: https://census-income-api-l4cf.onrender.com/

5. **live_post.png** ✅
   - Terminal output from `query_live_api.py`
   - Shows both predictions: <=50K and >50K

**All screenshots ready for submission!** See `screenshots/README.md` for details.

## Testing the Live API

### Manual Testing in Browser

1. **GET Request:**
   - Open: https://census-income-api-l4cf.onrender.com/
   - Should see welcome message with health status

2. **Interactive API Docs:**
   - Open: https://census-income-api-l4cf.onrender.com/docs
   - Try the POST /predict endpoint with example data
   - FastAPI provides interactive testing interface

3. **Test Different Predictions:**
   - Use the "Try it out" button in /docs
   - Test with low income example (should predict <=50K)
   - Test with high income example (should predict >50K)

### Automated Testing with Script

```bash
# Test local deployment (for development)
python query_live_api.py http://localhost:8000

# Test live Render deployment
python query_live_api.py https://census-income-api-l4cf.onrender.com
```

**Expected Output:**
```
Querying API at: https://census-income-api-l4cf.onrender.com
================================================================================

1. Testing GET request on root endpoint...
Status Code: 200
Response: {
  "message": "Welcome to the Census Income Classification API!",
  "docs": "Visit /docs for API documentation",
  "health": "operational"
}

2. Testing POST request - Low income example...
Status Code: 200
Prediction: {
  "prediction": "<=50K"
}

3. Testing POST request - High income example...
Status Code: 200
Prediction: {
  "prediction": ">50K"
}

================================================================================
API query completed!
```

## Troubleshooting

### Common Issues

1. **Import errors on deployment:**
   - ✅ **Solution:** All dependencies are in `requirements.txt`
   - ✅ **Verified:** Model artifacts are committed to Git
   - Check: Run `git ls-files starter/model/` to verify

2. **Port binding issues:**
   - ✅ **Solution:** Using `$PORT` in start command (not hardcoded 8000)
   - The platform assigns the port dynamically
   - Current: `cd starter && uvicorn main:app --host=0.0.0.0 --port=$PORT`

3. **Model files not found:**
   - ✅ **Verified:** All `.pkl` files are committed:
     - `starter/model/model.pkl`
     - `starter/model/encoder.pkl`
     - `starter/model/lb.pkl`
   - Check file paths in `main.py` are relative (they are!)

4. **Build fails:**
   - ✅ **Solution:** Python 3.13.2 specified in `runtime.txt`
   - Check Render logs for specific errors
   - Typical build time: 3-5 minutes

5. **Service unavailable / 404 errors:**
   - ✅ **Solution:** Ensure start command includes `cd starter`
   - Current command is correct: `cd starter && uvicorn main:app...`
   - Check that all routes start with correct paths

6. **Slow first request (30 seconds):**
   - ✅ **This is normal!** Render free tier spins down after 15 min
   - First request "wakes up" the service (~30 sec)
   - Subsequent requests are fast
   - **Not a bug** - expected behavior on free tier

### Viewing Logs

**Render (Current Platform):**
1. Go to https://dashboard.render.com
2. Click on your service: `census-income-api`
3. Click "Logs" tab
4. View real-time deployment and runtime logs

**Heroku (If Using):**
```bash
heroku logs --tail
```

### Debugging Tips

**Check Deployment Status:**
- ✅ Green "Live" badge on Render dashboard
- ✅ View recent deploys in "Events" tab
- ✅ Check build logs for errors

**Test Endpoints:**
```bash
# Quick health check
curl https://census-income-api-l4cf.onrender.com/

# Full API test
python query_live_api.py https://census-income-api-l4cf.onrender.com
```

**Common Log Messages:**
```
✅ "Your service is live" - Deployment successful
✅ "Started server process" - Uvicorn running
✅ "Application startup complete" - API ready
⚠️ "Waiting for application startup" - Loading models (normal)
```

## CI/CD Pipeline (Active & Configured)

**Current Setup:**
```
Git Push → GitHub Actions → Render Deployment
```

**GitHub Actions Workflow (`.github/workflows/python-app.yml`):**
1. ✅ Triggers on push to main/master
2. ✅ Sets up Python 3.13 environment
3. ✅ Installs dependencies from `starter/requirements.txt`
4. ✅ Runs flake8 linting (must pass with 0 errors)
5. ✅ Trains the model (ensures reproducibility)
6. ✅ Runs pytest (all 14 tests must pass)
7. ✅ Only deploys if all checks pass

**Render Integration:**
- ✅ Waits for GitHub Actions to complete
- ✅ Auto-deploys on successful CI
- ✅ Skips deployment if CI fails
- ✅ Shows deployment status in dashboard

**Deployment Flow:**
```
1. Developer pushes code
2. GitHub Actions runs (~3-5 min)
   - Linting: flake8 ✓
   - Testing: pytest (14 tests) ✓
   - Model training ✓
3. CI passes ✓
4. Render starts deployment (~3-5 min)
   - Build: Install dependencies ✓
   - Deploy: Start uvicorn ✓
5. Live at: census-income-api-l4cf.onrender.com ✓
```

**View CI Status:**
- GitHub: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- Render: https://dashboard.render.com → Your service → Events

## 💻 Local Development Setup

For development and testing before deploying:

### Initial Setup

```bash
# Clone repository (if starting fresh)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO
cd Deploying-a-Machine-Learning-Model-with-FastAPI

# Create virtual environment with uv (recommended)
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Or with standard venv
python3.13 -m venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -r starter/requirements.txt
# Or: pip install -r starter/requirements.txt
```

### Train Model Locally

```bash
# Navigate to starter directory
cd starter

# Run training script
python starter/train_model.py

# This creates:
# - model/model.pkl (trained Random Forest)
# - model/encoder.pkl (feature encoder)
# - model/lb.pkl (label binarizer)
# - slice_output.txt (performance metrics)
```

### Run API Locally

```bash
# Start the API (from starter directory)
uvicorn main:app --reload

# API will be available at:
# - http://localhost:8000
# - http://localhost:8000/docs (interactive docs)
```

**What `--reload` does:**
- Auto-reloads on code changes
- Perfect for development
- Don't use in production

### Test Local API

```bash
# In a new terminal (keep API running)
cd starter

# Test with query script
python query_live_api.py http://localhost:8000

# Or test endpoints directly
curl http://localhost:8000/
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @test_data.json

# View interactive docs
open http://localhost:8000/docs
```

### Run Tests Locally

```bash
# Run all tests
cd starter
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_model.py -v
python -m pytest tests/test_api.py -v

# Run with coverage
python -m pytest tests/ --cov=starter --cov-report=html

# Lint code
flake8 .
```

### Development Workflow

```bash
# 1. Make changes to code
# 2. Test locally
python -m pytest tests/ -v
flake8 .

# 3. Train model (if changed)
python starter/train_model.py

# 4. Test API locally
uvicorn main:app --reload
python query_live_api.py http://localhost:8000

# 5. Commit and push
git add .
git commit -m "Your changes"
git push origin main

# 6. GitHub Actions runs automatically
# 7. Render deploys if CI passes
# 8. Live at: https://census-income-api-l4cf.onrender.com
```

### Local Environment Variables (Optional)

Create `.env` file for local development (don't commit this):
```env
ENV=development
PORT=8000
LOG_LEVEL=debug
```

### Debugging Tips

**API not starting?**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 $(lsof -t -i :8000)

# Check Python version
python --version  # Should be 3.13.x

# Verify dependencies
pip list | grep fastapi
pip list | grep uvicorn
```

**Tests failing?**
```bash
# Check imports
python -c "from starter.ml.model import train_model; print('OK')"

# Verify model files exist
ls -la model/

# Run single test for debugging
python -m pytest tests/test_api.py::test_get_root -v -s
```

**Model not loading?**
```bash
# Verify model files are present
ls -la model/*.pkl

# Check file sizes (should not be empty)
ls -lh model/*.pkl

# Retrain if needed
python starter/train_model.py
```

## Security Considerations

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- For production, add authentication to endpoints
- Consider rate limiting for the API

## Performance Optimization

### Current Production Setup

**What's Running:**
- ✅ Uvicorn ASGI server
- ✅ Single worker (sufficient for free tier)
- ✅ FastAPI with automatic validation
- ✅ Model loaded once at startup

**Performance Stats:**
- Response time: ~100-300ms (after warm-up)
- First request: ~30 seconds (wake-up from sleep)
- Subsequent requests: Fast (<500ms)

### For Scaling to Paid Tier

If you upgrade or need higher performance:

**1. Use Gunicorn with Multiple Workers:**
```bash
# Update start command to:
gunicorn starter.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**2. Add Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_prediction(input_hash):
    # Cache frequent predictions
    pass
```

**3. Implement Request Limits:**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(data: CensusData):
    ...
```

**4. Add Monitoring:**
- Use Render's built-in metrics
- Add logging for prediction times
- Monitor error rates

**5. Database for Predictions (Optional):**
- Store predictions for audit trail
- Track usage patterns
- Analyze model performance over time

### Current Limitations (Free Tier)

**Render Free Tier:**
- ✅ Good for: Demo, portfolio, low traffic
- ⚠️ Limitation: Spins down after 15 min
- ⚠️ Cold start: ~30 seconds
- ✅ No time limits: Runs 24/7 when active

**When to Upgrade:**
- High traffic (>1000 requests/day)
- Need 24/7 availability without cold starts
- Multiple workers needed
- Custom domains
- More resources (CPU/RAM)

