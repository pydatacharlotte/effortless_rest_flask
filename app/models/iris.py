"Iris Model"
# pylint: disable=no-member
from app import db
from sqlalchemy.sql import select
import pandas as pd

# Iris dataset taken from: https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html
class Iris(db.Model):
    __tablename__ = "iris"

    iris_id = db.Column(db.Integer, primary_key=True)
    sep_length = db.Column(db.Float)
    sep_width = db.Column(db.Float)
    pet_length = db.Column(db.Float)
    pet_width = db.Column(db.Float)
    target = db.Column(db.Float)

    @classmethod
    def get_data(cls) -> pd.DataFrame:
        # train_df = pd.read_sql(db.session.query(cls), db.get_engine())
        train_df = pd.read_sql(select([cls]), db.get_engine())

        return train_df.drop(["target", "iris_id"], axis=1), train_df["target"]

    def __repr__(self):
        return f"<Iris {self.iris_id}>"
