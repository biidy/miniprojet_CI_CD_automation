import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import MagicMock
from unittest.mock import MagicMock, ANY
from src.train import train_model

def test_train_model_logic():
    # 1. Préparation d'un faux "context" MLRun
    # On simule les méthodes log_result et log_model pour éviter les erreurs
    mock_context = MagicMock()
    
    # 2. Préparation d'un faux "dataset"
    # On crée un petit DataFrame et on simule la méthode .as_df()
    data = {
        'tv': [100, 200, 300, 400, 500],
        'radio': [10, 20, 30, 40, 50],
        'newspaper': [5, 10, 15, 20, 25],
        'sales': [15, 25, 35, 45, 55]
    }
    mock_dataset = MagicMock()
    mock_dataset.as_df.return_value = pd.DataFrame(data)

    # 3. Exécution de la fonction
    # On vérifie que la fonction s'exécute jusqu'au bout sans crasher
    try:
        train_model(mock_context, mock_dataset)
    except Exception as e:
        pytest.fail(f"La fonction train_model a levé une exception : {e}")

    # 4. Vérifications (Assertions)
    # Vérifie si le fichier model.pkl a bien été créé localement
    assert os.path.exists("model.pkl"), "Le fichier model.pkl n'a pas été généré."
    
    # Vérifie si le contexte a bien enregistré un résultat (le RMSE)
    mock_context.log_result.assert_called()
    
    # Vérifie si le modèle a bien été enregistré dans MLRun
    mock_context.log_model.assert_called_with(
        'advertising_model',
        body=ANY,
        model_file='model.pkl',
        metrics=ANY,
        labels={'framework': 'scikit-learn'}
    )

    # Nettoyage après le test
    if os.path.exists("model.pkl"):
        os.remove("model.pkl")