from flask import Flask, render_template, request
import json
#this is the app.py file for the Flask application
app = Flask(__name__)

def load_referral_data():
    with open('referral_data.json') as f:
        data = json.load(f)

    cleaned_data = []
    for item in data:
        cleaned_data.append({
            'referring_hospital': item.get('Referring Hospital', item.get('referring_hospital', '')).strip(),
            'speciality': item.get('Specialty', item.get('specialty', '')).strip(),
            'receiving_hospital': item.get('Receiving Hospital', item.get('receiving_hospital', '')).strip(),
            'referral_method': item.get('Referral Method', item.get('referral_method', '')).strip(),
            'instructions': item.get('Instructions', item.get('instructions', '')).strip(),
        })
    return cleaned_data

# Load data once at startup
referral_data = load_referral_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    referring_hospitals = sorted(set(item['referring_hospital'] for item in referral_data))
    specialities = sorted(set(item['speciality'] for item in referral_data))

    if request.method == 'POST':
        referring_hospital = request.form.get('referring_hospital')
        speciality = request.form.get('speciality')

        match = next(
            (item for item in referral_data
             if item['referring_hospital'] == referring_hospital and item['speciality'] == speciality),
            None
        )

        if match:
            receiving_hospital = match['receiving_hospital']
            referral_method = match['referral_method']
            instructions = match['instructions']
        else:
            receiving_hospital = referral_method = instructions = "No matching referral found."

        return render_template('index.html',
                               referring_hospitals=referring_hospitals,
                               specialities=specialities,
                               receiving_hospital=receiving_hospital,
                               referral_method=referral_method,
                               instructions=instructions,
                               selected_referring=referring_hospital,
                               selected_speciality=speciality)

    return render_template('index.html',
                           referring_hospitals=referring_hospitals,
                           specialities=specialities)

if __name__ == '__main__':
    app.run(debug=True)

