from typing import Tuple

__all__ = [
    "check_isinstance"
]

def check_isinstance(*info: Tuple[Tuple]):
    """Check if all pairs satisfy isinstance(i[0], i[1]) for i in info"""
    for obj, cls in info:
        if not isinstance(obj, cls):
            raise TypeError("{} must implement {}".format(obj, cls))