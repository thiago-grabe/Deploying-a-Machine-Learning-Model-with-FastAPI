# Model Card - Census Income Classification

For additional information see the Model Card paper: https://arxiv.org/pdf/1810.03993.pdf

## Model Details

**Model Type:** Random Forest Classifier  
**Model Version:** 1.0.0  
**Author:** ML Engineering Team  
**Date:** October 2025  
**Framework:** scikit-learn 1.7.2  

The model is a Random Forest classifier with 100 estimators and a maximum depth of 10. It uses the following hyperparameters:
- n_estimators: 100
- max_depth: 10
- random_state: 42
- n_jobs: -1 (parallel processing)

The model predicts whether an individual's income exceeds $50K per year based on census data features.

## Intended Use

**Primary Use Cases:**
- Educational demonstration of machine learning deployment with FastAPI
- Income classification for census analysis
- Research into fairness and bias in classification models

**Intended Users:**
- Data scientists and ML engineers learning deployment practices
- Researchers studying income prediction and socioeconomic factors
- Students learning about CI/CD pipelines for ML models

**Out-of-Scope Uses:**
- This model should NOT be used for making real-world decisions about individuals
- Should NOT be used for loan approval, hiring, or any discriminatory purposes
- Not intended for production use without further validation and fairness testing

## Training Data

**Dataset:** UCI Census Income Dataset (also known as "Adult" dataset)  
**Source:** US Census Bureau (1994)  
**Size:** Approximately 32,561 records  
**Train/Test Split:** 80/20 split with random state 42  

**Features (14 total):**

Continuous Features:
- age: Age in years
- fnlgt: Final weight (census sampling weight)
- education-num: Number of years of education
- capital-gain: Capital gains
- capital-loss: Capital losses
- hours-per-week: Hours worked per week

Categorical Features:
- workclass: Type of employer (e.g., Private, State-gov, Self-emp)
- education: Highest education level attained
- marital-status: Marital status
- occupation: Type of occupation
- relationship: Family relationship
- race: Race category
- sex: Gender
- native-country: Country of origin

**Target Variable:**
- salary: Binary classification (<=50K or >50K)

**Preprocessing:**
- Categorical features: One-hot encoded using sklearn's OneHotEncoder
- Label: Binary encoding using LabelBinarizer
- No scaling applied to continuous features
- Spaces in the raw CSV data were removed during data cleaning

## Evaluation Data

**Test Set Size:** 20% of the total dataset (approximately 6,513 records)  
**Data Split:** Random split with seed 42 to ensure reproducibility  
**Processing:** Test data processed using the same encoders fitted on training data

## Metrics

The model is evaluated using three standard classification metrics:

### Overall Model Performance (Test Set):
- **Precision:** 0.7974 (79.74%)
  - Of all instances predicted as >50K, 79.74% were correctly classified
- **Recall:** 0.5385 (53.85%)
  - Of all actual >50K instances, the model correctly identified 53.85%
- **F1 Score:** 0.6429 (64.29%)
  - Harmonic mean of precision and recall

### Interpretation:
- The model shows strong precision, meaning when it predicts high income, it is usually correct
- The recall is moderate, indicating the model misses some high-income individuals (false negatives)
- This trade-off suggests the model is conservative in predicting >50K income
- The F1 score of 64.29% indicates reasonable balanced performance

### Slice Performance:
Performance varies across different demographic slices. Detailed slice metrics are available in `slice_output.txt`, showing performance breakdown by:
- Workclass categories
- Education levels
- Marital status
- Occupation types
- Relationship status
- Race categories
- Gender
- Native country

These slice metrics are crucial for identifying potential biases and ensuring fair model performance across different demographic groups.

## Ethical Considerations

**Bias and Fairness Concerns:**
- The model is trained on 1994 census data, which may not reflect current socioeconomic conditions
- Historical biases present in census data (e.g., wage gaps by gender, race) will be reflected in the model
- The model's predictions should be examined for disparate impact across protected characteristics
- Performance varies significantly across demographic slices (see slice_output.txt)

**Privacy:**
- The dataset contains aggregated census information, not individual identifiable data
- Model predictions should not be used to infer sensitive attributes about specific individuals

**Potential Harms:**
- Using this model for real-world decisions could perpetuate historical inequalities
- Lower recall rates for certain demographic groups could lead to systematic exclusion
- The binary classification of income (<=50K vs >50K) is an oversimplification

**Recommendations:**
- Always conduct fairness audits before deploying income prediction models
- Monitor for disparate impact across protected characteristics
- Consider the temporal gap between training data (1994) and current use
- Implement human oversight for any consequential decisions

## Caveats and Recommendations

**Data Limitations:**
- Training data is from 1994 and does not reflect current economic conditions
- The $50K threshold is not adjusted for inflation or regional cost of living differences
- Census data may have sampling biases and self-reporting inaccuracies

**Model Limitations:**
- Random Forest with limited depth may miss complex non-linear relationships
- No hyperparameter tuning was performed beyond baseline settings
- Feature engineering was minimal; domain expertise could improve performance
- The model does not account for temporal changes in the economy

**Recommendations for Use:**
- Regularly retrain the model with updated census data if used in production
- Conduct thorough fairness testing before any production deployment
- Consider ensemble approaches or more sophisticated models for critical applications
- Implement monitoring for concept drift and model degradation
- Use slice-based evaluation to ensure consistent performance across demographics
- Pair model predictions with human expertise for consequential decisions

**Technical Recommendations:**
- Add feature importance analysis to understand model behavior
- Implement cross-validation for more robust performance estimates
- Consider SHAP values or LIME for model interpretability
- Add calibration techniques if probability estimates are needed
- Version control all data preprocessing steps and model artifacts

**Maintenance:**
- Model should be retrained at least annually with fresh data
- Monitor prediction distributions for signs of drift
- Update slice performance metrics regularly
- Review fairness metrics quarterly
- Document all model updates and performance changes

