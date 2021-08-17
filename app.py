import flask, requests


app = flask.Flask(__name__)
@app.route("/predict", methods=["GET", "POST"])
def predict():
    # Load the Input
    data = requests.files['file'] # Image input
    data = requests.form['form_input_id'] # String input
    
    # Load the model
    model = load_model()
    
    # Make predictions on input data
    model.predict(data) # .predict() could change based on libarary/framework

# Start the flask app and allow remote connections
app.run(host='0.0.0.0', port = 80)