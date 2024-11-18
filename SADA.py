import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import math
import pyperclip
import webbrowser

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show_tip(self):
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(tw, text=self.text, justify=tk.LEFT,
                          background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                          wraplength=200)
        label.pack(ipadx=1, ipady=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

    def attach(self):
        self.widget.bind("<Enter>", lambda event: self.show_tip())
        self.widget.bind("<Leave>", lambda event: self.hide_tip())

def open_url(url):
    webbrowser.open(url)

class SoundLevelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SADA - Sound Level Calculation")
        self.root.geometry("1000x600")
        self.root.iconbitmap("C:/Users/nabde/OneDrive/Desktop/SADA/Assets/Icon.ico")  # Set the window icon
        self.images = []  # List to store image references
        self.create_widgets()

    def create_widgets(self):
        self.create_frames()
        self.create_home_frame()
        self.create_butler_frame()
        self.create_halliwell_frame()
        self.create_reference_frame()
        self.create_about_frame()
        self.create_menu()
        self.show_frame(self.home_frame)

    def create_frames(self):
        self.home_frame = ttk.Frame(self.root)
        self.butler_frame = ttk.Frame(self.root)
        self.halliwell_frame = ttk.Frame(self.root)
        self.reference_frame = ttk.Frame(self.root)
        self.about_frame = ttk.Frame(self.root)
        for frame in (self.home_frame, self.butler_frame, self.halliwell_frame, self.reference_frame, self.about_frame):
            frame.grid(row=0, column=0, sticky='nsew')

    def create_home_frame(self):
        ttk.Label(self.home_frame, text="Welcome to SADA", font=("Helvetica", 16)).pack(pady=20)
        
        # Add logo
        logo_image = Image.open("C:/Users/nabde/OneDrive/Desktop/SADA/Assets/Logo.png")  # Change this to the path to your logo image
        self.logo_image_tk = ImageTk.PhotoImage(logo_image)
        self.images.append(self.logo_image_tk)  # Store reference to the image
        ttk.Label(self.home_frame, image=self.logo_image_tk).pack(pady=10)
        
        button_font = ("Helvetica", 14)
        tk.Button(self.home_frame, text="Butler, Bowyer and Kew Method", command=lambda: self.show_frame(self.butler_frame), width=25, height=2, font=button_font).pack(pady=10)
        tk.Button(self.home_frame, text="Halliwell and Sultan Method", command=lambda: self.show_frame(self.halliwell_frame), width=25, height=2, font=button_font).pack(pady=10)

        # Add footer texts
        ttk.Label(self.home_frame, text="SADA - 2024").pack(side="left", padx=10, pady=10, anchor="s")
        ttk.Label(self.home_frame, text="V 0.1.0").pack(side="right", padx=10, pady=10, anchor="s")

    def create_butler_frame(self):
        ttk.Label(self.butler_frame, text="Butler, Bowyer and Kew Method", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=20)
        
        self.entries = {}
        input_fields = [
            ("L", "L: ", "L represents the sound power level of a horn, bell, speaker, or any sounder (dBA referenced to 10^-12 W)"),
            ("r", "r: ", "r is the distance from the sound source, used in calculating the sound power level and adjustments in the Butler, Bowyer, and Kew method"),
            ("C2", "C2: ", "C2 is a function of the distance from the wall to the point of interest. It adjusts the sound pressure level based on the distance from the sound source"),
            ("C3", "C3: ", "C3 is a correction for the number of directions that the sounder propagates. For example, if the sounder propagates in two directions"),
            ("C4", "C4: ", "C4 is a correction for the characteristics of the corridor walls, ceiling, and floor. It accounts for the acoustic properties of the surfaces, such as being acoustically soft or hard"),
            ("C5", "C5: ", "C5 is a function of the distance from the sounder to the center of the bedroom wall. It adjusts the sound pressure level based on this distance"),
            ("C6", "C6: ", "C6 is a function of the area of the room wall. It adjusts the sound pressure level based on the size of the wall that the sound is impacting"),
            ("C7", "C7: ", "C7 is a function of the frequency of the sound reaching the wall. It adjusts the sound pressure level based on the frequency, with different values for different frequencies"),
            ("R", "R: ", "R represents the average sound reduction index for the wall. It is used to account for the attenuation of sound as it passes through a wall")
        ]

        info_image = Image.open("C:/Users/nabde/OneDrive/Desktop/SADA/Assets/Tooltips.png")  # Change this to the path to your info image
        self.info_image_tk = ImageTk.PhotoImage(info_image)
        self.images.append(self.info_image_tk)  # Store reference to the image

        for i, (var_name, label_text, tooltip_text) in enumerate(input_fields):
            row = i // 2 + 1
            col = (i % 2) * 3
            label = ttk.Label(self.butler_frame, text=label_text)
            label.grid(row=row, column=col, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(self.butler_frame, width=15)
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries[var_name] = entry
            info_button = ttk.Label(self.butler_frame, image=self.info_image_tk)
            info_button.grid(row=row, column=col+2, padx=5, pady=5)
            ToolTip(info_button, tooltip_text).attach()

        self.result_labels = {
            "Lw": ttk.Label(self.butler_frame, text="Lw: "),
            "Lp1": ttk.Label(self.butler_frame, text="Lp1: "),
            "Lp2": ttk.Label(self.butler_frame, text="Lp2: ")
        }

        for i, (key, label) in enumerate(self.result_labels.items()):
            label.grid(row=7+i, column=0, sticky="w", padx=5, pady=5, columnspan=3)

        ttk.Button(self.butler_frame, text="Calculate", command=self.calculate_butler_bowyer_kew).grid(row=10, column=0, padx=5, pady=5)
        ttk.Button(self.butler_frame, text="Clear", command=self.clear_fields).grid(row=10, column=1, padx=5, pady=5)
        ttk.Button(self.butler_frame, text="Copy Results", command=self.copy_results).grid(row=10, column=2, padx=5, pady=5)

        # Resize and display Butler formula image
        butler_image = Image.open("C:/Users/nabde/OneDrive/Desktop/SADA/Assets/Butler Bowyer Kew SFPE .png")
        butler_image = butler_image.resize((300, 150), Image.Resampling.LANCZOS)  # Resize as needed
        self.butler_image_tk = ImageTk.PhotoImage(butler_image)
        self.images.append(self.butler_image_tk)  # Store reference to the image
        ttk.Label(self.butler_frame, image=self.butler_image_tk).grid(row=1, column=6, rowspan=10, padx=20, pady=5, sticky="nw")

    def create_halliwell_frame(self):
        ttk.Label(self.halliwell_frame, text="Halliwell and Sultan Method", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=4, pady=20)

        self.entries_hs = {}
        input_fields_hs = [
           ("P", "P: ", "Sound power level (SPL) of the sounder"),
            ("Vs", "Vs: ", "Volume of the source room"),
            ("T60", "T60: ", "Reverberation time"),
            ("Ss", "Ss: ", "Surface area of the source room"),
            ("λ", "λ: ", "Wavelength"),
            ("R", "R: ", "Room attenuation"),
            ("S", "S: ", "Surface area of the partition between the sounder room and the receiver room"),
            ("C", "C: ", "Constant related to sound propagation"),
            ("Vr", "Vr: ", "Volume of the receiver room"),
            ("corr", "corr: ", "Correction factor recommended by Halliwell and Sultan of - 5 dBA for every additional room in the propagation path.")  
        ]

        for i, (var_name, label_text, tooltip_text) in enumerate(input_fields_hs):
            row = i // 2 + 1
            col = (i % 2) * 3
            label = ttk.Label(self.halliwell_frame, text=label_text)
            label.grid(row=row, column=col, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(self.halliwell_frame, width=15)
            entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
            self.entries_hs[var_name] = entry
            info_button = ttk.Label(self.halliwell_frame, image=self.info_image_tk)
            info_button.grid(row=row, column=col+2, padx=5, pady=5)
            ToolTip(info_button, tooltip_text).attach()

        self.result_labels_hs = {
            "Ls": ttk.Label(self.halliwell_frame, text="Ls: "),
            "Lr": ttk.Label(self.halliwell_frame, text="Lr: ")
        }

        for i, (key, label) in enumerate(self.result_labels_hs.items()):
            label.grid(row=7+i, column=0, sticky="w", padx=5, pady=5, columnspan=3)

        ttk.Button(self.halliwell_frame, text="Calculate", command=self.calculate_halliwell_sultan).grid(row=10, column=0, padx=5, pady=5)
        ttk.Button(self.halliwell_frame, text="Clear", command=self.clear_fields_hs).grid(row=10, column=1, padx=5, pady=5)
        ttk.Button(self.halliwell_frame, text="Copy Results", command=self.copy_results_hs).grid(row=10, column=2, padx=5, pady=5)

        # Resize and display Halliwell formula image
        halliwell_image = Image.open("C:/Users/nabde/OneDrive/Desktop/SADA/Assets/Halliwell and Sultan.png")
        halliwell_image = halliwell_image.resize((300, 150), Image.Resampling.LANCZOS)  # Resize as needed
        self.halliwell_image_tk = ImageTk.PhotoImage(halliwell_image)
        self.images.append(self.halliwell_image_tk)  # Store reference to the image
        ttk.Label(self.halliwell_frame, image=self.halliwell_image_tk).grid(row=1, column=6, rowspan=10, padx=20, pady=5, sticky="nw")

    def create_reference_frame(self):
        ttk.Label(self.reference_frame, text="References", font=("Helvetica", 16)).pack(pady=20)

        references = [
            ("[1] Halliwell, R.E. and Sultan, M.A., 1986. Attenuation Of Smoke Detector Alarm Signals In Residential Buildings. Fire Safety Science 1: 689-697. doi:10.3801/IAFSS.FSS.1-689", "https://publications.iafss.org/publications/fss/1/689"),
            ("[2] Bowyer A, Butler H, Kew J (1981) Locating fire alarm sounders for audibility. BSRIA application guide, vol 81. Building Services Research and Information Association, Guildford", "http://scholar.google.com/scholar_lookup?&title=Locating%20fire%20alarm%20sounders%20for%20audibility%20BSRIA%20application%20guide&publication_year=1981&author=Bowyer%2CA&author=Butler%2CH&author=Kew%2CJ"),
            ("[3] Schiﬁliti RP, Custer RLP, Meacham BJ (2016) Design of detection systems. In: Hurley MJ (ed) et al SFPE handbook, 5th edn. Springer, Berlin", "https://doi.org/10.1007/978-1-4939-2565-0_40")
        ]

        for ref_text, ref_url in references:
            link = ttk.Label(self.reference_frame, text=ref_text, foreground="blue", cursor="hand2", anchor="w")
            link.pack(fill='x', padx=20, pady=5)
            link.bind("<Button-1>", lambda e, url=ref_url: open_url(url))

    def create_about_frame(self):
        ttk.Label(self.about_frame, text="About SADA", font=("Helvetica", 16)).pack(pady=20)

        about_text = """
        SADA is a comprehensive open source software tool designed to calculate sound levels using two well-established methods: the Butler, Bowyer, and Kew method, and the Halliwell and Sultan method.

        Methods

        **Butler, Bowyer, and Kew Method (Butler et al., 1981)**
        Developed in 1981 by H. Butler, A. Bowyer, and J. Kew, this method focuses on determining the optimal placement of fire alarm sounders within buildings. It takes into account various factors such as building size, shape, occupancy, construction type, presence of noise sources, and desired audibility levels. The method employs computer simulations to calculate sound pressure levels at different locations within a building, comparing these levels to the desired audibility thresholds.

        Key Features:
        - Comprehensive Analysis: Considers multiple factors affecting sound propagation, including building acoustics and ambient noise levels.
        - Computer Simulations: Utilizes simulations to predict sound pressure levels throughout the building.
        - Optimal Placement: Aims to ensure that alarm sounders are positioned to achieve effective audibility in all necessary areas.

        **Halliwell and Sultan Method (Halliwell & Sultan, 1986)**
        Introduced in 1986 by Halliwell and Sultan, this method provides a systematic approach for placing fire alarms in residential buildings. It is guided by principles such as central positioning of alarms and ensuring audibility in all occupied areas. The method calculates sound pressure levels based on room volume, surface areas, and other inputs, providing a comprehensive measure of audibility within each specific room.

        Key Features:
        - Residential Focus: Specifically designed for residential buildings, taking into account typical room layouts and occupancy patterns.
        - Systematic Approach: Uses detailed calculations to determine optimal alarm placement for effective audibility.
        - Room-Specific Analysis: Considers the acoustic properties and geometry of each room to ensure sound reaches all areas.
        """
        ttk.Label(self.about_frame, text=about_text, wraplength=900, justify=tk.LEFT).pack(padx=20, pady=10)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menubar.add_command(label="Home", command=lambda: self.show_frame(self.home_frame))
        menubar.add_command(label="References", command=lambda: self.show_frame(self.reference_frame))
        menubar.add_command(label="About", command=lambda: self.show_frame(self.about_frame))

    def show_frame(self, frame):
        frame.tkraise()

    def calculate_butler_bowyer_kew(self):
        try:
            L = float(self.entries["L"].get())
            r = float(self.entries["r"].get())
            C2 = float(self.entries["C2"].get())
            C3 = float(self.entries["C3"].get())
            C4 = float(self.entries["C4"].get())
            C5 = float(self.entries["C5"].get())
            C6 = float(self.entries["C6"].get())
            C7 = float(self.entries["C7"].get())
            R = float(self.entries["R"].get())

            Lw = L + 20 * math.log10(r) + 11
            Lp1 = Lw + C3 + C4 + C5
            Lp2 = Lp1 - R + C2 + C6 + C7 + 11

            self.result_labels["Lw"].config(text=f"Lw: {Lw:.2f} dB")
            self.result_labels["Lp1"].config(text=f"Lp1: {Lp1:.2f} dBA")
            self.result_labels["Lp2"].config(text=f"Lp2: {Lp2:.2f} dBA")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers")

    def calculate_halliwell_sultan(self):
        try:
            P = float(self.entries_hs["P"].get())
            Vs = float(self.entries_hs["Vs"].get())
            T60 = float(self.entries_hs["T60"].get())
            Ss = float(self.entries_hs["Ss"].get())
            λ = float(self.entries_hs["λ"].get())
            R = float(self.entries_hs["R"].get())
            S = float(self.entries_hs["S"].get())
            C = float(self.entries_hs["C"].get())
            Vr = float(self.entries_hs["Vr"].get())
            corr = float(self.entries_hs["corr"].get())

            term1 = Vs / T60 * (1 + (Ss * λ) / (8 * Vs))
            Ls = P - 10 * math.log10(term1) + 14

            term2 = (S * T60 * C * 1.086) / (60 * Vr)
            Lr = Ls - R + 10 * math.log10(term2) + corr

            self.result_labels_hs["Ls"].config(text=f"Ls: {Ls:.2f} dBA")
            self.result_labels_hs["Lr"].config(text=f"Lr: {Lr:.2f} dBA")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        for label in self.result_labels.values():
            label.config(text="")

    def clear_fields_hs(self):
        for entry in self.entries_hs.values():
            entry.delete(0, tk.END)
        for label in self.result_labels_hs.values():
            label.config(text="")

    def copy_results(self):
        results = "\n".join(label.cget("text") for label in self.result_labels.values() if label.cget("text"))
        pyperclip.copy(results)
        messagebox.showinfo("Copied", "Results copied to clipboard")

    def copy_results_hs(self):
        results = "\n".join(label.cget("text") for label in self.result_labels_hs.values() if label.cget("text"))
        pyperclip.copy(results)
        messagebox.showinfo("Copied", "Results copied to clipboard")

if __name__ == "__main__":
    root = tk.Tk()
    app = SoundLevelApp(root)
    root.mainloop()
