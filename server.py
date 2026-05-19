# ==========================================
# GOJO VS SUKUNA ONLINE SERVER
# ==========================================

import socket
import threading
import pickle

# ==========================================
# SERVER SETTINGS
# ==========================================
HOST = "0.0.0.0"

PORT = 5555

# ==========================================
# CREATE SERVER
# ==========================================
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))

server.listen(2)

print("SERVER STARTED")

# ==========================================
# PLAYERS
# ==========================================
players = []

players_data = {

    0: {

        "x": 100,

        "y": 500,

        "hp": 100
    },

    1: {

        "x": 700,

        "y": 500,

        "hp": 100
    }
}

# ==========================================
# CLIENT THREAD
# ==========================================
def client_thread(conn, player_id):

    print(f"PLAYER {player_id} CONNECTED")

    try:

        conn.send(
            pickle.dumps(player_id)
        )

    except:

        conn.close()

        return

    while True:

        try:

            data = conn.recv(4096)

            if not data:
                break

            data = pickle.loads(data)

            players_data[player_id] = data

            enemy_id = 1 - player_id

            enemy_data = players_data[enemy_id]

            conn.send(
                pickle.dumps(enemy_data)
            )

        except Exception as e:

            print("ERROR:", e)

            break

    print(f"PLAYER {player_id} DISCONNECTED")

    conn.close()

# ==========================================
# WAIT FOR PLAYERS
# ==========================================
while True:

    conn, addr = server.accept()

    print("CONNECTED:", addr)

    if len(players) < 2:

        players.append(conn)

        player_id = len(players) - 1

        thread = threading.Thread(
            target=client_thread,
            args=(conn, player_id)
        )

        thread.daemon = True

        thread.start()

    else:

        conn.send(
            pickle.dumps(
                {
                    "error": "SERVER FULL"
                }
            )
        )

        conn.close()
