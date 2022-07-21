import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

import pandas as pd
import numpy as np
import re
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import joblib
import shap
import json
from xgboost import XGBRegressor

# Parameters
response_variable="price_square_meter"
metrics_mlr_path="metrics/metrics_mlr.json"
metrics_xgbr_path="metrics/metrics_xgbr.json"
model_mlr_path="models/model_xgbr.joblib.dat"
model_xgbr_path="models/model_mlr.joblib.dat"
## Modificación


# Read data
train=pd.read_csv("data/train_reto_precios.csv")
test=pd.read_csv("data/test_reto_precios.csv")

x_train=train.drop([response_variable],axis=1)
x_test=test.drop([response_variable],axis=1)
y_train=train[response_variable]
y_test=test[response_variable]

##############################
# Multiple linear regression #
##############################
mlr = LinearRegression()  
mlr.fit(x_train, y_train)

print("Intercept: ", mlr.intercept_)
print("Coefficients:")
list(zip(x_train.columns, mlr.coef_))

# save coefficients
multiple_linear_regressor_coef=pd.DataFrame({"Variable":x_train.columns,"Coef":mlr.coef_})
multiple_linear_regressor_coef["Coef"]=multiple_linear_regressor_coef["Coef"].round(2)
multiple_linear_regressor_coef["Abs_Coef"]=multiple_linear_regressor_coef["Coef"].abs()
multiple_linear_regressor_coef=multiple_linear_regressor_coef.sort_values("Abs_Coef",ascending=False)
multiple_linear_regressor_coef.to_csv("metrics/MLR_Coef.csv",index=False)

# Evaluate the model
y_pred_mlr= mlr.predict(x_test)

R_squared_mlr=mlr.score(x_train,y_train)*100
meanAbErr_mlr = metrics.mean_absolute_error(y_test, y_pred_mlr)
meanSqErr_mlr = metrics.mean_squared_error(y_test, y_pred_mlr)
rootMeanSqErr_mlr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
print('R squared: {:.2f}'.format(mlr.score(x_test,y_test)*100))
print('Mean Absolute Error:', meanAbErr_mlr)
print('Mean Square Error:', meanSqErr_mlr)
print('Root Mean Square Error:', rootMeanSqErr_mlr)

# save metrics
with open(metrics_mlr_path, 'w') as fd:
    json.dump(
        {
                'R squared': R_squared_mlr,
                'Mean Absolute Error': meanAbErr_mlr,
                'Mean Square Error': meanSqErr_mlr, 
                'Root Mean Square Error': rootMeanSqErr_mlr
            }, 
            fd, indent=4
        )

##################
# XGB regression #
##################

xgbr = XGBRegressor(verbosity=0,max_depth=4,n_estimators=100) 
xgbr.fit(x_train,y_train)

# Model evaluation
score = xgbr.score(x_train, y_train)  
print("Training score: ", score)

score = xgbr.score(x_test, y_test)  
print("Test score: ", score)

xgbr_predict_y_test=xgbr.predict(x_test)

R_squared_xgbr=xgbr.score(x_test,y_test)*100
meanAbErr_xgbr = metrics.mean_absolute_error(y_test, xgbr_predict_y_test)
meanSqErr_xgbr = metrics.mean_squared_error(y_test, xgbr_predict_y_test)
rootMeanSqErr_xgbr = np.sqrt(metrics.mean_squared_error(y_test, xgbr_predict_y_test))
print('R squared: {:.2f}'.format(xgbr.score(x_test,y_test)*100))
print('Mean Absolute Error:', meanAbErr_xgbr)
print('Mean Square Error:', meanSqErr_xgbr)
print('Root Mean Square Error:', rootMeanSqErr_xgbr)

# save metrics

with open(metrics_xgbr_path, 'w') as fd:
    json.dump(
        {
                'R squared': R_squared_xgbr,
                'Mean Absolute Error': meanAbErr_xgbr,
                'Mean Square Error': meanSqErr_xgbr, 
                'Root Mean Square Error': rootMeanSqErr_xgbr
            }, 
            fd, indent=4
        )

# Feature importance

importance = xgbr.feature_importances_
feature_importance=pd.DataFrame({"Feature":x_train.columns,"Importance":importance})
feature_importance=feature_importance.sort_values("Importance",ascending=False)
feature_importance.to_csv("metrics/xgbr_feature_importance.csv",index=False)

# Model Explainability
print('Explainability...')
explainer = shap.TreeExplainer(xgbr)
shap_values = explainer(x_test)

# summarize the effects of all the features
shap.plots.beeswarm(shap_values, plot_size=(15, 8), max_display=20, show=False); plt.subplots_adjust(left=0.3)
plt.savefig('metrics/shap.png'); plt.close()

# Save both models
joblib.dump(xgbr, model_mlr_path)
joblib.dump(mlr, model_xgbr_path)

print("Done!")