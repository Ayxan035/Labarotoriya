import tkinter as tk
from tkinter import ttk, messagebox
import json  # JSON fayl emeliyyatadari ucun json daxil edirik

class ManageWorkers:  # Ishcileri idarə eden bir sinif
    def __init__(self, data_file="workers.json"):  # Sinifin konstruktoru, fayl adi parametri ile ishcileri yukleyirik
        self.data_file = data_file  # Ishchilerin saxlanacagi JSON faylinin adi
        self.all_workers = self.load_workers()  # Ishchileri yukleyiirk

    def load_workers(self):  # Ishcileri JSON faylindan yuklemek uchun metod
        try:
            with open(self.data_file, "r") as file:  # Fayli oxumag ucun acirig
                return json.load(file)  # JSON formatinda ishcileri oxuyuruq
        except (FileNotFoundError, json.JSONDecodeError):  # Fayl tapilmadigda ya da JSON duzgun formatda olmadiqda bosh siyahı qaytaririg
            return []

    def save_workers(self):  # Ishcileri JSON faylina saxlamaq üçün metod
        with open(self.data_file, "w") as file:  # Fayli yazmaq uchun achirig
            json.dump(self.all_workers, file, indent=4)  # Ishchileri fayla JSON formatinda yazirig, indentin menasi-4 boshlugla formatlanir
    def add_worker(self, worker):
        self.all_workers.append(worker)
        self.save_workers()

    def delete_worker(self, name, surname):
        self.all_workers = [worker for worker in self.all_workers if not (worker["Ad"] == name and worker["Soyad"] == surname)]  # Siyahini filterleyirik
        self.save_workers()

    def edit_worker(self, name, surname, updated_fields):
        for worker in self.all_workers:
            if worker["Ad"] == name and worker["Soyad"] == surname:
                worker.update(updated_fields)
                self.save_workers()
                return True  # Ishci tapilir ve yenilenir
        return False  # Ishchi tapilmasa false verir

manager = ManageWorkers()  # Ishcileri idare etmek uchun yaradirig

def create_login_window():
    def validate_login():
        email = email_entry.get()
        parol = password_entry.get()

        if email == "admin@gmail.com" and parol == "admin":
            login_window.destroy()
            create_main_window()
        else:
            messagebox.showerror("Ugursuz", "Email ve ya parol sehvdi")

    login_window = tk.Tk()  # Yeni pəncərəni yaradirig
    login_window.title("Login Page")
    login_window.geometry("400x300")
    login_window.configure(bg="lightgrey")


    # Email uchun etiket ve girish sahesi
    tk.Label(login_window, text="Email:", fg="black", bg="lightgrey").place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.05)
    email_entry = tk.Entry(login_window, bg="white", fg="black", insertbackground="black")
    email_entry.place(relx=0.3, rely=0.4, relwidth=0.6, relheight=0.05)

    # Shifre uchun etiket ve girish sahesi
    tk.Label(login_window, text="Password:", fg="black", bg="lightgrey").place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.05)
    password_entry = tk.Entry(login_window, bg="white", fg="black", insertbackground="black", show="*")
    password_entry.place(relx=0.3, rely=0.55, relwidth=0.6, relheight=0.05)

    # Girish duymesi
    tk.Button(login_window, text="Login", bg="green", fg="white", command=validate_login).place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.07)

    login_window.mainloop()  # Tkinter i basdadmag

def create_add_worker_window():
    def save_worker():
        name = name_entry.get()
        surname = surname_entry.get()
        father_name = father_name_entry.get()
        day = day_combo.get()
        month = month_combo.get()
        year = year_combo.get()
        gender = gender_var.get()
        position = position_combo.get()
        experience = experience_combo.get()
        city = city_combo.get()
        address = address_entry.get()

        if not (name and surname and day != "Gun" and month != "Ay" and year != "Il" and position != "Vezife" and city != "Sheher"):  # Əgər lazimli olan yerler boshdussa
            messagebox.showerror("Xeta", "Butun teleb olunan saheleri doldur")  # Xeta gosteririk
            return

        worker = {  # Yeni ishchi melumatini dictionary sheklinde hazirlayirig
            "Ad": name,
            "Soyad": surname,
            "Ata Adi": father_name,
            "Dogum tarixi": f"{day} {month} {year}",
            "Cinsiyet": gender,
            "Secilen vezife": position,
            "Ish tecrubesi": experience,
            "Seher": city,
            "Unvan": address
        }

        manager.add_worker(worker) # Yeni ishcini add eliyiriy
        messagebox.showinfo("Ugur", f"{name} {surname} ugurla qeyd olundu")

        # Formu temizdiyiriy
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        father_name_entry.delete(0, tk.END)
        day_combo.set("Gun")
        month_combo.set("Ay")
        year_combo.set("Il")
        gender_var.set("Kishi")
        position_combo.set("Vezife")
        experience_combo.set("Ish tecrubesi")
        city_combo.set("Sheher")
        address_entry.delete(0, tk.END)

    add_worker_window = tk.Toplevel()  # Teze pencere yaradirig
    add_worker_window.title("Yeni Isci Elave Et")
    add_worker_window.geometry("400x500")

    # Form elementlerini-etiketler ve girish sahelerini elave edirik
    tk.Label(add_worker_window, text="Ad:").pack()
    name_entry = tk.Entry(add_worker_window)
    name_entry.pack()

    tk.Label(add_worker_window, text="Soyad:").pack()
    surname_entry = tk.Entry(add_worker_window)
    surname_entry.pack()

    tk.Label(add_worker_window, text="Ata Adi:").pack()
    father_name_entry = tk.Entry(add_worker_window)
    father_name_entry.pack()

    tk.Label(add_worker_window, text="Dogum Tarixi:").pack()
    day_combo = ttk.Combobox(add_worker_window, values=[str(i) for i in range(1, 32)], state="readonly")
    day_combo.pack()
    day_combo.set("Gun")

    month_combo = ttk.Combobox(add_worker_window, values=["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"], state="readonly")
    month_combo.pack()
    month_combo.set("Ay")

    year_combo = ttk.Combobox(add_worker_window, values=[str(i) for i in range(1950, 2007)], state="readonly")
    year_combo.pack()
    year_combo.set("Il")

    tk.Label(add_worker_window, text="Cinsiyet:").pack()
    gender_var = tk.StringVar()
    gender_combo = ttk.Combobox(add_worker_window, values=["Kishi", "Qadin"], textvariable=gender_var, state="readonly")
    gender_combo.pack()
    gender_combo.set("Kishi")

    tk.Label(add_worker_window, text="Vezife:").pack()
    position_combo = ttk.Combobox(add_worker_window, values=["Mudur", "Polis", "Hekim", "Kassir", "Ofissiant", "Muellim", "Muhendis", "Dizayner", "Proqramchi", "Ekspert"], state="readonly")
    position_combo.pack()
    position_combo.set("Vezife")

    tk.Label(add_worker_window, text="Is Tecrubesi:").pack()
    experience_combo = ttk.Combobox(add_worker_window, values=["1 ilden az", "1-3 il", "3< il"], state="readonly")
    experience_combo.pack()
    experience_combo.set("Is tecrubesi")

    tk.Label(add_worker_window, text="Sheher:").pack()
    city_combo = ttk.Combobox(add_worker_window, values=["Baki", "Gence", "Sumqayit", "Mingachevir", "Lacin", "Semkir", "Qazax", "Kurdemir", "Daskesen", "Shusha", "Kelbecer", "Zengilan"], state="readonly")
    city_combo.pack()
    city_combo.set("Sheher")

    tk.Label(add_worker_window, text="Unvan:").pack()
    address_entry = tk.Entry(add_worker_window)
    address_entry.pack()

    tk.Button(add_worker_window, text="Save", command=save_worker, bg="green", fg="white").pack()  # Yadda saxla duymesini elave edirik

def create_delete_worker_window():
    def delete_worker():
        name = name_entry.get()
        surname = surname_entry.get()

        if not name or not surname:  # Ad ya da soyad bosh olarsa
            messagebox.showerror("Xeta", "Ad ve Soyadi daxil et")  # Xets gosteririk
            return

        manager.delete_worker(name, surname)
        messagebox.showinfo("Ugur", f"{name} {surname} silindi")
        delete_worker_window.destroy()

    delete_worker_window = tk.Toplevel()
    delete_worker_window.title("Isci Sil")
    delete_worker_window.geometry("300x200")

    # Ad və soyad sahələrini əlavə edirik
    tk.Label(delete_worker_window, text="Ad:").pack()
    name_entry = tk.Entry(delete_worker_window)
    name_entry.pack()

    tk.Label(delete_worker_window, text="Soyad:").pack()
    surname_entry = tk.Entry(delete_worker_window)
    surname_entry.pack()

    tk.Button(delete_worker_window, text="Sil", command=delete_worker, bg="red", fg="white").pack()      # Sil duymesini elavemedirik

def create_edit_worker_window():
    def edit_worker():
        name = name_entry.get()
        surname = surname_entry.get()

        if not name or not surname:
            messagebox.showerror("Xeta", "Ad ve Soyadi daxil et")
            return

        updated_fields = {  # Duzelmeli olan melumatlari teyin eliyiriy
            "Secilen vezife": position_combo.get(),
            "Ish tecrubesi": experience_combo.get(),
            "Sheher": city_combo.get()
        }

        success = manager.edit_worker(name, surname, updated_fields)  # İshci melumatdarini yenileyirik
        if success:
            messagebox.showinfo("Ugur", f"{name} {surname} melumatlari yenilendi")
            edit_worker_window.destroy()
        else:
            messagebox.showerror("Xeta", "Isci tapilmadi")

    edit_worker_window = tk.Toplevel()
    edit_worker_window.title("Ishci Edit")
    edit_worker_window.geometry("400x300")


    tk.Label(edit_worker_window, text="Ad:").pack()
    name_entry = tk.Entry(edit_worker_window)
    name_entry.pack()

    tk.Label(edit_worker_window, text="Soyad:").pack()
    surname_entry = tk.Entry(edit_worker_window)
    surname_entry.pack()


    tk.Label(edit_worker_window, text="Vezife:").pack()
    position_combo = ttk.Combobox(edit_worker_window, values=["Mudur", "Polis", "Hekim", "Kassir", "Ofissiant", "Muellim", "Muhendis", "Dizayner", "Proqramchi", "Ekspert"], state="readonly")
    position_combo.pack()

    tk.Label(edit_worker_window, text="Ish Tecrubesi:").pack()
    experience_combo = ttk.Combobox(edit_worker_window, values=["1 ilden az", "1-3 il", "3< il"], state="readonly")
    experience_combo.pack()

    tk.Label(edit_worker_window, text="Sheher:").pack()
    city_combo = ttk.Combobox(edit_worker_window, values=["Baki", "Gence", "Sumqayit", "Mingachevir", "Lacin", "Semkir", "Qazax", "Kurdemir", "Daskesen", "Shusha", "Kelbecer", "Zengilan"], state="readonly")
    city_combo.pack()

    tk.Button(edit_worker_window, text="Yenile", command=edit_worker, bg="blue", fg="white").pack()

def show_all_workers():
    all_workers_window = tk.Toplevel()
    all_workers_window.title("Butun Iscilerin Siyahisi")
    all_workers_window.geometry("400x400")

    workers_text = tk.Text(all_workers_window, wrap=tk.WORD, bg="white", fg="black")  # Yazi sahesi yaradirig
    workers_text.pack(fill=tk.BOTH, expand=True)  # Yazi sahesini pencereye yerleshdiririy

    if manager.all_workers:  # Ishciler siyahisi bosh deyilse
        for i, worker in enumerate(manager.all_workers, start=1):  # Butun ishcileri isyahi olarag gosteririk
            workers_text.insert(tk.END, f"Isci {i}:\n")  # Ishci nomresini gosteririk
            for key, value in worker.items():  # Ishci melumatlarini gosteririk
                workers_text.insert(tk.END, f"  {key}: {value}\n")
            workers_text.insert(tk.END, "\n")
    else:
        workers_text.insert(tk.END, "Hec bir isci tapilmadi")
def create_main_window():
    main_window = tk.Tk()
    main_window.title("Ishci İdareetmesi")
    main_window.geometry("500x500")

    # Menu elementlerini elvave edirik
    tk.Button(main_window, text="Yeni Isci Elave Et", command=create_add_worker_window, bg="green", fg="white").pack(fill=tk.X)
    tk.Button(main_window, text="Iscini Sil", command=create_delete_worker_window, bg="red", fg="white").pack(fill=tk.X)
    tk.Button(main_window, text="Iscini Yenile", command=create_edit_worker_window, bg="blue", fg="white").pack(fill=tk.X)
    tk.Button(main_window, text="Butun Isciler", command=show_all_workers, bg="lightgrey", fg="black").pack(fill=tk.X)

    main_window.mainloop()  # Tkinteri basdatmag

create_login_window()  # Giriş penceresini basdatmag