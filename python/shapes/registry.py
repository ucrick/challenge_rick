shape_registry = {}

def register_shape(shape_type):
    def decorator(cls):
        shape_registry[shape_type] = cls
        return cls
    return decorator
