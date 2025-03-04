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

        self.root.title("İşçi Məlumatları Sistemi")
        self.root.geometry("500x400")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.show_login_page()

    def show_login_page(self):
        login_frame = tk.Frame(self.root, bg=BG_COLOR)
        login_frame.pack(expand=True, fill="both")

        tk.Label(login_frame, text="İşçi Məlumatları Sistemi", font=("Arial", 16, "bold"), bg=BG_COLOR,
                 fg=FG_COLOR).pack(pady=20)

        username_entry = self.create_label_entry(login_frame, "İstifadəçi Adı:")
        password_entry = self.create_label_entry(login_frame, "Şifrə:")
        password_entry.config(show="*")

        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if username == USERNAME and password == PASSWORD:
                login_frame.destroy()
                self.show_main_page()
            else:
                messagebox.showerror("Xəta", "İstifadəçi adı və ya şifrə səhvdir!")

        login_button = tk.Button(login_frame, text="Daxil Ol", command=attempt_login, font=("Arial", 12), bg=BUTTON_BG,
                                 fg=BUTTON_FG)
        login_button.pack(pady=10)

    def show_main_page(self):
        button_font = ("Arial", 12)
        add_button = tk.Button(self.root, text="Yeni İşçi Əlavə Et", command=self.add_worker_window, font=button_font,
                               bg=BUTTON_BG, fg=BUTTON_FG)
        add_button.pack(pady=10)

        list_button = tk.Button(self.root, text="Bütün İşçiləri Göstər", command=self.list_workers_window,
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
        add_window.title("Yeni İşçi Əlavə Et")
        add_window.geometry("450x600")
        add_window.configure(bg=BG_COLOR)

        name_entry = self.create_label_entry(add_window, "Ad:")
        surname_entry = self.create_label_entry(add_window, "Soyad:")
        father_name_entry = self.create_label_entry(add_window, "Ata Adı:")

        # Cinsiyyət seçimi üçün RadioButtonlar
        gender_label = tk.Label(add_window, text="Cinsiyyət:", font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR)
        gender_label.pack(pady=5, anchor="w")

        gender_var = tk.StringVar(value="Erkək")  # Default olaraq "Erkək" seçili

        gender_frame = tk.Frame(add_window, bg=BG_COLOR)
        gender_frame.pack(pady=5, fill="x")  # Bu Frame-dən istifadə edirik ki, RadioButton-ları yan-yana yerləşdirək.

        male_rb = tk.Radiobutton(gender_frame, text="Erkək", variable=gender_var, value="Erkək", font=("Arial", 12),
                                 bg=BG_COLOR, fg=FG_COLOR)
        male_rb.pack(side="left", padx=10)  # RadioButtonları soldan sağa yerləşdiririk.

        female_rb = tk.Radiobutton(gender_frame, text="Qadın", variable=gender_var, value="Qadın", font=("Arial", 12),
                                   bg=BG_COLOR, fg=FG_COLOR)
        female_rb.pack(side="left", padx=10)

        position_combobox = self.create_combobox(add_window, "Vəzifə:",
                                                 ["Müəllim", "Mühəndis", "Mənəcer", "Həkim", "Müdür", "Kassir", "Polis",
                                                  "Ofisiant", "Ekspert", "Proqramist"])
        experience_combobox = self.create_combobox(add_window, "İş Təcrübəsi:", ["1 Ildən Az", "1-3 İl", "3 Ildən Çox"])
        city_combobox = self.create_combobox(add_window, "Şəhərlər:",
                                             ["Bakı", "Gəncə", "Sumqayıt", "Mingəçevir", "Laçın", "Şəmkir", "Qazax",
                                              "Kürdəmir", "Daşkəsən", "Şuşa", "Kəlbəcər", "Zəngilan"])
        address_entry = self.create_label_entry(add_window, "Ünvan:")

        def save_worker():
            name = name_entry.get().strip()
            surname = surname_entry.get().strip()
            father_name = father_name_entry.get().strip()

            if len(name) < 3 or len(surname) < 3 or len(father_name) < 3:
                messagebox.showerror("Xəta", "Ad, Soyad və Ata Adı minimum 3 hərfdən ibarət olmalıdır!")
                return

            worker = {
                "name": name,
                "surname": surname,
                "father_name": father_name,
                "position": position_combobox.get().strip(),
                "workExperience": experience_combobox.get().strip(),
                "city": city_combobox.get().strip(),
                "address": address_entry.get().strip(),
                "gender": gender_var.get(),  # Cinsiyyət məlumatını alır
            }
            self.manager.add_worker(worker)
            messagebox.showinfo("Uğur", "Yeni işçi əlavə olundu!")
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
        list_window.title("Bütün İşçilər")
        list_window.geometry("500x400")
        list_window.configure(bg=BG_COLOR)

        worker_listbox = tk.Listbox(list_window, font=("Arial", 12), bg=ENTRY_BG, fg=ENTRY_FG, width=50, height=15,
                                    selectbackground="#606060")
        worker_listbox.pack(pady=10, padx=10)

        if not self.manager.workers:
            messagebox.showinfo("Məlumat", "Heç bir işçi mövcud deyil!")
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
        details_window.title("İşçi Məlumatları")
        details_window.geometry("400x500")
        details_window.configure(bg=BG_COLOR)

        info = (
            f"Ad: {worker['name']}\n"
            f"Soyad: {worker['surname']}\n"
            f"Ata Adı: {worker['father_name']}\n"
            f"Vəzifə: {worker['position']}\n"
            f"İş Təcrübəsi: {worker['workExperience']}\n"
            f"Şəhər: {worker['city']}\n"
            f"Ünvan: {worker['address']}\n"
            f"Cinsiyyət: {worker['gender']}\n"
        )
        tk.Label(details_window, text="İşçi Haqqında Məlumat", font=("Arial", 14, "bold"), bg=BG_COLOR,
                 fg=FG_COLOR).pack(pady=10)
        tk.Label(details_window, text=info, font=("Arial", 12), bg=BG_COLOR, fg=FG_COLOR, justify="left").pack(pady=10)

        edit_button = tk.Button(details_window, text="Redaktə Et", command=lambda: self.edit_worker_window(worker),
                                font=("Arial", 12), bg=BUTTON_BG, fg=BUTTON_FG)
        edit_button.pack(pady=10)

        delete_button = tk.Button(details_window, text="Sil",
                                  command=lambda: self.delete_worker(worker, details_window), font=("Arial", 12),
                                  bg=DELETE_BUTTON_BG, fg=BUTTON_FG)
        delete_button.pack(pady=10)

    def edit_worker_window(self, worker):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Redaktə Et")
        edit_window.geometry("450x400")
        edit_window.configure(bg=BG_COLOR)

        position_combobox = self.create_combobox(edit_window, "Vəzifə:",
                                                 ["Müəllim", "Mühəndis", "Mənəcer", "Həkim", "Müdür", "Kassir", "Polis",
                                                  "Ofisiant", "Ekspert", "Proqramist"])
        position_combobox.set(worker["position"])

        experience_combobox = self.create_combobox(edit_window, "İş Təcrübəsi:",
                                                   ["1 Ildən Az", "1-3 İl", "3 Ildən Çox"])
        experience_combobox.set(worker["workExperience"])

        city_combobox = self.create_combobox(edit_window, "Şəhərlər:",
                                             ["Bakı", "Gəncə", "Sumqayıt", "Mingəçevir", "Laçın", "Şəmkir", "Qazax",
                                              "Kürdəmir", "Daşkəsən", "Şuşa", "Kəlbəcər", "Zəngilan"])
        city_combobox.set(worker["city"])

        address_entry = self.create_label_entry(edit_window, "Ünvan:", worker["address"])

        gender_var = tk.StringVar(value=worker["gender"])

        gender_frame = tk.Frame(edit_window, bg=BG_COLOR)
        gender_frame.pack(pady=5, fill="x")

        male_rb = tk.Radiobutton(gender_frame, text="Erkək", variable=gender_var, value="Erkək", font=("Arial", 12),
                                 bg=BG_COLOR, fg=FG_COLOR)
        male_rb.pack(side="left", padx=10)

        female_rb = tk.Radiobutton(gender_frame, text="Qadın", variable=gender_var, value="Qadın", font=("Arial", 12),
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
                messagebox.showinfo("Uğur", "İşçi məlumatları yeniləndi!")
                edit_window.destroy()
            else:
                messagebox.showinfo("Məlumat", "Heç bir dəyişiklik edilmədi!")

        save_button = tk.Button(edit_window, text="Dəyişiklikləri Saxla", command=save_edits, font=("Arial", 12),
                                bg=BUTTON_BG, fg=BUTTON_FG)
        save_button.pack(pady=20)

    def delete_worker(self, worker, window):
        self.manager.delete_worker(worker)
        messagebox.showinfo("Uğur", "İşçi silindi!")
        window.destroy()


if __name__ == "__main__":
    manager = WorkerManager()
    root = tk.Tk()
    app = UIManager(root, manager)
    root.mainloop()
