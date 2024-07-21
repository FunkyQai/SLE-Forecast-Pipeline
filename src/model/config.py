MODEL_PARAMETERS = {

    'SVC': {
        'C': 0.1,
        'kernel': 'linear',
        'gamma': 'scale',
    },

    'RandomForestClassifier': {
        'n_estimators': 200,
        'max_depth': 10,
        'min_samples_split': 10,
        'min_samples_leaf': 2,
        'bootstrap': False,
    },

    'GradientBoostingClassifier': {
        'n_estimators': 100,
        'max_depth': 3,
        'learning_rate': 0.01,
        'min_samples_split': 2, 
        'min_samples_leaf': 1,
    },

    'XGBClassifier': {
        'n_estimators': 100,
        'learning_rate': 0.01,
        'max_depth': 3,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
    },

}

#### PCA Variance Threshold ####
pca_variance_threshold = 0.95


#### Define the hyperparameter grid for the models ####

param_grid_svc = {
    'C': [0.1, 1, 10],  # Regularization parameter
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],  # Specifies the kernel type to be used in the algorithm
}

param_grid_rf = {
    'n_estimators': [100, 200],  # Number of trees in the forest
    'max_depth': [None, 10, 20],  # Maximum depth of the tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
    'bootstrap': [True, False]  # Whether bootstrap samples are used when building trees
}

param_grid_gb = {
    'n_estimators': [100, 200],  # Number of boosting stages to be run
    'max_depth': [3, 5, 10],  # Maximum depth of the individual regression estimators
    'learning_rate': [0.01, 0.1, 1],  # Learning rate shrinks the contribution of each tree
    'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
    'min_samples_leaf': [1, 2, 4]  # Minimum number of samples required to be at a leaf node
}

param_grid_xgb = {
    'n_estimators': [100, 200],  # Number of boosting rounds
    'learning_rate': [0.01, 0.1, 1],  # Step size shrinkage used in update to prevent overfitting
    'max_depth': [3, 5, 10],  # Maximum depth of the tree
    'subsample': [0.8, 1.0],  # Subsample ratio of the training instances
    'colsample_bytree': [0.8, 1.0]  # Subsample ratio of columns when constructing each tree
}