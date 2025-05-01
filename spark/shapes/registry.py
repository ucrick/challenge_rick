from typing import Dict, Type
from pydantic import BaseModel

SHAPE_REGISTRY: Dict[str, Type[BaseModel]] = {}

def register_shape(shape_type):
    def decorator(cls):
        SHAPE_REGISTRY[shape_type] = cls
        return cls
    return decorator
