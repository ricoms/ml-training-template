from abc import ABC, abstractmethod

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import plot_confusion_matrix
from sklearn.pipeline import Pipeline

from utils.logger import logger


class MLModel(ABC):

    @property
    @abstractmethod
    def model_id(self) -> str:
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def predict(self, data):
        pass


class ProjectModel(MLModel):

    @property
    def model_id(self) -> str:
        return "divorce"

    def save(self, model_prefix):
        self.model_path = model_prefix / 'model.joblib'
        joblib.dump(self.model, self.model_path)
        return self.model_path

    def load(self, model_prefix):
        self.model_path = model_prefix / self.model_id / 'model.joblib'
        try:
            self.model = joblib.load(self.model_path)
        except FileExistsError as e:
            logger.error(e)
        except Exception as e:
            raise e
        return self.model

    def __build_model(self):
        anova_filter = SelectKBest(f_regression, k=5)
        clf = svm.SVC(kernel='linear')
        anova_svm = Pipeline(
            [
                ('anova', anova_filter),
                ('svc', clf)
            ]
        )
        self.model = anova_svm.set_params(
            anova__k=10,
            svc__C=.1,
        )

    def train(
        self,
        X_train,
        y_train,
        X_validation,
        y_validation,
    ):
        self.__build_model()

        self.model.fit(
            X_train,
            y_train,
        )
        acc = self.model.score(X_validation, y_validation)
        y_pred = self.model.predict(X_validation)
        d = {'actual':y_validation, 'predicted':y_pred}
        df = pd.DataFrame(d)
        artifacts = {
            "metrics": {
                "accuracy": acc,
            },
            "dataframes": {
                "classes": df
            },
        }
        return artifacts

    def predict(self, ids, X):
        prediction = self.model.predict(X)
        return {i: pred for i, pred in zip(ids, prediction)}
