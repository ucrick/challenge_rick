import math
from pydantic import BaseModel, validator
from .registry import register_shape

@register_shape("circle")
class Circle(BaseModel):
    type: str
    radius: float

    @validator("radius")
    def radius_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("radius must be positive")
        return v

    def area(self):
        return math.pi * self.radius ** 2

@register_shape("rectangle")
class Rectangle(BaseModel):
    type: str
    width: float
    height: float

    @validator("width", "height")
    def dim_positive(cls, v):
        if v <= 0:
            raise ValueError("dimensions must be positive")
        return v

    def area(self):
        return self.width * self.height

@register_shape("triangle")
class Triangle(BaseModel):
    type: str
    base: float
    height: float

    def area(self):
        return 0.5 * self.base * self.height

@register_shape("trapezoid")
class Trapezoid(BaseModel):
    type: str
    top: float
    bottom: float
    height: float

    def area(self):
        return 0.5 * (self.top + self.bottom) * self.height
