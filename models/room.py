from models.point import Point
from models.wall import Wall


class Room:

    def __init__(self, left_wall: Wall, top_wall: Wall, right_wall: Wall, down_wall: Wall, transmitter: Point):
        self.left_wall = left_wall
        self.top_wall = top_wall
        self.right_wall = right_wall
        self.down_wall = down_wall
        self.height = left_wall.height
        self.length = down_wall.length
        # todo nadajnik, odbiornik
        self.transmitter = transmitter

    def __repr__(self):
        return \
            "left__w: " + str(self.left_wall) +\
            "\ntop___w " + str(self.top_wall) +\
            "\nright_w " + str(self.right_wall) +\
            "\ndown_w " + str(self.down_wall)

    def __str__(self):
        return self.__repr__()

    def equals(self, other_room) -> bool:
        return self.__eq__(other_room)

    def __eq__(self, other_room):
        if isinstance(other_room, Room):
            if (self.left_wall.equals(other_room.left_wall)
                    and self.top_wall.equals(other_room.top_wall)
                    and self.right_wall.equals(other_room.right_wall)
                    and self.down_wall.equals(other_room.down_wall)):
                return True
        return False

    def move_room_left(self):
        distance = self.length
        self.left_wall.start_point.x -= distance
        self.left_wall.end_point.x -= distance

        self.top_wall.start_point.x -= distance
        self.top_wall.end_point.x -= distance

        self.right_wall.start_point.x -= distance
        self.right_wall.end_point.x -= distance

        self.down_wall.start_point.x -= distance
        self.down_wall.end_point.x -= distance

        self.transmitter.x -= distance

    def move_room_up(self):
        distance = self.height
        self.left_wall.start_point.y += distance
        self.left_wall.end_point.y += distance

        self.top_wall.start_point.y += distance
        self.top_wall.end_point.y += distance

        self.right_wall.start_point.y += distance
        self.right_wall.end_point.y += distance

        self.down_wall.start_point.y += distance
        self.down_wall.end_point.y += distance

        self.transmitter.y += distance

    def move_room_right(self):
        distance = self.length
        self.left_wall.start_point.x += distance
        self.left_wall.end_point.x += distance

        self.top_wall.start_point.x += distance
        self.top_wall.end_point.x += distance

        self.right_wall.start_point.x += distance
        self.right_wall.end_point.x += distance

        self.down_wall.start_point.x += distance
        self.down_wall.end_point.x += distance

        self.transmitter.x += distance

    def move_room_down(self):
        distance = self.height
        self.left_wall.start_point.y -= distance
        self.left_wall.end_point.y -= distance

        self.top_wall.start_point.y -= distance
        self.top_wall.end_point.y -= distance

        self.right_wall.start_point.y -= distance
        self.right_wall.end_point.y -= distance

        self.down_wall.start_point.y -= distance
        self.down_wall.end_point.y -= distance

        self.transmitter.y -= distance

