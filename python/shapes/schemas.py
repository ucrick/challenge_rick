from pydantic import BaseModel, root_validator

class CircleSchema(BaseModel):
    type: str
    radius: float

class RectangleSchema(BaseModel):
    type: str
    width: float
    height: float

class TriangleSchema(BaseModel):
    type: str
    base: float
    height: float

class TrapezoidSchema(BaseModel):
    type: str
    top: float
    bottom: float
    height: float
