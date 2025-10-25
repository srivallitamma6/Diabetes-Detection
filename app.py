from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import pickle
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'key'  # Set a secret key for session management

# Load the dataset and model once when the app starts
try:
    logging.debug("Loading dataset and model...")
    df = pd.read_csv('diabetes.csv')
    model = pickle.load(open('model.pkl', 'rb'))
    logging.info("Dataset and model loaded successfully.")
except Exception as e:
    logging.error("Error loading dataset or model: %s", e)
    df, model = None, None  # Set to None if loading fails

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')  # Form for making predictions

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Gather user input from the form
        user_input = {
            'Pregnancies': int(request.form.get('Pregnancies', 0)),
            'Glucose': float(request.form.get('Glucose', 0.0)),
            'BloodPressure': float(request.form.get('BloodPressure', 0.0)),
            'SkinThickness': float(request.form.get('SkinThickness', 0.0)),
            'Insulin': float(request.form.get('Insulin', 0.0)),
            'BMI': float(request.form.get('BMI', 0.0)),
            'DiabetesPedigreeFunction': float(request.form.get('DiabetesPedigreeFunction', 0.0)),
            'Age': float(request.form.get('Age', 0.0))
        }

        # Convert input to DataFrame for prediction
        user_df = pd.DataFrame([user_input])

        # Make a prediction
        prediction = model.predict(user_df)
        is_diabetic = prediction[0] == 1

        # Log the prediction for debugging purposes
        logging.debug(f"Prediction result: {prediction[0]} (1 = Diabetic, 0 = Non-Diabetic)")

        # Prepare result based on diagnosis
        if is_diabetic:
            # If diabetic, classify type
            age = user_input['Age']
            bmi = user_input['BMI']
            blood_pressure = user_input['BloodPressure']
            
            # Classify diabetes type based on basic criteria
            if age < 30 and blood_pressure >= 140 and bmi < 25:
                diabetes_type = "Type 1"
            elif age >= 30 and bmi >= 25:
                diabetes_type = "Type 2"
            else:
                diabetes_type = "Type 2 (Uncertain)"
            
            result = f"Diagnosed as Diabetic - {diabetes_type}"
        else:
            # If not diabetic, return 'Non-Diabetic' and relevant message
            result = "Non-Diabetic"
            diabetes_type = 'Non-Diabetic'  # Explicitly set this for non-diabetic cases

        # Store diabetes type in session for later use
        session['diabetes_type'] = diabetes_type

        # Log the final result and diabetes type
        logging.debug(f"Result: {result}, Diabetes Type: {diabetes_type}")

        # Render the result with the prediction
        return render_template(
            'result.html',  # Render the correct template (you might want to adjust this)
            diabetes_type=diabetes_type,  # Pass diabetes_type directly to template
            is_diabetic=is_diabetic  # You might want to check this too for additional logic
        )
    
    except Exception as e:
        logging.error("Error in prediction: %s", e)
        return render_template('result.html', diabetes_type="Error in detection")

@app.route('/dashboard')
def dashboard():
    # The diabetes type can be passed in as part of the URL query string if needed
    diabetes_type = request.args.get('diabetes_type', 'Type 2')
    return render_template('dashboard.html', diabetes_type=diabetes_type)

@app.route('/future_risk_dashboard')
def future_risk_dashboard():
    try:
        # Retrieve user input from the session
        user_input = session.get('user_input', {})
        
        # If no data is available in session, redirect to home
        if not user_input:
            return redirect(url_for('home'))

        glucose = user_input.get('Glucose', 0)
        bmi = user_input.get('BMI', 0)
        age = user_input.get('Age', 0)

        # Calculate future risk score
        future_risk_score = (glucose + bmi + age) / 3
        future_risk_level = "Low" if future_risk_score < 100 else "Moderate" if future_risk_score < 150 else "High"

        # Render the future_risk_dashboard.html template with the data
        return render_template(
            'future_risk_dashboard.html',
            future_risk_level=future_risk_level,
            user_input=user_input
        )

    except Exception as e:
        logging.error("Error in future risk assessment: %s", e)
        return render_template('result.html', result="Error in future risk assessment")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
