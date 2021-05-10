import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
import time
import pandas as pd
import requests

file_names = [
    ["./data/cleaned/new_cases.csv", "new_cases"],
    ["./data/cleaned/total_cases.csv", "total_cases"],
    ["./data/cleaned/total_deaths.csv", "total_deaths"],
    ["./data/cleaned/new_deaths.csv", "new_deaths"],
    ["./data/cleaned/new_tests.csv", "new_tests"],
    ["./data/cleaned/total_cases.csv", "total_cases"],
    ["./data/cleaned/total_tests.csv", "total_tests"],
    ["./data/cleaned/positive_rate.csv", "positive_rate"],
    ["./data/cleaned/total_vaccinations.csv", "total_vaccinations"],
    ["./data/cleaned/new_vaccinations.csv", "new_vaccinations"],
    ["./data/cleaned/total_recovered.csv", "total_recovered"],
    ["./data/cleaned/new_recovered.csv", "new_recovered"],
]

cols = [
    ["./data/cleaned/new_cases.csv", "local_new_cases"],
    ["./data/cleaned/total_deaths.csv", "local_deaths"],
    ["./data/cleaned/new_deaths.csv", "local_new_deaths"],
    ["./data/cleaned/total_cases.csv", "local_total_cases"],
    ["./data/cleaned/total_recovered.csv", "local_recovered"],
    ["./data/cleaned/new_recovered.csv", "new_recovered"],
]
def update():
    while True:
        data = requests.get("https://hpb.health.gov.lk/api/get-current-statistical").json()
        for col in cols:
            date = data["data"]["update_date_time"].split(" ")
            date = date[0].replace("-", "")
            date = int(date)
            if col[1] == "new_recovered":
                print("Checking new recovered")
                df = pd.read_csv(col[0])
                df_recoverd = pd.read_csv("./data/cleaned/total_recovered.csv")
                print(data["data"]["local_recovered"])
                print(df_recoverd.iloc[-1]["total_recovered"])
                new_r = (
                    df_recoverd.iloc[-1]["total_recovered"]
                    - data["data"]["local_recovered"]
                )
                print(new_r)
                df = df.append({"date": date, df.columns[1]: new_r}, ignore_index=True)
                df.to_csv(col[0], index=False)
            else:
                df = pd.read_csv(col[0])
                info = data["data"][col[1]]
                df = df.append({"date": date, df.columns[1]: info}, ignore_index=True)
                df.to_csv(col[0], index=False)
        for file in file_names:
            data = pd.read_csv(file[0])
            X = data['date']
            X = np.array(X).reshape(-1,1)
            y = data[file[1]]
            model = GradientBoostingRegressor()
            model.fit(X,y)
            print(file[1])
            print(model.predict(np.array([20210509]).reshape(-1,1)))
            pickle.dump(model,open(f'./API/models/{file[1]}.pkl','wb'))
        time.sleep(86400)
        print("Updating...")

