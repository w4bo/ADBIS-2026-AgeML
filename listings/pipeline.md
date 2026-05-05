> **Created at:** 2026-04-23 16:28:51 UTC

## Pipeline 16

1. **imputation** with `iterative_imputer`
2. **normalization** with `standard`
3. **features** with `select_k_best`
4. **rebalancing** with `smote`
5. **classification** with `nn`

The machine learning pipeline consists of the following five steps: 

1. **Imputation**: Uses `IterativeImputer` to estimate missing values based on the relationships between other features in the dataset.
2. **Normalization**: Applies `StandardScaler` to transform features to have zero mean and unit variance, ensuring consistent feature scales for the model.
3. **Features**: Implements `SelectKBest` to identify and retain the top-k most relevant features based on statistical significance.
4. **Rebalancing**: Utilizes `SMOTE` (Synthetic Minority Over-sampling Technique) to address class imbalance by generating synthetic samples for the minority class.
5. **Classification**: Employs an `MLPClassifier` (Neural Network) to perform the final classification task based on the processed and balanced data features.

### Summary of Pipeline Development

- **Initial Design**: The pipeline was initially designed using standard scikit-learn components, but failed due to the dataset containing non-numeric strings and categorical variables, necessitating an explicit preprocessing step.
- **Categorical Handling**: We integrated a `ColumnTransformer` with `OrdinalEncoder` to transform string-based features into numeric format, allowing subsequent pipeline stages to function correctly.
- **Interface Constraints**: A recurring issue was the handling of target variable labels. Initially, we manually used `LabelEncoder`, but this caused conflicts during evaluation metrics because the model output numeric indices while the ground truth remained as original string classes. The final design removed the manual encoder from the pipeline sequence, allowing `MLPClassifier` to handle the target labels natively, ensuring consistency during fitting.
- **Tooling Selection**: The use of `imblearn.pipeline.Pipeline` was crucial to ensure that the `SMOTE` rebalancing step occurs exclusively during training and is correctly bypassed during inference.