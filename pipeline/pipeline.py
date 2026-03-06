import mlrun

project = mlrun.new_project("projet1", context="./")
mlrun.get_or_create_project("advertising-mlops")

train_fn = mlrun.code_to_function(
    name="train-function",  # Soit tu le mets explicitement ici
    filename="train.py",    # Assure-toi que le premier argument n'est pas déjà un string
    kind="job",
    image="mlrun/mlrun"
)

run = train_fn.run(
    inputs={"dataset": "data/Advertising.csv"}
)