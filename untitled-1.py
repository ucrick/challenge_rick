import json
import math
from typing import Dict, Any
from pydantic import BaseModel, ValidationError, root_validator

#Define JSON data
json_data = [
    '{"type": "rectangle", "width": 5, "height": 10}',
    '{"type": "triangle", "base": 2, "height": 3}',
    '{"type": "circle", "radius": 4}',
    '{"type": "rectangle", "width": 5, "height": 5}'
]

#Registry for all shape types
shape_registry = {}

#Decorator
def register_shape(shape_type):
    def decorator(func):
        shape_registry[shape_type] = func
        return func
    return decorator

#Base class
class Shape:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def area(self) -> float:
        raise NotImplementedError("Each shape must implement the area method.")

#validation
class CircleSchema(BaseModel):
    type: str
    radius: float

@register_shape("circle")
class Circle(Shape):
    def __init__(self, data):
        validated = CircleSchema(**data)
        self.radius = validated.radius

    def area(self):
        return math.pi * self.radius ** 2


class RectangleSchema(BaseModel):
    type: str
    width: float
    height: float

@register_shape("rectangle")
class Rectangle(Shape):
    def __init__(self, data):
        validated = RectangleSchema(**data)
        self.width = validated.width
        self.height = validated.height

    def area(self):
        return self.width * self.height


class TriangleSchema(BaseModel):
    type: str
    base: float
    height: float

@register_shape("triangle")
class Triangle(Shape):
    def __init__(self, data):
        validated = TriangleSchema(**data)
        self.base = validated.base
        self.height = validated.height

    def area(self):
        return 0.5 * self.base * self.height


class TrapezoidSchema(BaseModel):
    type: str
    top: float
    bottom: float
    height: float

@register_shape("trapezoid")
class Trapezoid(Shape):
    def __init__(self, data):
        validated = TrapezoidSchema(**data)
        self.top = validated.top
        self.bottom = validated.bottom
        self.height = validated.height

    def area(self):
        return 0.5 * (self.top + self.bottom) * self.height

#Calculate the area of all shapes
def calculate_total_area(json_data):
    total_area = 0
    for line in json_data:
        shape_data = json.loads(line)
        shape_type = shape_data["type"].lower()
        shape_class = shape_registry.get(shape_type)
        if not shape_class:
            raise ValueError(f"Unrecognized shape type: {shape_type}")
        shape = shape_class(shape_data)
        total_area += shape.area()
    return total_area

if __name__ == "__main__":
    total = calculate_total_area(json_data)
    print(f"Total area: {total:.2f}")