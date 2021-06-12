# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gLcDAr--nVMGPcJf79rUpkmIinfwjl4c
"""

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from category_encoders import *
import sys

app = Flask(__name__)
model = pickle.load(open('Hpred.pkl', 'rb'))
test_merged=pd.read_csv('cols.csv')
import logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    features=pd.DataFrame({'avg_sqft':int_features[3],'area_type':int_features[1],'location':int_features[0],'size':int_features[2]},index=[0])
    features['location']=features['location'].astype('category')
    features['area_type']=features['area_type'].astype('category')
    features['size']=features['size'].astype('category')
    features['avg_sqft']=features['avg_sqft'].astype('float')
    cols_to_transform = features.select_dtypes(include=['category','uint8']).columns
    final_features=pd.get_dummies(columns=cols_to_transform, data=features, prefix=cols_to_transform, prefix_sep="_",drop_first=False)
 # # Get missing columns in the training test
    ff=final_features.copy()
    missing_cols = set( test_merged.columns ) - set( ff.columns )
    # # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        ff[c] = 0
    # # Ensure the order of column in the test set is in the same order than in train set
    ff = ff[test_merged.columns]
    ff.update(final_features,overwrite=False)
    prediction = model.predict(ff)
    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='House price should be  {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
