import math
import pytest
from main import Circle, Rectangle, Triangle, Trapezoid

def test_circle():
    shape = Circle({"type": "circle", "radius": 3})
    assert round(shape.area(), 2) == round(math.pi * 9, 2)

def test_rectangle():
    shape = Rectangle({"type": "rectangle", "width": 4, "height": 5})
    assert shape.area() == 20

def test_triangle():
    shape = Triangle({"type": "triangle", "base": 6, "height": 3})
    assert shape.area() == 9

def test_trapezoid():
    shape = Trapezoid({"type": "trapezoid", "top": 3, "bottom": 5, "height": 4})
    assert shape.area() == 0.5 * (3 + 5) * 4  # 16

def test_invalid_circle_radius():
    with pytest.raises(Exception):
        Circle({"type": "circle", "radius": "oops"})

def test_missing_rectangle_field():
    with pytest.raises(Exception):
        Rectangle({"type": "rectangle", "width": 10})
