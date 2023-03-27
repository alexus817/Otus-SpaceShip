from interfaces.command import Command
from interfaces.uobject import UObject
from ioc.container import IoC
from objects import TypeObjects


class CreateObject(Command):
    def __init__(self, obj: dict):
        self._obj = obj

    def execute(self) -> None:
        obj = TypeObjects.get(self._obj.pop("type"))(**self._obj)
        # battlefield = IoC.resolve('BattleField')
        gameobjects = IoC.resolve('GameObjects')
        gameobjects.append(obj)
        self._obj["conn"].send(f"OBJECT_ID: {obj.obj_id}")
