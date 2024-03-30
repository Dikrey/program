import datetime
import platform
import subprocess
import sys
import importlib.util
import webbrowser
import colorama
from colorama import Fore, Style

# Fungsi untuk memeriksa apakah modul sudah terpasang
def check_module(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        return True
    else:
        return False

# Fungsi untuk menginstal modul menggunakan pip
def install_module(module_name):
    print(f"Modul {module_name} belum terinstal.")
    print("Menginstal modul...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"Modul {module_name} berhasil diinstal.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menginstal modul {module_name}: {str(e)}")

# List modul yang diperlukan
required_modules = ["colorama", "webbrowser"]

# Loop untuk memeriksa dan menginstal modul
for module in required_modules:
    if not check_module(module):
        install_module(module)

# Setelah modul terinstal, import modul yang diperlukan
import colorama
from colorama import Fore, Style

# Inisialisasi colorama
colorama.init(autoreset=True)

# Dictionary untuk menyimpan data nasabah
database = {
    '123456': {
        'nama': 'Muhammad Raihan',
        'pin': '1234',
        'saldo': 5000,
        'request_top_up': 0,  # Request top up yang belum disetujui oleh admin
        'request_status': 'Not Verified',  # Status request top up
        'pesan_nasabah': '',  # Pesan dari nasabah
        'pesan_admin': ''  # Pesan balasan dari admin
    },
    '654321': {
        'nama': 'Bruno',
        'pin': '4321',
        'saldo': 3000,
        'request_top_up': 0,  # Request top up yang belum disetujui oleh admin
        'request_status': 'Not Verified',  # Status request top up
        'pesan_nasabah': '',  # Pesan dari nasabah
        'pesan_admin': ''  # Pesan balasan dari admin
    }
}

details_admin = {
    'username': 'admin',
    'password': 'admin123',
    'password_ubah': 'admin456'  
}

def cek_saldo(nasabah):
    return nasabah['saldo']

def tarik_tunai(nasabah, jumlah):
    if jumlah > nasabah['saldo']:
        return Fore.RED + "Saldo tidak mencukupi" + Style.RESET_ALL
    else:
        nasabah['saldo'] -= jumlah
        return Fore.GREEN + "Penarikan berhasil. Saldo Anda sekarang: {}".format(nasabah['saldo']) + Style.RESET_ALL

def transfer(nomor_rekening_pengirim, nomor_rekening_penerima, jumlah):
    if nomor_rekening_pengirim not in database:
        return Fore.RED + "Nomor rekening pengirim tidak ditemukan" + Style.RESET_ALL
    elif nomor_rekening_penerima not in database:
        return Fore.RED + "Nomor rekening penerima tidak ditemukan" + Style.RESET_ALL
    elif jumlah > database[nomor_rekening_pengirim]['saldo']:
        return Fore.RED + "Saldo tidak mencukupi untuk transfer" + Style.RESET_ALL
    else:
        database[nomor_rekening_pengirim]['saldo'] -= jumlah
        database[nomor_rekening_penerima]['saldo'] += jumlah
        return Fore.GREEN + "Transfer berhasil. Saldo Anda sekarang: {}".format(database[nomor_rekening_pengirim]['saldo']) + Style.RESET_ALL

def ubah_pin(nomor_rekening, pin_baru):
    if nomor_rekening in database:
        database[nomor_rekening]['pin'] = pin_baru
        return Fore.GREEN + "PIN berhasil diubah" + Style.RESET_ALL
    else:
        return Fore.RED + "Nomor rekening tidak ditemukan" + Style.RESET_ALL

def tambah_nasabah(nama, pin, saldo_awal):
    nomor_rekening = str(len(database) + 1)  # Nomor rekening dijadikan sebagai angka unik sederhana
    database[nomor_rekening] = {
        'nama': nama,
        'pin': pin,
        'saldo': saldo_awal,
        'request_top_up': 0,
        'request_status': 'Not Verified',
        'pesan_nasabah': '',
        'pesan_admin': ''
    }
    return Fore.GREEN + "Nasabah baru berhasil ditambahkan. Nomor rekening Anda adalah: {}".format(nomor_rekening) + Style.RESET_ALL

def request_top_up(nomor_rekening, jumlah, pesan):
    if nomor_rekening in database:
        database[nomor_rekening]['request_top_up'] = jumlah
        database[nomor_rekening]['request_status'] = 'Not Verified'
        database[nomor_rekening]['pesan_nasabah'] = pesan
        return Fore.GREEN + "Request top up berhasil. Menunggu persetujuan admin." + Style.RESET_ALL
    else:
        return Fore.RED + "Nomor rekening tidak ditemukan" + Style.RESET_ALL

def top_up_approved(nomor_rekening):
    if nomor_rekening in database:
        database[nomor_rekening]['saldo'] += database[nomor_rekening]['request_top_up']
        database[nomor_rekening]['request_top_up'] = 0
        database[nomor_rekening]['request_status'] = 'Verified'
        return Fore.GREEN + "Top up berhasil disetujui. Saldo Anda sekarang: {}".format(database[nomor_rekening]['saldo']) + Style.RESET_ALL
    else:
        return Fore.RED + "Nomor rekening tidak ditemukan" + Style.RESET_ALL

def daftar_nasabah():
    print(Fore.CYAN + "=== Daftar Nasabah ===" + Style.RESET_ALL)
    for nomor_rekening, nasabah in database.items():
        print(Fore.YELLOW + "Nomor Rekening:", nomor_rekening)
        print("Nama:", nasabah['nama'])
        print("PIN:", nasabah['pin'])  # Menampilkan PIN untuk admin
        print("Saldo:", nasabah['saldo'])
        print("Request Top Up:", nasabah['request_top_up'])  # Menampilkan request top up
        print("Status Request:", nasabah['request_status'])  # Menampilkan status request top up
        print("Pesan Nasabah:", nasabah['pesan_nasabah'])  # Menampilkan pesan dari nasabah
        print("Pesan Admin:", nasabah['pesan_admin'])  # Menampilkan pesan balasan dari admin
        print("=====================")

def daftar_request_top_up():
    print(Fore.CYAN + "=== Request Top Up Nasabah ===" + Style.RESET_ALL)
    for nomor_rekening, nasabah in database.items():
        if nasabah['request_top_up'] > 0 and nasabah['request_status'] == 'Not Verified':
            print(Fore.YELLOW + "Nomor Rekening:", nomor_rekening)
            print("Nama:", nasabah['nama'])
            print("Nominal Top Up:", nasabah['request_top_up'])
            print("Pesan Nasabah:", nasabah['pesan_nasabah'])  # Menampilkan pesan dari nasabah
            print("=====================")

def balas_pesan_admin(nomor_rekening):
    if nomor_rekening in database:
        pesan_admin = input(Fore.CYAN + "Balas pesan kepada nasabah: " + Style.RESET_ALL)
        database[nomor_rekening]['pesan_admin'] = pesan_admin
        print(Fore.GREEN + "Pesan terkirim." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Nomor rekening tidak ditemukan." + Style.RESET_ALL)

def login_nasabah():
    print(Fore.CYAN + "===== Login Nasabah =====" + Style.RESET_ALL)
    nomor_rekening = input(Fore.YELLOW + "Nomor Rekening: " + Style.RESET_ALL)
    pin = input(Fore.YELLOW + "PIN: " + Style.RESET_ALL)

    if nomor_rekening in database and database[nomor_rekening]['pin'] == pin:
        print(Fore.GREEN + "Login nasabah berhasil" + Style.RESET_ALL)
        return nomor_rekening
    else:
        print(Fore.RED + "Login nasabah gagal. Nomor rekening atau PIN salah." + Style.RESET_ALL)
        return None

def login_admin():
    print(Fore.CYAN + "===== Login Admin =====" + Style.RESET_ALL)
    username = input(Fore.YELLOW + "Username: " + Style.RESET_ALL)
    password = input(Fore.YELLOW + "Password: " + Style.RESET_ALL)

    if username == details_admin['username'] and password == details_admin['password']:
        print(Fore.GREEN + "Login admin berhasil" + Style.RESET_ALL)
        return True
    else:
        print(Fore.RED + "Login admin gagal. Coba lagi." + Style.RESET_ALL)
        return False

def ubah_password_admin():
    print(Fore.CYAN + "=== Ubah Password Admin ===" + Style.RESET_ALL)
    password_admin = input(Fore.YELLOW + "Masukkan password admin: " + Style.RESET_ALL)
    
    if password_admin == details_admin['password_ubah']:
        new_password = input(Fore.YELLOW + "Masukkan password admin baru: " + Style.RESET_ALL)
        details_admin['password'] = new_password
        print(Fore.GREEN + "Password admin berhasil diubah" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Password untuk mengubah password admin salah." + Style.RESET_ALL)

def subscribe_channel():
    subscribe_link = "https://www.youtube.com/channel/UCqN2HFixFhWs5WJRnIR0cgg"  # Ganti dengan link channel YouTube Anda
    if platform.system() == "Windows":
        webbrowser.get("chrome").open(subscribe_link)
    elif platform.system() == "Linux":
        webbrowser.open_new(subscribe_link)
    elif platform.system() == "Darwin":  # MacOS
        webbrowser.open(subscribe_link)
    else:
        print("Sistem operasi tidak dikenali. Silakan buka browser dan kunjungi:", subscribe_link)
    print(Fore.GREEN + "Terima kasih telah berlangganan channel developer!" + Style.RESET_ALL)

def main():
    print("")
    print(Fore.LIGHTCYAN_EX + "==== Selamat Datang di simulasi Bank Raihan ====" + Style.RESET_ALL)
    print("")
    print(Fore.RED +"Program ini dibuat oleh Raihan ini hanya simulasi")
    print(Fore.LIGHTRED_EX +"jangan lupa subscribe : Raihan_official03017")
    print(Fore.LIGHTYELLOW_EX +"program ini dibuat menggunakan bahasa python")
    print("===============================")
    print("")
    print(Fore.YELLOW + "Tanggal:", datetime.datetime.now().strftime("%d %B %Y"))
    print(Fore.LIGHTYELLOW_EX + "Sistem Operasi:", platform.system())
    print("Versi Python:", platform.python_version())
    while True:
        print("\nPilih jenis transaksi:")
        print("1. Login Nasabah")
        print("2. Login Admin")
        print("3. Keluar")

        pilihan = input(Fore.YELLOW + "Masukkan pilihan Anda (1/2/3): " + Style.RESET_ALL)

        if pilihan == '1':
            nomor_rekening = login_nasabah()
            if nomor_rekening is not None:
                nasabah = database[nomor_rekening]
                print(Fore.GREEN + "Halo, {}!".format(nasabah['nama']) + Style.RESET_ALL)

                while True:
                    print("\nPilih jenis transaksi:")
                    print("1. Cek Saldo")
                    print("2. Tarik Tunai")
                    print("3. Transfer")
                    print("4. Request Top Up")
                    print("5. Lihat Balasan Admin")
                    print("6. Keluar")

                    pilihan = input(Fore.YELLOW + "Masukkan pilihan Anda (1/2/3/4/5/6): " + Style.RESET_ALL)

                    if pilihan == '1':
                        print("Saldo Anda saat ini:", cek_saldo(nasabah))
                    elif pilihan == '2':
                        jumlah = int(input("Masukkan jumlah penarikan: "))
                        print(tarik_tunai(nasabah, jumlah))
                    elif pilihan == '3':
                        rek_penerima = input("Masukkan nomor rekening penerima: ")
                        jumlah = int(input("Masukkan jumlah transfer: "))
                        print(transfer(nomor_rekening, rek_penerima, jumlah))
                    elif pilihan == '4':
                        jumlah = int(input("Masukkan jumlah top up yang diinginkan: "))
                        pesan = input("Masukkan pesan Anda: ")
                        print(request_top_up(nomor_rekening, jumlah, pesan))
                    elif pilihan == '5':
                        print(Fore.CYAN + "=== Balasan Admin ===" + Style.RESET_ALL)
                        print("Pesan dari Admin:", nasabah['pesan_admin'])
                    elif pilihan == '6':
                        print("Terima kasih telah menggunakan layanan ATM")
                        break
                    else:
                        print(Fore.RED + "Pilihan tidak valid, silakan pilih 1, 2, 3, 4, 5, atau 6" + Style.RESET_ALL)
        elif pilihan == '2':
            if login_admin():
                while True:
                    print("\nPilih jenis transaksi admin:")
                    print("1. Daftar Nasabah (termasuk PIN)")
                    print("2. Tambah Nasabah")
                    print("3. Ubah Pin Nasabah")
                    print("4. Ubah Password Admin")
                    print("5. Lihat Request Top Up Nasabah")
                    print("6. Verifikasi Request Top Up")
                    print("7. Balas Pesan Nasabah")
                    print("8. Keluar")

                    admin_pilihan = input(Fore.YELLOW + "Masukkan pilihan Anda (1/2/3/4/5/6/7/8): " + Style.RESET_ALL)

                    if admin_pilihan == '1':
                        daftar_nasabah()
                    elif admin_pilihan == '2':
                        nama = input("Masukkan nama nasabah: ")
                        pin = input("Masukkan PIN nasabah: ")
                        saldo_awal = int(input("Masukkan saldo awal nasabah: "))
                        print(tambah_nasabah(nama, pin, saldo_awal))
                    elif admin_pilihan == '3':
                        nomor_rekening = input("Masukkan nomor rekening nasabah: ")
                        pin_baru = input("Masukkan PIN baru: ")
                        print(ubah_pin(nomor_rekening, pin_baru))
                    elif admin_pilihan == '4':
                        ubah_password_admin()
                    elif admin_pilihan == '5':
                        daftar_request_top_up()  # Menampilkan daftar request top up nasabah
                    elif admin_pilihan == '6':
                        nomor_rekening = input("Masukkan nomor rekening nasabah yang ingin diverifikasi top up: ")
                        if nomor_rekening in database and database[nomor_rekening]['request_status'] == 'Not Verified':
                            print("1. Verifikasi")
                            print("2. Not Verified")
                            verifikasi_pilihan = input("Masukkan pilihan Anda (1/2): ")
                            if verifikasi_pilihan == '1':
                                print(top_up_approved(nomor_rekening))
                            elif verifikasi_pilihan == '2':
                                print("Top up belum diverifikasi.")
                            else:
                                print("Pilihan tidak valid.")
                        else:
                            print("Nomor rekening tidak ditemukan atau sudah diverifikasi.")
                    elif admin_pilihan == '7':
                        nomor_rekening = input("Masukkan nomor rekening nasabah yang ingin dibalas pesannya: ")
                        balas_pesan_admin(nomor_rekening)
                    elif admin_pilihan == '8':
                        print("Keluar dari mode admin")
                        break
                    else:
                        print(Fore.RED + "Pilihan tidak valid, silakan pilih 1, 2, 3, 4, 5, 6, 7, atau 8" + Style.RESET_ALL)
        elif pilihan == '3':
            print(Fore.CYAN + "Terima kasih telah menggunakan layanan ATM" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Pilihan tidak valid, silakan pilih 1, 2, atau 3" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
    subscribe_channel()
