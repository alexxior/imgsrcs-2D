from models.point import Point


class Wall:

    def __init__(self, start_point: Point, end_point: Point, coefficient: float = 1):
        self.start_point = start_point
        self.end_point = end_point
        self.length = abs(start_point.x - end_point.x)
        self.height = abs(start_point.y - end_point.y)
        self.coefficient = coefficient

    def equals(self, other) -> bool:
        return self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, Wall):
            if self.start_point.equals(other.start_point) and self.end_point.equals(other.end_point):
                return True
        return False

    def __repr__(self):
        return str(self.start_point) + "  " + str(self.end_point)

    def __str__(self):
        return self.__repr__()
