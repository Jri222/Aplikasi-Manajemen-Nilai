import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from mahasiswa import Mahasiswa
from matakuliah import MataKuliah
from nilai import Nilai
from laporan import Laporan

# PRAKTIKUM 9: EXCEPTION HANDLING
class InputValidationError(Exception):
    """Custom Exception untuk validasi input"""
    pass

class DatabaseOperationError(Exception):
    """Custom Exception untuk operasi database"""
    pass

class DataNotFoundError(Exception):
    """Custom Exception untuk data tidak ditemukan"""
    pass


class AplikasiManajemenNilai:
    """
    PRAKTIKUM 10: APLIKASI PEMROGRAMAN BERORIENTASI OBJEK
    
    Aplikasi GUI lengkap yang mengintegrasikan semua konsep OOP:
    - Praktikum 3: Konstruktor dan Enkapsulasi
    - Praktikum 4: Pewarisan
    - Praktikum 5: Polymorphism
    - Praktikum 6: Relasi Antar Class
    - Praktikum 7: Class Abstrak
    - Praktikum 8: Interface
    - Praktikum 9: Exception Handling
    """
    
    def __init__(self, root):
        """Konstruktor aplikasi GUI"""
        self.root = root
        self.root.title("Aplikasi Manajemen Nilai Mahasiswa - OOP")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_style()
        self.setup_ui()
    
    def setup_style(self):
        """Setup style untuk ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                       background='#2c3e50', foreground='white')
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Treeview', font=('Arial', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def setup_ui(self):
        """Setup UI components"""
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, 
                               text="SISTEM MANAJEMEN NILAI MAHASISWA (OOP)", 
                               style='Title.TLabel')
        title_label.pack(expand=True)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_mahasiswa_tab()
        self.create_matakuliah_tab()
        self.create_nilai_tab()
        self.create_laporan_tab()
    
    # PRAKTIKUM 9: EXCEPTION HANDLING dalam method validasi
    def validate_input(self, **fields) -> None:
        """
        Validasi input dengan custom exception
        
        Raises:
            InputValidationError: Jika input tidak valid
        """
        for field_name, value in fields.items():
            if not value or (isinstance(value, str) and not value.strip()):
                raise InputValidationError(f"Field '{field_name}' tidak boleh kosong!")
    
    def safe_execute(self, operation, success_msg: str, error_msg: str):
        """
        Wrapper untuk eksekusi operasi dengan exception handling
        Demonstrasi try-except-finally pattern
        """
        try:
            result = operation()
            if result:
                messagebox.showinfo("Sukses", success_msg)
                return True
            else:
                raise DatabaseOperationError(error_msg)
        except InputValidationError as e:
            messagebox.showwarning("Validasi Error", str(e))
        except DatabaseOperationError as e:
            messagebox.showerror("Database Error", str(e))
        except ValueError as e:
            messagebox.showerror("Value Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        finally:
            # Cleanup atau logging bisa dilakukan di sini
            pass
        return False
    
    # ==================== MAHASISWA TAB ====================
    def create_mahasiswa_tab(self):
        """Tab untuk manajemen data mahasiswa"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Data Mahasiswa")
        
        # Form frame
        form_frame = ttk.LabelFrame(tab, text="Form Data Mahasiswa", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(form_frame, text="NIM:").grid(row=0, column=0, sticky='w', pady=5)
        self.mhs_nim_entry = ttk.Entry(form_frame, width=30)
        self.mhs_nim_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Nama:").grid(row=0, column=2, sticky='w', pady=5, padx=(20, 0))
        self.mhs_nama_entry = ttk.Entry(form_frame, width=40)
        self.mhs_nama_entry.grid(row=0, column=3, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Jurusan:").grid(row=1, column=0, sticky='w', pady=5)
        self.mhs_jurusan_entry = ttk.Entry(form_frame, width=30)
        self.mhs_jurusan_entry.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Angkatan:").grid(row=1, column=2, sticky='w', pady=5, padx=(20, 0))
        self.mhs_angkatan_entry = ttk.Entry(form_frame, width=20)
        self.mhs_angkatan_entry.grid(row=1, column=3, pady=5, padx=5, sticky='w')
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Tambah", command=self.tambah_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hapus", command=self.hapus_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_mahasiswa, width=12).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.mhs_tree = ttk.Treeview(tree_frame, columns=('NIM', 'Nama', 'Jurusan', 'Angkatan'),
                                      show='headings', yscrollcommand=v_scroll.set,
                                      xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.mhs_tree.yview)
        h_scroll.config(command=self.mhs_tree.xview)
        
        for col in ('NIM', 'Nama', 'Jurusan', 'Angkatan'):
            self.mhs_tree.heading(col, text=col)
        
        self.mhs_tree.column('NIM', width=150)
        self.mhs_tree.column('Nama', width=300)
        self.mhs_tree.column('Jurusan', width=250)
        self.mhs_tree.column('Angkatan', width=100)
        
        self.mhs_tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        self.mhs_tree.bind('<Double-1>', self.select_mahasiswa)
        self.load_mahasiswa()
    
    def tambah_mahasiswa(self):
        """
        PRAKTIKUM 9: EXCEPTION HANDLING
        Tambah mahasiswa dengan comprehensive error handling
        """
        def operation():
            # Validasi input
            nim = self.mhs_nim_entry.get().strip()
            nama = self.mhs_nama_entry.get().strip()
            jurusan = self.mhs_jurusan_entry.get().strip()
            angkatan = self.mhs_angkatan_entry.get().strip()
            
            self.validate_input(NIM=nim, Nama=nama, Jurusan=jurusan, Angkatan=angkatan)
            
            # Validasi angkatan sebagai integer
            try:
                angkatan = int(angkatan)
            except ValueError:
                raise ValueError("Angkatan harus berupa angka!")
            
            # Cek duplikasi
            if Mahasiswa.is_nim_exists(nim):
                raise InputValidationError("NIM sudah terdaftar!")
            
            # Tambah mahasiswa menggunakan OOP
            mhs = Mahasiswa(nim, nama, jurusan, angkatan)
            if not mhs.tambah():
                raise DatabaseOperationError("Gagal menambahkan data ke database")
            
            self.clear_form_mahasiswa()
            self.load_mahasiswa()
            return True
        
        self.safe_execute(operation, 
                         "Data mahasiswa berhasil ditambahkan!", 
                         "Gagal menambahkan data mahasiswa")
    
    def update_mahasiswa(self):
        """Update mahasiswa dengan exception handling"""
        def operation():
            nim = self.mhs_nim_entry.get().strip()
            nama = self.mhs_nama_entry.get().strip()
            jurusan = self.mhs_jurusan_entry.get().strip()
            angkatan = self.mhs_angkatan_entry.get().strip()
            
            self.validate_input(NIM=nim, Nama=nama, Jurusan=jurusan, Angkatan=angkatan)
            
            angkatan = int(angkatan)
            
            if not Mahasiswa.is_nim_exists(nim):
                raise DataNotFoundError("NIM tidak ditemukan!")
            
            mhs = Mahasiswa(nim, nama, jurusan, angkatan)
            if not mhs.update():
                raise DatabaseOperationError("Gagal mengupdate data")
            
            self.clear_form_mahasiswa()
            self.load_mahasiswa()
            return True
        
        self.safe_execute(operation, 
                         "Data mahasiswa berhasil diupdate!", 
                         "Gagal mengupdate data mahasiswa")
    
    def hapus_mahasiswa(self):
        """Hapus mahasiswa dengan confirmation"""
        try:
            selected = self.mhs_tree.selection()
            if not selected:
                raise InputValidationError("Pilih data yang akan dihapus!")
            
            item = self.mhs_tree.item(selected[0])
            nim = item['values'][0]
            
            confirm = messagebox.askyesno("Konfirmasi", 
                                         f"Hapus mahasiswa dengan NIM {nim}?\n"
                                         "Data nilai mahasiswa ini juga akan terhapus!")
            
            if confirm:
                if Mahasiswa.hapus(nim):
                    messagebox.showinfo("Sukses", "Data mahasiswa berhasil dihapus!")
                    self.clear_form_mahasiswa()
                    self.load_mahasiswa()
                else:
                    raise DatabaseOperationError("Gagal menghapus data")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def select_mahasiswa(self, event):
        """Pilih data dari treeview"""
        try:
            selected = self.mhs_tree.selection()
            if selected:
                item = self.mhs_tree.item(selected[0])
                values = item['values']
                
                self.mhs_nim_entry.delete(0, 'end')
                self.mhs_nim_entry.insert(0, values[0])
                
                self.mhs_nama_entry.delete(0, 'end')
                self.mhs_nama_entry.insert(0, values[1])
                
                self.mhs_jurusan_entry.delete(0, 'end')
                self.mhs_jurusan_entry.insert(0, values[2])
                
                self.mhs_angkatan_entry.delete(0, 'end')
                self.mhs_angkatan_entry.insert(0, values[3])
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memilih data: {e}")
    
    def clear_form_mahasiswa(self):
        """Clear form mahasiswa"""
        self.mhs_nim_entry.delete(0, 'end')
        self.mhs_nama_entry.delete(0, 'end')
        self.mhs_jurusan_entry.delete(0, 'end')
        self.mhs_angkatan_entry.delete(0, 'end')
    
    def load_mahasiswa(self):
        """Load data mahasiswa ke treeview"""
        try:
            for item in self.mhs_tree.get_children():
                self.mhs_tree.delete(item)
            
            data = Mahasiswa.get_all()
            for row in data:
                self.mhs_tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")
    
    # ==================== MATA KULIAH & NILAI TABS ====================
    # (Methods lainnya mengikuti pattern yang sama dengan exception handling)
    
    def create_matakuliah_tab(self):
        """Implementasi serupa dengan mahasiswa_tab"""
        pass  # Implementasi lengkap seperti pada kode asli
    
    def create_nilai_tab(self):
        """Implementasi serupa dengan mahasiswa_tab"""
        pass  # Implementasi lengkap seperti pada kode asli
    
    def create_laporan_tab(self):
        """
        PRAKTIKUM 10: INTEGRASI SEMUA KONSEP OOP
        Tab laporan yang menggunakan:
        - Class Abstrak (LaporanBase)
        - Interface (IExportable, IPrintable)
        - Exception Handling
        """
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Laporan")
        
        control_frame = ttk.LabelFrame(tab, text="Generate Laporan", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(control_frame, text="Laporan Mahasiswa:").grid(row=0, column=0, sticky='w', pady=5)
        self.laporan_nim_entry = ttk.Entry(control_frame, width=25)
        self.laporan_nim_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(control_frame, text="Lihat Laporan", command=self.tampilkan_laporan).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Simpan Laporan", command=self.simpan_laporan).grid(row=0, column=3, padx=5)
        
        text_frame = ttk.LabelFrame(tab, text="Preview Laporan", padding=10)
        text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        v_scroll = ttk.Scrollbar(text_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(text_frame, orient='horizontal')
        
        self.laporan_text = tk.Text(text_frame, wrap='none', font=('Courier', 9),
                                     yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.laporan_text.yview)
        h_scroll.config(command=self.laporan_text.xview)
        
        self.laporan_text.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
    
    def tampilkan_laporan(self):
        """Tampilkan laporan dengan exception handling"""
        try:
            nim = self.laporan_nim_entry.get().strip()
            
            if not nim:
                raise InputValidationError("Masukkan NIM terlebih dahulu!")
            
            # Menggunakan class abstrak dan interface
            laporan = Laporan.cetak_laporan_mahasiswa(nim)
            
            if laporan:
                self.laporan_text.delete('1.0', 'end')
                self.laporan_text.insert('1.0', laporan)
            else:
                raise DataNotFoundError("Mahasiswa tidak ditemukan!")
        except InputValidationError as e:
            messagebox.showwarning("Validasi", str(e))
        except DataNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan laporan: {e}")
    
    def simpan_laporan(self):
        """Simpan laporan menggunakan interface IExportable"""
        try:
            nim = self.laporan_nim_entry.get().strip()
            
            if not nim:
                raise InputValidationError("Masukkan NIM terlebih dahulu!")
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"laporan_{nim}.txt"
            )
            
            if filename:
                if Laporan.simpan_laporan(nim, filename):
                    messagebox.showinfo("Sukses", f"Laporan berhasil disimpan ke:\n{filename}")
                else:
                    raise DatabaseOperationError("Gagal menyimpan laporan!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    """
    PRAKTIKUM 10: ENTRY POINT APLIKASI
    Fungsi utama untuk menjalankan aplikasi OOP
    """
    root = tk.Tk()
    app = AplikasiManajemenNilai(root)
    root.mainloop()


if __name__ == "__main__":
    main()