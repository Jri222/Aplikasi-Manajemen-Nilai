from mahasiswa import Mahasiswa
from nilai import hitung_nilai_akhir, status_kelulusan

# === STRUKTUR DATA LIST ===
# List digunakan untuk menyimpan banyak objek mahasiswa
data_mahasiswa = []


# === CRUD : CREATE ===
def tambah_mahasiswa():
    nim = input("NIM : ")
    nama = input("Nama : ")
    mata_kuliah = input("Mata Kuliah : ")
    tugas = float(input("Nilai Tugas : "))
    uts = float(input("Nilai UTS : "))
    uas = float(input("Nilai UAS : "))

    # OOP: membuat objek Mahasiswa
    mhs = Mahasiswa(nim, nama, mata_kuliah, tugas, uts, uas)

    # Abstraksi: hitung nilai lewat fungsi
    mhs.nilai_akhir = hitung_nilai_akhir(tugas, uts, uas)
    mhs.status = status_kelulusan(mhs.nilai_akhir)

    # Struktur data list
    data_mahasiswa.append(mhs)


# === CRUD : READ ===
def tampilkan_mahasiswa():
   
    for mhs in data_mahasiswa:
        print(mhs.nim, mhs.nama, mhs.nilai_akhir, mhs.status)


# === CRUD : SEARCH (READ) ===
def cari_mahasiswa():
    nim = input("Masukkan NIM: ")
    for mhs in data_mahasiswa:
        if mhs.nim == nim:    
            print(mhs.nama, mhs.status)
            return


# === CRUD : DELETE ===
def hapus_mahasiswa():
    nim = input("Masukkan NIM: ")
    for mhs in data_mahasiswa:
        if mhs.nim == nim:
            data_mahasiswa.remove(mhs)
            return
