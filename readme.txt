This project is a graphical area calculation system built using Python and PySpark, with:

-Using Pydance+object-oriented design
-Unit testing and logging support
-Good module layering design, easy to expand and test

Use pytest test_shapes.py in the root directory to perform functional validation on shape classes, including:

-Is the area calculated correctly
-Does illegal input throw an exception
-Missing field validation
-Unregistered shape testing

Support users to add shapes classes by implementing the.area() method and registering it in shape_registry
Support reading data from .jsonl and .json files (by extending main)
Support logging for easy debugging and error tracking
