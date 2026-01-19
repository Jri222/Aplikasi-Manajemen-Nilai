from database import Database
from typing import List, Optional

class Person:
    """
    PRAKTIKUM 4: PEWARISAN (INHERITANCE)
    Class induk/parent class untuk merepresentasikan Person
    """
    
    def __init__(self, nama: str):
        """Konstruktor class Person"""
        self._nama = nama  # Protected attribute
    
    @property
    def nama(self) -> str:
        """Getter untuk nama"""
        return self._nama
    
    @nama.setter
    def nama(self, value: str):
        """Setter untuk nama dengan validasi"""
        if not value or len(value) < 3:
            raise ValueError("Nama minimal 3 karakter")
        self._nama = value
    
    def get_info(self) -> str:
        """Method untuk mendapatkan informasi person"""
        return f"Nama: {self._nama}"


class Mahasiswa(Person):
    """
    PRAKTIKUM 4: PEWARISAN
    Class Mahasiswa mewarisi (inheritance) dari class Person
    - Single Inheritance: Mahasiswa extends Person
    - Method Overriding: get_info() di-override
    - Super(): Menggunakan konstruktor parent class
    """
    
    def __init__(self, nim: str, nama: str, jurusan: str, angkatan: int):
        """
        Konstruktor dengan pemanggilan super()
        Memanggil konstruktor parent class (Person)
        """
        super().__init__(nama)  # Memanggil konstruktor Person
        self.__nim = nim  # Private attribute
        self.__jurusan = jurusan
        self.__angkatan = angkatan
        self.db = Database()
    
    # Getter dan Setter untuk enkapsulasi
    @property
    def nim(self) -> str:
        return self.__nim
    
    @property
    def jurusan(self) -> str:
        return self.__jurusan
    
    @jurusan.setter
    def jurusan(self, value: str):
        if not value:
            raise ValueError("Jurusan tidak boleh kosong")
        self.__jurusan = value
    
    @property
    def angkatan(self) -> int:
        return self.__angkatan
    
    @angkatan.setter
    def angkatan(self, value: int):
        if value < 2000 or value > 2100:
            raise ValueError("Angkatan tidak valid")
        self.__angkatan = value
    
    def get_info(self) -> str:
        """
        Method Overriding: Override method dari parent class
        Menambahkan informasi spesifik mahasiswa
        """
        parent_info = super().get_info()  # Memanggil method parent
        return f"{parent_info}, NIM: {self.__nim}, Jurusan: {self.__jurusan}, Angkatan: {self.__angkatan}"
    
    def tambah(self) -> bool:
        """Menambah data mahasiswa ke database"""
        query = "INSERT INTO mahasiswa (nim, nama, jurusan, angkatan) VALUES (?, ?, ?, ?)"
        return self.db.execute_query(query, (self.__nim, self._nama, self.__jurusan, self.__angkatan))
    
    def update(self) -> bool:
        """Update data mahasiswa"""
        query = "UPDATE mahasiswa SET nama=?, jurusan=?, angkatan=? WHERE nim=?"
        return self.db.execute_query(query, (self._nama, self.__jurusan, self.__angkatan, self.__nim))
    
    @staticmethod
    def hapus(nim: str) -> bool:
        """Hapus data mahasiswa berdasarkan NIM"""
        db = Database()
        query = "DELETE FROM mahasiswa WHERE nim=?"
        return db.execute_query(query, (nim,))
    
    @staticmethod
    def cari_by_nim(nim: str) -> Optional['Mahasiswa']:
        """Cari mahasiswa berdasarkan NIM"""
        db = Database()
        query = "SELECT * FROM mahasiswa WHERE nim=?"
        result = db.fetch_one(query, (nim,))
        
        if result:
            return Mahasiswa(result[0], result[1], result[2], result[3])
        return None
    
    @staticmethod
    def cari_by_nama(nama: str) -> List[tuple]:
        """Cari mahasiswa berdasarkan nama (pencarian partial)"""
        db = Database()
        query = "SELECT * FROM mahasiswa WHERE nama LIKE ?"
        return db.fetch_all(query, (f"%{nama}%",))
    
    @staticmethod
    def get_all() -> List[tuple]:
        """Ambil semua data mahasiswa"""
        db = Database()
        query = "SELECT * FROM mahasiswa ORDER BY nim"
        return db.fetch_all(query)
    
    @staticmethod
    def is_nim_exists(nim: str) -> bool:
        """Cek apakah NIM sudah ada di database"""
        db = Database()
        query = "SELECT nim FROM mahasiswa WHERE nim=?"
        result = db.fetch_one(query, (nim,))
        return result is not None
    
    def __str__(self):
        """Magic method untuk representasi string"""
        return f"Mahasiswa(NIM: {self.__nim}, Nama: {self._nama}, Jurusan: {self.__jurusan}, Angkatan: {self.__angkatan})"