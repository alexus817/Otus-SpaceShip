import json
import pickle
from multiprocessing.connection import Client
from struct import pack
from time import sleep

# from interfaces.move import Movable
# from commands.move import Move
# from mtypes.vector import Vector

address = ('localhost', 5577)
password = "P@$$w0rd"


with Client(address, authkey=bytes(password, "UTF8")) as conn:
    # start connection

    # auth
    print(conn.recv())
    # user = "USER: " + input()
    conn.send("USER: user3")

    print(conn.recv())
    conn.send("PASSWORD: pass3")

    token = conn.recv()
    print(token)
    token = token.replace("TOKEN: ", "")

    # new game command
    new_game = pack("3i", -1, -1, 0) + bytes(   # 0 -> operation = Game.New see server.message.operation
        json.dumps(
            {
                "players": [0, 3],
                "jwt": token
            }
        ),
        "UTF8"
    )
    conn.send(new_game)
    game_id = conn.recv()
    print(game_id)
    game_id = game_id.replace("GAME_ID: ", "")

    spaceship = pack("3i", int(game_id), -1, 14) + bytes(   # 14 -> operation = Create_Object see server.message.operation
        json.dumps(
            {
                "type": "SpaceShip",
                "position": (7, 7),
                "velocity": (5, 2),
                "radius": 5,
                "jwt": token
            }
        ),
        "UTF8"
    )
    conn.send(spaceship)
    spaceship_id = conn.recv()
    print(spaceship_id)
    spaceship_id = spaceship_id.replace("OBJECT_ID: ", "")

    move = pack("3i", int(game_id), int(spaceship_id), 1) + bytes(   # 1 -> operation = Command_Move see server.message.operation
        json.dumps(
            {
                "jwt": token
            }
        ),
        "UTF8"
    )
    conn.send(move)
    spaceship_id = conn.recv()
    print(spaceship_id)



    sleep(5)
    i = input()
    # cmd = Move(MoveObj(position=Vector(1, 2), velocity=Vector(0, 0)))
    # conn.send(pickle.dumps(cmd))
    # buf = conn.recv()

    # print(conn.recv_bytes())            # => 'привет'
    #
    # arr = array('i', [0, 0, 0, 0, 0])
    # print(conn.recv_bytes_into(arr))    # => 8
    # print(arr)
