import socket
import sys
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

while True:
    inputan = raw_input("\nOpsi perintah: \n1. req [nama_folder] [nama_file]\n2. upload [nama_file]\n3. quit\n ")
    sock.send(inputan)
    opsi = inputan.split()

    if opsi[0] == "req":#proses dimulai
        pesan= sock.recv(51200)
        print(pesan)

        cekGambar = sock.recv(51200)
        print(cekGambar)

        if len(cekGambar) < 30:
            folder = 'C:/Users/Safira Vanillia P/PycharmProjects/Tugas 3 - TCP UTS/client/request'
            lokasi = os.path.join(folder, "Request-" + opsi[2])

            prosesReq = open(lokasi, "wb")
            fileGambar = sock.recv(51200)
            dataGambar = prosesReq.write(fileGambar)
            prosesReq.close()
            print("File " + \
                  opsi[2] +  " sudah terkirim. Silahkan cek pada direktori Anda")
    elif opsi[0] == "upload":
        if os.path.isfile(opsi[1]):  # cek keberadaan gambar
            pesan = "\nProses upload file " + opsi[1]
            sock.send(pesan)

            ukuran = os.stat(opsi[1])  # print size & bagi dalam bentuk paket
            ukuranGambar = ukuran.st_size
            print("\nUk.File (bytes):" + str(ukuranGambar))

            prosesReq = open(opsi[1], "rb")
            fileGambar = prosesReq.read()
            sock.send(fileGambar)
            prosesReq.close()
            print ("Harap tunggu")
            pesan = sock.recv(51200)
            print(pesan)
        else:
            print("Error! File " + opsi[1]+ " tidak ditemukan")
    elif opsi[0] == "quit":
        print("\nSistem berakhir...")
        sys.exit()
    else: #opsi salah
        pesan= sock.recv(51200)
        print(pesan)