import heapq
import os
from time import sleep

try:
    from gtts import gTTS
    from playsound import playsound as mainPlaysound
    suaraAktif = True
except ImportError:
    suaraAktif = False
    def tts_speak(teks):
        print(teks)
else:
    def tts_speak(teks):
        try:
            tts = gTTS(text=teks, lang='id')
            tts.save("temp.mp3")
            mainPlaysound("temp.mp3")
            os.remove("temp.mp3")
        except Exception as e:
            print(f"(TTS Error: {e})")
            print(teks)

antrian = []
nomor_bisnis = 1
nomor_pribadi = 1
urutan = 1
meja1 = "-"
meja2 = "-"

def bersihkanLayar():
    try:
        if os.name == "nt":
            os.system("cls")
        elif os.getenv("TERM"):
            os.system("clear")
        else:
            print("\n" * 100)
    except:
        print("\n" * 100)


def tampilInfo():
    bersihkanLayar()
    berikutnya = antrian[0][2] if antrian else "-"
    print("="*40)
    print("     SISTEM ANTRIAN BANK MINI")
    print("="*40)
    print(f" Meja 1     Meja 2     Selanjutnya")
    print("-" * 40)
    print(f" {meja1:<9}  {meja2:<9}  {berikutnya}")
    print("-" * 40)
    print()

def tampilMenu():
    print("1. Tambah Antrian Bisnis")
    print("2. Tambah Antrian Pribadi")
    print("3. Panggil Meja 1")
    print("4. Panggil Meja 2")
    print("5. Keluar")

def tambahBisnis():
    global nomor_bisnis, urutan
    kode = f"B{nomor_bisnis:03d}"
    heapq.heappush(antrian, (0, urutan, kode))
    nomor_bisnis += 1
    urutan += 1
    print(f">> {kode} masuk ke antrian bisnis.")
    sleep(1)

def tambahPribadi():
    global nomor_pribadi, urutan
    kode = f"P{nomor_pribadi:03d}"
    heapq.heappush(antrian, (1, urutan, kode))
    nomor_pribadi += 1
    urutan += 1
    print(f">> {kode} masuk ke antrian pribadi.")
    sleep(1)

def panggil(meja):
    global meja1, meja2
    if not antrian:
        print("Antrian masih kosong.")
        sleep(1.5)
        return

    _, _, kode = heapq.heappop(antrian)

    if meja == 1:
        meja1 = kode
    else:
        meja2 = kode

    kode_lengkap = " ".join(kode)
    teks = f"Nomor antrian {kode_lengkap}, silakan ke Meja {meja}."

    print(f"-> {teks}")

    if suaraAktif:
        try:
            mainPlaysound("ding.mp3")  # <- Suara intro sebelum TTS
            tts_speak(teks)
        except Exception as e:
            print(f"(Suara gagal diputar: {e})")

    sleep(2)

def main():
    while True:
        tampilInfo()
        tampilMenu()
        pilih = input("Pilih : ")
        if pilih == "1":
            tambahBisnis()
        elif pilih == "2":
            tambahPribadi()
        elif pilih == "3":
            panggil(1)
        elif pilih == "4":
            panggil(2)
        elif pilih == "5":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")
            sleep(1)

if __name__ == "__main__":
    main()
