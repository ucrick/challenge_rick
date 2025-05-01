from pyspark.sql.types import StructType, StructField, DoubleType, StringType

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
