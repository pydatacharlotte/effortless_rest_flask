from typing import List

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from app.models.iris import Iris


class ClassifierNotInit(Exception):
    """Exception when classifier is not instantiated"""


class IrisClf:
    def __init__(self, load=False):
        self.clf = None

        if load:
            self.load_clf(load)

    def train_iris_model(self) -> float:
        X, y = Iris.get_data()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        self.clf = DecisionTreeClassifier().fit(X_train, y_train)

        return self.clf.score(X_test, y_test)

    def get_clf(self):
        if not self.clf:
            raise (ClassifierNotInit("Please call train_iris_model"))
        return self.clf

    def query_clf(self, X: List[List[float]]) -> List[float]:
        if not self.clf:
            raise (ClassifierNotInit("Please call train_iris_model"))

        return self.clf.predict(X)

    def load_clf(self, load):
        """Method to load model
        
        Args:
            load ([type]): param to help load model from data source
        """

        pass
