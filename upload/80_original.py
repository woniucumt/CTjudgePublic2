# use feature importance for feature selection
from numpy import loadtxt
from numpy import sort
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectFromModel
from xgboost import plot_importance
from matplotlib import pyplot
import xgboost as xgb
from sklearn.grid_search import GridSearchCV   #Perforing grid search


# load data
dataset = loadtxt('80_original.csv', delimiter=",")
# split data into X and y
X = dataset[:,0:21]
Y = dataset[:,21]
# split data into train and test sets
#下面这行是交叉检验的意思吗
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=7)
# fit model on all training data
num_round=4
#model = XGBClassifier(max_depth=4, eta=0.1, learning_rate=0.5, silent=True, n_estimators=num_round,objective='binary:logistic')
model = XGBClassifier()
model.fit(X_train, y_train)

#画过拟合的图
eval_set = [(X_train, y_train), (X_test, y_test)]
model.fit(X_train, y_train, eval_metric=["error", "logloss"], eval_set=eval_set, verbose=True)
# make predictions for test data and evaluate
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
# Fit model using each importance as a threshold
thresholds = sort(model.feature_importances_)

print ("thresholds = sort(model.feature_importances_)" + str(thresholds))

for thresh in thresholds:
	# select features using threshold
	selection = SelectFromModel(model, threshold=thresh, prefit=True)
	select_X_train = selection.transform(X_train)
	# train model
	selection_model = XGBClassifier()
	selection_model.fit(select_X_train, y_train)
	# eval model
	select_X_test = selection.transform(X_test)
	y_pred = selection_model.predict(select_X_test)
	predictions = [round(value) for value in y_pred]
	accuracy = accuracy_score(y_test, predictions)
	print("Thresh=%.3f, n=%d, Accuracy: %.2f%%" % (thresh, select_X_train.shape[1], accuracy*100.0))
	print(thresh)
plot_importance(model)
pyplot.show()
# retrieve performance metrics
results = model.evals_result()
epochs = len(results['validation_0']['error'])
x_axis = range(0, epochs)

# plot log loss
fig, ax = pyplot.subplots()
ax.plot(x_axis, results['validation_0']['logloss'], label='Train')
ax.plot(x_axis, results['validation_1']['logloss'], label='Test')
ax.legend()
pyplot.ylabel('Log Loss')
pyplot.title('XGBoost Log Loss')
pyplot.show()

# plot classification error
fig, ax = pyplot.subplots()
ax.plot(x_axis, results['validation_0']['error'], label='Train')
ax.plot(x_axis, results['validation_1']['error'], label='Test')
ax.legend()
pyplot.ylabel('Classification Error')
pyplot.title('XGBoost Classification Error')
pyplot.show()


eval_set = [(X_test, y_test)]
model.fit(X_train, y_train, early_stopping_rounds=5, eval_metric="logloss", eval_set=eval_set, verbose=True)
print(model.evals_result)
print(model.feature_importances_)
plot_importance(model)
pyplot.show()

model.get_booster().save_model('xgb.model')

test_model = xgb.Booster(model_file='xgb.model')
print (X_test[6:7])
X_test = xgb.DMatrix(X_test[6:7])
X_test=[[119,	4,	25,	23,	12,	0,	36,	90,
14,	11,	6,	5,	3,	6,	5,	2,
1.8,	20,	193.2092968,	8.571428571]]
X_test=[[7,	79,	3,	2,	2,	19,	0,	2,	8,
3,	0,	2,	0,	0,	1,	0,	0,	0,
4,	10,	1]]
X_test = xgb.DMatrix(X_test)
print(test_model.predict(X_test,ntree_limit=model.best_iteration))
print ("test_model : ")
print (str(test_model))


'''
print("new")
model = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bynode=1, colsample_bytree=1, gamma=0, learning_rate=0.1,
       max_delta_step=0, max_depth=3, min_child_weight=1, missing=None,
       n_estimators=100, n_jobs=1, nthread=None,
       objective='binary:logistic', random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None, silent=None,
       subsample=1, verbosity=1)
model = XGBClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
'''


