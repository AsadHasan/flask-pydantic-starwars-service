from enum import Enum


class Gender(Enum):
    FEMALE = "female"
    MALE = "male"
    N_A = "n/a"
    NONE = "none"
    HERMAPHRODITE = "hermaphrodite"

    class Config:
        frozen = True
