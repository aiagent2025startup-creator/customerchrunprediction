import optuna
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold, cross_val_score
import numpy as np

def optimize_hyperparameters(X, y, n_trials=20):
    """
    Run Optuna optimization to find best LightGBM hyperparameters.
    """
    def objective(trial):
        param = {
            'objective': 'binary',
            'metric': 'binary_logloss',
            'verbosity': -1,
            'boosting_type': 'gbdt',
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'num_leaves': trial.suggest_int('num_leaves', 20, 300),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
            'random_state': 42
        }
        
        model = lgb.LGBMClassifier(**param)
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        # Optimize for F1 score or ROC-AUC
        scores = cross_val_score(model, X, y, cv=skf, scoring='f1')
        return scores.mean()

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    
    print(f"✅ Best trial: {study.best_trial.value}")
    print(f"✅ Best params: {study.best_trial.params}")
    
    return study.best_trial.params
