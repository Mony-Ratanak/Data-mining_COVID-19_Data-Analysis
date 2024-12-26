import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load the Dataset
data = pd.read_csv("data.csv", encoding='latin1')

# Step 2: Data Exploration
print("\nDataset Head:\n", data.head())
print("\nDataset Info:\n")
data.info()
print("\nMissing Values:\n", data.isnull().sum())

# Step 3: Data Cleaning
# Handle missing values
for column in data.columns:
    if data[column].dtype == 'object':
        data[column].fillna(data[column].mode()[0], inplace=True)
    else:
        data[column].fillna(data[column].mean(), inplace=True)

# Step 4: Feature Engineering
# Encode categorical variables
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Normalize numerical features
scaler = MinMaxScaler()
numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
scaled_features = scaler.fit_transform(data[numerical_columns])
data[numerical_columns] = scaled_features

# Step 5: EDA
# Distribution of target variable
sns.histplot(data['Injury Type'], kde=True)
plt.title('Distribution of Accident Severity')
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# Scatterplot of Latitude vs Longitude (Geospatial Analysis)
sns.scatterplot(x='Longitude', y='Latitude', hue='Injury Type', data=data)
plt.title('Accident Locations by Severity')
plt.show()

# Step 6: Model Training
# Define features and target variable
X = data.drop('Injury Type', axis=1)
y = data['Injury Type']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Predictions
y_pred = lr_model.predict(X_test)

# Step 7: Model Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nLinear Regression Results:")
print(f"Mean Squared Error: {mse:.4f}")
print(f"R-squared Score: {r2:.4f}")

# Step 8: Insights
# Feature Importance (using coefficients)
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': np.abs(lr_model.coef_)
}).sort_values(by='Importance', ascending=False)

print("\nFeature Importance:\n", feature_importance)

# Visualization of feature importance
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title('Feature Importance from Linear Regression')
plt.show()

# Insights on Contributing Factors
print("\nKey Factors Contributing to Traffic Accidents:")
for index, row in feature_importance.iterrows():
    print(f"- {row['Feature']}: {row['Importance']:.4f}")
