import tkinter as tk
from tkinter import ttk, messagebox


def create_login_window():
    def validate_login():
        email = email_entry.get()
        parol = password_entry.get()

        if email == "AyxanNasibzada@gmail.com" and parol == "Ayxan0535":
            messagebox.showinfo("Ugurlu", "Ugurla daxil olundu")
            login_window.destroy()
            create_main_window()
        else:
            messagebox.showerror("Ugursuz", "Email ve ya parol sehvdi")

    login_window = tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("400x250")
    login_window.configure(bg="gold")

    tk.Label(login_window, text="Email:", fg="black", bg="silver", font=("Comic Sans MS", 10)).place(relx=0.1, rely=0.2,
                                                                                                  relwidth=0.2,
                                                                                                  relheight=0.05)
    email_entry = tk.Entry(login_window, bg="white", fg="black")
    email_entry.place(relx=0.3, rely=0.2, relwidth=0.6, relheight=0.05)

    tk.Label(login_window, text="Password:", fg="black", bg="silver", font=("Comic Sans MS", 10)).place(relx=0.1,
                                                                                                     rely=0.35,
                                                                                                     relwidth=0.2,
                                                                                                     relheight=0.05)
    password_entry = tk.Entry(login_window, bg="white", fg="black")
    password_entry.place(relx=0.3, rely=0.35, relwidth=0.6, relheight=0.05)

    tk.Button(login_window, text="Login", bg="blue", fg="white", command=validate_login).place(relx=0.35, rely=0.5,
                                                                                               relwidth=0.3,
                                                                                               relheight=0.07)

    login_window.mainloop()


def create_main_window():
    all_workers = []

    def clear_fields():
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        father_name_entry.delete(0, tk.END)
        day_combo.set("Gun")
        month_combo.set("Ay")
        year_combo.set("Il")
        gender_var.set("Kisi")
        position_combo.set("Vezife")
        experience_combo.set("Is tecrubesi")
        city_combo.set("Sheher")
        address_entry.delete(0, tk.END)
        about_text.delete("1.0", tk.END)

    def validate_name(name, surname):
        if len(name) < 3 or len(surname) < 3:
            messagebox.showerror("Xeta", "Ad ve Soyad en az 3 simvoldan ibaret olmalidir")
            return False
        return True

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
        about = about_text.get("1.0", tk.END).strip()

        if not (
                name and surname and day != "Gun" and month != "Ay" and year != "Il" and position != "Vezife" and city != "Sheher"):
            messagebox.showerror("Xeta", "Butun teleb olunan saheleri doldurun.")
            return

        if not validate_name(name, surname):
            return

        worker = {
            "Ad": name,
            "Soyad": surname,
            "Ata Adi": father_name,
            "Dogum tarixi": f"{day} {month} {year}",
            "Cinsiyet": gender,
            "Secilen vezife": position,
            "Is tecrubesi": experience,
            "Seher": city,
            "Unvan": address,
            "Haqqinda": about
        }

        all_workers.append(worker)

        messagebox.showinfo("Ugur", f"{name} {surname} ugurla qeyd olundu!")
        clear_fields()

    def edit_worker():
        edit_window = tk.Toplevel(root)
        edit_window.title("Ishci Melumatlarinin Deyishdirilmesi")
        edit_window.geometry("600x400")

        tk.Label(edit_window, text="Iscinin Adini ve Soyadini daxil edin:", fg="white", bg="#bd99ba").pack(pady=5)
        name_surname_entry = tk.Entry(edit_window)
        name_surname_entry.pack(pady=5)

        def update_worker():

            name_surname = name_surname_entry.get()
            matched_workers = [worker for worker in all_workers if f"{worker['Ad']} {worker['Soyad']}" == name_surname]

            if len(matched_workers) == 0:
                messagebox.showerror("Xeta", "Isci tapilmadi.")
            elif len(matched_workers) > 1:
                messagebox.showerror("Xeta", "Birden chox ishci tapildi. Ad ve Soyadi daha deqiq daxil edin.")
            else:
                worker = matched_workers[0]
                worker["Secilen vezife"] = position_combo.get()
                worker["Is tecrubesi"] = experience_combo.get()
                worker["Seher"] = city_combo.get()
                worker["Unvan"] = address_entry.get()
                worker["Haqqinda"] = about_text.get("1.0", tk.END).strip()
                messagebox.showinfo("Ugur", f"{name_surname} melumatlari ugurla yenilendi!")
                clear_fields()

        tk.Button(edit_window, text="Yenile", bg="#4CAF50", fg="white", command=update_worker).pack(pady=20)

    def delete_worker():
        delete_window = tk.Toplevel(root)
        delete_window.title("Isci Silinmesi")
        delete_window.geometry("400x200")

        tk.Label(delete_window, text="Iscinin Adini ve Soyadini daxil edin:", fg="white", bg="#2C2F36").pack(pady=5)
        name_surname_entry = tk.Entry(delete_window)
        name_surname_entry.pack(pady=5)

        def confirm_delete():
            name_surname = name_surname_entry.get()
            matched_workers = [worker for worker in all_workers if f"{worker['Ad']} {worker['Soyad']}" == name_surname]

            if len(matched_workers) == 0:
                messagebox.showerror("Xeta", "Isci tapilmadi.")
            elif len(matched_workers) > 1:
                messagebox.showerror("Xeta", "Birden chox ishci tapildi. Ad ve Soyadi daha deqiq daxil edin.")
            else:
                worker = matched_workers[0]
                all_workers.remove(worker)
                messagebox.showinfo("Ugur", f"{name_surname} silindi!")
                delete_window.destroy()

        tk.Button(delete_window, text="Sil", bg="#F44336", fg="white", command=confirm_delete).pack(pady=20)

    def show_all_workers():

        all_workers_window = tk.Toplevel(root)
        all_workers_window.title("Butun Iscilerin Siyahisi")
        all_workers_window.geometry("600x400")

        workers_text = tk.Text(all_workers_window, wrap=tk.WORD, bg="#2C2F36", fg="white")
        workers_text.pack(fill=tk.BOTH, expand=True)

        if all_workers:
            for i, worker in enumerate(all_workers, start=1):
                workers_text.insert(tk.END, f"Isci {i}:\n")
                for key, value in worker.items():
                    workers_text.insert(tk.END, f"  {key}: {value}\n")
                workers_text.insert(tk.END, "\n")
        else:
            workers_text.insert(tk.END, "Hec bir isci yoxdur.")

    def sort_workers():

        all_workers.sort(key=lambda worker: worker["Secilen vezife"])
        show_all_workers()

    root = tk.Tk()
    root.title("Ishci Idareetme Sistemi")
    root.geometry("800x600")
    root.configure(bg="#2C2F36")

    left_panel = tk.Frame(root, bg="#333333", relief=tk.RAISED, bd=1)
    left_panel.place(relx=0, rely=0, relwidth=0.3, relheight=1)

    tk.Button(left_panel, text="Yeni Ishci Elave Et", anchor="w", bg="#4CAF50", fg="white", command=save_worker).place(
        relx=0.05, rely=0.05, relwidth=0.9, relheight=0.07)
    tk.Button(left_panel, text="Isci Melumatlarinin Edit Edilmesi", anchor="w", bg="#2196F3", fg="white",
              command=edit_worker).place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.07)
    tk.Button(left_panel, text="Ishcinin Silinmesi", anchor="w", bg="#F44336", fg="white", command=delete_worker).place(
        relx=0.05, rely=0.25, relwidth=0.9, relheight=0.07)
    tk.Button(left_panel, text="Butun Ishcilerin Siyahisi", anchor="w", bg="#9C27B0", fg="white",
              command=show_all_workers).place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.07)
    tk.Button(left_panel, text="Vezifeye Gore Sirala", anchor="w", bg="#FFC107", fg="white",
              command=sort_workers).place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.07)

    right_panel = tk.Frame(root, relief=tk.RAISED, bd=1, bg="#2C2F36")
    right_panel.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

    tk.Label(right_panel, text="Ad:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.05, relwidth=0.1,
                                                                                  relheight=0.05)
    name_entry = tk.Entry(right_panel, bg="#444444", fg="white", insertbackground="white")
    name_entry.place(relx=0.15, rely=0.05, relwidth=0.3, relheight=0.05)

    tk.Label(right_panel, text="Soyad:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.5, rely=0.05, relwidth=0.1,
                                                                                     relheight=0.05)
    surname_entry = tk.Entry(right_panel, bg="#444444", fg="white", insertbackground="white")
    surname_entry.place(relx=0.6, rely=0.05, relwidth=0.3, relheight=0.05)

    tk.Label(right_panel, text="Ata Adi:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.15,
                                                                                       relwidth=0.1, relheight=0.05)
    father_name_entry = tk.Entry(right_panel, bg="#444444", fg="white", insertbackground="white")
    father_name_entry.place(relx=0.15, rely=0.15, relwidth=0.3, relheight=0.05)

    tk.Label(right_panel, text="Dogum Tarixi:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.25,
                                                                                            relwidth=0.2,
                                                                                            relheight=0.05)
    day_combo = ttk.Combobox(right_panel, values=[str(i) for i in range(1, 32)], state="readonly")
    day_combo.place(relx=0.25, rely=0.25, relwidth=0.1, relheight=0.05)
    day_combo.set("Gun")

    months = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr",
              "Dekabr"]
    month_combo = ttk.Combobox(right_panel, values=months, state="readonly")
    month_combo.place(relx=0.35, rely=0.25, relwidth=0.2, relheight=0.05)
    month_combo.set("Ay")

    year_combo = ttk.Combobox(right_panel, values=[str(i) for i in range(1950, 2007)], state="readonly")
    year_combo.place(relx=0.6, rely=0.25, relwidth=0.2, relheight=0.05)
    year_combo.set("Il")

    tk.Label(right_panel, text="Cinsiyet:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.35,
                                                                                        relwidth=0.2, relheight=0.05)
    gender_var = tk.StringVar()
    gender_var = tk.StringVar()

    male_radio = tk.Radiobutton(root, text="Kişi", variable=gender_var, value="Kişi")
    female_radio = tk.Radiobutton(root, text="Qadın", variable=gender_var, value="Qadın")

    male_radio.pack()
    female_radio.pack()
    male_radio.place(relx=0.45, rely=0.35, relwidth=0.2, relheight=0.05)
    female_radio.place(relx=0.65, rely=0.35, relwidth=0.2, relheight=0.05)

    tk.Label(right_panel, text="Vezife:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.45,
                                                                                      relwidth=0.2, relheight=0.05)
    position_combo = ttk.Combobox(right_panel,
                                  values=["Satici", "Dekan", "Hekim", "Kuryer", "Ofissiant", "Muellim", "Direktor",
                                          "Dizayner", "Proqramist", "Polis"], state="readonly")
    position_combo.place(relx=0.25, rely=0.45, relwidth=0.3, relheight=0.05)
    position_combo.set("Vezife")

    tk.Label(right_panel, text="Is Tecrubesi:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.55,
                                                                                            relwidth=0.2,
                                                                                            relheight=0.05)
    experience_combo = ttk.Combobox(right_panel, values=["1 ilden az", "2-4 il", "4< il"], state="readonly")
    experience_combo.place(relx=0.25, rely=0.55, relwidth=0.3, relheight=0.05)
    experience_combo.set("Is tecrubesi")

    tk.Label(right_panel, text="Seher:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.65,
                                                                                      relwidth=0.2, relheight=0.05)
    city_combo = ttk.Combobox(right_panel,
                              values=["Baki", "Gence", "Sumqayit", "Mingachevir", "Lacin", "Semkir", "Qazax",
                                      "Kurdemir","Tovuz" "Shusha", "Kelbecer", "Zengilan"], state="readonly")
    city_combo.place(relx=0.25, rely=0.65, relwidth=0.3, relheight=0.05)
    city_combo.set("Seher")

    tk.Label(right_panel, text="Unvan:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.75, relwidth=0.2,
                                                                                     relheight=0.05)
    address_entry = tk.Entry(right_panel, bg="#444444", fg="white", insertbackground="white")
    address_entry.place(relx=0.25, rely=0.75, relwidth=0.3, relheight=0.05)

    tk.Label(right_panel, text="Haqqinda:", anchor="w", fg="white", bg="#2C2F36").place(relx=0.05, rely=0.85,
                                                                                        relwidth=0.2, relheight=0.05)
    about_text = tk.Text(right_panel, bg="#444444", fg="white", height=3)
    about_text.place(relx=0.25, rely=0.85, relwidth=0.6, relheight=0.1)

    tk.Button(right_panel, text="Save", bg="#468aa3", fg="white", command=save_worker).place(relx=0.05, rely=0.95,
                                                                                             relwidth=0.3,
                                                                                             relheight=0.05)

    root.mainloop()


create_login_window()