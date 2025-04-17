import math
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import DoubleType, StructType, StructField, StringType
from pydantic import BaseModel, ValidationError
import os

#os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17'
#os.environ['PYSPARK_PYTHON'] = r'e:\python\python.exe'
#os.environ['PYSPARK_DRIVER_PYTHON'] = r'e:\python\python.exe'

#Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("spark_shape_processor.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

#Validation
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

#Calculation
def compute_area(type_, radius, width, height, base, top, bottom):
    try:
        shape_data = {
            "type": type_,
            "radius": radius,
            "width": width,
            "height": height,
            "base": base,
            "top": top,
            "bottom": bottom
        }

        if type_ == "circle":
            CircleSchema(**shape_data)
            return math.pi * radius ** 2
        elif type_ == "rectangle":
            RectangleSchema(**shape_data)
            return width * height
        elif type_ == "triangle":
            TriangleSchema(**shape_data)
            return 0.5 * base * height
        elif type_ == "trapezoid":
            TrapezoidSchema(**shape_data)
            return 0.5 * (top + bottom) * height
        else:
            logging.warning(f"Unknown shape type: {type_}")
            return None

    except ValidationError as e:
        logging.warning(f"Validation failed for shape {type_}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error for shape {type_}: {e}")
        return None

def main():
    spark = SparkSession.builder.appName("AreaCalculator").getOrCreate()

    logging.info("Reading data")

    schema = StructType([
        StructField("type", StringType(), True),
        StructField("radius", DoubleType(), True),
        StructField("width", DoubleType(), True),
        StructField("height", DoubleType(), True),
        StructField("base", DoubleType(), True),
        StructField("top", DoubleType(), True),
        StructField("bottom", DoubleType(), True),
    ])

    #df = spark.read.schema(schema).json("shapes.jsonl")
    
    data = [
        {"type": "rectangle", "width": 5, "height": 10},
        {"type": "triangle", "base": 2, "height": 3},
        {"type": "circle", "radius": 4},
        {"type": "rectangle", "width": 5, "height": 5},
        {"type": "trapezoid", "top": 3, "bottom": 5, "height": 4}
    ]
    df = spark.createDataFrame(data, schema=schema)    
    
    area_udf = udf(compute_area, DoubleType())
    df_with_area = df.withColumn(
        "area",
        area_udf(
            col("type"),
            col("radius"),
            col("width"),
            col("height"),
            col("base"),
            col("top"),
            col("bottom")
        )
    )

    df_with_area.show(truncate=False)
    total_area = df_with_area.selectExpr("sum(area) as total_area").collect()[0]["total_area"]
    logging.info(f"Total area of all valid shapes: {total_area:.2f}")

    spark.stop()

if __name__ == "__main__":
    main()
