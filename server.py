import socket
import threading

# Inisialisasi server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Menentukan alamat dan port server
server_address = ('localhost', 12345)

# Mengikat server ke alamat dan port yang ditentukan
server_socket.bind(server_address)

# Mendengarkan koneksi masuk
server_socket.listen(5)
print("Server listening on {}:{}".format(*server_address))

# Daftar klien yang terhubung beserta nama file mereka
connected_clients = {}

# Fungsi untuk menangani koneksi klien


def handle_client(client_socket):
    try:
        # Menerima nama file dari klien
        client_name = client_socket.recv(1024).decode()
        print("Klien terhubung: {}".format(client_name))

        # Menambahkan klien ke daftar klien yang terhubung
        connected_clients[client_socket] = client_name

        while True:
            # Menerima pesan dari klien
            message = client_socket.recv(1024).decode()

            if not message:
                break

            # Mengirim pesan dengan informasi pengirim (nama file klien)
            for client, _ in connected_clients.items():
                if client != client_socket:
                    sender_name = connected_clients[client_socket]
                    client.send("{}: {}".format(sender_name, message).encode())

    except Exception as e:
        print("Koneksi klien terputus: {}".format(e))
    finally:
        # Menghapus klien dari daftar klien yang terhubung
        del connected_clients[client_socket]
        client_socket.close()


# Menerima koneksi dari klien
while True:
    client_socket, client_address = server_socket.accept()
    print("Koneksi dari {}:{}".format(*client_address))

    # Membuat thread baru untuk menangani koneksi klien
    client_handler = threading.Thread(
        target=handle_client, args=(client_socket,))
    client_handler.start()
