from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from features.constants import TRAINING_COLUMNS
from config import MODEL_PARAMETERS
import numpy as np
import logging
import warnings
warnings.filterwarnings("ignore")

class ModelTrainer():
    def __init__(self, data):
        self.data = data
        self.models = {}
        self.tuned_models = {}
        self.model_metrics = {}
        self.X = self.data.drop(columns=TRAINING_COLUMNS['TARGET'])
        self.y = self.data[TRAINING_COLUMNS['TARGET']]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42, stratify=self.y)
        logging.info("ModelTrainer initialized.")

    def evaluate_model(self, model):
        model_name = str(model).split("(")[0]
        model.fit(self.X_train, self.y_train)
        predictions = model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        precision = precision_score(self.y_test, predictions, average='weighted')
        recall = recall_score(self.y_test, predictions, average='weighted')
        f1 = f1_score(self.y_test, predictions, average='weighted')

        logging.info(f'''
        {model_name.center(30, '-')}
        Accuracy\t: {accuracy:.4f}
        Precision\t: {precision:.4f}
        Recall\t\t: {recall:.4f}
        F1 Score\t: {f1:.4f}
        {''.center(30, '-')}''')

        self.model_metrics[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    def determine_pca_components(self, variance_threshold=0.95):
        '''Determine the number of components for PCA'''
        pca = PCA()
        pca.fit(self.X_train)
        cumsum = np.cumsum(pca.explained_variance_ratio_)
        d = np.argmax(cumsum >= variance_threshold) + 1
        logging.info(f'Number of components for {variance_threshold} variance: {d}')
        return d

    def perform_pca(self, n_components):
        '''Perform PCA'''
        pca = PCA(n_components=n_components)
        self.X_train = pca.fit_transform(self.X_train)
        self.X_test = pca.transform(self.X_test)
        logging.info(f'Performed PCA with {n_components} components.')

    def hyperparameter_tuning(self, model, param_grid):
        '''Perform hyperparameter tuning using GridSearchCV with weighted F1 score'''
        logging.info(f'Tuning {model}...')
        # Define a weighted F1 scorer
        weighted_f1_scorer = make_scorer(f1_score, average='weighted')
        # Update GridSearchCV to use the weighted F1 scorer
        grid_search = GridSearchCV(model, param_grid, cv=5, scoring=weighted_f1_scorer, n_jobs=-1, verbose=2)
        grid_search.fit(self.X_train, self.y_train)
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
        logging.info(f'Best Parameters: {best_params}')
        logging.info(f'Best Score: {best_score}')

        self.tuned_models[str(model).split("(")[0]] = grid_search.best_estimator_

    def train_svm(self):
        '''Train SVC model'''
        logging.info('Training SVC...')
        C = MODEL_PARAMETERS['SVC']['C']
        kernel = MODEL_PARAMETERS['SVC']['kernel']
        gamma = MODEL_PARAMETERS['SVC']['gamma']

        model = SVC(C=C, kernel=kernel, gamma=gamma, probability=True)
        model.fit(self.X_train, self.y_train)
        self.evaluate_model(model)
        self.models[str(model).split("(")[0]] = model

        return model
    
    def train_random_forest(self):
        '''Train RandomForestClassifier model'''
        logging.info('Training RandomForestClassifier...')
        n_estimators = MODEL_PARAMETERS['RandomForestClassifier']['n_estimators']
        max_depth = MODEL_PARAMETERS['RandomForestClassifier']['max_depth'] 
        min_samples_split = MODEL_PARAMETERS['RandomForestClassifier']['min_samples_split']
        min_samples_leaf = MODEL_PARAMETERS['RandomForestClassifier']['min_samples_leaf']
        bootstrap = MODEL_PARAMETERS['RandomForestClassifier']['bootstrap']

        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, bootstrap=bootstrap)
        model.fit(self.X_train, self.y_train)
        self.evaluate_model(model)
        self.models[str(model).split("(")[0]] = model

        return model

    def train_gradient_boosting(self):
        '''Train GradientBoostingClassifier model'''
        logging.info('Training GradientBoostingClassifier...')
        n_estimators = MODEL_PARAMETERS['GradientBoostingClassifier']['n_estimators']
        learning_rate = MODEL_PARAMETERS['GradientBoostingClassifier']['learning_rate']
        max_depth = MODEL_PARAMETERS['GradientBoostingClassifier']['max_depth']
        min_samples_split = MODEL_PARAMETERS['GradientBoostingClassifier']['min_samples_split']
        min_samples_leaf = MODEL_PARAMETERS['GradientBoostingClassifier']['min_samples_leaf']

        model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
        model.fit(self.X_train, self.y_train)
        self.evaluate_model(model)
        self.models[str(model).split("(")[0]] = model

        return model

    def train_xgboost(self):
        '''Train XGBClassifier model'''
        logging.info('Training XGBClassifier...')
        n_estimators = MODEL_PARAMETERS['XGBClassifier']['n_estimators']
        learning_rate = MODEL_PARAMETERS['XGBClassifier']['learning_rate']
        max_depth = MODEL_PARAMETERS['XGBClassifier']['max_depth']
        subsample = MODEL_PARAMETERS['XGBClassifier']['subsample']
        colsample_bytree = MODEL_PARAMETERS['XGBClassifier']['colsample_bytree']

        model = XGBClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, subsample=subsample, colsample_bytree=colsample_bytree)
        model.fit(self.X_train, self.y_train)
        self.evaluate_model(model)
        self.models[str(model).split("(")[0]] = model

        return model   