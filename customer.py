import socket
import tkinter as tk
from tkinter import scrolledtext, END
import threading
import os
import sys

# Inisialisasi klien socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Menentukan alamat dan port server
server_address = ('localhost', 12345)

try:
    # Menghubungkan klien ke server
    client_socket.connect(server_address)
except ConnectionRefusedError:
    print("Servermu error cok.")
    sys.exit(1)

# Fungsi untuk mengirim pesan ke server


def send_message():
    message = message_entry.get()
    if message:
        try:
            client_socket.send(message.encode())
            message_entry.delete(0, END)
            # Menambahkan pesan yang dikirim ke area chat
            chat_history.insert(tk.END, "Anda: " + message + '\n')
            chat_history.see(tk.END)
        except ConnectionError:
            print("Koneksi dengan server terputus.")

# Fungsi untuk menampilkan pesan yang diterima dari server


def receive_message():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            chat_history.insert(tk.END, data + '\n')
            chat_history.see(tk.END)
        except ConnectionError:
            print("Koneksi dengan server terputus.")
            break

# Fungsi untuk mengirim nama file client ke server


def send_client_name():
    client_name = os.path.basename(__file__)
    client_socket.send(client_name.encode())


# Membuat antarmuka GUI dengan tkinter
root = tk.Tk()
root.title("Cromboloni Cake")
root.geometry("550x650")

root.configure(bg='#FFC0CB')

# Label untuk menampilkan nama klien
client_name_label = tk.Label(
    root, text="Customer: " + os.path.basename(__file__), font=("Arial", 12))
client_name_label.pack(pady=10)

# Menambahkan textarea untuk menampilkan pesan
chat_history = scrolledtext.ScrolledText(
    root, width=50, height=20, font=("Arial", 12))
chat_history.pack(padx=10, pady=10)

# Menambahkan input teks untuk pesan
message_entry = tk.Entry(root, width=30, font=("Arial", 12))
message_entry.pack(pady=10)

# Tombol untuk mengirim pesan
send_button = tk.Button(
    root, text="Kirim", command=send_message, font=("Arial", 12))
send_button.pack()

# Thread untuk mengirim nama file client ke server
name_thread = threading.Thread(target=send_client_name)
name_thread.start()

# Thread untuk menerima pesan dari server
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

root.mainloop()
