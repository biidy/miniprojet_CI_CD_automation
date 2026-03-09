'''import mlrun
import os
# On dit à MLRun : "Oublie le réseau, travaille uniquement sur le disque local"
os.environ["MLRUN_DBPATH"] = "local"
os.environ["MLRUN_ARTIFACT_PATH"] = "./artifacts"

# 1. Configuration des chemins absolus (indispensable pour GitHub Actions)
project_root = os.path.abspath("./")
artifact_path = os.path.join(project_root, "artifacts")

# S'assurer que le dossier artifacts existe localement
if not os.path.exists(artifact_path):
    os.makedirs(artifact_path)

# 2. Initialisation du projet
# On utilise get_or_create_project pour éviter les doublons
project = mlrun.get_or_create_project("advertising-mlops", context=project_root)
project.artifact_path = artifact_path

# 3. Définition de la fonction d'entraînement
# On pointe vers src/train.py car c'est là que se trouve ton code métier
train_fn = mlrun.code_to_function(
    name="train-function",
    filename="src/train.py",
    kind="job",
    image="mlrun/mlrun"
)

# 4. Exécution du Job
# On ajoute explicitement l'artifact_path pour satisfaire les exigences de MLRun
run = train_fn.run(
    handler="train_model",
    inputs={"dataset": "data/Advertising.csv"},
    artifact_path=artifact_path,
    local=True # Recommandé pour un mini-projet sans serveur distant
)

# 5. Déploiement du modèle (CD)serving_fn = mlrun.new_function("serving", kind="serving", image="mlrun/mlrun")

# Au lieu de run.outputs['model'], on donne le chemin direct vers l'artefact local
# MLRun enregistre les modèles dans 'artifacts/models/advertising_model.pkl' par défaut
model_path = os.path.join(artifact_path, "model.pkl")

# On vérifie si le fichier existe avant de l'ajouter (sécurité)
if os.path.exists(model_path):
    serving_fn.add_model("advertising_v1", model_path=model_path)
    print(f"Modèle trouvé et ajouté au service : {model_path}")
else:
    # Si le chemin par défaut de MLRun est différent, on peut utiliser le dossier racine des artifacts
    serving_fn.add_model("advertising_v1", model_path=artifact_path)
    print(f"Modèle ajouté depuis le dossier : {artifact_path}")

# On enregistre la fonction
project.set_function(serving_fn)
project.save()

print("Mission accomplie ! Le pipeline de déploiement est prêt.")'''

import mlrun
import os

# --- ÉTAPE 0 : Configuration de l'environnement local ---
# On force MLRun à travailler sur le disque (pas d'API réseau)
os.environ["MLRUN_DBPATH"] = "local"
# On définit le chemin absolu pour les artefacts
os.environ["MLRUN_ARTIFACT_PATH"] = os.path.abspath("./artifacts")

# 1. Chemins et dossiers
project_root = os.path.abspath("./")
artifact_path = os.path.join(project_root, "artifacts")

if not os.path.exists(artifact_path):
    os.makedirs(artifact_path)

# 2. Initialisation du projet MLRun
project = mlrun.get_or_create_project("advertising-mlops", context=project_root)
project.artifact_path = artifact_path

# 3. Définition de la fonction d'entraînement (CI)
# On lie le code source (src/train.py) à une fonction MLRun
train_fn = mlrun.code_to_function(
    name="train-function",
    filename="src/train.py",
    kind="job",
    image="mlrun/mlrun"
)

# 4. Exécution de l'entraînement
# C'est ici que le modèle est créé et évalué
run = train_fn.run(
    handler="train_model",
    inputs={"dataset": "data/Advertising.csv"},
    artifact_path=artifact_path,
    local=True 
)

# 5. Déploiement du modèle (CD)
# On prépare le serveur de prédiction
serving_fn = mlrun.new_function("serving", kind="serving", image="mlrun/mlrun")

# Chemin direct vers le fichier généré par ton script train.py
model_file_path = os.path.join(artifact_path, "model.pkl")

# On configure le serveur avec le modèle et la classe de service V2
if os.path.exists(model_file_path):
    serving_fn.add_model(
        "advertising_v1", 
        model_path=model_file_path,
        class_name="mlrun.serving.V2ModelServer" # Indispensable pour le serving
    )
    print(f"✅ Modèle détecté et configuré : {model_file_path}")
else:
    # Backup : utilise le dossier d'artefacts si le fichier n'est pas à la racine
    serving_fn.add_model(
        "advertising_v1", 
        model_path=artifact_path,
        class_name="mlrun.serving.V2ModelServer"
    )
    print(f"⚠️ Modèle configuré via le dossier : {artifact_path}")

# Enregistrement final dans le projet
project.set_function(serving_fn)
project.save()

print("\n" + "="*40)
print("🚀 MISSION CI/CD ACCOMPLIE !")
print("Le modèle est entraîné et le service de déploiement est prêt.")
print("="*40)