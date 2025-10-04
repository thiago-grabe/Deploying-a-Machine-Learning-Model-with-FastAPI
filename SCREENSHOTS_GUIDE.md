# Screenshots Guide for Project Submission

This guide helps you capture all required screenshots for the project submission.

## Required Screenshots

You need to capture 5 screenshots total:

### 1. continuous_integration.png

**What to capture:** GitHub Actions CI passing

**Steps:**
1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Complete ML pipeline implementation"
   git push origin main
   ```

2. Go to your GitHub repository
3. Click on the "Actions" tab at the top
4. Wait for the workflow to complete (green checkmark)
5. Click on the successful workflow run
6. Take a screenshot showing:
   - Green checkmark indicating success
   - The workflow name ("Python CI/CD")
   - All steps passing (Setup Python, Install dependencies, Lint with flake8, Train model, Test with pytest)
   - The commit message and branch

**What the graders look for:**
- ✅ GitHub Actions is set up
- ✅ Tests run on push to main/master
- ✅ Both pytest and flake8 pass without errors

---

### 2. continuous_deployment.png

**What to capture:** Continuous Deployment configuration enabled

**For Heroku:**
1. Log into Heroku Dashboard
2. Go to your app
3. Click on the "Deploy" tab
4. Take a screenshot showing:
   - Deployment method: GitHub (connected)
   - Your repository name
   - "Automatic deploys" section with checkbox enabled
   - "Wait for CI to pass before deploy" enabled

**For Render:**
1. Log into Render Dashboard
2. Go to your web service
3. Click on "Settings"
4. Take a screenshot showing:
   - GitHub repository connected
   - Branch: main/master
   - Auto-Deploy: Yes

**What the graders look for:**
- ✅ App is connected to GitHub repository
- ✅ Automatic deployments are enabled
- ✅ Deployments wait for CI to pass

---

### 3. example.png

**What to capture:** FastAPI automatic documentation with example data

**Steps:**
1. Go to your deployed app URL (or http://localhost:8000 for local testing)
2. Add `/docs` to the URL (e.g., `https://your-app.herokuapp.com/docs`)
3. Scroll down to find the `POST /predict` endpoint
4. Click on the endpoint to expand it
5. Click on "Try it out" button
6. The example data should automatically populate in the request body
7. Take a screenshot showing:
   - The URL in the browser (showing /docs)
   - The POST /predict endpoint expanded
   - The example data visible in the request body field
   - The schema showing field names with hyphens handled correctly

**What the graders look for:**
- ✅ FastAPI automatic documentation is accessible
- ✅ Pydantic model includes example data
- ✅ Example data is visible and properly formatted
- ✅ Handles hyphenated column names

**Alternative:** You can also capture the "Example Value" section in the Schema view

---

### 4. live_get.png

**What to capture:** Browser showing GET request response

**Steps:**
1. Open your web browser
2. Navigate to your deployed app's root URL (e.g., `https://your-app.herokuapp.com/`)
3. The page should display a JSON response with a welcome message
4. Take a screenshot showing:
   - The full URL in the browser address bar
   - The JSON response with the welcome message
   - The status code (you can see this in the page or browser developer tools)

**Expected response:**
```json
{
  "message": "Welcome to the Census Income Classification API!",
  "docs": "Visit /docs for API documentation",
  "health": "operational"
}
```

**What the graders look for:**
- ✅ The deployed app is accessible
- ✅ GET request on root returns appropriate response
- ✅ Response contains meaningful content

---

### 5. live_post.png

**What to capture:** Terminal showing POST request to live API

**Steps:**
1. Open a terminal/command prompt
2. Make sure you're in the project directory
3. Activate your virtual environment:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Run the query script with your deployed app URL:
   ```bash
   python starter/query_live_api.py https://your-app.herokuapp.com
   ```
5. The script will make GET and POST requests and display results
6. Take a screenshot showing:
   - The command you ran (with the deployed URL)
   - All three test sections:
     - Test 1: GET request with status code 200
     - Test 2: POST request (low income) with status code 200 and prediction
     - Test 3: POST request (high income) with status code 200 and prediction
   - The "API query completed!" message at the end

**What the graders look for:**
- ✅ Script successfully queries the live API
- ✅ Both GET and POST requests return status code 200
- ✅ POST requests return predictions (both <=50K and >50K)
- ✅ The requests module is used (visible in the script)

---

## Screenshot Specifications

**Format:**
- PNG format (as specified in rubric)
- Good resolution (readable text)
- Full window visible (don't crop too much)

**Naming:**
- Exactly as specified (case-sensitive):
  - `continuous_integration.png`
  - `continuous_deployment.png`
  - `example.png`
  - `live_get.png`
  - `live_post.png`

**Where to save:**
- Save in `starter/screenshots/` directory
- Or in the root of your repository
- Make sure they are committed to Git

## Testing Locally First

Before deploying, you can test and capture local screenshots:

**Start local server:**
```bash
cd starter
uvicorn main:app --reload
```

**Then you can:**
1. Visit http://localhost:8000 (for live_get equivalent)
2. Visit http://localhost:8000/docs (for example equivalent)
3. Run query script: `python starter/query_live_api.py http://localhost:8000`

This helps verify everything works before deployment!

## Deployment Quick Checklist

Before capturing screenshots, ensure:

- [ ] All tests pass locally (`pytest tests/`)
- [ ] Flake8 passes (`flake8 .`)
- [ ] Model is trained and artifacts exist in `model/` directory
- [ ] All changes are committed to Git
- [ ] Pushed to GitHub
- [ ] GitHub Actions CI passes
- [ ] App is deployed to Heroku/Render
- [ ] Deployment is connected to GitHub
- [ ] Auto-deploy is enabled
- [ ] Live API is accessible

## Common Issues

**Issue:** API returns 404 or 500 errors
- Check Heroku/Render logs
- Verify model files are committed and pushed
- Check all file paths are relative, not absolute

**Issue:** GitHub Actions fails
- Review the workflow logs
- Common causes: flake8 errors, test failures, missing dependencies
- Fix issues and push again

**Issue:** Can't access deployed app
- Wait a few minutes after deployment
- Check deployment status in Heroku/Render dashboard
- Verify the URL is correct (include https://)

**Issue:** Example data not showing in docs
- Clear browser cache
- Check Pydantic model has `json_schema_extra`
- Verify FastAPI is using correct Pydantic version

## Screenshot Submission

**Where to include screenshots:**

1. **In your GitHub repository:**
   - Create a `screenshots/` directory in `starter/`
   - Add all 5 PNG files
   - Commit and push

2. **In your project submission:**
   - If submitting as a zip, include screenshots folder
   - If submitting GitHub link, ensure screenshots are in the repo
   - Screenshots should be easily accessible to graders

## Example Directory Structure After Screenshots

```
starter/
├── screenshots/
│   ├── continuous_integration.png
│   ├── continuous_deployment.png
│   ├── example.png
│   ├── live_get.png
│   └── live_post.png
├── data/
├── model/
├── tests/
└── ...
```

## Tips for Good Screenshots

1. **Full Context:** Include enough context (URL bars, terminal prompts)
2. **Readable:** Make sure text is clear and readable
3. **Relevant:** Focus on what's being evaluated
4. **Recent:** Take screenshots after final deployment
5. **Consistent:** All from the same deployment/commit

## Verification Checklist

Before submitting, verify each screenshot shows:

**continuous_integration.png:**
- [ ] Green checkmark/success indicator
- [ ] GitHub Actions workflow
- [ ] All steps completed successfully
- [ ] Recent commit (your final code)

**continuous_deployment.png:**
- [ ] Platform name visible (Heroku/Render)
- [ ] GitHub connection shown
- [ ] Auto-deploy enabled
- [ ] Your repository name visible

**example.png:**
- [ ] /docs URL visible
- [ ] POST /predict endpoint
- [ ] Example data visible
- [ ] Schema shows hyphenated field names

**live_get.png:**
- [ ] Deployed URL visible
- [ ] JSON response displayed
- [ ] Welcome message content
- [ ] Browser rendering properly

**live_post.png:**
- [ ] Terminal/command prompt visible
- [ ] Command with deployed URL
- [ ] Status code 200 for both POST requests
- [ ] Both predictions shown (<=50K and >50K)

---

**Ready to Deploy?**

Follow the steps in `starter/DEPLOYMENT.md` to deploy your app, then return here to capture screenshots!

Good luck with your submission! 🚀

