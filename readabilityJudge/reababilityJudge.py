import xgboost as xgb
from xgboost import XGBClassifier

X_test=[[ 29,         70,           3,           5,          34,
   16,           6,         48,          86,           6,
    3,           6,           1,           1,           7,
    2,           2,           2,          17,         262.9879004,
   17.35714286]]
X_test=[[119,	4,	25,	23,	12,	0,	36,	90,
14,	11,	6,	5,	3,	6,	5,	2,
1.8,	20,	193.2092968,	8.571428571]]
model = XGBClassifier()
test_model = xgb.Booster(model_file='xgb.model')
print (X_test)
X_test = xgb.DMatrix(X_test)
print(test_model.predict(X_test))
print ("test_model : ")
print (str(test_model))