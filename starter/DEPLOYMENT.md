# Deployment Guide

This guide covers deploying the Census Income Classification API to cloud platforms like Heroku or Render.

## Prerequisites

- Git repository connected to GitHub
- GitHub Actions CI/CD configured and passing
- Trained model artifacts (`model.pkl`, `encoder.pkl`, `lb.pkl`) committed to the repository

## Option 1: Deploy to Heroku

### 1. Create Heroku Account and App

```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create a new app
heroku create your-app-name

# Or via Heroku Dashboard:
# 1. Go to https://dashboard.heroku.com/
# 2. Click "New" -> "Create new app"
# 3. Enter app name and region
```

### 2. Configure Heroku

The project includes necessary files:
- `Procfile`: Tells Heroku how to run the app
- `runtime.txt`: Specifies Python version
- `starter/requirements.txt`: Lists dependencies

### 3. Connect to GitHub

**Via Heroku Dashboard:**
1. Go to your app's dashboard
2. Click on the "Deploy" tab
3. Under "Deployment method", select "GitHub"
4. Connect your GitHub account
5. Search for your repository and connect
6. Enable "Automatic deploys" from the main/master branch
7. Check "Wait for CI to pass before deploy"

**Via CLI:**
```bash
# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

### 4. Verify Deployment

```bash
# Open the app in browser
heroku open

# View logs
heroku logs --tail

# Test the API
python starter/query_live_api.py https://your-app-name.herokuapp.com
```

## Option 2: Deploy to Render

### 1. Create Render Account

1. Go to https://render.com/
2. Sign up and connect your GitHub account

### 2. Create a New Web Service

1. Click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: your-service-name
   - **Region**: Choose closest to you
   - **Branch**: main or master
   - **Root Directory**: (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r starter/requirements.txt`
   - **Start Command**: `cd starter && uvicorn main:app --host=0.0.0.0 --port=$PORT`

### 3. Enable Auto-Deploy

- Render automatically deploys on push to the connected branch
- It will wait for CI to pass if GitHub Actions is configured

### 4. Verify Deployment

Once deployed, Render provides a URL like: `https://your-service-name.onrender.com`

```bash
# Test the API
python starter/query_live_api.py https://your-service-name.onrender.com
```

## Screenshots Required for Submission

Take and save the following screenshots:

1. **continuous_integration.png**
   - GitHub Actions CI passing (green checkmark)
   - Navigate to: Your repo -> Actions tab
   - Show a successful workflow run

2. **continuous_deployment.png**
   - Show automatic deployments enabled
   - For Heroku: Deploy tab showing GitHub connection and auto-deploy enabled
   - For Render: Settings showing auto-deploy from GitHub

3. **example.png**
   - FastAPI automatic documentation showing the example
   - Navigate to: `https://your-app-url.com/docs`
   - Show the POST /predict endpoint with example data visible

4. **live_get.png**
   - Browser showing GET request to root endpoint
   - Navigate to: `https://your-app-url.com/`
   - Show the welcome message JSON response

5. **live_post.png**
   - Terminal showing result of running `query_live_api.py`
   - Show both the status code and prediction result

## Testing the Live API

### Manual Testing in Browser

1. **GET Request:**
   - Open: `https://your-app-url.com/`
   - Should see welcome message

2. **Interactive API Docs:**
   - Open: `https://your-app-url.com/docs`
   - Try the POST /predict endpoint with example data

### Automated Testing with Script

```bash
# Test local deployment
python starter/query_live_api.py http://localhost:8000

# Test live deployment
python starter/query_live_api.py https://your-app-url.com
```

## Troubleshooting

### Common Issues

1. **Import errors on deployment:**
   - Ensure all dependencies are in `requirements.txt`
   - Check that model artifacts are committed to Git

2. **Port binding issues:**
   - Make sure to use `--port=${PORT}` in Procfile
   - The platform assigns the port dynamically

3. **Model files not found:**
   - Ensure model artifacts are committed: `git add starter/model/`
   - Check file paths in `main.py` are relative

4. **Build fails:**
   - Check Python version in `runtime.txt` is supported
   - Review build logs for specific errors

### Viewing Logs

**Heroku:**
```bash
heroku logs --tail
```

**Render:**
- Go to your service dashboard -> Logs tab

## CI/CD Pipeline

The project includes a GitHub Actions workflow that:
1. Runs on push to main/master
2. Installs dependencies
3. Runs flake8 linting
4. Trains the model
5. Runs pytest tests
6. Deployment only happens if all checks pass

## Local Development

To run the API locally:

```bash
# Setup environment
cd starter
source ../.venv/bin/activate  # or use uv

# Train model if not done yet
python starter/train_model.py

# Run API
uvicorn main:app --reload

# Test API
python query_live_api.py http://localhost:8000
```

## Security Considerations

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- For production, add authentication to endpoints
- Consider rate limiting for the API

## Performance Optimization

For production deployments:
- Consider using gunicorn with multiple workers
- Implement caching for model predictions
- Add request validation and error handling
- Monitor response times and scale as needed

