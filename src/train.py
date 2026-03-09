import pandas as pd 
import numpy as np # N'oublie pas d'ajouter l'import au début du fichier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import mlrun
import joblib

def train_model(context, dataset):
    # Charger les données
    df = dataset.as_df()
    
    # NETTOYAGE : Supprimer les espaces dans les noms de colonnes et mettre en minuscule
    df.columns = df.columns.str.strip().str.lower()
    
    # Log pour débugger dans GitHub Actions (tu verras les colonnes dans les logs)
    context.logger.info(f"Colonnes détectées : {df.columns.tolist()}")

    # Vérifier si 'sales' existe après nettoyage
    if 'sales' not in df.columns:
        # Si ça échoue encore, on prend la dernière colonne par défaut
        target_col = df.columns[-1]
    else:
        target_col = 'sales'

    # Préparation des données
    X = df.drop(target_col, axis=1)
    Y = df[target_col]

    X_train, X_test, Y_train, Y_test= train_test_split(
        X, Y, test_size=0.2, random_state=42)

    model = LinearRegression()

    model.fit (X_train, Y_train)

    predictions = model.predict(X_test)

    # Calcul du MSE d'abord
    mse = mean_squared_error(Y_test, predictions)
    # Calcul du RMSE manuellement (plus robuste)
    rmse = np.sqrt(mse)
    #rmse= mean_squared_error(Y_test, predictions, squared=False)

    context.log_result("RMSE", float(rmse))

    joblib.dump(model, "model.pkl")

    context.log_model(
        "advertising-model",
        body=model,
        model_file="model.pkl",
        metrics={"RMSE": float(rmse)}, # Optionnel : lie le score directement au modèle
        labels={'framework': 'scikit-learn'}
    )

