import mlrun

project = 
mlrun.get_or_create_project("advertising-mlops")

train_fn = mlrun.code_to_function(
    "src/train.py",
    name="train-model",
    kind="job",
    image="mlrun/mlrun"
)

run = train_fn.run(
    inputs={"dataset": "data/Advertising.csv"}
)