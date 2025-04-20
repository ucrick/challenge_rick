import math
import pytest
import logging
from main import Circle, Rectangle, Triangle, Trapezoid

#Logging
logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)

#avoid duplicate handlers if reloaded
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler("test_log.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

#test
def test_circle():
    shape = Circle({"type": "circle", "radius": 3})
    result = round(shape.area(), 2)
    expected = round(math.pi * 9, 2)
    logger.info(f"Testing circle area: result={result}, expected={expected}")
    assert result == expected

def test_rectangle():
    shape = Rectangle({"type": "rectangle", "width": 4, "height": 5})
    result = shape.area()
    logger.info(f"Testing rectangle area: result={result}, expected=20")
    assert result == 20

def test_triangle():
    shape = Triangle({"type": "triangle", "base": 6, "height": 3})
    result = shape.area()
    logger.info(f"Testing triangle area: result={result}, expected=9")
    assert result == 9

def test_trapezoid():
    shape = Trapezoid({"type": "trapezoid", "top": 3, "bottom": 5, "height": 4})
    result = shape.area()
    logger.info(f"Testing trapezoid area: result={result}, expected=16")
    assert result == 0.5 * (3 + 5) * 4

def test_invalid_circle_radius():
    logger.info("Testing invalid circle radius input")
    with pytest.raises(Exception):
        Circle({"type": "circle", "radius": "oops"})

def test_missing_rectangle_field():
    logger.info("Testing missing rectangle height field")
    with pytest.raises(Exception):
        Rectangle({"type": "rectangle", "width": 10})

def test_invalid_shape_type():
    logger.info("Testing unknown shape type")
    with pytest.raises(Exception):
        UnknownShape({"type": "hexagon", "side": 5})

