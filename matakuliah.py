from database import Database
from typing import List, Optional

class MataKuliah:
    """Class untuk mengelola data mata kuliah"""
    
    def __init__(self, kode_mk: str, nama_mk: str, sks: int):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks
        self.db = Database()
    
    def tambah(self) -> bool:
        """Menambah data mata kuliah ke database"""
        query = "INSERT INTO mata_kuliah (kode_mk, nama_mk, sks) VALUES (?, ?, ?)"
        return self.db.execute_query(query, (self.kode_mk, self.nama_mk, self.sks))
    
    def update(self) -> bool:
        """Update data mata kuliah"""
        query = "UPDATE mata_kuliah SET nama_mk=?, sks=? WHERE kode_mk=?"
        return self.db.execute_query(query, (self.nama_mk, self.sks, self.kode_mk))
    
    @staticmethod
    def hapus(kode_mk: str) -> bool:
        """Hapus data mata kuliah berdasarkan kode"""
        db = Database()
        query = "DELETE FROM mata_kuliah WHERE kode_mk=?"
        return db.execute_query(query, (kode_mk,))
    
    @staticmethod
    def cari_by_kode(kode_mk: str) -> Optional['MataKuliah']:
        """Cari mata kuliah berdasarkan kode"""
        db = Database()
        query = "SELECT * FROM mata_kuliah WHERE kode_mk=?"
        result = db.fetch_one(query, (kode_mk,))
        
        if result:
            return MataKuliah(result[0], result[1], result[2])
        return None
    
    @staticmethod
    def get_all() -> List[tuple]:
        """Ambil semua data mata kuliah"""
        db = Database()
        query = "SELECT * FROM mata_kuliah ORDER BY kode_mk"
        return db.fetch_all(query)
    
    @staticmethod
    def is_kode_exists(kode_mk: str) -> bool:
        """Cek apakah kode MK sudah ada di database"""
        db = Database()
        query = "SELECT kode_mk FROM mata_kuliah WHERE kode_mk=?"
        result = db.fetch_one(query, (kode_mk,))
        return result is not None
    
    def __str__(self):
        return f"MataKuliah(Kode: {self.kode_mk}, Nama: {self.nama_mk}, SKS: {self.sks})"