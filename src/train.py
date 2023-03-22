from utils import update_model, save_simple_metrics_report, get_model_performance_test_set
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV, ShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer
from sklearn.preprocessing import PowerTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import make_scorer, mean_absolute_percentage_error

import logging
import sys
import numpy as np
import pandas as pd

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

logger.info('Loading Data...')
data = pd.read_csv('dataset/full_data.csv')


logger.info('Scaled Dataset')

# mejoras 1.0
data_scaled = data.copy()
scaler = PowerTransformer(method='box-cox')
data_scaled = scaler.fit_transform(data_scaled)
data_scaled = pd.DataFrame(data_scaled, columns = data.columns)


logger.info('Loading model...')

# mejoras 2.0
test_size = 0.20
imputer = KNNImputer(missing_values=np.nan)
cv = ShuffleSplit(n_splits=10, test_size=test_size, random_state=42)
n_jobs = -1
scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)


model = Pipeline([
    ('imputer', imputer),
    ('core_model', GradientBoostingRegressor())
])

logger.info('Seraparating dataset into train and test')

X = data_scaled.drop(['worldwide_gross'], axis= 1)
y = data_scaled['worldwide_gross']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

logger.info('Setting Hyperparameter to tune')
param_tuning = {'core_model__n_estimators': range(160, 260, 5),
                'core_model__criterion': ['friedman_mse'],
                'core_model__learning_rate': [0.15, 0.017, 0.2],
                'core_model__loss': ['huber'],
                'core_model__max_depth': [2],
                'core_model__min_samples_leaf': [3],
                'core_model__min_samples_split': [3]}

grid_search = GridSearchCV(model, param_grid= param_tuning, scoring=scorer, cv=cv, n_jobs=n_jobs)


logger.info('Starting grid search...')
grid_search.fit(X_train, y_train)

logger.info('Cross validating with best model...')
final_result = cross_validate(grid_search.best_estimator_, X_train, y_train, return_train_score=True, cv=cv, n_jobs=n_jobs)

cross_validate_train_score = np.mean(final_result['train_score'])
cross_validate_test_score = np.mean(final_result['test_score'])

# breakpoint()

assert cross_validate_train_score > 0.7
assert cross_validate_test_score > 0.65

logger.info(f'Train Score: {cross_validate_train_score}')
logger.info(f'Test Score: {cross_validate_test_score}')

logger.info('Updating model...')
update_model(grid_search.best_estimator_)

logger.info('Generating model report...')
grid_search_test_score = grid_search.best_estimator_.score(X_test, y_test)
save_simple_metrics_report(cross_validate_train_score, cross_validate_test_score, grid_search_test_score, grid_search.best_estimator_)

y_test_pred = grid_search.best_estimator_.predict(X_test)
get_model_performance_test_set(y_test, y_test_pred)

logger.info('Training Finished')