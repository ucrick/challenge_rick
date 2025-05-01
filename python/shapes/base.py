from typing import Dict, Any

class Shape:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def area(self) -> float:
        raise NotImplementedError("Each shape must implement the area method.")
