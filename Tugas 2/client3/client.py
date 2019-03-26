import socket
import sys

def cekArgumen():
    if len(sys.argv) != 3:
        print("Gagal! belum ada 3 argumen")
        sys.exit()
    else:
        print("Berhasil! sudah ada 3 argumen")

def cekPort():
    if int(sys.argv[2]) != 9000:
        print("Port yang dimasukkan salah! coba lagi")
        sys.exit()
    else:
        print("Port diterima!")

#program dimulai disini
cekArgumen()
try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Host yang dimasukkan salah! coba lagi")
    sys.exit()

host = sys.argv[1] #host = "127.0.0.1"
port = int(sys.argv[2]) #port = 9000
cekPort()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Inisialisasi socket")
    sock.setblocking(0)
    sock.settimeout(15)
except socket.error:
    print("Gagal membuat socket")
    sys.exit()

while True:
    inputan = raw_input("\nOpsi perintah: \n1. req [nama_file]\n2. quit\n ")
    sock.sendto(inputan, (host, port))
    opsi = inputan.split()

    if opsi[0] == "req":#proses dimulai
        pesan, addr = sock.recvfrom(51200)
        print(pesan)
        print("Berada di client req")

        cekGambar, addr2 = sock.recvfrom(51200)
        print(cekGambar)

        if len(cekGambar) < 30:
            if opsi[0] == "req":
                prosesReq = open("Kiriman-" + opsi[1], "wb")

                numStr, addr3 = sock.recvfrom(4096)
                temp = int(numStr)
                print("Penerimaan no.paket gambar dimulai...")

                c = 0
                while temp != 0:
                    fileGambar, clientbAddr = sock.recvfrom(4096)
                    dataGambar = prosesReq.write(fileGambar)
                    c += 1
                    print("No.Paket yang diterima:" + str(c))
                    temp -= 1

                prosesReq.close()
                print("Gambar " + \
                        opsi[1] +  " sudah terkirim. Silahkan cek pada direktori Anda")
    elif opsi[0] == "quit":
        print("\nSistem berakhir...")
        sys.exit()
    else: #opsi salah
        pesan, addr = sock.recvfrom(51200)
        print(pesan)
