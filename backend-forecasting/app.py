import pandas as pd
from flask import Flask, request, jsonify
from controller.data_forecasting import predict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, origins=["localhost:8080", "http://localhost:8080"])

@app.route('/')
def healthcheck():
    return 'hellow world'

@app.route('/predict', methods=['GET', 'POST'])
def predict_route():
    uploaded_file = pd.read_csv(request.files.get('file'))
    filename = 'test'
    if filename != '':
        forecasted = predict(uploaded_file)
        # Process or display success message (see next section)
        return jsonify({"data": forecasted})
    else:
        return 'No file selected!'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")