from commands.check_collision import CheckCollision
from commands.macro_mass_collisions import MassCollisions
from interfaces.command import Command
from interfaces.uobject import UObject
from ioc.container import IoC
from mtypes.shape import Circle, Rect


class HandleObject(Command):
    def __init__(self, obj: UObject):
        self._obj = obj

    def execute(self):
        battle_field = IoC.resolve('BattleField', -1)
        queue = IoC.resolve('Queue', -1)

        regions = battle_field.get_property("regions")
        position = self._obj.get_property("position")  # Vector (x, y)  hmm: why vector? may be need rename to point?
        radius = self._obj.get_property("radius")

        obj_regions = [
            region
            # optimization is possible: use not all regions, but only those that are not further than the object radius
            for region, obj_list in regions.items()
            if self.intersects(Circle(position.x, position.y, radius), region)
        ]

        for region, obj_list in regions.items():
            if region in obj_regions:       # object in region
                if self._obj in obj_list:   # object was exist in region
                    continue
                else:                       # new region for object
                    obj_list.append(self._obj)
                    queue.put(
                        MassCollisions(
                            [CheckCollision(self._obj, obj) for obj in obj_list]
                        )
                    )
            else:                           # object not in region
                if self._obj in obj_list:   # object was exist in region
                    obj_list.remove(self._obj)
                else:                       # object was not in this region
                    continue

    @staticmethod
    def intersects(circle: Circle, rect: Rect):

        circle_distance_x = abs(circle.x - (rect.x + rect.width / 2))
        circle_distance_y = abs(circle.y - (rect.y + rect.height / 2))

        # too large distance intersection not possible
        if circle_distance_x > (rect.width / 2 + circle.r):
            return False
        if circle_distance_y > (rect.height / 2 + circle.r):
            return False

        # too small distance 100% intersection
        if circle_distance_x <= (rect.width / 2):
            return True
        if circle_distance_y <= (rect.height / 2):
            return True

        # corner case (x2-x1)^2 + (y2-y1)^2 = r^2
        corner_distance_sq = (circle_distance_x - rect.width / 2)**2 + (circle_distance_y - rect.height / 2)**2

        return corner_distance_sq <= (circle.r**2)


if __name__ == "__main__":
    c = Circle(30, 30, 10)
    r = Rect(0, 50, 200, 200)
    print(HandleObject.intersects(c, r))
