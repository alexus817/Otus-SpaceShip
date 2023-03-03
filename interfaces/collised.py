import math
from abc import abstractmethod

from interfaces.uobject import UObject
from mtypes.vector import Vector


class Collised(UObject):
    """ command interface """

    @property
    @abstractmethod
    def position(self) -> Vector:
        """
        get position
        :return: Vector
        """
        ...

    @position.setter
    @abstractmethod
    def position(self, v: Vector) -> None:
        """
        set position
        :return: Vector
        """
        ...

    @property
    @abstractmethod
    def radius(self) -> int:
        """
        get radius object
        :return: int
        """
        ...

    @radius.setter
    @abstractmethod
    def radius(self, r: int) -> None:
        """
        set radius
        :return: None
        """
        ...

    def is_collised(self, obj: "Collised") -> bool:
        """
        function detect collision with obj
        """
        x1 = self.position.x
        x2 = obj.position.x
        y1 = self.position.y
        y2 = obj.position.y

        # to simplify object collision model is circle
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < (self.radius + obj.radius)
