# -*- coding: utf-8 -*-
"""CLASIFFICAION FINAALL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NseT2UCLT-Ka1NLtQRMaNH7oDswcw1XO

### **IMPORTING LIBRARIES**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import scipy.sparse

"""### **DATA LOADING**"""

data = pd.read_csv("/content/drive/MyDrive/CTA/Datasets/STAR.csv")
print(data.head())

"""**DATA EXPLORATION AND ANALYSIS**

"""

print(data.describe())

# Check for missing values
print(data.isnull().sum())

# Drop any rows with missing values
data.dropna(inplace=True)

# Recheck for missing values
print(data.isnull().sum())

print(data.dtypes)

"""### DATA VISUALIZATION"""

# Check the distribution of the target variable (Spectral Class)
print(data['Spectral Class'].value_counts())

# Visualize the distribution of the target variable
sns.countplot(x='Spectral Class', data=data)
plt.title('Distribution of Spectral Classes')
plt.show()

# Correlation matrix for numeric features
numeric_features = data.select_dtypes(include=[np.number]).columns.difference(['Spectral Class'])
corr_matrix = data[numeric_features].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

"""HIST BETWEEN SPECTRALCLASS AND OTHER FEATUERS OA"""

# Bar plot for Star Color against Spectral Class
plt.figure(figsize=(12, 6))
sns.countplot(data=data, x='Star color', hue='Spectral Class', order=data['Star color'].value_counts().index)
plt.title('Count of Stars by Star Color and Spectral Class')
plt.xlabel('Star color')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Spectral Class')
plt.show()

# Bar plot for Star type against Spectral Class
plt.figure(figsize=(15, 40))
sns.countplot(data=data, x='Star type', hue='Spectral Class', order=data['Star type'].value_counts().index)
plt.title('Count of Stars by Star type and Spectral Class')
plt.xlabel('Star type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Spectral Class')
plt.show()

# Set the figure size
plt.figure(figsize=(30, 20))

# Create a vertical box plot
sns.boxplot(data=data, x='Star color', y='Spectral Class')

# Set the title and labels
plt.title('Box Plot of Star Color by Spectral Class')
plt.xlabel('Star Color')
plt.ylabel('Spectral Class')

# Show the plot
plt.show()

"""### DATA MODEL BUILD"""

# Encode the target variable
label_encoder = LabelEncoder()
data['Spectral Class'] = label_encoder.fit_transform(data['Spectral Class'])

# Split the dataset
X = data.drop('Spectral Class', axis=1)
y = data['Spectral Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

data.info()

# Identify numeric and categorical features
numeric_features = data.select_dtypes(include=[np.number]).columns.difference(['Spectral Class'])
categorical_features = data.select_dtypes(include=['object']).columns

# Create a preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Transform the data
X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

"""**Logistic Regression from Scratch.**

## BUILD DATA FROM SCRATCH USING SOFTMAX
"""

class LogisticRegressionScratch:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        self.m, self.n = X.shape
        self.weights = np.zeros(self.n)
        self.bias = 0

        for _ in range(self.n_iterations):
            linear_model = X.dot(self.weights) + self.bias
            y_predicted = self.sigmoid(linear_model)

            dw = (1 / self.m) * X.T.dot(y_predicted - y)
            db = (1 / self.m) * np.sum(y_predicted - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        linear_model = X.dot(self.weights) + self.bias
        y_predicted = self.sigmoid(linear_model)
        y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
        return np.array(y_predicted_cls)

# Custom evaluation metrics
def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)

def confusion_matrix(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return np.array([[tn, fp], [fn, tp]])

def classification_report(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    tp, fp, fn, tn = cm[1, 1], cm[0, 1], cm[1, 0], cm[0, 0]

    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    return {
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1_score
    }
# Train the model
model_scratch = LogisticRegressionScratch(learning_rate=0.01, n_iterations=1000)
model_scratch.fit(X_train_preprocessed, y_train)

# Predict and evaluate
y_pred_scratch = model_scratch.predict(X_test_preprocessed)
print("Accuracy (Scratch):", accuracy_score(y_test, y_pred_scratch))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_scratch))
print("Classification Report:", classification_report(y_test, y_pred_scratch))

"""##  MODEL 1 Sklearn Logistic Regression Model

"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score

log_reg = LogisticRegression(max_iter=1000, solver='liblinear')
log_reg.fit(X_train_preprocessed, y_train)
y_pred_log_reg = log_reg.predict(X_test_preprocessed)

# Evaluate Logistic Regression model
accuracy_log_reg = accuracy_score(y_test, y_pred_log_reg)
conf_matrix_log_reg = confusion_matrix(y_test, y_pred_log_reg)
class_report_log_reg = classification_report(y_test, y_pred_log_reg)

print("Logistic Regression Accuracy:", accuracy_log_reg)
print("Confusion Matrix (Logistic Regression):\n", conf_matrix_log_reg)
print("Classification Report (Logistic Regression):\n", class_report_log_reg)

# Perform cross-validation
cv_scores_log_reg = cross_val_score(log_reg, X_train_preprocessed, y_train, cv=5)  # 5-fold cross-validation
print("Cross-Validation Scores (Logistic Regression):", cv_scores_log_reg)
print("Mean Cross-Validation Score (Logistic Regression):", cv_scores_log_reg.mean())

"""best model comparison

## *Model - 2: Random Forest Classifier*
"""

random_forest_clf = RandomForestClassifier(n_estimators=100, random_state=42)
random_forest_clf.fit(X_train_preprocessed, y_train)
y_pred_random_forest_clf = random_forest_clf.predict(X_test_preprocessed)

# Evaluate Random Forest Classifier model
accuracy_random_forest_clf = accuracy_score(y_test, y_pred_random_forest_clf)
conf_matrix_random_forest_clf = confusion_matrix(y_test, y_pred_random_forest_clf)
class_report_random_forest_clf = classification_report(y_test, y_pred_random_forest_clf)

print("Random Forest Classifier Accuracy:", accuracy_random_forest_clf)
print("Confusion Matrix (Random Forest Classifier):\n", conf_matrix_random_forest_clf)
print("Classification Report (Random Forest Classifier):\n", class_report_random_forest_clf)
cv_scores_random_forest_clf = cross_val_score(random_forest_clf, X_train_preprocessed, y_train, cv=5)  # 5-fold cross-validation
print("Cross-Validation Scores (Random Forest Classifier):", cv_scores_random_forest_clf)
print("Mean Cross-Validation Score (Random Forest Classifier):", cv_scores_random_forest_clf.mean())

# Result - Which Model Performed Better?
if accuracy_log_reg > accuracy_random_forest_clf:
    print("Logistic Regression performed better.")
elif accuracy_random_forest_clf > accuracy_log_reg:
    print("Random Forest Classifier performed better.")
else:
    print("Both models performed equally well.")

"""**The sklearn Logistic Regression model significantly outperformed the custom model.**

# **Hyper-parameter Optimizations with Cross Validation**

## **CROSS VALIDATION MODEL 1**
"""

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score
# Hyperparameter tuning for Logistic Regression using GridSearchCV
param_grid_log_reg = {
    'C': [0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'saga']
}

grid_search_log_reg = GridSearchCV(LogisticRegression(max_iter=10000), param_grid_log_reg, cv=5, scoring='accuracy')
grid_search_log_reg.fit(X_train_preprocessed, y_train)
best_params_log_reg = grid_search_log_reg.best_params_
best_score_log_reg = grid_search_log_reg.best_score_

print("Best parameters for Logistic Regression (GridSearchCV):", best_params_log_reg)
print("Best cross-validation score for Logistic Regression (GridSearchCV):", best_score_log_reg)

# Evaluate the best model on the test set
best_log_reg = grid_search_log_reg.best_estimator_
y_pred_best_log_reg = best_log_reg.predict(X_test_preprocessed)

accuracy_best_log_reg = accuracy_score(y_test, y_pred_best_log_reg)
conf_matrix_best_log_reg = confusion_matrix(y_test, y_pred_best_log_reg)
class_report_best_log_reg = classification_report(y_test, y_pred_best_log_reg)

print("Test Accuracy (Logistic Regression):", accuracy_best_log_reg)
print("Confusion Matrix (Logistic Regression):\n", conf_matrix_best_log_reg)
print("Classification Report (Logistic Regression):\n", class_report_best_log_reg)

"""## **CROSS VALIDATION MODEL 2**"""

# Hyperparameter tuning for Random Forest Classifier using GridSearchCV
param_grid_rf = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

grid_search_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid_rf, cv=5, scoring='accuracy')
grid_search_rf.fit(X_train_preprocessed, y_train)
best_params_rf = grid_search_rf.best_params_
best_score_rf = grid_search_rf.best_score_

print("Best parameters for Random Forest Classifier (GridSearchCV):", best_params_rf)
print("Best cross-validation score for Random Forest Classifier (GridSearchCV):", best_score_rf)

# Evaluate the best model on the test set
best_rf = grid_search_rf.best_estimator_
y_pred_best_rf = best_rf.predict(X_test_preprocessed)

accuracy_best_rf = accuracy_score(y_test, y_pred_best_rf)
conf_matrix_best_rf = confusion_matrix(y_test, y_pred_best_rf)
class_report_best_rf = classification_report(y_test, y_pred_best_rf)

print("Test Accuracy (Random Forest Classifier):", accuracy_best_rf)
print("Confusion Matrix (Random Forest Classifier):\n", conf_matrix_best_rf)
print("Classification Report (Random Forest Classifier):\n", class_report_best_rf)

# Compare the best models
models = {
    "Logistic Regression (GridSearchCV)": (accuracy_best_log_reg, best_score_log_reg),
    "Random Forest Classifier (GridSearchCV)": (accuracy_best_rf, best_score_rf),
}

best_model = max(models, key=lambda k: models[k][0])
best_accuracy = models[best_model][0]
best_cv_score = models[best_model][1]

print(f"The best model is {best_model} with test accuracy {best_accuracy} and cross-validation score {best_cv_score}.")

"""# **Feature Selection**

##**MODEL 1 logistic regression **
"""

import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(score_func=f_classif, k=10)
X_new = selector.fit_transform(X_train_preprocessed, y_train)

# Get the scores and feature names
scores = selector.scores_
p_values = selector.pvalues_

# Get feature names from the preprocessor
feature_names = preprocessor.get_feature_names_out()

# Create a DataFrame to display the scores
feature_scores = pd.DataFrame({'Feature': feature_names, 'Score': scores, 'P-value': p_values})

# Display the top 10 features based on their scores
best_features_model_1 = feature_scores.nlargest(10, 'Score')  # Change 10 to the number of features you want
print("Best Features for Model 1:")
print(best_features_model_1)

# Optionally, you can also display all features sorted by score
print("\nAll Features Sorted by Score:")
print(feature_scores.sort_values(by='Score', ascending=False))

"""## **Feature Selection for Model 2 (Random Forest Classifier)**"""

# Select the best features
selector = SelectKBest(score_func=f_classif, k='all')  # You can change 'k' to select a specific number of features
X_new = selector.fit_transform(X_train_preprocessed, y_train)

# Get the scores and feature names
scores = selector.scores_
p_values = selector.pvalues_

# Get feature names from the preprocessor
feature_names = preprocessor.get_feature_names_out()

# Create a DataFrame to display the scores
feature_scores = pd.DataFrame({'Feature': feature_names, 'Score': scores, 'P-value': p_values})

# Display the top 10 features based on their scores
best_features_model_2 = feature_scores.nlargest(10, 'Score')  # Change 10 to the number of features you want
print("Best Features for Model 2 (Random Forest Classifier):")
print(best_features_model_2)

# Optionally, you can also display all features sorted by score
print("\nAll Features Sorted by Score:")
print(feature_scores.sort_values(by='Score', ascending=False))

"""**Compare the Best Features**"""

# Calculate the average score for the top 10 features for each model
avg_score_model_1 = best_features_model_1['Score'].mean()
avg_score_model_2 = best_features_model_2['Score'].mean()

print("\nComparison of Best Features:")
print(f"Average Score of Top 10 Features for Logistic Regression: {avg_score_model_1}")
print(f"Average Score of Top 10 Features for Random Forest Classifier: {avg_score_model_2}")

# Determine which model had the best features
if avg_score_model_1 > avg_score_model_2:
    print("\nLogistic Regression had the best features.")
elif avg_score_model_2 > avg_score_model_1:
    print("\nRandom Forest Classifier had the best features.")
else:
    print("\nBoth models had equally good features.")

"""**Random Forest Classifier performed better.**

# **FINAL MODEL**
"""

# Random Forest without optimization
rf_clf = RandomForestClassifier(random_state=42)
rf_clf.fit(X_train_preprocessed, y_train)
y_pred_random_forest_clf = rf_clf.predict(X_test_preprocessed)

# Print performance metrics before optimization
print("Random Forest Accuracy (Before Optimization):", accuracy_score(y_test, y_pred_random_forest_clf))
print("Confusion Matrix (Random Forest Classifier):\n", conf_matrix_random_forest_clf)
print("Classification Report (Random Forest Classifier):\n", class_report_random_forest_clf)

# Random Forest with optimal hyperparameters
rf_clf_optimized = RandomForestClassifier(n_estimators=best_params_rf_clf['n_estimators'],
    max_depth=best_params_rf_clf['max_depth'],
    min_samples_split=best_params_rf_clf['min_samples_split'],random_state=42)
rf_clf_optimized.fit(X_train_preprocessed, y_train)
y_pred_random_forest_clf_optimized = rf_clf_optimized.predict(X_test_preprocessed)
print("Optimized Random Forest Accuracy:", accuracy_score(y_test, y_pred_random_forest_clf_optimized))
print(confusion_matrix(y_test, y_pred_rf_clf_optimized))
print(classification_report(y_test, y_pred_rf_clf_optimized))