import socket
import threading

# 儲存房間資訊
rooms = {}
MAX_THREADS = 3


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
                    except:
                        # 如果發生錯誤，可能是該使用者已經離開，移除該使用者
                        rooms[room_number].remove(other_client)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 關閉連線
        client_socket.close()
        rooms[room_number].remove(client_socket)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen(5)
    print("[*] Server listening on port 9999")

    while True:
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
                client.send(
                    "Success! Waiting for other player...".encode('utf-8'))
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


if __name__ == "__main__":
    main()
