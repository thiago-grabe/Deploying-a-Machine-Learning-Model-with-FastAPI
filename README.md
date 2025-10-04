# Census Income Classification - ML Pipeline with FastAPI

A complete machine learning pipeline for predicting whether an individual's income exceeds $50K/year based on US Census data. Features a Random Forest classifier, RESTful API built with FastAPI, comprehensive testing, and CI/CD integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.13
- Git
- UV package manager (recommended) or pip

### Installation

**Option 1: Using UV (Recommended)**
```bash
# Install uv if not already installed
# curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd Deploying-a-Machine-Learning-Model-with-FastAPI

# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r starter/requirements.txt
```

**Option 2: Using pip and venv**
```bash
# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r starter/requirements.txt
```

### Train the Model
```bash
cd starter
python starter/train_model.py
```

### Run the API Locally
```bash
cd starter
uvicorn main:app --reload
```
Visit http://localhost:8000/docs for interactive API documentation

### Run Tests
```bash
cd starter
python -m pytest tests/ -v
flake8 .
```

## 📋 Project Structure

```
.
├── .github/workflows/
│   └── python-app.yml          # CI/CD pipeline
├── starter/
│   ├── data/
│   │   └── census.csv          # Clean census data
│   ├── model/
│   │   ├── model.pkl          # Trained model
│   │   ├── encoder.pkl        # Feature encoder
│   │   └── lb.pkl             # Label binarizer
│   ├── starter/
│   │   ├── ml/
│   │   │   ├── data.py       # Data processing
│   │   │   └── model.py      # ML model functions
│   │   └── train_model.py    # Training script
│   ├── tests/
│   │   ├── test_model.py     # Model unit tests
│   │   └── test_api.py       # API tests
│   ├── screenshots/          # Required screenshots
│   ├── main.py              # FastAPI application
│   ├── query_live_api.py    # API query script
│   ├── model_card.md        # Model documentation
│   └── slice_output.txt     # Slice performance metrics
├── Procfile                  # Heroku/Render config
├── runtime.txt              # Python version
├── PROJECT_SUMMARY.md       # Detailed project overview
├── SCREENSHOTS_GUIDE.md     # Screenshot instructions
└── README.md               # This file
```

## 🎯 Features

- **Machine Learning Model**: Random Forest classifier with 79.74% precision
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Comprehensive Testing**: 14 unit tests covering models and API
- **CI/CD Pipeline**: GitHub Actions with pytest and flake8
- **Data Slice Validation**: Performance metrics across demographic groups
- **Production Ready**: Deployment configs for Heroku/Render
- **Full Documentation**: Model card and deployment guides

## 📊 Model Performance

- **Precision**: 79.74%
- **Recall**: 53.85%
- **F1 Score**: 64.29%

Performance metrics available for all categorical feature slices in `starter/slice_output.txt`

## 🧪 Environment Set up
* **Option 1: Using UV (Recommended)**
    * Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
    * Create virtual environment: `uv venv .venv`
    * Activate environment: `source .venv/bin/activate` (On Windows: `.venv\Scripts\activate`)
    * Install dependencies: `uv pip install -r starter/requirements.txt`

* **Option 2: Using pip and venv**
    * Ensure you have Python 3.13 installed
    * Create virtual environment: `python3.13 -m venv .venv`
    * Activate environment: `source .venv/bin/activate` (On Windows: `.venv\Scripts\activate`)
    * Install dependencies: `pip install -r starter/requirements.txt`

## 🔧 API Endpoints

### GET /
Returns welcome message and API information.

**Response:**
```json
{
  "message": "Welcome to the Census Income Classification API!",
  "docs": "Visit /docs for API documentation",
  "health": "operational"
}
```

### POST /predict
Performs income classification prediction.

**Request Body Example:**
```json
{
  "age": 37,
  "workclass": "Private",
  "fnlgt": 178356,
  "education": "HS-grad",
  "education-num": 10,
  "marital-status": "Married-civ-spouse",
  "occupation": "Prof-specialty",
  "relationship": "Husband",
  "race": "White",
  "sex": "Male",
  "capital-gain": 0,
  "capital-loss": 0,
  "hours-per-week": 40,
  "native-country": "United-States"
}
```

**Response:**
```json
{
  "prediction": ">50K"
}
```

## 🧪 Testing

The project includes comprehensive tests:

**Model Tests (10 tests):**
- Model training and type validation
- Inference functionality
- Metrics computation
- Model/encoder persistence
- Data processing

**API Tests (5 tests):**
- GET endpoint (status and content)
- POST endpoints (both prediction classes)
- Input validation
- OpenAPI documentation

**Run all tests:**
```bash
cd starter
python -m pytest tests/ -v
```

**Run specific test file:**
```bash
python -m pytest tests/test_model.py -v
python -m pytest tests/test_api.py -v
```

## 🚀 Deployment

### Quick Deploy to Heroku

1. **Setup Heroku:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

2. **Enable auto-deploy from GitHub:**
   - Go to Heroku Dashboard → Your App → Deploy tab
   - Connect to GitHub repository
   - Enable "Automatic deploys"
   - Check "Wait for CI to pass before deploy"

### Quick Deploy to Render

1. Connect GitHub repository on Render
2. Configure:
   - Build Command: `pip install -r starter/requirements.txt`
   - Start Command: `cd starter && uvicorn main:app --host=0.0.0.0 --port=$PORT`
3. Deploy automatically on push

**Detailed deployment instructions:** See `starter/DEPLOYMENT.md`

## 📸 Required Screenshots

For project submission, capture these screenshots (guide in `SCREENSHOTS_GUIDE.md`):

1. `continuous_integration.png` - GitHub Actions passing
2. `continuous_deployment.png` - Auto-deploy enabled
3. `example.png` - API docs showing example data
4. `live_get.png` - Browser GET request response
5. `live_post.png` - Terminal POST request results

## 📚 Documentation

- **`PROJECT_SUMMARY.md`** - Complete project overview and rubric compliance
- **`starter/model_card.md`** - Detailed model documentation
- **`starter/DEPLOYMENT.md`** - Deployment guide for cloud platforms
- **`SCREENSHOTS_GUIDE.md`** - Instructions for required screenshots
- **`starter/slice_output.txt`** - Model performance across demographic slices

## 🔄 CI/CD Pipeline

GitHub Actions workflow automatically:
1. Runs on push to main/master
2. Sets up Python 3.13 environment
3. Installs dependencies
4. Lints code with flake8
5. Trains the model
6. Runs all pytest tests
7. Blocks deployment if any step fails

## 📦 Key Technologies

- **Python 3.13** - Latest Python version
- **FastAPI** - Modern web framework for APIs
- **Pydantic** - Data validation using type hints
- **scikit-learn** - Machine learning library
- **pytest** - Testing framework
- **GitHub Actions** - CI/CD automation
- **Heroku/Render** - Cloud deployment platforms

## 🎓 Learning Outcomes

This project demonstrates:
- End-to-end ML pipeline development
- RESTful API design and implementation
- Unit testing best practices
- CI/CD automation
- Model deployment to production
- Code quality and linting
- Documentation and model cards
- Bias detection through slice validation

## 📋 Project Checklist

- [x] Data cleaning (remove spaces from CSV)
- [x] Model training (Random Forest)
- [x] Model persistence (save/load functions)
- [x] Unit tests (14 tests total)
- [x] Slice validation (8 categorical features)
- [x] FastAPI application
- [x] Pydantic models with examples
- [x] API tests (GET and 2 POST)
- [x] Model card documentation
- [x] GitHub Actions CI/CD
- [x] Deployment configuration
- [x] Query script for live API
- [x] flake8 compliance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

See LICENSE.txt for details

## 🆘 Support

- Review `PROJECT_SUMMARY.md` for detailed implementation guide
- Check `starter/DEPLOYMENT.md` for deployment troubleshooting
- Consult `SCREENSHOTS_GUIDE.md` for screenshot requirements

## 🎯 Next Steps

1. **Review the code:** Explore the implementation in `starter/`
2. **Run tests:** Verify everything works locally
3. **Train model:** Generate model artifacts
4. **Test API:** Try the endpoints locally
5. **Deploy:** Follow `DEPLOYMENT.md` guide
6. **Screenshots:** Capture required screenshots using `SCREENSHOTS_GUIDE.md`
7. **Submit:** Include GitHub link and screenshots

---

**Project Status:** ✅ Complete and Production Ready

For detailed information about rubric compliance and project structure, see `PROJECT_SUMMARY.md`
