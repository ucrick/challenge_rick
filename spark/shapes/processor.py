from shapes.registry import SHAPE_REGISTRY
from pydantic import ValidationError

def validate_and_compute(data_list, logger):
    valid_data = []
    for shape in data_list:
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
    return valid_data
