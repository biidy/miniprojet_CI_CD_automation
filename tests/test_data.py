import pytest
import pandas as pd
import numpy as np

def test_advertising_csv_structure():
    """Vérifie que le fichier CSV est présent et bien formaté."""
    path = "data/Advertising.csv"
    df = pd.read_csv(path)
    
    # Vérification des colonnes (sensible à la casse car le script train.py fait le strip/lower ensuite)
    required = ["TV", "Radio", "Newspaper", "Sales"]
    for col in required:
        assert col in df.columns, f"La colonne {col} est absente du fichier CSV."
    
    # Vérification des types
    assert df["Sales"].dtype in [np.float64, np.int64]
    
    # Vérification du volume
    assert len(df) > 0, "Le fichier CSV est vide."