import pickle
with open("model.pkl", "rb") as f:
    models = pickle.load(f)
print(type(models))
print(models.keys())
