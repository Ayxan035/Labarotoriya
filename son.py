import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

BG_COLOR = "#2E2E2E"
FG_COLOR = "#FFFFFF"
BUTTON_BG = "#4CAF50"
BUTTON_FG = "#FFFFFF"
DELETE_BUTTON_BG = "#FF5555"
ENTRY_BG = "#505050"
ENTRY_FG = "#FFFFFF"

USERNAME = "ayxan@gmail.com"
PASSWORD = "ayxan"


class WorkerManager:
    WORKERS_FILE = "isci_melumatlari.json"

    def __init__(self):
        self.workers = []
        self.load_workers()

    def load_workers(self):
        if os.path.exists(self.WORKERS_FILE):
            with open(self.WORKERS_FILE, "r") as file:
                try:
                    self.workers = json.load(file)
                except json.JSONDecodeError:
                    self.workers = []
        else:
            self.workers = []

    def save_workers(self):
        with open(self.WORKERS_FILE, "w") as file:
            json.dump(self.workers, file, indent=4)

    def add_worker(self, worker):
        self.workers.append(worker)
        self.save_workers()

    def delete_worker(self, worker):
        self.workers.remove(worker)
        self.save_workers()

    def update_worker(self, worker, updated_data):
        worker.update(updated_data)
        self.save_workers()


class UIManager:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.root.title("Isci Melumatlari Sistemi")
        self.root.geometry("500x400")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.show_login_page()

    def show_login_page(self):
        login_frame = tk.Frame(self.root, bg=BG_COLOR)
        login_frame.pack(expand=True, fill="both")

        tk.Label(login_frame, text="Isci Melumatlari Sistemi", font=("Arial", 16, "bold"), bg=BG_COLOR,
                 fg=FG_COLOR).pack(pady=20)

        username_entry = self.create_label_entry(login_frame, "Istifadeci Adi:")
        password_entry = self.create_label_entry(login_frame, "Sifra:")
        password_entry.config(show="*")

        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username == USERNAME and password == PASSWORD:
                login_frame.destroy()
                self.show_main_page()
            else:
                messagebox.showerror("Xeta", "Istifadeci adi ve ya sifre sehvdird!")

        login_button = tk.Button(login_frame, text="Daxil Ol", command=attempt_login, font=("Arial", 12), bg=BUTTON_BG,
                                 fg=BUTTON_FG)
        login_button.pack(pady=10)

    def show_main_page(self):
        button_font = ("Arial", 12)
        add_button = tk.Button(self.root, text="Yeni Isci Elave Et", command=self.add_worker_window, font=button_font,
                               bg=BUTTON_BG, fg=BUTTON_FG)
        add_button.pack(pady=10)

        list_button = tk.Button(self.root, text="Butun Iscileri Goster", command=self.list_workers_window,
                                font=button_font, bg=BUTTON_BG, fg=BUTTON_FG)
        list_button.pack(pady=10)

    def create_label_entry(self, parent, text, initial_value=""):
        label = tk.Label(parent, text=text, font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
        label.pack(pady=5, anchor="w")
        entry = tk.Entry(parent, font=("Arial", 12), bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=FG_COLOR)
        entry.insert(0, initial_value)
        entry.pack(pady=5, fill="x")
        return entry

    def add_worker_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Yeni Isci Elave Et")
        add_window.geometry("450x600")
        add_window.configure(bg=BG_COLOR)

        name_entry = self.create_label_entry(add_window, "Ad:")
        surname_entry = self.create_label_entry(add_window, "Soyad:")
        father_name_entry = self.create_label_entry(add_window, "Ata Adi:")



        gender_label = tk.Label(add_window, text="Cinsiyyet:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
        gender_label.pack(pady=5, anchor="w")

        gender_var = tk.StringVar(value="Kisi")

        gender_frame = tk.Frame(add_window, bg=BG_COLOR)
        gender_frame.pack(pady=5, fill="x")

        male_rb = tk.Radiobutton(gender_frame, text="Kisi", variable=gender_var, value="Kisi", font=("Arial", 12),
                                 bg=BG_COLOR, fg=FG_COLOR)
        male_rb.pack(side="left", padx=10)

        female_rb = tk.Radiobutton(gender_frame, text="Qadin", variable=gender_var, value="Qadin", font=("Arial", 12),
                                   bg=BG_COLOR, fg=FG_COLOR)
        female_rb.pack(side="left", padx=10)

        position_combobox = self.create_combobox(add_window, "Vezife:",
                                                 ["Muellim", "Muhendis", "Menecer", "Hekim", "Mudur", "Kassir", "Polis",
                                                  "Ofisiant", "Ekspert", "Proqramist"])
        experience_combobox = self.create_combobox(add_window, "Is Tecrubesi:", ["1 Ilden Az", "1-3 Il", "3 Ilden Cox"])
        city_combobox = self.create_combobox(add_window, "Seherler:",
                                             ["Baki", "Gence", "Sumqayit", "Mingecevir", "Lacin", "Semkir", "Qazax",
                                              "Kurdemir", "Dashkesen", "Shusha", "Kelbecer", "Zengilan"])
        address_entry = self.create_label_entry(add_window, "Unvan:")

        def save_worker():
            name = name_entry.get().strip()
            surname = surname_entry.get().strip()
            father_name = father_name_entry.get().strip()

            if len(name) < 3 or len(surname) < 3 or len(father_name) < 3:
                messagebox.showerror("Xeta", "Ad, Soyad ve Ata Adi minimum 3 herfden ibaret olmalidir!")
                return

            worker = {
                "name": name,
                "surname": surname,
                "father_name": father_name,
                "position": position_combobox.get().strip(),
                "workExperience": experience_combobox.get().strip(),
                "city": city_combobox.get().strip(),
                "address": address_entry.get().strip(),
                "gender": gender_var.get(),
            }
            self.manager.add_worker(worker)
            messagebox.showinfo("Ugur", "Yeni isci elave olundu!")
            add_window.destroy()

        save_button = tk.Button(add_window, text="Saxla", command=save_worker, font=("Arial", 12), bg=BUTTON_BG,
                                fg=BUTTON_FG)
        save_button.pack(pady=20)

    def create_combobox(self, parent, text, values):
        label = tk.Label(parent, text=text, font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
        label.pack(pady=5, anchor="w")
        combobox = ttk.Combobox(parent, values=values, font=("Arial", 12), state="readonly")
        combobox.pack(pady=5, fill="x")
        return combobox

    def list_workers_window(self):
        list_window = tk.Toplevel(self.root)
        list_window.title("Butun Isciler")
        list_window.geometry("500x400")
        list_window.configure(bg=BG_COLOR)

        worker_listbox = tk.Listbox(list_window, font=("Arial", 12), bg=ENTRY_BG, fg=ENTRY_FG, width=50, height=15,
                                    selectbackground="#606060")
        worker_listbox.pack(pady=10, padx=10)

        if not self.manager.workers:
            messagebox.showinfo("Melumat", "Hech bir isci movcud deyil!")
            return

        for worker in self.manager.workers:
            worker_listbox.insert(tk.END, f"{worker['name']} {worker['surname']} - {worker['position']}")

        def show_worker_details(event):
            selected_index = worker_listbox.curselection()
            if selected_index:
                selected_worker = self.manager.workers[selected_index[0]]
                self.show_worker_details_window(selected_worker)

        worker_listbox.bind("<Double-Button-1>", show_worker_details)

    def show_worker_details_window(self, worker):
        details_window = tk.Toplevel(self.root)
        details_window.title("Isci Melumatlari")
        details_window.geometry("400x500")
        details_window.configure(bg=BG_COLOR)

        info = (
            f"Ad: {worker['name']}\n"
            f"Soyad: {worker['surname']}\n"
            f"Ata Adi: {worker['father_name']}\n"
            f"Vezife: {worker['position']}\n"
            f"Is Tecrubesi: {worker['workExperience']}\n"
            f"Seher: {worker['city']}\n"
            f"Unvan: {worker['address']}\n"
            f"Cinsiyyet: {worker['gender']}\n"
        )
        tk.Label(details_window, text="Isci Haqqinda Melumat", font=("Arial", 14, "bold"), bg=BG_COLOR,
                 fg=FG_COLOR).pack(pady=10)
        tk.Label(details_window, text=info, font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR, justify="left").pack(pady=10)

        edit_button = tk.Button(details_window, text="Redakte Et", command=lambda: self.edit_worker_window(worker),
                                font=("Arial", 12), bg=BUTTON_BG, fg=BUTTON_FG)
        edit_button.pack(pady=10)

        delete_button = tk.Button(details_window, text="Sil",
                                  command=lambda: self.delete_worker(worker, details_window), font=("Arial", 12),
                                  bg=DELETE_BUTTON_BG, fg=BUTTON_FG)
        delete_button.pack(pady=10)

    def edit_worker_window(self, worker):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Redakte Et")
        edit_window.geometry("450x400")
        edit_window.configure(bg=BG_COLOR)

        position_combobox = self.create_combobox(edit_window, "Vezife:",
                                                 ["Muellim", "Muhendis", "Menecer", "Hekim", "Mudur", "Kassir", "Polis",
                                                  "Ofisiant", "Ekspert", "Proqramist"])
        position_combobox.set(worker["position"])

        experience_combobox = self.create_combobox(edit_window, "Is Tecrubesi:",
                                                   ["1 Il", "2-4 Il", "4 Ilden Cox"])
        experience_combobox.set(worker["workExperience"])

        city_combobox = self.create_combobox(edit_window, "Seherler:",
                                             ["Baki", "Gence", "Sumqayit", "Mingecevir", "Lacin", "Semkir", "Qazax",
                                              "Kurdemir", "Daskesen", "Susa", "Kelbecer", "Zengilan"])
        city_combobox.set(worker["city"])

        address_entry = self.create_label_entry(edit_window, "Unvan:", worker["address"])

        gender_var = tk.StringVar(value=worker["gender"])

        gender_frame = tk.Frame(edit_window, bg=BG_COLOR)
        gender_frame.pack(pady=5, fill="x")

        male_rb = tk.Radiobutton(gender_frame, text="Kisi", variable=gender_var, value="Kisi", font=("Arial", 12),
                                 bg=BG_COLOR, fg=FG_COLOR)
        male_rb.pack(side="left", padx=10)

        female_rb = tk.Radiobutton(gender_frame, text="Qadin", variable=gender_var, value="Qadin", font=("Arial", 12),
                                   bg=BG_COLOR, fg=FG_COLOR)
        female_rb.pack(side="left", padx=10)

        def save_edits():
            updated_data = {
                "position": position_combobox.get().strip(),
                "workExperience": experience_combobox.get().strip(),
                "city": city_combobox.get().strip(),
                "address": address_entry.get().strip(),
                "gender": gender_var.get(),
            }
            if updated_data != worker:
                self.manager.update_worker(worker, updated_data)
                messagebox.showinfo("Ugur", "Isci melumatlari yenilendi!")
                edit_window.destroy()
            else:
                messagebox.showinfo("Melumat", "Hech bir deyisiklik edilmedi!")

        save_button = tk.Button(edit_window, text="Deyisikleri Saxla", command=save_edits, font=("Arial", 12),
                                bg=BUTTON_BG, fg=BUTTON_FG)
        save_button.pack(pady=20)

    def delete_worker(self, worker, window):
        self.manager.delete_worker(worker)
        messagebox.showinfo("Ugur", "Isci silindi!")
        window.destroy()


if __name__ == "__main__":
    manager = WorkerManager()
    root = tk.Tk()
    app = UIManager(root, manager)
    root.mainloop()
