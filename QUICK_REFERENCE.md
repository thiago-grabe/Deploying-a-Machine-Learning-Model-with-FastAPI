# Quick Reference Guide

A cheat sheet for common commands and important information.

## 🚀 Setup Commands

```bash
# Clone and setup
git clone <repo-url>
cd Deploying-a-Machine-Learning-Model-with-FastAPI

# Create virtual environment (using uv)
uv venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -r starter/requirements.txt

# Train model
cd starter
python starter/train_model.py
```

## 🧪 Testing Commands

```bash
# Run all tests
cd starter
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_model.py -v
python -m pytest tests/test_api.py -v

# Run with coverage
python -m pytest tests/ --cov=starter --cov-report=html

# Lint code
flake8 .

# Run sanity check
echo "tests/test_api.py" | python sanitycheck.py
```

## 🌐 API Commands

```bash
# Start API locally
cd starter
uvicorn main:app --reload

# Start API on specific port
uvicorn main:app --host 0.0.0.0 --port 8080

# Query local API
python query_live_api.py http://localhost:8000

# Query live API
python query_live_api.py https://your-app.herokuapp.com
```

## 📁 Important File Locations

| File | Location | Purpose |
|------|----------|---------|
| **Model artifacts** | `starter/model/*.pkl` | Trained model and encoders |
| **Training script** | `starter/starter/train_model.py` | Train and evaluate model |
| **API application** | `starter/main.py` | FastAPI application |
| **Model functions** | `starter/starter/ml/model.py` | ML model code |
| **Data processing** | `starter/starter/ml/data.py` | Data preprocessing |
| **Model tests** | `starter/tests/test_model.py` | Unit tests for model |
| **API tests** | `starter/tests/test_api.py` | Unit tests for API |
| **Slice output** | `starter/slice_output.txt` | Performance on slices |
| **Model card** | `starter/model_card.md` | Model documentation |
| **CI/CD workflow** | `.github/workflows/python-app.yml` | GitHub Actions |
| **Requirements** | `starter/requirements.txt` | Python dependencies |

## 🔍 Quick Checks

### Verify Everything Works
```bash
# 1. Check flake8
cd starter && flake8 .

# 2. Run tests
python -m pytest tests/ -v

# 3. Start API
uvicorn main:app --reload

# 4. In another terminal, test API
python query_live_api.py http://localhost:8000
```

### Model Performance
- **Precision:** 79.74%
- **Recall:** 53.85%  
- **F1 Score:** 64.29%

### Test Coverage
- **Total tests:** 14
- **Model tests:** 10
- **API tests:** 5

## 📸 Screenshot Checklist

Save in `starter/screenshots/`:

- [ ] `continuous_integration.png` - GitHub Actions passing
- [ ] `continuous_deployment.png` - Auto-deploy enabled
- [ ] `example.png` - API docs with example
- [ ] `live_get.png` - Browser GET response
- [ ] `live_post.png` - Terminal POST results

## 🚢 Deployment Quick Start

### Heroku
```bash
# Install Heroku CLI
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

### Render
1. Go to https://render.com
2. Connect GitHub repo
3. Create Web Service
4. Set build command: `pip install -r starter/requirements.txt`
5. Set start command: `cd starter && uvicorn main:app --host=0.0.0.0 --port=$PORT`

## 🔧 Troubleshooting

### Tests Failing?
```bash
# Check imports
cd starter
python -c "from ml.model import train_model; print('OK')"

# Retrain model
python starter/train_model.py

# Run single test
python -m pytest tests/test_api.py::test_get_root -v
```

### Flake8 Errors?
```bash
# Check specific file
flake8 main.py

# Auto-fix some issues
autopep8 --in-place --aggressive main.py
```

### API Not Starting?
```bash
# Check if port is in use
lsof -i :8000

# Kill process on port
kill -9 $(lsof -t -i :8000)

# Check model files exist
ls -la model/
```

### Import Errors?
```bash
# Verify virtual environment
which python
python --version  # Should be 3.13

# Reinstall dependencies
pip install -r starter/requirements.txt
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/docs` | Interactive API docs |
| GET | `/openapi.json` | OpenAPI schema |
| POST | `/predict` | Model inference |

## 🔑 Key Environment Variables

For deployment (if needed):
```bash
# Heroku
heroku config:set PYTHON_VERSION=3.13

# Local .env file (if used)
PORT=8000
ENV=production
```

## 📝 Git Commands

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <repo-url>
git push -u origin main

# Regular workflow
git add .
git commit -m "Your message"
git push

# Check status
git status
git log --oneline
```

## 🎯 Rubric Quick Check

✅ **Model Building:**
- [x] Random Forest trained
- [x] Train/test split (80/20)
- [x] Functions: train, inference, compute_metrics
- [x] Model save/load implemented
- [x] Training script complete

✅ **Testing:**
- [x] 10+ model tests
- [x] 3+ API tests
- [x] pytest passing
- [x] flake8 passing

✅ **Slice Validation:**
- [x] Function implemented
- [x] All categorical features
- [x] Output to slice_output.txt

✅ **Model Card:**
- [x] All sections complete
- [x] Metrics included
- [x] Complete sentences

✅ **API:**
- [x] GET / endpoint
- [x] POST /predict endpoint
- [x] Type hints used
- [x] Pydantic models
- [x] Examples in schema
- [x] Hyphens handled

✅ **CI/CD:**
- [x] GitHub Actions workflow
- [x] pytest on push
- [x] flake8 on push
- [x] Python 3.13

✅ **Deployment:**
- [x] Procfile created
- [x] runtime.txt created
- [x] Query script created

## 🔗 Important URLs

**Local:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

**After Deployment:**
- Heroku: https://your-app.herokuapp.com
- Render: https://your-app.onrender.com

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview and setup |
| `PROJECT_SUMMARY.md` | Detailed rubric compliance |
| `DEPLOYMENT.md` | Deployment instructions |
| `SCREENSHOTS_GUIDE.md` | Screenshot requirements |
| `QUICK_REFERENCE.md` | This file - quick commands |
| `model_card.md` | Model documentation |

## 💡 Tips

1. **Before committing:** Run `flake8 .` and `pytest`
2. **Before deploying:** Test locally with `query_live_api.py`
3. **For screenshots:** Use high resolution, full window
4. **Git commits:** Commit often, small changes
5. **Model artifacts:** Ensure `.pkl` files are committed

## 🆘 Help Resources

- **Detailed docs:** See `PROJECT_SUMMARY.md`
- **Deployment help:** See `starter/DEPLOYMENT.md`
- **Screenshot help:** See `SCREENSHOTS_GUIDE.md`
- **Model details:** See `starter/model_card.md`

---

**Need more help?** All commands assume you're in the project root or `starter/` directory as indicated.

