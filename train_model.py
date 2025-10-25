import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load your dataset
df = pd.read_csv('diabetes.csv')  

# Prepare your data
X = df[['Pregnancies','Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
Y = df['Outcome']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

# Train the Random Forest model
rf = RandomForestClassifier(n_estimators=200)
rf.fit(X_train, Y_train)

# Save the model
pickle.dump(rf, open('model.pkl', 'wb'))
print("Model saved as model.pkl")

from sklearn.metrics import accuracy_score

# Predict on the test set
Y_pred = rf.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
