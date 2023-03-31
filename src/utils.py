from sklearn.pipeline import Pipeline
from joblib import dump
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def update_model(model: Pipeline) -> None:
    dump(model, 'model/model.pkl')


def save_simple_metrics_report(cross_validate_train_score: float, cross_validate_test_score: float, grid_search_test_score: float, model: Pipeline) -> None:
    with open('report.txt', 'w') as report_file:

        report_file.write('# Model Pipeline Description' + '\n')

        for key, value in model.named_steps.items():
            report_file.write(f'### {key}:{value.__repr__()}' + '\n')

        report_file.write(f'### Cross Validating Train Score: {cross_validate_train_score}' + '\n')
        report_file.write(f'### Cross Validating Test Score: {cross_validate_test_score}' + '\n')
        report_file.write(f'### Grid Search Test Score: {grid_search_test_score}' + '\n')

def get_model_performance_test_set(y_real: pd.Series, y_pred: pd.Series) ->None:
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.regplot(x=y_pred, y=y_real, ax = ax)
    ax.set_xlabel('Predicted worldwide gross')
    ax.set_ylabel('Real worldwide gross')
    ax.set_title('Behavior of model prediction')
    fig.savefig('prediction_behavior.png')