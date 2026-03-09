import mlrun
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

# 5. Déploiement du modèle (CD)
# On crée la fonction de service
serving_fn = mlrun.new_function("serving", kind="serving", image="mlrun/mlrun")

# On lui ajoute le modèle qui vient d'être créé par 'run'
serving_fn.add_model("advertising_v1", model_path=run.outputs['model'])

# On enregistre la fonction dans le projet pour confirmer qu'elle est prête
project.set_function(serving_fn)
project.save()

print(f"Mission accomplie ! Modèle entraîné et prêt pour le déploiement.")

#print(f"Pipeline terminé ! Les résultats sont ici : {artifact_path}")