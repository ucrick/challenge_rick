import json
import math

#Define JSON data
json_data = [
    '{"type": "rectangle", "width": 5, "height": 10}',
    '{"type": "triangle", "base": 2, "height": 3}',
    '{"type": "circle", "radius": 4}',
    '{"type": "rectangle", "width": 5, "height": 5}'
]

#Calculate area based on different shapes
def calculate_area(shape):
    if shape["type"] == "circle":
        return math.pi * shape["radius"] ** 2
    elif shape["type"] == "rectangle":
        return shape["width"] * shape["height"]
    elif shape["type"] == "triangle":
        return 0.5 * shape["base"] * shape["height"]
    else:
        raise ValueError(f"other shape: {shape['type']}")

total_area = 0

#Read each row of data and call the function
for line in json_data:
    shape = json.loads(line)
    total_area += calculate_area(shape)

print(f"The total area is: {total_area:.2f}")