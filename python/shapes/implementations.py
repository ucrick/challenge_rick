import math
from .base import Shape
from .schemas import CircleSchema, RectangleSchema, TriangleSchema, TrapezoidSchema
from .registry import register_shape

@register_shape("circle")
class Circle(Shape):
    def __init__(self, data):
        validated = CircleSchema(**data)
        self.radius = validated.radius

    def area(self):
        return math.pi * self.radius ** 2

@register_shape("rectangle")
class Rectangle(Shape):
    def __init__(self, data):
        validated = RectangleSchema(**data)
        self.width = validated.width
        self.height = validated.height

    def area(self):
        return self.width * self.height

@register_shape("triangle")
class Triangle(Shape):
    def __init__(self, data):
        validated = TriangleSchema(**data)
        self.base = validated.base
        self.height = validated.height

    def area(self):
        return 0.5 * self.base * self.height

@register_shape("trapezoid")
class Trapezoid(Shape):
    def __init__(self, data):
        validated = TrapezoidSchema(**data)
        self.top = validated.top
        self.bottom = validated.bottom
        self.height = validated.height

    def area(self):
        return 0.5 * (self.top + self.bottom) * self.height
    
class UnknownShape:
    def __init__(self, data):
        shape_type = data.get("type", "").lower()
        raise ValueError(f"Unknown shape type: '{shape_type}'")

