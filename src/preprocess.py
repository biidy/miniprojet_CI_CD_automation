import pandas as pd 
import mlrun

def preprocess(context, dataset):
    df= pd.read_csv(dataset)

    #supprimer colonne index si existe
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    context.log_dataset("clean_data", df=df)

    return df