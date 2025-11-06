# pip install scikit-learn

import xgboost as xgb
import pandas as pd

data = pd.read_json("booker_stats.json")

X = data.drop(columns=["Label",  "Opponent"])  # remove label and categorical text columns
y = data["Label"]

model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X, y)

model.save_model("booker_model.json")

# your trained model
model = xgb.XGBClassifier()
model.load_model("booker_model.json")

# your next-game features
next_game = pd.DataFrame([{
    "Game": 9,
    "Prev_5_Points": 28.7,
    "Prev_5_FG%": 47.5,
    "Prev_5_3P%": 39.2,
    "Opp_Def_Rating": 110.3,
    "Is_Home": 1,
    "Over_Under": 29.5
}])

# prediction (1 = Over, 0 = Under)
pred = model.predict(next_game)
prob = model.predict_proba(next_game)

print("Prediction:", "Over" if pred[0] == 1 else "Under")
print("Confidence:", round(prob[0][1]*100, 2), "percent chance Over")