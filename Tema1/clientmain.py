import socket
import tkinter as tk
import time
import datetime
import sys
from time import sleep
from functools import partial
import os
from PIL import ImageTk, Image
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000  # The port used by the server
DIRECT_PORT = 8000


def startClient(entryField, root_local):
    mesaj = entryField.get()
    mesaj = bytearray(mesaj, "utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(mesaj)
        image_bytes = s.recv(1024 * 1024 * 10)
        if sys.getsizeof(image_bytes) < 1024:
            display_message = image_bytes.decode("utf-8")
            rez_label = tk.Label(root_local, text=display_message)
            rez_label.pack()
            s.close()
            return
        unique = "photoclient" + datetime.datetime.now().strftime("%m%d%Y%H%M%S") + ".jpg"
        fd = open(unique, "wb")
        fd.write(image_bytes)
        fd.close()
        if not os.path.isfile(unique):
            display_message = "Salvarea a esuat!"
            rez_label = tk.Label(root_local, text=display_message)
            rez_label.pack()
            s.close()
            return
        display_message = "Download succes ! Cauta in dosarul local poza " + unique
        rez_label = tk.Label(root_local, text=display_message)
        img = ImageTk.PhotoImage(Image.open(unique))
        panel = tk.Label(root_local, image=img)
        panel.image = img
        panel.pack()
        rez_label.pack()
        s.close()


if __name__ == '__main__':
    root = tk.Tk()
    welcomeLabel = tk.Label(root, text="Welcome !")
    howtouseLabel = tk.Label(root, text="Input a Flickr userid and we will download for you the first image, "
                                        "at a randomized size and compressed!")
    entryField = tk.Entry(root, width=50)
    sendButton = tk.Button(root, text="Send", command=partial(startClient, entryField, root))
    welcomeLabel.pack()
    howtouseLabel.pack()
    entryField.pack()
    sendButton.pack()
    root.mainloop()
