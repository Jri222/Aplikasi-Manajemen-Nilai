class Mahasiswa:
    def __init__(self,nim,nama,prodi):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi

class Matakuliah:
    def __init__(self,kode_mk,nama_mk,sks):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks

class Nilai:
     def __init__(self, nim, kode_mk, tugas, uts, uas):
         self.nim = nim
         self.kode_mk = kode_mk
         self.tugas = tugas
         self.uts = uts
         self.uas = uas
         self.nilai_akhir = self.hitung_nilai_akhir()
         self.status = self.hitung_status()

     def hitung_nilai_akhir(self):
         return (0.3 * self.tugas) + (0.3 * self.uts) + (0.4 * self.uas)
     
     def hitung_status(self):
         return "lulus" if self.nilai_akhir >= 60 else " tidak lulus"