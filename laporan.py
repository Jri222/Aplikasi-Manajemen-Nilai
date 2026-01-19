from datetime import datetime
from mahasiswa import Mahasiswa
from matakuliah import MataKuliah
from nilai import Nilai
from typing import Optional
from abc import ABC, abstractmethod

# PRAKTIKUM 7: CLASS ABSTRAK
class LaporanBase(ABC):
    """
    Abstract Base Class untuk laporan
    Mendefinisikan kontrak/template yang harus diikuti oleh subclass
    """
    
    @abstractmethod
    def generate_header(self) -> str:
        """Abstract method: Harus diimplementasikan oleh subclass"""
        pass
    
    @abstractmethod
    def generate_body(self) -> str:
        """Abstract method: Harus diimplementasikan oleh subclass"""
        pass
    
    @abstractmethod
    def generate_footer(self) -> str:
        """Abstract method: Harus diimplementasikan oleh subclass"""
        pass
    
    def generate_laporan(self) -> str:
        """
        Template Method Pattern
        Method konkret yang menggunakan abstract methods
        """
        header = self.generate_header()
        body = self.generate_body()
        footer = self.generate_footer()
        return f"{header}\n{body}\n{footer}"


# PRAKTIKUM 8: INTERFACE (menggunakan ABC dengan semua abstract methods)
class IExportable(ABC):
    """
    Interface untuk objek yang bisa di-export
    Semua method adalah abstract (pure interface)
    """
    
    @abstractmethod
    def export_to_text(self, filename: str) -> bool:
        """Export ke file text"""
        pass
    
    @abstractmethod
    def export_to_console(self) -> str:
        """Export ke console/string"""
        pass


class IPrintable(ABC):
    """
    Interface untuk objek yang bisa di-print
    """
    
    @abstractmethod
    def print_preview(self) -> str:
        """Preview sebelum print"""
        pass


# PRAKTIKUM 7 & 8: Implementasi Class Abstrak dan Interface
class Laporan(LaporanBase, IExportable, IPrintable):
    """
    Class Laporan yang:
    - Mengimplementasikan abstract class LaporanBase (Praktikum 7)
    - Mengimplementasikan interface IExportable dan IPrintable (Praktikum 8)
    
    Demonstrasi Multiple Inheritance dari abstract class dan interface
    """
    
    def __init__(self, nim: Optional[str] = None):
        """Konstruktor dengan optional NIM untuk laporan per mahasiswa"""
        self._nim = nim
        self._laporan_content = ""
    
    # Implementasi abstract methods dari LaporanBase
    def generate_header(self) -> str:
        """Override abstract method: Generate header laporan"""
        if self._nim:
            title = "LAPORAN NILAI MAHASISWA"
        else:
            title = "LAPORAN NILAI SEMUA MAHASISWA"
        
        header = []
        header.append("=" * 80)
        header.append(title.center(80))
        header.append("=" * 80)
        header.append(f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        header.append("")
        return "\n".join(header)
    
    def generate_body(self) -> str:
        """Override abstract method: Generate body laporan"""
        if self._nim:
            return self._generate_body_single()
        else:
            return self._generate_body_all()
    
    def generate_footer(self) -> str:
        """Override abstract method: Generate footer laporan"""
        return "=" * 80
    
    def _generate_body_single(self) -> str:
        """Private method: Generate body untuk satu mahasiswa"""
        mhs = Mahasiswa.cari_by_nim(self._nim)
        if not mhs:
            return "Mahasiswa tidak ditemukan."
        
        nilai_list = Nilai.get_by_nim(self._nim)
        ipk, total_sks, jumlah_lulus = Nilai.get_statistik_mahasiswa(self._nim)
        
        body = []
        body.append("DATA MAHASISWA")
        body.append("-" * 80)
        body.append(f"NIM        : {mhs.nim}")
        body.append(f"Nama       : {mhs.nama}")
        body.append(f"Jurusan    : {mhs.jurusan}")
        body.append(f"Angkatan   : {mhs.angkatan}")
        body.append("")
        body.append("DAFTAR NILAI")
        body.append("-" * 80)
        
        if nilai_list:
            body.append(f"{'Kode MK':<12} {'Nama Mata Kuliah':<25} {'Tugas':>8} {'UTS':>8} {'UAS':>8} {'N.Akhir':>8} {'Grade':>6} {'Status':<12}")
            body.append("-" * 80)
            
            for data in nilai_list:
                nim, nama, kode_mk, nama_mk, tugas, uts, uas, nilai_akhir, grade, status = data
                body.append(f"{kode_mk:<12} {nama_mk:<25} {tugas:>8.2f} {uts:>8.2f} {uas:>8.2f} {nilai_akhir:>8.2f} {grade:>6} {status:<12}")
        else:
            body.append("Tidak ada data nilai.")
        
        body.append("-" * 80)
        body.append("")
        body.append("STATISTIK")
        body.append("-" * 80)
        body.append(f"IPK                : {ipk:.2f}")
        body.append(f"Total SKS          : {total_sks}")
        body.append(f"Mata Kuliah Lulus  : {jumlah_lulus}")
        
        return "\n".join(body)
    
    def _generate_body_all(self) -> str:
        """Private method: Generate body untuk semua mahasiswa"""
        mahasiswa_list = Mahasiswa.get_all()
        
        body = []
        if mahasiswa_list:
            body.append(f"{'NIM':<15} {'Nama':<25} {'Jurusan':<20} {'IPK':>8} {'Total SKS':>10} {'MK Lulus':>10}")
            body.append("-" * 100)
            
            for mhs_data in mahasiswa_list:
                nim, nama, jurusan, angkatan = mhs_data
                ipk, total_sks, jumlah_lulus = Nilai.get_statistik_mahasiswa(nim)
                body.append(f"{nim:<15} {nama:<25} {jurusan:<20} {ipk:>8.2f} {total_sks:>10} {jumlah_lulus:>10}")
        else:
            body.append("Tidak ada data mahasiswa.")
        
        return "\n".join(body)
    
    # Implementasi interface IExportable
    def export_to_text(self, filename: str) -> bool:
        """
        Override interface method: Export laporan ke file
        
        Args:
            filename: Nama file output
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            content = self.generate_laporan()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error exporting to text: {e}")
            return False
    
    def export_to_console(self) -> str:
        """Override interface method: Export laporan ke console"""
        return self.generate_laporan()
    
    # Implementasi interface IPrintable
    def print_preview(self) -> str:
        """Override interface method: Preview laporan"""
        return self.generate_laporan()
    
    # Static methods untuk kemudahan penggunaan
    @staticmethod
    def cetak_laporan_mahasiswa(nim: str) -> Optional[str]:
        """
        Generate laporan nilai untuk satu mahasiswa
        Menggunakan polymorphism dan abstract class
        """
        laporan = Laporan(nim)
        content = laporan.export_to_console()
        return content if content else None
    
    @staticmethod
    def cetak_laporan_semua() -> str:
        """Generate laporan nilai untuk semua mahasiswa"""
        laporan = Laporan()
        return laporan.export_to_console()
    
    @staticmethod
    def simpan_laporan(nim: str, filename: str = None) -> bool:
        """
        Simpan laporan ke file
        Demonstrasi penggunaan interface IExportable
        """
        try:
            laporan = Laporan(nim)
            
            if not filename:
                filename = f"laporan_{nim}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            return laporan.export_to_text(filename)
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    @staticmethod
    def simpan_laporan_semua(filename: str = None) -> bool:
        """Simpan laporan semua mahasiswa ke file"""
        try:
            laporan = Laporan()
            
            if not filename:
                filename = f"laporan_semua_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            return laporan.export_to_text(filename)
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


# PRAKTIKUM 8: Contoh implementasi interface lain
class LaporanPDF(IExportable):
    """
    Contoh class lain yang mengimplementasikan interface IExportable
    Demonstrasi bahwa berbagai class dapat mengimplementasikan interface yang sama
    """
    
    def __init__(self, content: str):
        self._content = content
    
    def export_to_text(self, filename: str) -> bool:
        """Implementasi export ke text (simulasi PDF)"""
        try:
            # Simulasi export PDF (dalam praktik nyata gunakan library seperti reportlab)
            with open(filename.replace('.txt', '.pdf'), 'w') as f:
                f.write(f"[PDF Format]\n{self._content}")
            return True
        except:
            return False
    
    def export_to_console(self) -> str:
        """Implementasi export ke console"""
        return f"[PDF Preview]\n{self._content}"