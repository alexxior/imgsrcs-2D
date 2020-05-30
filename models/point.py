class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def equals(self, other) -> bool:
        return self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __str__(self):
        return self.__repr__()

