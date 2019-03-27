from threading import Thread
import socket
import os
import sys

def serverUpload(nama,file):
        folder= 'C:/Users/Safira Vanillia P/PycharmProjects/Tugas 3 - TCP UTS/server/upload'
        lokasi=os.path.join(folder, "upload-" + str(nama))
        tulis = open(lokasi, "wb")
        tulis.write(file)
        tulis.close()
        print ("Upload file " + str(nama)+" berhasil")

        pesan="File " + str(nama)+ " berhasil diupload!"
        connection.send(pesan)

def serverReq(namafolder, namaGambar):
    pesan = "\nPerintah req valid! proses berlanjut..."
    connection.send(pesan)

    lokasi = namafolder+"/"+namaGambar
    if os.path.isfile(lokasi): #cek keberadaan gambar
        pesan = "File " + \
            namaGambar + " ditemukan! "
        connection.send(pesan)

        ukuran = os.stat(lokasi) #print size & bagi dalam bentuk paket
        ukuranGambar = ukuran.st_size
        print("Uk.File (bytes):" + str(ukuranGambar))
        num = int(ukuranGambar / 4096)
        num = num + 1

        c = 0
        temp = int(num)
        prosesReq = open(lokasi, "rb")
        print("Proses pengiriman data ke "+ str(host) + " : " + str(port))
        while temp != 0:
            fileGambar = prosesReq.read()
            connection.send(fileGambar)
            c += 1
            temp -= 1
            print("No.Paket:" + str(c))
        prosesReq.close()
        print ("Pengiriman "  + \
            namaGambar +" berhasil!")
    else:
        pesan = "Error! File " + \
        namaGambar + " tidak ditemukan pada direktori server"
        connection.send(pesan)

def serverOpsi():
    pesan = "\nError! Perintah: " + \
            command[0] + " tidak dikenali server"
    connection.send(pesan)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ='localhost'
port=10000
server_address = (host,port)
sock.bind(server_address)
print "Inisiasi socket\n"
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    while True:
        data= connection.recv(4096)
        command = data.split()

        if command[0] == "req":
            print("\nProses request file "+command[2]+"...")
            thread = Thread(target=serverReq, args=(command[1],command[2]))
            thread.start()
        elif command[0] == "upload":
            print (connection.recv(4096))
            file=connection.recv(51200)
            thread = Thread(target=serverUpload, args=(command[1], file))
            thread.start()
        elif command[0] == "quit":
            print("\nSistem berakhir...")
            sys.exit()
        else:
            print ("\nPerintah tidak dikenali...")
            thread = Thread(target=serverOpsi)
            thread.start()