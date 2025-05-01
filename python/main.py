import json
import logging
from shapes.registry import shape_registry
import shapes.implementations
from pydantic import ValidationError

def calculate_total_area(json_data):
    total_area = 0
    for i, shape_data in enumerate(json_data, 1):
        try:
            shape_type = shape_data.get("type", "").lower()
            shape_class = shape_registry.get(shape_type)
            if not shape_class:
                raise ValueError(f"Unknown shape type: '{shape_type}'")
            shape = shape_class(shape_data)
            area = shape.area()
            total_area += area
            logging.debug(f"Line {i}: {shape_type} -> Area = {area:.2f}")
        except (ValidationError, ValueError, KeyError, TypeError) as e:
            logging.warning(f"[Line {i}] Skipped due to error: {e}")
    return total_area

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("shape_processor.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    try:
        """
        with open('data.json', 'r') as f:
            json_data = json.load(f)
        """
            
        with open('shapes.jsonl', 'r') as f:
            json_data = [json.loads(line) for line in f if line.strip()]
            
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        exit(1)

    logging.info("Start")
    total = calculate_total_area(json_data)
    logging.info(f"Total valid area: {total:.2f}")
