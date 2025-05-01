import logging
from pyspark.sql import SparkSession
from spark_app.schema import schema
from spark_app.processor import validate_and_compute
import shapes.implementations 
from shapes.registry import SHAPE_REGISTRY

# log
logger = logging.getLogger("spark_logger")
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(stream_handler)

def main():
    spark = SparkSession.builder.appName("AreaCalculator").getOrCreate()
    logger.info("Creating data")

    raw_data = [
        {"type": "circle", "radius": 4.0},
        {"type": "rectangle", "width": 5.0, "height": 5.0},
        {"type": "triangle", "base": 2.0, "height": 3.0},
        {"type": "trapezoid", "top": 3.0, "bottom": 5.0, "height": 4.0},
        {"type": "rectangle", "width": -1.0, "height": 5.0},
        {"type": "hexagon", "side": 6.0}
    ]
    #df = spark.read.schema(schema).json("shapes.jsonl")
    valid_data = validate_and_compute(raw_data, logger)
    df = spark.createDataFrame(valid_data, schema=schema)
    df.show(truncate=False)

    total_area = df.selectExpr("sum(area) as total_area").collect()[0]["total_area"]
    logger.info(f"Total area of all valid shapes: {total_area:.2f}")
    print(f"Total area of all valid shapes: {total_area:.2f}")
    print("Spark session stopped")

if __name__ == "__main__":
    main()
