import math
import logging
import os
from typing import Dict, Type
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DoubleType, StructType, StructField, StringType
from pydantic import BaseModel, ValidationError, validator

#log
logger = logging.getLogger("spark_logger")
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#Registry 
SHAPE_REGISTRY: Dict[str, Type[BaseModel]] = {}

def register_shape(shape_type):
    def decorator(cls):
        SHAPE_REGISTRY[shape_type] = cls
        return cls
    return decorator

#Define a shape
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

#Calculation
def compute_area(type_, radius, width, height, base, top, bottom):
    shape_cls = SHAPE_REGISTRY.get(type_)
    if not shape_cls:
        return None
    try:
        obj = shape_cls(
            type=type_,
            radius=radius,
            width=width,
            height=height,
            base=base,
            top=top,
            bottom=bottom
        )
        return obj.area()
    except Exception:
        return None
    
def main():
    spark = SparkSession.builder.appName("AreaCalculator").getOrCreate()
    logger.info("Creating data")

    schema = StructType([
        StructField("type", StringType(), True),
        StructField("radius", DoubleType(), True),
        StructField("width", DoubleType(), True),
        StructField("height", DoubleType(), True),
        StructField("base", DoubleType(), True),
        StructField("top", DoubleType(), True),
        StructField("bottom", DoubleType(), True),
        StructField("area", DoubleType(), True),
    ])

    #df = spark.read.schema(schema).json("shapes.jsonl")
    
    raw_data = [
        {"type": "circle", "radius": 4.0},
        {"type": "rectangle", "width": 5.0, "height": 5.0},
        {"type": "triangle", "base": 2.0, "height": 3.0},
        {"type": "trapezoid", "top": 3.0, "bottom": 5.0, "height": 4.0},
        {"type": "rectangle", "width": -1.0, "height": 5.0}, #erroneous data 
        {"type": "hexagon", "side": 6.0} #Unregistered graphics
    ]

    valid_data = []
    for shape in raw_data:
        shape_type = shape.get("type")
        if shape_type not in SHAPE_REGISTRY:
            logger.warning(f"Unsupported shape type: {shape_type} — skipping")
            continue
        shape_cls = SHAPE_REGISTRY[shape_type]
        try:
            obj = shape_cls(**shape)
            shape["area"] = obj.area()
            valid_data.append(shape)
        except ValidationError as e:
            logger.warning(f"Validation failed for shape {shape_type}: {e}")

    df = spark.createDataFrame(valid_data, schema=schema)
    df.show(truncate=False)

    total_area = df.selectExpr("sum(area) as total_area").collect()[0]["total_area"]
    logging.info(f"Total area of all valid shapes: {total_area:.2f}")
    print(f"Total area of all valid shapes: {total_area:.2f}")
    #spark.stop()
    print("Spark session stopped")

if __name__ == "__main__":
    main()