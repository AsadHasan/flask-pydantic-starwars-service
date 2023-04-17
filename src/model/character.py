from dataclasses import dataclass


from src import db
from src.model.gender import Gender


@dataclass
class Character(db.Model):
    __tablename__ = "characters"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String())
    nickname: str = db.Column(db.String())
    height: int = db.Column(db.Integer)
    mass: int | str = db.Column(db.String())
    hair_color: str = db.Column(db.String())
    skin_color: str = db.Column(db.String())
    eye_color: str = db.Column(db.String())
    birth_year: str = db.Column(db.String())
    gender: Gender = db.Column(db.String())
