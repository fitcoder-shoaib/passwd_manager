import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from pass_gen import pass_gen
from test import load_data, save_data, verify_master

class PasswordManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Password Manager")
        self.root.geometry("650x520")
        self.root.minsize(650, 520)
        self.root.configure(bg="#1e1e1e")  # Dark background
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)
        self.root.rowconfigure(5, weight=1)

        # ---------- STYLE ----------
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=25)

        style.configure("Treeview.Heading",
                        background="#444",
                        foreground="white")

        style.configure("Primary.TButton",
                        padding=(10, 6),
                        font=("Arial", 10, "bold"))

        style.configure("Secondary.TButton",
                        padding=(10, 6),
                        font=("Arial", 10))

        # ---------- LABELS ----------
        label_style = {"bg": "#1e1e1e", "fg": "white", "font": ("Arial", 10)}

        tk.Label(self.root, text="Website", **label_style)\
            .grid(row=0, column=0, padx=10, pady=5, sticky="w")

        tk.Label(self.root, text="Password", **label_style)\
            .grid(row=1, column=0, padx=10, pady=5, sticky="w")

        tk.Label(self.root, text="Notes", **label_style)\
            .grid(row=2, column=0, padx=10, pady=5, sticky="nw")

        # ---------- ENTRIES ----------
        entry_style = {"bg": "#2b2b2b", "fg": "white", "insertbackground": "white"}

        self.website_entry = tk.Entry(self.root, width=40, **entry_style)
        self.website_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.password_entry = tk.Entry(self.root, width=30, **entry_style)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self.root, text="Generate Password",
                   style="Secondary.TButton", command=self.generate)\
            .grid(row=1, column=2, padx=5, sticky="ew")

        # ---------- NOTES BOX ----------
        self.notes_text = tk.Text(self.root, height=5, width=45,
                                  bg="#2b2b2b", fg="white", insertbackground="white")
        self.notes_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="nsew")

        # ---------- BUTTONS ----------
        ttk.Button(self.root, text="Save", style="Primary.TButton",
                   command=self.save)\
            .grid(row=3, column=1, pady=10, sticky="w")

        ttk.Button(self.root, text="Clear", style="Secondary.TButton",
                   command=self.clear)\
            .grid(row=3, column=1, pady=10, sticky="e")

        # ---------- TABLE ----------
        tk.Label(self.root, text="Saved Passwords:",
                 bg="#1e1e1e", fg="white")\
            .grid(row=4, column=0, padx=10, pady=5, sticky="w")

        columns = ("Website", "Password", "Notes")
        self.tree = ttk.Treeview(self.root, columns=columns,
                                 show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        self.tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        master = simpledialog.askstring(
            "Master Password",
            "Enter master password:",
            show="*"
        )

        if verify_master(master):
            self.display_data()
        else:
            messagebox.showerror("Access Denied", "Wrong master password")
            self.root.destroy()

    # ---------- FUNCTIONS ----------
    def generate(self):
        password = pass_gen(16)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save(self):
        website = self.website_entry.get()
        password = self.password_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if website == "" or password == "":
            messagebox.showwarning("Warning", "Fields cannot be empty!")
            return

        save_data(website, password, notes)
        messagebox.showinfo("Success", "Data Saved!")

        self.clear()
        self.display_data()

    def clear(self):
        self.website_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.notes_text.delete("1.0", tk.END)

    def display_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = load_data()

        for record in data:
            self.tree.insert("", tk.END, values=(
                record["website"],
                record["password"],
                record["notes"]
            ))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.run()
