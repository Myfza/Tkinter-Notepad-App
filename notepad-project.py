# Import semua modul yang dibutuhkan
import re
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from tkinter  import messagebox
from tkinter import filedialog,simpledialog
from tkinter.scrolledtext import ScrolledText

# Membuat jendela utama aplikasi
root = Tk()
root.title('Notepad Sederhana - by Muhammad Yusuf Aditiya')
root.resizable(0, 0)  # Tidak bisa diubah ukurannya

# Menambahkan area teks dengan scrollbar otomatis
notepad = ScrolledText(root, width=90, height=40)
file = None  # Untuk menyimpan path file saat ini


# ======== FUNGSI FILE =========

# Membuat dokumen baru
def cmdNew():
    global file
    if len(notepad.get('1.0', END + '-1c')) > 0:
        if messagebox.askyesno("Simpan", "Apakah kamu ingin menyimpan file?"):
            cmdSave()
        else:
            notepad.delete('1.0', END)
    root.title("Notepad Sederhana")
    file = None

# Membuka file dari komputer
def cmdOpen():
    global file
    file = filedialog.askopenfilename(defaultextension=".txt",
                                       filetypes=[("All Files", "*.*"),
                                                  ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title("Notepad - " + file)
        notepad.delete('1.0', END)
        f = open(file, "r")
        notepad.insert('1.0', f.read())
        f.close()

# Menyimpan dokumen
def cmdSave():
    global file
    if file is None:
        cmdSaveAs()
    else:
        f = open(file, "w")
        f.write(notepad.get('1.0', END))
        f.close()

# Menyimpan sebagai file baru
def cmdSaveAs():
    f = filedialog.asksaveasfilename(initialfile='Untitled.txt',
                                     defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"),
                                                ("Text Documents", "*.txt")])
    if f is None:
        return
    else:
        global file
        file = f
        f = open(f, "w")
        f.write(notepad.get('1.0', END))
        f.close()
        root.title("Notepad - " + str(file))

# Keluar dari aplikasi
def cmdExit():
    if messagebox.askyesno("Keluar", "Apakah kamu yakin ingin keluar?"):
        root.destroy()


# ======== FUNGSI EDIT =========

# Potong teks
def cmdCut():
    notepad.event_generate("<<Cut>>")

# Salin teks
def cmdCopy():
    notepad.event_generate("<<Copy>>")

# Tempel teks
def cmdPaste():
    notepad.event_generate("<<Paste>>")

# Hapus seluruh isi teks
def cmdClear():
    notepad.delete('1.0', END)

# Cari dan sorot teks
def cmdFind():
    notepad.tag_remove('found', '1.0', END)
    find = simpledialog.askstring("Cari", "Masukkan teks yang ingin dicari:")
    if find:
        idx = '1.0'
        while 1:
            idx = notepad.search(find, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(find))
            notepad.tag_add('found', idx, lastidx)
            idx = lastidx
        notepad.tag_config('found', foreground='blue', background='yellow')

# Pilih semua teks
def cmdSelectAll():
    notepad.tag_add('sel', '1.0', 'end')

# Tampilkan waktu dan tanggal
def cmdTimeDate():
    now = datetime.now()
    notepad.insert(INSERT, now.strftime("%H:%M %d-%m-%Y"))

# Tentang pembuat aplikasi
def cmdAbout():
    messagebox.showinfo("Tentang", "Notepad Sederhana\nby Muhammad Yusuf Aditiya")


# Klik area teks, hapus highlight pencarian
def click(event):
    notepad.tag_config('found', foreground='black', background='white')


# ======== MENU BAR =========

# Menu File
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Baru", command=cmdNew)
filemenu.add_command(label="Buka", command=cmdOpen)
filemenu.add_command(label="Simpan", command=cmdSave)
filemenu.add_command(label="Simpan Sebagai", command=cmdSaveAs)
filemenu.add_separator()
filemenu.add_command(label="Keluar", command=cmdExit)
menubar.add_cascade(label="File", menu=filemenu)

# Menu Edit
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Potong", command=cmdCut)
editmenu.add_command(label="Salin", command=cmdCopy)
editmenu.add_command(label="Tempel", command=cmdPaste)
editmenu.add_command(label="Hapus", command=cmdClear)
editmenu.add_separator()
editmenu.add_command(label="Cari", command=cmdFind)
editmenu.add_command(label="Pilih Semua", command=cmdSelectAll)
editmenu.add_command(label="Waktu/Tanggal", command=cmdTimeDate)
menubar.add_cascade(label="Edit", menu=editmenu)

# Menu Bantuan
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Tentang Notepad", command=cmdAbout)
menubar.add_cascade(label="Bantuan", menu=helpmenu)

# Menambahkan menu ke root window
root.config(menu=menubar)

# Menampilkan teks editor
notepad.pack()
notepad.bind("<Button-1>", click)

# Menjalankan aplikasi
root.mainloop()
