
"""
app.py
Tkinter graphical interface for CampusFlow.
Run this file with: python app.py
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

from database import Database
from dataset import CAMPUSES, CAMPUS_POLICIES

COLORS = {
    "navy": "#172554", "blue": "#2563eb", "bg": "#f3f6fb",
    "white": "#ffffff", "ink": "#172033", "muted": "#64748b",
    "line": "#dbe3ef", "green": "#15803d", "pale": "#eaf1ff"
}


class CampusFlowApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.user = None
        self.active_campus = CAMPUSES[0]
        self.root.title("CampusFlow | Smart Campus Resource Hub")
        self.root.geometry("1180x740")
        self.root.minsize(950, 620)
        self.root.configure(bg=COLORS["bg"])
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("Treeview", rowheight=29, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.show_login()

    def button(self, parent, text, command, primary=True):
        return tk.Button(
            parent, text=text, command=command,
            bg=COLORS["blue"] if primary else "#e8edf5",
            fg="white" if primary else COLORS["ink"],
            activebackground=COLORS["navy"], activeforeground="white",
            relief="flat", bd=0, padx=13, pady=9,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )

    def clear(self):
        for child in self.root.winfo_children():
            child.destroy()

    def show_login(self):
        self.clear()
        panel = tk.Frame(
            self.root, bg="white", padx=42, pady=34,
            highlightbackground=COLORS["line"], highlightthickness=1
        )
        panel.place(relx=.5, rely=.5, anchor="center", width=470)

        tk.Label(
            panel, text="CAMPUSFLOW", bg="white", fg=COLORS["blue"],
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            panel, text="Space to do your best work.", bg="white",
            fg=COLORS["ink"], font=("Segoe UI", 23, "bold"),
            wraplength=360, justify="left"
        ).pack(anchor="w", pady=(8, 5))

        tk.Label(
            panel,
            text="Smart campus resource booking • Richfield Graduate Institution",
            bg="white", fg=COLORS["muted"], wraplength=360, justify="left"
        ).pack(anchor="w", pady=(0, 22))

        tk.Label(panel, text="Username", bg="white").pack(anchor="w")
        self.username = tk.Entry(
            panel, font=("Segoe UI", 11), relief="solid", bd=1
        )
        self.username.pack(fill="x", ipady=7, pady=(4, 12))

        tk.Label(panel, text="Password", bg="white").pack(anchor="w")
        self.password = tk.Entry(
            panel, show="●", font=("Segoe UI", 11), relief="solid", bd=1
        )
        self.password.pack(fill="x", ipady=7, pady=(4, 16))

        self.button(
            panel, "Sign in to CampusFlow", self.do_login
        ).pack(fill="x")

        self.button(
            panel, "Create lecturer account",
            self.register_window, False
        ).pack(fill="x", pady=(8, 0))

        tk.Label(
            panel, text="DEMO ACCOUNTS", bg="white", fg=COLORS["blue"],
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(20, 5))

        tk.Label(
            panel,
            text="Lecturer: lecturer / Learn123!\n"
                 "Admin: admin / Admin123!\n"
                 "Operator: operator / Operator123!",
            bg="white", fg=COLORS["muted"],
            font=("Consolas", 9), justify="left"
        ).pack(anchor="w")

        self.password.bind("<Return>", lambda event: self.do_login())

    def do_login(self):
        user = self.db.login(
            self.username.get(), self.password.get()
        )
        if not user:
            messagebox.showerror(
                "Sign in failed",
                "Username or password is incorrect."
            )
            return

        self.user = user
        self.active_campus = (
            user["campus"]
            if user["role"] == "Campus Administrator"
            else CAMPUSES[0]
        )
        self.show_dashboard()

    def register_window(self):
        win = tk.Toplevel(self.root)
        win.title("Create lecturer account")
        win.geometry("390x420")
        win.configure(bg="white")
        entries = {}

        for label in ("Full name", "Username", "Password"):
            tk.Label(
                win, text=label, bg="white"
            ).pack(anchor="w", padx=24, pady=(12, 2))

            entry = tk.Entry(
                win, show="●" if label == "Password" else "",
                relief="solid", bd=1
            )
            entry.pack(fill="x", padx=24, ipady=5)
            entries[label] = entry

        tk.Label(
            win, text="Home campus", bg="white"
        ).pack(anchor="w", padx=24, pady=(12, 2))

        campus = tk.StringVar(value=CAMPUSES[0])
        ttk.Combobox(
            win, textvariable=campus,
            values=CAMPUSES, state="readonly"
        ).pack(fill="x", padx=24)

        def save():
            try:
                self.db.register_lecturer(
                    entries["Full name"].get(),
                    entries["Username"].get(),
                    entries["Password"].get(),
                    campus.get()
                )
                messagebox.showinfo(
                    "Account created",
                    "You can now sign in.",
                    parent=win
                )
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Username taken",
                    "Choose a different username.",
                    parent=win
                )
            except ValueError as exc:
                messagebox.showerror(
                    "Check details", str(exc), parent=win
                )

        self.button(
            win, "Create account", save
        ).pack(fill="x", padx=24, pady=20)

    def show_dashboard(self):
        self.clear()
        shell = tk.Frame(self.root, bg=COLORS["bg"])
        shell.pack(fill="both", expand=True)

        side = tk.Frame(shell, bg=COLORS["navy"], width=215)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        tk.Label(
            side, text="CAMPUSFLOW", bg=COLORS["navy"], fg="white",
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", padx=20, pady=(25, 3))

        tk.Label(
            side, text="SMART CAMPUS HUB",
            bg=COLORS["navy"], fg="#9db8f8",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 25))

        for label, action in [
            ("Overview", self.show_overview),
            ("Resources", self.show_resources),
            ("Bookings", self.show_bookings),
            ("Reports", self.show_reports)
        ]:
            tk.Button(
                side, text="   " + label, command=action, anchor="w",
                bg=COLORS["navy"], fg="#e4ebff",
                activebackground="#263b70",
                activeforeground="white", relief="flat", bd=0,
                font=("Segoe UI", 11), padx=12, pady=12
            ).pack(fill="x", padx=9, pady=2)

        tk.Frame(
            side, bg="#334477", height=1
        ).pack(fill="x", padx=18, pady=20)

        tk.Label(
            side, text=self.user["full_name"], bg=COLORS["navy"],
            fg="white", font=("Segoe UI", 10, "bold"),
            wraplength=175
        ).pack(anchor="w", padx=20)

        tk.Label(
            side, text=self.user["role"], bg=COLORS["navy"],
            fg="#b8c7e8", font=("Segoe UI", 9), wraplength=175
        ).pack(anchor="w", padx=20, pady=(4, 12))

        self.button(
            side, "Sign out", self.show_login, False
        ).pack(side="bottom", fill="x", padx=14, pady=16)

        self.content = tk.Frame(shell, bg=COLORS["bg"])
        self.content.pack(side="left", fill="both", expand=True)
        self.show_overview()

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def header(self, title, subtitle):
        box = tk.Frame(self.content, bg=COLORS["bg"])
        box.pack(fill="x", padx=26, pady=(24, 16))

        tk.Label(
            box, text=title, bg=COLORS["bg"], fg=COLORS["ink"],
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            box, text=subtitle, bg=COLORS["bg"],
            fg=COLORS["muted"]
        ).pack(anchor="w", pady=(4, 0))

    def campus_row(self):
        row = tk.Frame(self.content, bg=COLORS["bg"])
        row.pack(fill="x", padx=26, pady=(0, 12))

        tk.Label(
            row, text="ACTIVE CAMPUS", bg=COLORS["bg"],
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        if self.user["role"] == "Campus Administrator":
            tk.Label(
                row, text=self.active_campus, bg=COLORS["pale"],
                fg=COLORS["blue"], padx=10, pady=5
            ).pack(side="left", padx=10)
        else:
            self.campus_var = tk.StringVar(value=self.active_campus)
            combo = ttk.Combobox(
                row, textvariable=self.campus_var,
                values=CAMPUSES, state="readonly", width=17
            )
            combo.pack(side="left", padx=10)
            combo.bind(
                "<<ComboboxSelected>>", self.change_campus
            )

        tk.Label(
            row,
            text=CAMPUS_POLICIES[self.active_campus]["description"],
            bg=COLORS["bg"], fg=COLORS["muted"],
            font=("Segoe UI", 9)
        ).pack(side="left", padx=8)

    def change_campus(self, event=None):
        self.active_campus = self.campus_var.get()
        self.show_overview()

    def stat_card(self, parent, title, value, note, color):
        card = tk.Frame(
            parent, bg="white", padx=17, pady=15,
            highlightbackground=COLORS["line"], highlightthickness=1
        )

        tk.Label(
            card, text=title.upper(), bg="white",
            fg=COLORS["muted"], font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            card, text=str(value), bg="white", fg=color,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=(6, 2))

        tk.Label(
            card, text=note, bg="white", fg=COLORS["muted"],
            font=("Segoe UI", 9), wraplength=200
        ).pack(anchor="w")
        return card

    def show_overview(self):
        self.clear_content()
        self.header(
            "Welcome, " + self.user["full_name"].split()[0],
            "Your campus resources, organised in one place."
        )
        self.campus_row()

        scope = (
            None if self.user["role"] == "System Operator"
            else self.active_campus
        )
        resources = self.db.get_resources(scope)
        bookings = self.db.get_bookings(scope)
        active = [
            b for b in bookings if b["status"] == "Active"
        ]

        cards = tk.Frame(self.content, bg=COLORS["bg"])
        cards.pack(fill="x", padx=26, pady=7)

        for i in range(3):
            cards.columnconfigure(i, weight=1, uniform="cards")

        self.stat_card(
            cards, "Resources", len(resources),
            "Registered rooms and equipment", COLORS["blue"]
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.stat_card(
            cards, "Active bookings", len(active),
            "Current confirmed reservations", COLORS["green"]
        ).grid(row=0, column=1, sticky="nsew", padx=4)

        self.stat_card(
            cards, "Campuses", len(CAMPUSES),
            "Connected resource network", "#0891b2"
        ).grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        banner = tk.Frame(
            self.content, bg=COLORS["navy"], padx=20, pady=16
        )
        banner.pack(fill="x", padx=26, pady=17)

        tk.Label(
            banner, text="CAMPUS POLICY IN EFFECT",
            bg=COLORS["navy"], fg="#9db8f8",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            banner,
            text=self.active_campus + "  •  " +
                 CAMPUS_POLICIES[self.active_campus]["description"],
            bg=COLORS["navy"], fg="white",
            font=("Segoe UI", 11, "bold"), wraplength=760
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            self.content, text="Resource spotlight",
            bg=COLORS["bg"], fg=COLORS["ink"],
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=26, pady=(3, 8))

        for r in resources[:5]:
            line = tk.Frame(
                self.content, bg="white", padx=12, pady=9,
                highlightbackground=COLORS["line"],
                highlightthickness=1
            )
            line.pack(fill="x", padx=26, pady=3)

            tk.Label(
                line, text=r["category"].upper(), bg="white",
                fg=COLORS["blue"], font=("Segoe UI", 8, "bold"),
                width=20, anchor="w"
            ).pack(side="left")

            tk.Label(
                line, text=r["name"], bg="white",
                fg=COLORS["ink"], font=("Segoe UI", 10, "bold")
            ).pack(side="left", padx=7)

            tk.Label(
                line, text=r["resource_code"], bg="white",
                fg=COLORS["muted"], font=("Consolas", 9)
            ).pack(side="right")

    def selected_values(self, tree):
        chosen = tree.selection()
        if not chosen:
            messagebox.showwarning(
                "Select a row",
                "Choose an item from the table first."
            )
            return None
        return tree.item(chosen[0])["values"]

    def show_resources(self):
        self.clear_content()
        self.header(
            "Resource directory",
            "Browse campus facilities and manage the resource inventory."
        )
        self.campus_row()

        if self.user["role"] != "Lecturer":
            bar = tk.Frame(self.content, bg=COLORS["bg"])
            bar.pack(fill="x", padx=26, pady=(0, 10))

            self.button(
                bar, "+ Add resource", self.resource_form
            ).pack(side="left")

            self.button(
                bar, "Edit selected", self.edit_resource, False
            ).pack(side="left", padx=7)

            self.button(
                bar, "Remove selected", self.remove_resource, False
            ).pack(side="left")
        else:
            tk.Label(
                self.content,
                text="To reserve a resource, open Bookings and choose New booking.",
                bg=COLORS["bg"], fg=COLORS["muted"]
            ).pack(anchor="w", padx=26, pady=(0, 10))

        frame = tk.Frame(self.content, bg="white")
        frame.pack(
            fill="both", expand=True, padx=26, pady=(0, 22)
        )

        cols = ("id", "code", "name", "category", "campus", "capacity")
        heads = (
            "ID", "Resource code", "Resource name",
            "Type", "Campus", "Capacity"
        )
        widths = (45, 125, 240, 165, 130, 75)

        self.resource_tree = ttk.Treeview(
            frame, columns=cols, show="headings"
        )

        for col, heading, width in zip(cols, heads, widths):
            self.resource_tree.heading(col, text=heading)
            self.resource_tree.column(col, width=width, anchor="w")

        scroll = ttk.Scrollbar(
            frame, orient="vertical",
            command=self.resource_tree.yview
        )
        self.resource_tree.configure(yscrollcommand=scroll.set)
        self.resource_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for r in self.db.get_resources(self.active_campus):
            self.resource_tree.insert(
                "", "end",
                values=(
                    r["id"], r["resource_code"], r["name"],
                    r["category"], r["campus"], r["capacity"]
                )
            )

    def resource_form(self, existing=None):
        win = tk.Toplevel(self.root)
        win.title("Resource details")
        win.geometry("420x480")
        win.configure(bg="white")

        values = (
            list(existing) if existing
            else [None, "", "", "Computer Lab", self.active_campus, 1]
        )
        fields = {}

        for label, value in (
            ("Resource code", values[1]),
            ("Resource name", values[2])
        ):
            tk.Label(
                win, text=label, bg="white"
            ).pack(anchor="w", padx=24, pady=(12, 2))

            entry = tk.Entry(win, relief="solid", bd=1)
            entry.pack(fill="x", padx=24, ipady=5)
            entry.insert(0, str(value or ""))
            fields[label] = entry

        tk.Label(
            win, text="Category", bg="white"
        ).pack(anchor="w", padx=24, pady=(10, 2))

        category = tk.StringVar(value=values[3] or "Computer Lab")
        ttk.Combobox(
            win, textvariable=category,
            values=[
                "Computer Lab", "Seminar Room", "Projector",
                "Presentation Equipment", "Lecture Hall", "Other"
            ],
            state="readonly"
        ).pack(fill="x", padx=24)

        tk.Label(
            win, text="Campus", bg="white"
        ).pack(anchor="w", padx=24, pady=(10, 2))

        campus = tk.StringVar(value=values[4] or self.active_campus)
        ttk.Combobox(
            win, textvariable=campus,
            values=CAMPUSES, state="readonly"
        ).pack(fill="x", padx=24)

        tk.Label(
            win, text="Capacity", bg="white"
        ).pack(anchor="w", padx=24, pady=(10, 2))

        capacity = tk.Entry(win, relief="solid", bd=1)
        capacity.pack(fill="x", padx=24, ipady=5)
        capacity.insert(0, str(values[5] or 1))

        tk.Label(
            win, text="Notes (optional)", bg="white"
        ).pack(anchor="w", padx=24, pady=(10, 2))

        notes = tk.Entry(win, relief="solid", bd=1)
        notes.pack(fill="x", padx=24, ipady=5)

        def save():
            try:
                if existing:
                    self.db.update_resource(
                        existing[0],
                        fields["Resource code"].get(),
                        fields["Resource name"].get(),
                        category.get(), campus.get(),
                        int(capacity.get()), notes.get()
                    )
                else:
                    self.db.add_resource(
                        fields["Resource code"].get(),
                        fields["Resource name"].get(),
                        category.get(), campus.get(),
                        int(capacity.get()), notes.get()
                    )

                win.destroy()
                self.show_resources()

            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Duplicate code",
                    "Each resource code must be unique.",
                    parent=win
                )
            except ValueError as exc:
                messagebox.showerror(
                    "Check details", str(exc), parent=win
                )

        self.button(
            win, "Save resource", save
        ).pack(fill="x", padx=24, pady=16)

    def edit_resource(self):
        row = self.selected_values(self.resource_tree)
        if row:
            self.resource_form(row)

    def remove_resource(self):
        row = self.selected_values(self.resource_tree)
        if row and messagebox.askyesno(
            "Remove resource", f"Remove {row[2]}?"
        ):
            try:
                self.db.delete_resource(row[0])
                self.show_resources()
            except ValueError as exc:
                messagebox.showerror(
                    "Cannot remove resource", str(exc)
                )

    def show_bookings(self):
        self.clear_content()
        self.header(
            "Bookings",
            "Create reservations, review booking history and cancel future sessions."
        )
        self.campus_row()

        bar = tk.Frame(self.content, bg=COLORS["bg"])
        bar.pack(fill="x", padx=26, pady=(0, 10))

        if self.user["role"] == "Lecturer":
            self.button(
                bar, "+ New booking", self.booking_form
            ).pack(side="left")

        self.button(
            bar, "Cancel selected", self.cancel_booking, False
        ).pack(side="left", padx=7)

        frame = tk.Frame(self.content, bg="white")
        frame.pack(
            fill="both", expand=True, padx=26, pady=(0, 22)
        )

        cols = (
            "id", "date", "time", "duration", "resource",
            "campus", "lecturer", "purpose", "status"
        )
        headings = (
            "ID", "Date", "Start", "Hours", "Resource",
            "Campus", "Booked by", "Purpose", "Status"
        )
        widths = (40, 95, 65, 55, 160, 105, 125, 145, 80)

        self.booking_tree = ttk.Treeview(
            frame, columns=cols, show="headings"
        )

        for col, heading, width in zip(cols, headings, widths):
            self.booking_tree.heading(col, text=heading)
            self.booking_tree.column(col, width=width, anchor="w")

        scroll = ttk.Scrollbar(
            frame, orient="vertical",
            command=self.booking_tree.yview
        )
        self.booking_tree.configure(yscrollcommand=scroll.set)
        self.booking_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        if self.user["role"] == "Lecturer":
            rows = self.db.get_bookings(user_id=self.user["id"])
        elif self.user["role"] == "Campus Administrator":
            rows = self.db.get_bookings(campus=self.user["campus"])
        else:
            rows = self.db.get_bookings()

        for b in rows:
            self.booking_tree.insert(
                "", "end",
                values=(
                    b["id"], b["booking_date"], b["start_time"],
                    b["duration"], b["resource_name"], b["campus"],
                    b["full_name"], b["purpose"], b["status"]
                )
            )

    def booking_form(self):
        win = tk.Toplevel(self.root)
        win.title("Create a booking")
        win.geometry("440x510")
        win.configure(bg="white")

        tk.Label(
            win, text="New resource booking", bg="white",
            fg=COLORS["ink"], font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=24, pady=(18, 3))

        tk.Label(
            win, text="Campus rules are checked before a booking is saved.",
            bg="white", fg=COLORS["muted"], wraplength=380
        ).pack(anchor="w", padx=24, pady=(0, 10))

        campus = tk.StringVar(value=self.active_campus)

        tk.Label(
            win, text="Campus", bg="white"
        ).pack(anchor="w", padx=24, pady=(6, 2))

        ttk.Combobox(
            win, textvariable=campus,
            values=CAMPUSES, state="readonly"
        ).pack(fill="x", padx=24)

        tk.Label(
            win, text="Resource", bg="white"
        ).pack(anchor="w", padx=24, pady=(9, 2))

        resource_var = tk.StringVar()
        resource_combo = ttk.Combobox(
            win, textvariable=resource_var, state="readonly"
        )
        resource_combo.pack(fill="x", padx=24)

        resources = []

        def refresh(*_):
            nonlocal resources
            resources = self.db.get_resources(campus.get())
            resource_combo["values"] = [
                f'{r["resource_code"]} — {r["name"]}'
                for r in resources
            ]
            resource_var.set(
                resource_combo["values"][0]
                if resources else ""
            )
            policy_label.config(
                text=CAMPUS_POLICIES[campus.get()]["description"]
            )

        campus.trace_add("write", refresh)

        for label in ("Date (YYYY-MM-DD)", "Start time (HH:MM)"):
            tk.Label(
                win, text=label, bg="white"
            ).pack(anchor="w", padx=24, pady=(9, 2))

            e = tk.Entry(win, relief="solid", bd=1)
            e.pack(fill="x", padx=24, ipady=5)

            if label.startswith("Date"):
                e.insert(0, date.today().isoformat())
                date_entry = e
            else:
                e.insert(0, "10:00")
                time_entry = e

        row = tk.Frame(win, bg="white")
        row.pack(fill="x", padx=24, pady=(10, 0))

        tk.Label(
            row, text="Duration (hours)", bg="white"
        ).pack(side="left")

        duration = tk.StringVar(value="1")
        ttk.Combobox(
            row, textvariable=duration,
            values=["1", "2", "3", "4"],
            state="readonly", width=6
        ).pack(side="right")

        tk.Label(
            win, text="Purpose", bg="white"
        ).pack(anchor="w", padx=24, pady=(9, 2))

        purpose = tk.Entry(win, relief="solid", bd=1)
        purpose.pack(fill="x", padx=24, ipady=5)

        policy_label = tk.Label(
            win, text="", bg="white", fg=COLORS["blue"],
            wraplength=380, justify="left"
        )
        policy_label.pack(anchor="w", padx=24, pady=(8, 0))

        refresh()

        def save():
            try:
                if not resources or resource_combo.current() < 0:
                    raise ValueError(
                        "There are no resources at this campus. "
                        "Select another campus."
                    )

                resource = resources[resource_combo.current()]

                self.db.create_booking(
                    resource["id"], self.user["id"], campus.get(),
                    date_entry.get().strip(),
                    time_entry.get().strip(),
                    int(duration.get()), purpose.get()
                )

                self.active_campus = campus.get()

                messagebox.showinfo(
                    "Booking confirmed",
                    "Your booking has been saved.",
                    parent=win
                )
                win.destroy()
                self.show_bookings()

            except (ValueError, sqlite3.Error) as exc:
                messagebox.showerror(
                    "Booking not saved", str(exc), parent=win
                )

        self.button(
            win, "Confirm booking", save
        ).pack(fill="x", padx=24, pady=14)

    def cancel_booking(self):
        row = self.selected_values(self.booking_tree)
        if not row or not messagebox.askyesno(
            "Cancel booking", f"Cancel booking #{row[0]}?"
        ):
            return

        try:
            user_id = (
                self.user["id"]
                if self.user["role"] == "Lecturer"
                else None
            )
            self.db.cancel_booking(row[0], user_id)
            self.show_bookings()
        except ValueError as exc:
            messagebox.showerror("Cannot cancel", str(exc))

    def show_reports(self):
        self.clear_content()
        self.header(
            "Insights & reports",
            "Review campus usage and compare resource demand."
        )

        if self.user["role"] == "Lecturer":
            tk.Label(
                self.content,
                text="Reports are available to campus administrators "
                     "and system operators.",
                bg=COLORS["bg"], fg=COLORS["muted"]
            ).pack(anchor="w", padx=26)
            return

        if self.user["role"] == "Campus Administrator":
            self.active_campus = self.user["campus"]
            campus_filter = self.active_campus
        else:
            campus_filter = None
            self.campus_row()

        bookings = self.db.get_bookings(campus=campus_filter)
        active = [
            b for b in bookings if b["status"] == "Active"
        ]
        resources = self.db.get_resources(campus_filter)

        avg = (
            round(
                sum(b["duration"] for b in active) / len(active), 1
            )
            if active else 0
        )

        cards = tk.Frame(self.content, bg=COLORS["bg"])
        cards.pack(fill="x", padx=26, pady=10)

        for i in range(3):
            cards.columnconfigure(i, weight=1, uniform="reports")

        self.stat_card(
            cards, "Active bookings", len(active),
            "Bookings in this report", COLORS["blue"]
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.stat_card(
            cards, "Average duration", f"{avg} h",
            "Average hours per active booking", COLORS["green"]
        ).grid(row=0, column=1, sticky="nsew", padx=4)

        self.stat_card(
            cards, "Resources", len(resources),
            "Resources in selected scope", "#0891b2"
        ).grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        title = (
            "Campus comparison"
            if self.user["role"] == "System Operator"
            else "Most-used resources"
        )

        tk.Label(
            self.content, text=title, bg=COLORS["bg"],
            fg=COLORS["ink"], font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=26, pady=(16, 7))

        frame = tk.Frame(self.content, bg="white")
        frame.pack(
            fill="both", expand=True, padx=26, pady=(0, 22)
        )

        if self.user["role"] == "System Operator":
            cols = ("campus", "bookings", "average", "policy")
            headings = (
                "Campus", "Active bookings",
                "Avg. duration", "Booking policy"
            )
            rows = []

            for name, policy in CAMPUS_POLICIES.items():
                campus_rows = [
                    b for b in active if b["campus"] == name
                ]
                campus_avg = (
                    round(
                        sum(b["duration"] for b in campus_rows)
                        / len(campus_rows), 1
                    )
                    if campus_rows else 0
                )
                rows.append((
                    name, len(campus_rows),
                    f"{campus_avg} h", policy["description"]
                ))

            widths = (135, 130, 115, 440)

        else:
            cols = ("code", "name", "campus", "uses")
            headings = (
                "Resource code", "Resource", "Campus", "Bookings"
            )
            rows = [
                (
                    r["resource_code"], r["name"],
                    r["campus"], r["uses"]
                )
                for r in self.db.resource_usage(campus_filter)
            ]
            widths = (130, 250, 150, 100)

        tree = ttk.Treeview(frame, columns=cols, show="headings")

        for col, heading, width in zip(cols, headings, widths):
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True, padx=8, pady=8)

    def close(self):
        self.db.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CampusFlowApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
