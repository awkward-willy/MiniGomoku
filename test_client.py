import socket
import threading


def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received: {message}")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    # 讓使用者輸入房間號碼
    room_number = input("Enter room number: ")
    client.send(room_number.encode('utf-8'))

    # 接收從 server 傳來的訊息
    message = client.recv(1024).decode('utf-8')
    if (message == "Room is full. Try again later."):
        print(message)
        client.close()
        return
    elif (message == "Server is busy. Try again later."):
        print(message)
        client.close()
        return
    elif (message == "Success! Waiting for other player..."):
        print(message)
    else:
        print("Error: Invalid message received.")
        client.close()
        return

    # 啟動接收訊息的 thread
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        client.send(message.encode('utf-8'))


if __name__ == "__main__":
    main()
