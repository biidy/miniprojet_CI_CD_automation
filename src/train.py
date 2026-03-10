

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlrun
import pickle
import os

def train_model(context, dataset):
    # 1. Chargement & Nettoyage (CI)
    df = dataset.as_df()
    df.columns = df.columns.str.strip().str.lower()
    
    target_col = 'sales' if 'sales' in df.columns else df.columns[-1]
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # 2. Entraînement
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 3. Évaluation (Validation du CD)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    context.log_result('rmse', float(rmse))
    
    # 4. Exportation de l'Artefact (Cœur du CD)
    model_filename = 'model.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
        
    context.log_model(
        'advertising_model',
        body=open(model_filename, 'rb').read(),
        model_file=model_filename,
        metrics={'rmse': float(rmse)},
        labels={'framework': 'scikit-learn'}
    )