import json
import math

#Define JSON data
json_data = [
    '{"type": "rectangle", "width": 5, "height": 10}',
    '{"type": "triangle", "base": 2, "height": 3}',
    '{"type": "circle", "radius": 4}',
    '{"type": "rectangle", "width": 5, "height": 5}',
    '{"type": "ellipse", "top": 5, "height": 5, "bottom": 10}'
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
    def __init__(self, data):
        self.data = data

    def area(self):
        raise NotImplementedError("Each shape must implement the area method.")

@register_shape("circle")
class Circle(Shape):
    def area(self):
        return math.pi * self.data["radius"] ** 2

@register_shape("rectangle")
class Rectangle(Shape):
    def area(self):
        return self.data["width"] * self.data["height"]

@register_shape("triangle")
class Triangle(Shape):
    def area(self):
        return 0.5 * self.data["base"] * self.data["height"]

#Calculation method for registering new shape area
@register_shape("trapezoid")
class Trapezoid(Shape):
    def area(self):
        return 0.5 * (self.data["top"] + self.data["bottom"]) * self.data["height"]

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