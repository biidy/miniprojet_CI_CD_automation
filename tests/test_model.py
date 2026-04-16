import pytest
import joblib
import pandas as pd
import os

def test_model_inference():
    """Vérifie que le modèle chargé peut prédire correctement."""
    model_path = "model.pkl"
    
    if not os.path.exists(model_path):
        pytest.skip("model.pkl non trouvé, test ignoré.")
        
    model = joblib.load(model_path)
    
    # Test avec une entrée typique (doit correspondre au format d'entrée du modèle)
    # Note : les noms de colonnes doivent être en minuscules si votre train.py les a modifiées
    sample = pd.DataFrame([[100.0, 20.0, 10.0]], columns=['tv', 'radio', 'newspaper'])
    prediction = model.predict(sample)
    
    assert len(prediction) == 1
    assert prediction[0] > 0, "Le modèle prédit des ventes négatives ou nulles."