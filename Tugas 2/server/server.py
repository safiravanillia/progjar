import socket
import os
import sys

def cekArgumen():
    if len(sys.argv) != 2:
        print("Gagal! belum ada 2 argumen")
        sys.exit()
    else:
        print("Berhasil! sudah ada 2 argumen")

def cekPort():
    if int(sys.argv[1]) != 9000:
        print("Port yang dimasukkan salah! coba lagi")
        sys.exit()
    else:
        print("Port diterima!")

def serverQuit():
    print("Sistem berakhir! menutup socket...")
    sock.close()
    sys.exit()

def serverReq(namaGambar):
    pesan = "\nPerintah req valid! proses berlanjut..."
    sock.sendto(pesan, addr)

    if os.path.isfile(namaGambar): #cek keberadaan gambar
        pesan = "Gambar " + \
            namaGambar + " ditemukan! "
        sock.sendto(pesan, addr)

        ukuran = os.stat(namaGambar) #print size & bagi dalam bentuk paket
        ukuranGambar = ukuran.st_size
        print("Uk.Gambar (bytes):" + str(ukuranGambar))
        num = int(ukuranGambar / 4096)
        num = num + 1
        numStr = str(num)
        sock.sendto(numStr, addr)

        c = 0
        temp = int(num)
        prosesReq = open(namaGambar, "rb")
        print("Proses pengiriman data ke "+ str(addr[0]) + " : " + str(addr[1]))
        while temp != 0:
            fileGambar = prosesReq.read(4096)
            sock.sendto(fileGambar, addr)
            c += 1
            temp -= 1
            print("No.Paket:" + str(c))
        prosesReq.close()
    else:
        pesan = "Error! gambar " + \
            namaGambar + " tidak ditemukan pada direktori server"
        sock.sendto(pesan, addr)

def serverOpsi():
    pesan = "\nError! Perintah: " + \
            command[0] + " tidak dikenali server"
    sock.sendto(pesan, addr)

host = ""
cekArgumen()
port = int(sys.argv[1]) #port = 9000
cekPort()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Inisialisasi socket")
    sock.bind((host, port))
except socket.error:
    print("Gagal membuat socket")
    sys.exit()

while True:
    data, addr = sock.recvfrom(4096)
    command = data.split()
    if command[0] == "req":
        print("\nMenuju fungsi req...")
        serverReq(command[1])
    elif command[0] == "quit":
        print("\nMenuju fungsi quit...")
        serverQuit()
    else:
        serverOpsi()