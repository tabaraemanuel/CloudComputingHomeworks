# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import socket
from _thread import start_new_thread
import os
from time import sleep
import flickrapi
from rdoclient import RandomOrgClient
import tinify
import datetime
import urllib.request
import sys
import urllib.response
import os.path
import io
from PIL import Image

# try to import C parser then fallback in pure python parser.
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

HOST = '127.0.0.1'
PORT = 8000


def log(to_log):
    to_log = to_log + '\n'
    with open("logging.txt", "a") as f:
        f.write(to_log)


def monitor_log(to_log):
    to_log = to_log + '\n'
    with open("monitor.txt", "a") as f:
        f.write(to_log)


def monitor_and_abuse():
    counter = 0
    filename = "config.txt"
    with open(filename) as f:
        content = f.read().splitlines()
    api_key = content[0]
    api_secret = content[1]
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')
    while True:
        status = urllib.request.urlopen("https://www.random.org/quota/?format=plain").code
        if 300 > status >= 200:
            to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :Random.org is up and running"

        else:
            to_log = datetime.datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S") + " :Random.org has problems, status code:" + str(status)
        monitor_log(to_log)
        status = urllib.request.urlopen("https://tinypng.com").code
        if 300 > status >= 200:
            to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :tinypng.com is up and running"

        else:
            to_log = datetime.datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S") + " :tinypng.com has problems, status code:" + str(status)
        monitor_log(to_log)
        status = urllib.request.urlopen("https://www.flickr.com").code
        if 300 > status >= 200:
            to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :flickr.com is up and running"

        else:
            to_log = datetime.datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S") + " :flickr.com has problems, status code:" + str(status)
        monitor_log(to_log)
        sleep(10)
        counter -= -1
        if counter > 10:
            exit()


def handle_client(conn, request, ishhtp):
    filename = "config.txt"
    with open(filename) as f:
        content = f.read().splitlines()
    api_key = content[0]
    api_secret = content[1]
    random_api_key = content[2]
    tinify_api_key = content[3]
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')
    user_id = request
    to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :Sent flickr.FlickAPI request"
    log(to_log)
    try:
        photos = flickr.photos.search(api_key=api_key, user_id=user_id, per_page='20')
    except:
        msj_bytes = b'Sorry, your id returned no photos!'
        conn.sendall(msj_bytes)
        conn.close()
        exit(1)
    to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :Sent flickr.photos.search request"
    log(to_log)
    random_gen = RandomOrgClient(random_api_key)
    to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :Sent RandomOrgClient request"
    log(to_log)
    random_id = random_gen.generate_integers(1, 1, 8)[0]
    to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :Sent random_gen.generate_integers request"
    log(to_log)
    to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ":Response from random_gen.generate_integers " \
                                                                      "request was number " + str(random_id)
    log(to_log)
    sizes = ['s', 'q', 't', 'm', 'n', 'w', 'z', 'c', 'b']
    size = sizes[random_id]
    random_id = int(random_id)
    enough = photo_id = photos.find('photos').attrib['total']
    to_log = datetime.datetime.now().strftime(
        "%m/%d/%Y, %H:%M:%S") + " :Response from flickr.photos.search request contains " + str(enough) + " photos"
    log(to_log)
    photo_id = photos.find('photos').findall('photo')[0].attrib['id']
    secret_photo = photos.find('photos').findall('photo')[0].attrib['secret']
    server_photo = photos.find('photos').findall('photo')[0].attrib['server']
    link = "https://live.staticflickr.com/" + server_photo + "/" + photo_id + "_" + secret_photo + "_" + size + ".jpg"
    print(link)
    unique = "photo" + datetime.datetime.now().strftime("%m%d%Y%H%M%S") + ".jpg"
    tinify.key = tinify_api_key
    try:
        source = tinify.from_url(link)
        to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + " :Sent compression request"
        log(to_log)
        source.to_file(unique)
    except:
        msj_bytes = b'Sorry, we ran out of compressions!'
        conn.sendall(msj_bytes)
        conn.close()
        exit(1)
    to_log = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ":Response from compression request was " \
                                                                      "succesful "
    log(to_log)
    imageFileObj = open(unique, "rb")
    imageBinaryBytes = imageFileObj.read()
    if not ishhtp:
        conn.sendall(imageBinaryBytes)
    else:
        conn.send('HTTP/1.1 200 OK\r\n'.encode())
        conn.send("Content-Type: image/jpeg\r\n".encode())
        conn.send("Accept-Ranges: bytes\r\n\r\n".encode())
        conn.send(imageBinaryBytes)
    conn.close()
    exit(1)


def getmetrics(conn):
    with open("logging.txt") as f:
        content = f.read()
        str = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "\n" + "<html><body>" + content + "</body></html>\n"
        str = bytes(str, "utf-8")
        conn.sendall(str)
        conn.close()


def main_funcion():
    start_new_thread(monitor_and_abuse, ())
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(10)
            conn, addr = s.accept()
            print('Connected by', addr)
            data = conn.recv(1024)
            request = data.decode("utf-8")
            ishhtp = False
            a = request
            if request[:3] == "GET":
                ishhtp = True
                request = request[5:]
                a = ""
                for j in request:
                    if not j == ' ':
                        a += j
                    else:
                        break
                if a == "metrics":
                    start_new_thread(getmetrics, (conn,))
                    continue
            start_new_thread(handle_client, (conn, a, ishhtp,))


if __name__ == '__main__':
    main_funcion()
