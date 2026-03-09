import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import mlrun
import joblib

def train_model(context, dataset):
    df = dataset.as_df()

    if "Unnamed: 0" in df.columns:
        df=df.drop(columns=["Unnamed: 0"])

    X= df[["TV","Radio","Newspaper"]]
    Y= df["sales"]

    X_train, X_test, Y_train, Y_test= train_test_split(
        X, Y, test_size=0.2, random_state=42)

    model = LinearRegression()

    model.fit (X_train, Y_train)

    predictions = model.predict(X_test)

    rmse= mean_squared_error(Y_test, predictions, squared=False)

    context.log_result("RMSE", rmse)

    joblib.dump(model, "model.pkl")

    context.log_model(
        "advertising-model",
        body=model,
        model_file="model.pkl",
        metrics={"RMSE": rmse} # Optionnel : lie le score directement au modèle
    )

