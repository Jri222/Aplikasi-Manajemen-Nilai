import sqlite3
from typing import List, Tuple, Optional

class Database:
    """
    Class untuk mengelola koneksi dan operasi database
    
    PRAKTIKUM 3: KONSTRUKTOR DAN ENKAPSULASI
    - Konstruktor (__init__): Menginisialisasi objek dengan db_name dan membuat tabel
    - Enkapsulasi: Atribut db_name bersifat private dengan naming convention
    - Method get_connection() menyembunyikan detail implementasi koneksi
    """
    
    def __init__(self, db_name: str = "mahasiswa.db"):
        """
        Konstruktor untuk inisialisasi database
        
        Args:
            db_name: Nama file database (default: mahasiswa.db)
        """
        self.__db_name = db_name  # Private attribute (enkapsulasi)
        self.create_tables()
    
    # Getter untuk db_name (enkapsulasi)
    @property
    def db_name(self) -> str:
        """Getter untuk mengakses nama database"""
        return self.__db_name
    
    # Setter untuk db_name (enkapsulasi dengan validasi)
    @db_name.setter
    def db_name(self, value: str):
        """Setter untuk mengubah nama database dengan validasi"""
        if not value or not value.endswith('.db'):
            raise ValueError("Nama database harus berakhiran .db")
        self.__db_name = value
    
    def get_connection(self):
        """
        Membuat koneksi ke database
        Method ini menyembunyikan detail implementasi (enkapsulasi)
        """
        return sqlite3.connect(self.__db_name)
    
    def create_tables(self):
        """Membuat tabel-tabel yang diperlukan"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabel Mahasiswa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mahasiswa (
                nim TEXT PRIMARY KEY,
                nama TEXT NOT NULL,
                jurusan TEXT NOT NULL,
                angkatan INTEGER NOT NULL
            )
        ''')
        
        # Tabel Mata Kuliah
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mata_kuliah (
                kode_mk TEXT PRIMARY KEY,
                nama_mk TEXT NOT NULL,
                sks INTEGER NOT NULL
            )
        ''')
        
        # Tabel Nilai
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nilai (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nim TEXT NOT NULL,
                kode_mk TEXT NOT NULL,
                tugas REAL DEFAULT 0,
                uts REAL DEFAULT 0,
                uas REAL DEFAULT 0,
                nilai_akhir REAL DEFAULT 0,
                grade TEXT DEFAULT '-',
                status TEXT DEFAULT 'Belum Lulus',
                FOREIGN KEY (nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE,
                FOREIGN KEY (kode_mk) REFERENCES mata_kuliah(kode_mk) ON DELETE CASCADE,
                UNIQUE(nim, kode_mk)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> bool:
        """
        Eksekusi query INSERT, UPDATE, DELETE
        Enkapsulasi error handling di dalam method
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Fetch semua data dari query SELECT"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Tuple]:
        """Fetch satu data dari query SELECT"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None