from flask import Flask, request, render_template
import numpy
import pickle

# Importing model
model = pickle.load(open('model.pkl', 'rb'))
ferti = pickle.load(open('model1.pkl', 'rb'))

# Creating Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
# Render crop recommendation form page
@app.route('/crop-recommend')
def crop_recommend():
    title = 'HARIYALI'
    return render_template('crop.html')

# Render fertilizer recommendation form page
@app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'HARIYALI - Fertilizer Suggestion'
    return render_template('fertilizer.html')

# Render crop recommendation result page
@app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    title = 'KHETI-KAKSHA - Crop Recommendation'

    if request.method == 'POST':
        N = (float(request.form['nitrogen']))
        P = float(request.form['phosphorous'])
        K = float(request.form['potassium'])
        T = float(request.form['temperature'])
        H = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        data = numpy.array([[N, P, K, T, H, ph, rainfall]])
        my_prediction = model.predict(data)
        final_prediction = my_prediction[0]

        return render_template('crop-result.html', prediction=final_prediction, title=title)

# Render fertilizer recommendation result page
@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'KHETI-KAKSHA - Fertilizer Suggestion'

    if request.method == 'POST':
        temp = float(request.form.get('temp'))
        humi = float(request.form.get('humid'))
        soil = int(request.form.get('soil'))
        crop = int(request.form.get('crop'))
        # Assign integer values to soil and crop types
        soil_types = {
            0: 'Black',
            1: 'Clayey',
            2: 'Loamy',
            3: 'Red',
            4: 'Sandy',
            5: 'Alluvial',
            6: 'Clay Loam',
            7: 'Coastal',
            8: 'Laterite',
            9: 'Silty Clay',
            10: 'Silty Loam'
        }

        crop_types = {
            0: 'Barley',
            1: 'Coconut',
            2: 'Cotton',
            3: 'Ground Nuts',
            4: 'Maize',
            5: 'Corn',
            6: 'Oil Seeds',
            7: 'Paddy',
            8: 'Pulses',
            9: 'Sugarcane',
            10: 'Tobacco',
            11: 'Wheat',
            12: 'Coffee',
            13: 'Kidney Beans',
            14: 'Orange',
            15: 'Pomegranate',
            16: 'Rice',
            17: 'Watermelon'
        }

        # Use the assigned integer values to make predictions
        soil_name = soil_types[soil]
        crop_name = crop_types[crop]
        nitro = float(request.form.get('nitro'))
        pota = float(request.form.get('pota'))
        phosp = request.form.get('phosp')

        if phosp is not None:
            phosp = float(phosp)
        else:
            phosp = 0
        data = numpy.array([[temp,humi,soil,crop,nitro,pota,phosp]])
        my_prediction = ferti.predict(data)
        final_prediction = my_prediction[0]


        return render_template('fertilizer-result.html', prediction=final_prediction, title=title)

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Here you can add code to send the message, e.g., via email or save it in a database
    # For now, we'll just flash a success message
    flash('Thank you for your message. We will get back to you shortly.', 'success')
    return redirect(url_for('contact'))
# Python main
if __name__ == "__main__":
    app.run(debug=False)
