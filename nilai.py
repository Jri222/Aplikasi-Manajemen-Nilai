from database import Database
from typing import List, Optional, Tuple

class Penilaian:
    """
    PRAKTIKUM 5: POLYMORPHISM
    Abstract base class untuk berbagai jenis penilaian
    """
    
    def hitung_nilai_akhir(self) -> float:
        """Method yang akan di-override (polymorphism)"""
        raise NotImplementedError("Method harus diimplementasikan")
    
    def hitung_grade(self, nilai_akhir: float) -> str:
        """
        Polymorphism: Method yang sama dengan implementasi berbeda
        di child classes
        """
        if nilai_akhir >= 85:
            return 'A'
        elif nilai_akhir >= 80:
            return 'A-'
        elif nilai_akhir >= 75:
            return 'B+'
        elif nilai_akhir >= 70:
            return 'B'
        elif nilai_akhir >= 65:
            return 'B-'
        elif nilai_akhir >= 60:
            return 'C+'
        elif nilai_akhir >= 55:
            return 'C'
        elif nilai_akhir >= 50:
            return 'D'
        else:
            return 'E'


class Nilai(Penilaian):
    """
    PRAKTIKUM 5: POLYMORPHISM
    PRAKTIKUM 6: RELASI ANTAR CLASS
    
    Class Nilai yang mewarisi dari Penilaian
    - Polymorphism: Override method hitung_nilai_akhir()
    - Relasi: Memiliki relasi dengan Mahasiswa dan MataKuliah (Composition/Association)
    """
    
    def __init__(self, nim: str, kode_mk: str, tugas: float = 0, uts: float = 0, uas: float = 0):
        """
        Konstruktor dengan komposisi objek
        
        PRAKTIKUM 6: RELASI ANTAR CLASS
        - nim: Foreign key ke Mahasiswa (Association)
        - kode_mk: Foreign key ke MataKuliah (Association)
        """
        self.__nim = nim
        self.__kode_mk = kode_mk
        self.__tugas = tugas
        self.__uts = uts
        self.__uas = uas
        self.__nilai_akhir = self.hitung_nilai_akhir()  # Polymorphism
        self.__grade = self.hitung_grade(self.__nilai_akhir)  # Polymorphism
        self.__status = self.hitung_status()
        self.db = Database()
    
    # Property untuk enkapsulasi
    @property
    def nim(self) -> str:
        return self.__nim
    
    @property
    def kode_mk(self) -> str:
        return self.__kode_mk
    
    @property
    def tugas(self) -> float:
        return self.__tugas
    
    @tugas.setter
    def tugas(self, value: float):
        if not 0 <= value <= 100:
            raise ValueError("Nilai tugas harus antara 0-100")
        self.__tugas = value
        self.__update_calculated_values()
    
    @property
    def uts(self) -> float:
        return self.__uts
    
    @uts.setter
    def uts(self, value: float):
        if not 0 <= value <= 100:
            raise ValueError("Nilai UTS harus antara 0-100")
        self.__uts = value
        self.__update_calculated_values()
    
    @property
    def uas(self) -> float:
        return self.__uas
    
    @uas.setter
    def uas(self, value: float):
        if not 0 <= value <= 100:
            raise ValueError("Nilai UAS harus antara 0-100")
        self.__uas = value
        self.__update_calculated_values()
    
    @property
    def nilai_akhir(self) -> float:
        return self.__nilai_akhir
    
    @property
    def grade(self) -> str:
        return self.__grade
    
    @property
    def status(self) -> str:
        return self.__status
    
    def __update_calculated_values(self):
        """Private method untuk update nilai terhitung"""
        self.__nilai_akhir = self.hitung_nilai_akhir()
        self.__grade = self.hitung_grade(self.__nilai_akhir)
        self.__status = self.hitung_status()
    
    def hitung_nilai_akhir(self) -> float:
        """
        PRAKTIKUM 5: POLYMORPHISM
        Override method dari parent class Penilaian
        Implementasi spesifik untuk perhitungan nilai
        Bobot: Tugas 30%, UTS 30%, UAS 40%
        """
        return round((self.__tugas * 0.3) + (self.__uts * 0.3) + (self.__uas * 0.4), 2)
    
    def hitung_status(self) -> str:
        """Hitung status kelulusan (Lulus jika nilai >= 55)"""
        return "Lulus" if self.__nilai_akhir >= 55 else "Tidak Lulus"
    
    def tambah(self) -> bool:
        """Menambah data nilai ke database"""
        query = """INSERT INTO nilai (nim, kode_mk, tugas, uts, uas, nilai_akhir, grade, status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (self.__nim, self.__kode_mk, self.__tugas, self.__uts, self.__uas, 
                  self.__nilai_akhir, self.__grade, self.__status)
        return self.db.execute_query(query, params)
    
    def update(self) -> bool:
        """Update data nilai"""
        # Recalculate nilai akhir, grade, dan status
        self.__update_calculated_values()
        
        query = """UPDATE nilai SET tugas=?, uts=?, uas=?, nilai_akhir=?, grade=?, status=? 
                   WHERE nim=? AND kode_mk=?"""
        params = (self.__tugas, self.__uts, self.__uas, self.__nilai_akhir, 
                  self.__grade, self.__status, self.__nim, self.__kode_mk)
        return self.db.execute_query(query, params)
    
    @staticmethod
    def hapus(nim: str, kode_mk: str) -> bool:
        """Hapus data nilai"""
        db = Database()
        query = "DELETE FROM nilai WHERE nim=? AND kode_mk=?"
        return db.execute_query(query, (nim, kode_mk))
    
    @staticmethod
    def get_by_nim_and_kode(nim: str, kode_mk: str) -> Optional['Nilai']:
        """Ambil data nilai berdasarkan NIM dan Kode MK"""
        db = Database()
        query = "SELECT nim, kode_mk, tugas, uts, uas FROM nilai WHERE nim=? AND kode_mk=?"
        result = db.fetch_one(query, (nim, kode_mk))
        
        if result:
            return Nilai(result[0], result[1], result[2], result[3], result[4])
        return None
    
    @staticmethod
    def get_by_nim(nim: str) -> List[tuple]:
        """
        PRAKTIKUM 6: RELASI ANTAR CLASS
        Demonstrasi JOIN query - relasi antar tabel
        """
        db = Database()
        query = """
            SELECT n.nim, m.nama, n.kode_mk, mk.nama_mk, 
                   n.tugas, n.uts, n.uas, n.nilai_akhir, n.grade, n.status
            FROM nilai n
            JOIN mahasiswa m ON n.nim = m.nim
            JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
            WHERE n.nim = ?
            ORDER BY n.kode_mk
        """
        return db.fetch_all(query, (nim,))
    
    @staticmethod
    def get_all() -> List[tuple]:
        """Ambil semua data nilai dengan JOIN"""
        db = Database()
        query = """
            SELECT n.nim, m.nama, n.kode_mk, mk.nama_mk, 
                   n.tugas, n.uts, n.uas, n.nilai_akhir, n.grade, n.status
            FROM nilai n
            JOIN mahasiswa m ON n.nim = m.nim
            JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
            ORDER BY n.nim, n.kode_mk
        """
        return db.fetch_all(query)
    
    @staticmethod
    def is_nilai_exists(nim: str, kode_mk: str) -> bool:
        """Cek apakah nilai sudah ada untuk mahasiswa dan mata kuliah tertentu"""
        db = Database()
        query = "SELECT id FROM nilai WHERE nim=? AND kode_mk=?"
        result = db.fetch_one(query, (nim, kode_mk))
        return result is not None
    
    @staticmethod
    def get_statistik_mahasiswa(nim: str) -> Tuple[float, int, int]:
        """
        PRAKTIKUM 6: RELASI ANTAR CLASS
        Demonstrasi aggregation - menghitung statistik dari relasi
        
        Returns:
            Tuple[IPK, Total SKS, Jumlah MK Lulus]
        """
        db = Database()
        
        # Ambil nilai dan SKS melalui JOIN
        query = """
            SELECT n.nilai_akhir, mk.sks, n.status
            FROM nilai n
            JOIN mata_kuliah mk ON n.kode_mk = mk.kode_mk
            WHERE n.nim = ?
        """
        results = db.fetch_all(query, (nim,))
        
        if not results:
            return 0.0, 0, 0
        
        total_bobot = 0
        total_sks = 0
        jumlah_lulus = 0
        
        for nilai_akhir, sks, status in results:
            # Konversi nilai ke bobot
            if nilai_akhir >= 85:
                bobot = 4.0
            elif nilai_akhir >= 80:
                bobot = 3.7
            elif nilai_akhir >= 75:
                bobot = 3.3
            elif nilai_akhir >= 70:
                bobot = 3.0
            elif nilai_akhir >= 65:
                bobot = 2.7
            elif nilai_akhir >= 60:
                bobot = 2.3
            elif nilai_akhir >= 55:
                bobot = 2.0
            elif nilai_akhir >= 50:
                bobot = 1.0
            else:
                bobot = 0.0
            
            total_bobot += bobot * sks
            total_sks += sks
            
            if status == "Lulus":
                jumlah_lulus += 1
        
        ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
        
        return ipk, total_sks, jumlah_lulus
    
    def __str__(self):
        return (f"Nilai(NIM: {self.__nim}, Kode MK: {self.__kode_mk}, "
                f"Tugas: {self.__tugas}, UTS: {self.__uts}, UAS: {self.__uas}, "
                f"Nilai Akhir: {self.__nilai_akhir}, Grade: {self.__grade}, Status: {self.__status})")