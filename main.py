# Building the API --> Flask
from flask import Flask, request
from datetime import datetime
import joblib
import sqlite3

# Instantiate
application = Flask(__name__)

# Loading the model
stat_model = joblib.load('model_random_forest_v100.pkl')


# Function to receive our API
@application.route(
    '/prediction_api/<area>;<bathroom>;<parking_spaces>;<floor>;<animal>;<furniture>;<hoa>;<property_tax>',
    methods=['GET'])
def func_01(area, bathroom, parking_spaces, floor, animal, furniture, hoa, property_tax):
    # Initial date & hour
    initial_date = datetime.now()

    # API inputs
    _list = [
        float(area), float(bathroom), float(parking_spaces), float(floor), float(animal), float(furniture), float(hoa),
        float(property_tax)
    ]

    # Prediction try
    try:

        # Predict
        prevision = stat_model.predict(str[_list])

        # Insert the prevision value
        _list.append(str(prevision))

        # _list --> str
        _input = ''
        for value in _list:
            _input = _input + ';' + str(value)

        # Final date & hour
        end_date = datetime.now()
        processing = end_date - initial_date

        # Database connection
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Query
        query_data_insert = f'''
            INSERT INTO Log_API (
                inputs, initial, end, processing
            )
            VALUES (
                '{_input}', '{initial_date}', '{end_date}', '{processing}'
            )
        '''

        # Execute
        cursor.execute(query_data_insert)
        connection.commit()

        # Close connection
        cursor.close()

        # Model
        return {'Rent value': prevision}

    except:
        return {'Warning': 'Error'}


if __name__ == '__main__':
    application.run(debug=True)
