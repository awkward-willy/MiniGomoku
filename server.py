import socket
import threading

# 儲存房間資訊
rooms = {}
ADDR = '127.0.0.1'
backlog = 10
PORT = 8000
MAX_THREADS = 10

# Flag to signal termination
terminate_server = False


def handle_client(client_socket, room_number):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # 將訊息轉發給同一房間的其他人
            for other_client in rooms[room_number]:
                if other_client != client_socket:
                    try:
                        other_client.send(message.encode('utf-8'))
                    except Exception as e:
                        # 如果發生錯誤，可能是該使用者已經離開，移除該使用者
                        print(
                            f"Error: {other_client} has left the room. Error: {e}")
                        rooms[room_number].remove(other_client)
    except Exception as e:
        if e == ConnectionResetError:
            print(f"Connection Reset Error Occurs, Error Detail: {e}")
        # winerror 10054: 遠端主機已強制關閉一個現存的連線
        elif e.winerror == 10054:
            # print socket id
            print(
                f"A socket has left the room. Socket ID: {client_socket.fileno()}")
        else:
            print(f"Error: {e}")
    finally:
        # 關閉連線
        client_socket.close()
        rooms[room_number].remove(client_socket)


def main():
    global terminate_server

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ADDR, PORT))
    server.listen(backlog)
    print(f"[*] Listening on {ADDR}:{PORT}")

    while not terminate_server:
        client, addr = server.accept()
        print(f"[*] Accepted connection from: {addr}")

        room_number = client.recv(1024).decode('utf-8')

        # 檢查房間是否已經存在，若不存在則創建
        if room_number not in rooms:
            rooms[room_number] = []

        # 檢查房間是否已滿
        if len(rooms[room_number]) < 2:
            rooms[room_number].append(client)
            # 啟動一個新的執行緒處理該使用者
            if threading.active_count() <= MAX_THREADS:
                if len(rooms[room_number]) == 1:
                    # 房間內只有一人，等待另一人加入
                    client.send(
                        "Success! Waiting for other player...".encode('utf-8'))
                else:
                    # 房間內有兩人，對已經加入的人說可以開始遊戲
                    rooms[room_number][0].send("Start game!".encode('utf-8'))
                    client.send("Start game!".encode('utf-8'))
                client_handler = threading.Thread(
                    target=handle_client, args=(client, room_number))
                client_handler.start()
            else:
                print("Max threads reached. Connection rejected.")
                client.send("Server is busy. Try again later.".encode('utf-8'))
                client.close()
        else:
            # 房間已滿，拒絕連線
            client.send("Room is full. Try again later.".encode('utf-8'))
            client.close()

    # Terminate all client connections and close the server socket
    for room_clients in rooms.values():
        for client_socket in room_clients:
            client_socket.send("Server terminate".encode('utf-8'))
            client_socket.close()
    server.close()


if __name__ == "__main__":
    try:
        main_thread = threading.Thread(target=main)
        main_thread.daemon = True  # Set the thread as a daemon
        main_thread.start()
        while True:
            user_input = input("Enter 'stop' to terminate the server: ")
            if user_input.lower() == 'stop':
                terminate_server = True
                break
    except KeyboardInterrupt:
        terminate_server = True
    print("Server terminated.")
