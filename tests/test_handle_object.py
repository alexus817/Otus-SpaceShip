from queue import Queue

from commands import LogWriter
from commands.handle_object import HandleObject
from ioc.container import GameCommand
from mtypes.vector import Vector
from objects import SpaceShip

obj_a = SpaceShip(position=Vector(50, 30), radius=10, velocity=Vector(0, 0), owner="test")
obj_b = SpaceShip(position=Vector(40, 60), radius=50, velocity=Vector(0, 0), owner="test")

game_objects = [obj_a, obj_b]
game_queue = Queue()
worker_queue = Queue()
game = GameCommand({"queue": game_queue, "worker_queue": worker_queue, "game_id": 1})
[game._game_objects.add_game_object(obj) for obj in game_objects]   # need IoC


class TestHandleObject:

    def test_handle_object(self):
        HandleObject(obj_a).execute()
        HandleObject(obj_b).execute()
        cmds = []
        while not game._queue.empty():
            cmd = game._queue.get()
            cmds.append(cmd)
            cmd.execute()

        logcmd = [cmd for cmd in cmds if isinstance(cmd, LogWriter)]
        assert len(logcmd) == 1
        assert 'are collided' in logcmd[0]._ex.args[0]
