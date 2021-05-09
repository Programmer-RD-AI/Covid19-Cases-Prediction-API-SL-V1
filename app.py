import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
import os
from flask import *
from flask_restful import *
from flask_restful import reqparse

app = Flask(__name__)
app.debug = True
app.secret_key = "This Key is secret_key for sure"
api = Api(app)
files = os.listdir("./models")


class Pred(Resource):
    def get(self, date):
        print(date)
        results = {}
        for file in files:
            model = pickle.load(open(f"./models/{file}", "rb"))
            preds = model.predict(np.array(date).astype(np.float32).reshape(1,-1))
            print(file)
            print(preds)
            file = str(file.replace(".pkl", ""))
            results[file] = list(preds)[0]
        print('returning...')
        return results

api.add_resource(Pred, "/<int:date>")

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
