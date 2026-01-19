import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from mahasiswa import Mahasiswa
from matakuliah import MataKuliah
from nilai import Nilai
from laporan import Laporan

class AplikasiManajemenNilai:
    """Aplikasi GUI untuk manajemen nilai mahasiswa"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Nilai Mahasiswa")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Style configuration
        self.setup_style()
        
        # Create main container
        self.setup_ui()
        
    def setup_style(self):
        """Setup style untuk ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white')
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Treeview', font=('Arial', 9), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
    def setup_ui(self):
        """Setup UI components"""
        # Title bar
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, text="SISTEM MANAJEMEN NILAI MAHASISWA", 
                                style='Title.TLabel')
        title_label.pack(expand=True)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_mahasiswa_tab()
        self.create_matakuliah_tab()
        self.create_nilai_tab()
        self.create_laporan_tab()
        
    def create_mahasiswa_tab(self):
        """Tab untuk manajemen data mahasiswa"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Data Mahasiswa")
        
        # Form frame
        form_frame = ttk.LabelFrame(tab, text="Form Data Mahasiswa", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # NIM
        ttk.Label(form_frame, text="NIM:").grid(row=0, column=0, sticky='w', pady=5)
        self.mhs_nim_entry = ttk.Entry(form_frame, width=30)
        self.mhs_nim_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Nama
        ttk.Label(form_frame, text="Nama:").grid(row=0, column=2, sticky='w', pady=5, padx=(20, 0))
        self.mhs_nama_entry = ttk.Entry(form_frame, width=40)
        self.mhs_nama_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # Jurusan
        ttk.Label(form_frame, text="Jurusan:").grid(row=1, column=0, sticky='w', pady=5)
        self.mhs_jurusan_entry = ttk.Entry(form_frame, width=30)
        self.mhs_jurusan_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Angkatan
        ttk.Label(form_frame, text="Angkatan:").grid(row=1, column=2, sticky='w', pady=5, padx=(20, 0))
        self.mhs_angkatan_entry = ttk.Entry(form_frame, width=20)
        self.mhs_angkatan_entry.grid(row=1, column=3, pady=5, padx=5, sticky='w')
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Tambah", command=self.tambah_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hapus", command=self.hapus_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form_mahasiswa, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_mahasiswa, width=12).pack(side='left', padx=5)
        
        # Search frame
        search_frame = ttk.LabelFrame(tab, text="Pencarian", padding=10)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="Cari NIM:").pack(side='left', padx=5)
        self.mhs_search_entry = ttk.Entry(search_frame, width=30)
        self.mhs_search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Cari", command=self.cari_mahasiswa).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.mhs_tree = ttk.Treeview(tree_frame, columns=('NIM', 'Nama', 'Jurusan', 'Angkatan'),
                                      show='headings', yscrollcommand=v_scroll.set,
                                      xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.mhs_tree.yview)
        h_scroll.config(command=self.mhs_tree.xview)
        
        # Column headings
        self.mhs_tree.heading('NIM', text='NIM')
        self.mhs_tree.heading('Nama', text='Nama')
        self.mhs_tree.heading('Jurusan', text='Jurusan')
        self.mhs_tree.heading('Angkatan', text='Angkatan')
        
        # Column widths
        self.mhs_tree.column('NIM', width=150)
        self.mhs_tree.column('Nama', width=300)
        self.mhs_tree.column('Jurusan', width=250)
        self.mhs_tree.column('Angkatan', width=100)
        
        # Pack
        self.mhs_tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        # Bind double click
        self.mhs_tree.bind('<Double-1>', self.select_mahasiswa)
        
        # Load data
        self.load_mahasiswa()
    
    def create_matakuliah_tab(self):
        """Tab untuk manajemen data mata kuliah"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Mata Kuliah")
        
        # Form frame
        form_frame = ttk.LabelFrame(tab, text="Form Data Mata Kuliah", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # Kode MK
        ttk.Label(form_frame, text="Kode MK:").grid(row=0, column=0, sticky='w', pady=5)
        self.mk_kode_entry = ttk.Entry(form_frame, width=25)
        self.mk_kode_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Nama MK
        ttk.Label(form_frame, text="Nama MK:").grid(row=0, column=2, sticky='w', pady=5, padx=(20, 0))
        self.mk_nama_entry = ttk.Entry(form_frame, width=50)
        self.mk_nama_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # SKS
        ttk.Label(form_frame, text="SKS:").grid(row=1, column=0, sticky='w', pady=5)
        self.mk_sks_entry = ttk.Entry(form_frame, width=15)
        self.mk_sks_entry.grid(row=1, column=1, pady=5, padx=5, sticky='w')
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Tambah", command=self.tambah_matakuliah, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_matakuliah, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hapus", command=self.hapus_matakuliah, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form_matakuliah, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_matakuliah, width=12).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.mk_tree = ttk.Treeview(tree_frame, columns=('Kode', 'Nama MK', 'SKS'),
                                     show='headings', yscrollcommand=v_scroll.set,
                                     xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.mk_tree.yview)
        h_scroll.config(command=self.mk_tree.xview)
        
        # Column headings
        self.mk_tree.heading('Kode', text='Kode MK')
        self.mk_tree.heading('Nama MK', text='Nama Mata Kuliah')
        self.mk_tree.heading('SKS', text='SKS')
        
        # Column widths
        self.mk_tree.column('Kode', width=150)
        self.mk_tree.column('Nama MK', width=500)
        self.mk_tree.column('SKS', width=100)
        
        # Pack
        self.mk_tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        # Bind double click
        self.mk_tree.bind('<Double-1>', self.select_matakuliah)
        
        # Load data
        self.load_matakuliah()
    
    def create_nilai_tab(self):
        """Tab untuk manajemen nilai"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Nilai Mahasiswa")
        
        # Form frame
        form_frame = ttk.LabelFrame(tab, text="Form Input Nilai", padding=10)
        form_frame.pack(fill='x', padx=10, pady=5)
        
        # NIM
        ttk.Label(form_frame, text="NIM:").grid(row=0, column=0, sticky='w', pady=5)
        self.nilai_nim_entry = ttk.Entry(form_frame, width=25)
        self.nilai_nim_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(form_frame, text="Cek", command=self.cek_mahasiswa).grid(row=0, column=2, padx=5)
        
        # Nama (readonly)
        ttk.Label(form_frame, text="Nama:").grid(row=0, column=3, sticky='w', pady=5, padx=(20, 0))
        self.nilai_nama_label = ttk.Label(form_frame, text="-", foreground='blue')
        self.nilai_nama_label.grid(row=0, column=4, pady=5, padx=5, sticky='w')
        
        # Kode MK
        ttk.Label(form_frame, text="Kode MK:").grid(row=1, column=0, sticky='w', pady=5)
        self.nilai_kode_entry = ttk.Entry(form_frame, width=25)
        self.nilai_kode_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Nama MK (readonly)
        ttk.Label(form_frame, text="Nama MK:").grid(row=1, column=3, sticky='w', pady=5, padx=(20, 0))
        self.nilai_nama_mk_label = ttk.Label(form_frame, text="-", foreground='blue')
        self.nilai_nama_mk_label.grid(row=1, column=4, pady=5, padx=5, sticky='w')
        
        # Nilai frame
        nilai_detail_frame = ttk.Frame(form_frame)
        nilai_detail_frame.grid(row=2, column=0, columnspan=5, pady=10)
        
        ttk.Label(nilai_detail_frame, text="Tugas:").grid(row=0, column=0, sticky='w', padx=5)
        self.nilai_tugas_entry = ttk.Entry(nilai_detail_frame, width=15)
        self.nilai_tugas_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(nilai_detail_frame, text="UTS:").grid(row=0, column=2, sticky='w', padx=(20, 5))
        self.nilai_uts_entry = ttk.Entry(nilai_detail_frame, width=15)
        self.nilai_uts_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(nilai_detail_frame, text="UAS:").grid(row=0, column=4, sticky='w', padx=(20, 5))
        self.nilai_uas_entry = ttk.Entry(nilai_detail_frame, width=15)
        self.nilai_uas_entry.grid(row=0, column=5, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=5, pady=10)
        
        ttk.Button(btn_frame, text="Tambah", command=self.tambah_nilai, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_nilai, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hapus", command=self.hapus_nilai, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form_nilai, width=12).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.load_nilai, width=12).pack(side='left', padx=5)
        
        # Search frame
        search_frame = ttk.LabelFrame(tab, text="Filter Data", padding=10)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="NIM:").pack(side='left', padx=5)
        self.nilai_search_entry = ttk.Entry(search_frame, width=25)
        self.nilai_search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Filter", command=self.filter_nilai).pack(side='left', padx=5)
        ttk.Button(search_frame, text="Tampilkan Semua", command=self.load_nilai).pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        self.nilai_tree = ttk.Treeview(tree_frame, 
                                        columns=('NIM', 'Nama', 'Kode MK', 'Nama MK', 
                                                'Tugas', 'UTS', 'UAS', 'N.Akhir', 'Grade', 'Status'),
                                        show='headings', yscrollcommand=v_scroll.set,
                                        xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.nilai_tree.yview)
        h_scroll.config(command=self.nilai_tree.xview)
        
        # Column headings
        for col in ('NIM', 'Nama', 'Kode MK', 'Nama MK', 'Tugas', 'UTS', 'UAS', 'N.Akhir', 'Grade', 'Status'):
            self.nilai_tree.heading(col, text=col)
        
        # Column widths
        self.nilai_tree.column('NIM', width=100)
        self.nilai_tree.column('Nama', width=180)
        self.nilai_tree.column('Kode MK', width=80)
        self.nilai_tree.column('Nama MK', width=200)
        self.nilai_tree.column('Tugas', width=60)
        self.nilai_tree.column('UTS', width=60)
        self.nilai_tree.column('UAS', width=60)
        self.nilai_tree.column('N.Akhir', width=70)
        self.nilai_tree.column('Grade', width=60)
        self.nilai_tree.column('Status', width=100)
        
        # Pack
        self.nilai_tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
        # Bind double click
        self.nilai_tree.bind('<Double-1>', self.select_nilai)
        
        # Load data
        self.load_nilai()
    
    def create_laporan_tab(self):
        """Tab untuk laporan"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Laporan")
        
        # Control frame
        control_frame = ttk.LabelFrame(tab, text="Generate Laporan", padding=10)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Laporan per mahasiswa
        ttk.Label(control_frame, text="Laporan Mahasiswa:").grid(row=0, column=0, sticky='w', pady=5)
        self.laporan_nim_entry = ttk.Entry(control_frame, width=25)
        self.laporan_nim_entry.grid(row=0, column=1, pady=5, padx=5)
        ttk.Button(control_frame, text="Lihat Laporan", command=self.tampilkan_laporan).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Simpan Laporan", command=self.simpan_laporan).grid(row=0, column=3, padx=5)
        
        # Laporan semua mahasiswa
        ttk.Label(control_frame, text="Laporan Semua:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Button(control_frame, text="Lihat Semua", command=self.tampilkan_laporan_semua).grid(row=1, column=1, padx=5, sticky='w')
        ttk.Button(control_frame, text="Simpan Semua", command=self.simpan_laporan_semua).grid(row=1, column=2, padx=5, sticky='w')
        
        # Text area untuk menampilkan laporan
        text_frame = ttk.LabelFrame(tab, text="Preview Laporan", padding=10)
        text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(text_frame, orient='vertical')
        h_scroll = ttk.Scrollbar(text_frame, orient='horizontal')
        
        self.laporan_text = tk.Text(text_frame, wrap='none', font=('Courier', 9),
                                     yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.config(command=self.laporan_text.yview)
        h_scroll.config(command=self.laporan_text.xview)
        
        self.laporan_text.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
    
    # ==================== MAHASISWA METHODS ====================
    
    def tambah_mahasiswa(self):
        """Tambah data mahasiswa"""
        nim = self.mhs_nim_entry.get().strip()
        nama = self.mhs_nama_entry.get().strip()
        jurusan = self.mhs_jurusan_entry.get().strip()
        angkatan = self.mhs_angkatan_entry.get().strip()
        
        if not all([nim, nama, jurusan, angkatan]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        try:
            angkatan = int(angkatan)
        except ValueError:
            messagebox.showerror("Error", "Angkatan harus berupa angka!")
            return
        
        if Mahasiswa.is_nim_exists(nim):
            messagebox.showerror("Error", "NIM sudah terdaftar!")
            return
        
        mhs = Mahasiswa(nim, nama, jurusan, angkatan)
        if mhs.tambah():
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
            self.clear_form_mahasiswa()
            self.load_mahasiswa()
        else:
            messagebox.showerror("Error", "Gagal menambahkan data mahasiswa!")
    
    def update_mahasiswa(self):
        """Update data mahasiswa"""
        nim = self.mhs_nim_entry.get().strip()
        nama = self.mhs_nama_entry.get().strip()
        jurusan = self.mhs_jurusan_entry.get().strip()
        angkatan = self.mhs_angkatan_entry.get().strip()
        
        if not all([nim, nama, jurusan, angkatan]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        try:
            angkatan = int(angkatan)
        except ValueError:
            messagebox.showerror("Error", "Angkatan harus berupa angka!")
            return
        
        if not Mahasiswa.is_nim_exists(nim):
            messagebox.showerror("Error", "NIM tidak ditemukan!")
            return
        
        mhs = Mahasiswa(nim, nama, jurusan, angkatan)
        if mhs.update():
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil diupdate!")
            self.clear_form_mahasiswa()
            self.load_mahasiswa()
        else:
            messagebox.showerror("Error", "Gagal mengupdate data mahasiswa!")
    
    def hapus_mahasiswa(self):
        """Hapus data mahasiswa"""
        selected = self.mhs_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        
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
                messagebox.showerror("Error", "Gagal menghapus data mahasiswa!")
    
    def cari_mahasiswa(self):
        """Cari mahasiswa berdasarkan NIM"""
        nim = self.mhs_search_entry.get().strip()
        
        if not nim:
            self.load_mahasiswa()
            return
        
        mhs = Mahasiswa.cari_by_nim(nim)
        
        # Clear tree
        for item in self.mhs_tree.get_children():
            self.mhs_tree.delete(item)
        
        if mhs:
            self.mhs_tree.insert('', 'end', values=(mhs.nim, mhs.nama, mhs.jurusan, mhs.angkatan))
        else:
            messagebox.showinfo("Info", "Data tidak ditemukan!")
    
    def select_mahasiswa(self, event):
        """Pilih data mahasiswa dari treeview"""
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
    
    def clear_form_mahasiswa(self):
        """Clear form mahasiswa"""
        self.mhs_nim_entry.delete(0, 'end')
        self.mhs_nama_entry.delete(0, 'end')
        self.mhs_jurusan_entry.delete(0, 'end')
        self.mhs_angkatan_entry.delete(0, 'end')
        self.mhs_search_entry.delete(0, 'end')
    
    def load_mahasiswa(self):
        """Load semua data mahasiswa ke treeview"""
        # Clear tree
        for item in self.mhs_tree.get_children():
            self.mhs_tree.delete(item)
        
        # Load data
        data = Mahasiswa.get_all()
        for row in data:
            self.mhs_tree.insert('', 'end', values=row)
    
    # ==================== MATA KULIAH METHODS ====================
    
    def tambah_matakuliah(self):
        """Tambah data mata kuliah"""
        kode = self.mk_kode_entry.get().strip()
        nama = self.mk_nama_entry.get().strip()
        sks = self.mk_sks_entry.get().strip()
        
        if not all([kode, nama, sks]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        try:
            sks = int(sks)
        except ValueError:
            messagebox.showerror("Error", "SKS harus berupa angka!")
            return
        
        if MataKuliah.is_kode_exists(kode):
            messagebox.showerror("Error", "Kode MK sudah terdaftar!")
            return
        
        mk = MataKuliah(kode, nama, sks)
        if mk.tambah():
            messagebox.showinfo("Sukses", "Data mata kuliah berhasil ditambahkan!")
            self.clear_form_matakuliah()
            self.load_matakuliah()
        else:
            messagebox.showerror("Error", "Gagal menambahkan data mata kuliah!")
    
    def update_matakuliah(self):
        """Update data mata kuliah"""
        kode = self.mk_kode_entry.get().strip()
        nama = self.mk_nama_entry.get().strip()
        sks = self.mk_sks_entry.get().strip()
        
        if not all([kode, nama, sks]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        try:
            sks = int(sks)
        except ValueError:
            messagebox.showerror("Error", "SKS harus berupa angka!")
            return
        
        if not MataKuliah.is_kode_exists(kode):
            messagebox.showerror("Error", "Kode MK tidak ditemukan!")
            return
        
        mk = MataKuliah(kode, nama, sks)
        if mk.update():
            messagebox.showinfo("Sukses", "Data mata kuliah berhasil diupdate!")
            self.clear_form_matakuliah()
            self.load_matakuliah()
        else:
            messagebox.showerror("Error", "Gagal mengupdate data mata kuliah!")
    
    def hapus_matakuliah(self):
        """Hapus data mata kuliah"""
        selected = self.mk_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        
        item = self.mk_tree.item(selected[0])
        kode = item['values'][0]
        
        confirm = messagebox.askyesno("Konfirmasi", 
                                       f"Hapus mata kuliah {kode}?\n"
                                       "Data nilai untuk mata kuliah ini juga akan terhapus!")
        
        if confirm:
            if MataKuliah.hapus(kode):
                messagebox.showinfo("Sukses", "Data mata kuliah berhasil dihapus!")
                self.clear_form_matakuliah()
                self.load_matakuliah()
            else:
                messagebox.showerror("Error", "Gagal menghapus data mata kuliah!")
    
    def select_matakuliah(self, event):
        """Pilih data mata kuliah dari treeview"""
        selected = self.mk_tree.selection()
        if selected:
            item = self.mk_tree.item(selected[0])
            values = item['values']
            
            self.mk_kode_entry.delete(0, 'end')
            self.mk_kode_entry.insert(0, values[0])
            
            self.mk_nama_entry.delete(0, 'end')
            self.mk_nama_entry.insert(0, values[1])
            
            self.mk_sks_entry.delete(0, 'end')
            self.mk_sks_entry.insert(0, values[2])
    
    def clear_form_matakuliah(self):
        """Clear form mata kuliah"""
        self.mk_kode_entry.delete(0, 'end')
        self.mk_nama_entry.delete(0, 'end')
        self.mk_sks_entry.delete(0, 'end')
    
    def load_matakuliah(self):
        """Load semua data mata kuliah ke treeview"""
        # Clear tree
        for item in self.mk_tree.get_children():
            self.mk_tree.delete(item)
        
        # Load data
        data = MataKuliah.get_all()
        for row in data:
            self.mk_tree.insert('', 'end', values=row)
    
    # ==================== NILAI METHODS ====================
    
    def cek_mahasiswa(self):
        """Cek dan tampilkan nama mahasiswa"""
        nim = self.nilai_nim_entry.get().strip()
        if not nim:
            return
        
        mhs = Mahasiswa.cari_by_nim(nim)
        if mhs:
            self.nilai_nama_label.config(text=mhs.nama)
        else:
            self.nilai_nama_label.config(text="Mahasiswa tidak ditemukan!")
            messagebox.showwarning("Peringatan", "NIM tidak terdaftar!")
    
    def tambah_nilai(self):
        """Tambah data nilai"""
        nim = self.nilai_nim_entry.get().strip()
        kode_mk = self.nilai_kode_entry.get().strip()
        tugas = self.nilai_tugas_entry.get().strip()
        uts = self.nilai_uts_entry.get().strip()
        uas = self.nilai_uas_entry.get().strip()
        
        if not all([nim, kode_mk, tugas, uts, uas]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        # Validasi mahasiswa
        if not Mahasiswa.is_nim_exists(nim):
            messagebox.showerror("Error", "NIM tidak terdaftar!")
            return
        
        # Validasi mata kuliah
        if not MataKuliah.is_kode_exists(kode_mk):
            messagebox.showerror("Error", "Kode MK tidak terdaftar!")
            return
        
        # Validasi nilai sudah ada
        if Nilai.is_nilai_exists(nim, kode_mk):
            messagebox.showerror("Error", "Nilai untuk mahasiswa dan mata kuliah ini sudah ada!\nGunakan tombol Update untuk mengubah.")
            return
        
        try:
            tugas = float(tugas)
            uts = float(uts)
            uas = float(uas)
            
            if not all(0 <= x <= 100 for x in [tugas, uts, uas]):
                messagebox.showerror("Error", "Nilai harus antara 0-100!")
                return
        except ValueError:
            messagebox.showerror("Error", "Nilai harus berupa angka!")
            return
        
        nilai = Nilai(nim, kode_mk, tugas, uts, uas)
        if nilai.tambah():
            messagebox.showinfo("Sukses", f"Data nilai berhasil ditambahkan!\n"
                                         f"Nilai Akhir: {nilai.nilai_akhir}\n"
                                         f"Grade: {nilai.grade}\n"
                                         f"Status: {nilai.status}")
            self.clear_form_nilai()
            self.load_nilai()
        else:
            messagebox.showerror("Error", "Gagal menambahkan data nilai!")
    
    def update_nilai(self):
        """Update data nilai"""
        nim = self.nilai_nim_entry.get().strip()
        kode_mk = self.nilai_kode_entry.get().strip()
        tugas = self.nilai_tugas_entry.get().strip()
        uts = self.nilai_uts_entry.get().strip()
        uas = self.nilai_uas_entry.get().strip()
        
        if not all([nim, kode_mk, tugas, uts, uas]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        
        if not Nilai.is_nilai_exists(nim, kode_mk):
            messagebox.showerror("Error", "Data nilai tidak ditemukan!")
            return
        
        try:
            tugas = float(tugas)
            uts = float(uts)
            uas = float(uas)
            
            if not all(0 <= x <= 100 for x in [tugas, uts, uas]):
                messagebox.showerror("Error", "Nilai harus antara 0-100!")
                return
        except ValueError:
            messagebox.showerror("Error", "Nilai harus berupa angka!")
            return
        
        nilai = Nilai(nim, kode_mk, tugas, uts, uas)
        if nilai.update():
            messagebox.showinfo("Sukses", f"Data nilai berhasil diupdate!\n"
                                         f"Nilai Akhir: {nilai.nilai_akhir}\n"
                                         f"Grade: {nilai.grade}\n"
                                         f"Status: {nilai.status}")
            self.clear_form_nilai()
            self.load_nilai()
        else:
            messagebox.showerror("Error", "Gagal mengupdate data nilai!")
    
    def hapus_nilai(self):
        """Hapus data nilai"""
        selected = self.nilai_tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")
            return
        
        item = self.nilai_tree.item(selected[0])
        nim = item['values'][0]
        kode_mk = item['values'][2]
        
        confirm = messagebox.askyesno("Konfirmasi", 
                                       f"Hapus nilai {nim} - {kode_mk}?")
        
        if confirm:
            if Nilai.hapus(nim, kode_mk):
                messagebox.showinfo("Sukses", "Data nilai berhasil dihapus!")
                self.clear_form_nilai()
                self.load_nilai()
            else:
                messagebox.showerror("Error", "Gagal menghapus data nilai!")
    
    def filter_nilai(self):
        """Filter nilai berdasarkan NIM"""
        nim = self.nilai_search_entry.get().strip()
        
        if not nim:
            self.load_nilai()
            return
        
        # Clear tree
        for item in self.nilai_tree.get_children():
            self.nilai_tree.delete(item)
        
        # Load filtered data
        data = Nilai.get_by_nim(nim)
        if data:
            for row in data:
                self.nilai_tree.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Info", "Data tidak ditemukan!")
    
    def select_nilai(self, event):
        """Pilih data nilai dari treeview"""
        selected = self.nilai_tree.selection()
        if selected:
            item = self.nilai_tree.item(selected[0])
            values = item['values']
            
            self.nilai_nim_entry.delete(0, 'end')
            self.nilai_nim_entry.insert(0, values[0])
            
            self.nilai_nama_label.config(text=values[1])
            
            self.nilai_kode_entry.delete(0, 'end')
            self.nilai_kode_entry.insert(0, values[2])
            
            self.nilai_nama_mk_label.config(text=values[3])
            
            self.nilai_tugas_entry.delete(0, 'end')
            self.nilai_tugas_entry.insert(0, values[4])
            
            self.nilai_uts_entry.delete(0, 'end')
            self.nilai_uts_entry.insert(0, values[5])
            
            self.nilai_uas_entry.delete(0, 'end')
            self.nilai_uas_entry.insert(0, values[6])
    
    def clear_form_nilai(self):
        """Clear form nilai"""
        self.nilai_nim_entry.delete(0, 'end')
        self.nilai_kode_entry.delete(0, 'end')
        self.nilai_tugas_entry.delete(0, 'end')
        self.nilai_uts_entry.delete(0, 'end')
        self.nilai_uas_entry.delete(0, 'end')
        self.nilai_nama_label.config(text="-")
        self.nilai_nama_mk_label.config(text="-")
        self.nilai_search_entry.delete(0, 'end')
    
    def load_nilai(self):
        """Load semua data nilai ke treeview"""
        # Clear tree
        for item in self.nilai_tree.get_children():
            self.nilai_tree.delete(item)
        
        # Load data
        data = Nilai.get_all()
        for row in data:
            self.nilai_tree.insert('', 'end', values=row)
    
    # ==================== LAPORAN METHODS ====================
    
    def tampilkan_laporan(self):
        """Tampilkan laporan mahasiswa"""
        nim = self.laporan_nim_entry.get().strip()
        
        if not nim:
            messagebox.showwarning("Peringatan", "Masukkan NIM terlebih dahulu!")
            return
        
        laporan = Laporan.cetak_laporan_mahasiswa(nim)
        
        if laporan:
            self.laporan_text.delete('1.0', 'end')
            self.laporan_text.insert('1.0', laporan)
        else:
            messagebox.showerror("Error", "Mahasiswa tidak ditemukan!")
    
    def simpan_laporan(self):
        """Simpan laporan mahasiswa ke file"""
        nim = self.laporan_nim_entry.get().strip()
        
        if not nim:
            messagebox.showwarning("Peringatan", "Masukkan NIM terlebih dahulu!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"laporan_{nim}.txt"
        )
        
        if filename:
            if Laporan.simpan_laporan(nim, filename):
                messagebox.showinfo("Sukses", f"Laporan berhasil disimpan ke:\n{filename}")
            else:
                messagebox.showerror("Error", "Gagal menyimpan laporan!")
    
    def tampilkan_laporan_semua(self):
        """Tampilkan laporan semua mahasiswa"""
        laporan = Laporan.cetak_laporan_semua()
        self.laporan_text.delete('1.0', 'end')
        self.laporan_text.insert('1.0', laporan)
    
    def simpan_laporan_semua(self):
        """Simpan laporan semua mahasiswa ke file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="laporan_semua_mahasiswa.txt"
        )
        
        if filename:
            if Laporan.simpan_laporan_semua(filename):
                messagebox.showinfo("Sukses", f"Laporan berhasil disimpan ke:\n{filename}")
            else:
                messagebox.showerror("Error", "Gagal menyimpan laporan!")


def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    root = tk.Tk()
    app = AplikasiManajemenNilai(root)
    root.mainloop()


if __name__ == "__main__":
    main()