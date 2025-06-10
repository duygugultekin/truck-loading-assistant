print("✅ Bu dosya gerçekten çalışıyor!")
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import Toplevel, ttk, messagebox, Button, Label
import tkinter.simpledialog as simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from collections import defaultdict
import hashlib
import io
from PIL import Image
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.pagesizes import A4, A6
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import mm
import time
from math import radians, cos, sin, asin, sqrt
import mplcursors
import webbrowser
import tempfile
from PyPDF2 import PdfMerger, PdfReader
import os
import json
import pyvista as pv
from pyvistaqt import BackgroundPlotter
import random
from PyQt5.QtWidgets import QApplication



# === GUI VERİ YAPISI ===
products = []
placements = []
manual_placements = []
placement_log = []
truck_length = 1360
truck_width = 245
truck_height = 270
dev_mode = False


root = tk.Tk()

# === TÜM TÜRKİYE İL-İLÇE VERİSİ ===
# Güncellenmiş TÜM TÜRKİYE İL-İLÇE VERİSİ
city_districts = {
    "Adana": ["Aladağ", "Ceyhan", "Çukurova", "Feke", "İmamoğlu", "Karaisalı", "Karataş", "Kozan", "Pozantı", "Saimbeyli", "Sarıçam", "Seyhan", "Tufanbeyli", "Yumurtalık", "Yüreğir"],
    "Ankara": ["Akyurt", "Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere", "Çankaya", "Çubuk", "Elmadağ", "Etimesgut", "Evren", "Gölbaşı", "Güdül", "Haymana", "Kalecik", "Kahramankazan", "Keçiören", "Kızılcahamam", "Mamak", "Nallıhan", "Polatlı", "Pursaklar", "Sincan", "Şereflikoçhisar", "Yenimahalle"],
    "İstanbul": ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa", "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"],
    "İzmir": ["Aliağa", "Balçova", "Bayındır", "Bayraklı", "Bergama", "Beydağ", "Bornova", "Buca", "Çeşme", "Çiğli", "Dikili", "Foça", "Gaziemir", "Güzelbahçe", "Karabağlar", "Karaburun", "Karşıyaka", "Kemalpaşa", "Kınık", "Kiraz", "Konak", "Menderes", "Menemen", "Narlıdere", "Ödemiş", "Seferihisar", "Selçuk", "Tire", "Torbalı", "Urla"],
    "Bursa": ["Büyükorhan", "Gemlik", "Gürsu", "Harmancık", "İnegöl", "İznik", "Karacabey", "Keles", "Kestel", "Mudanya", "Mustafakemalpaşa", "Nilüfer", "Orhaneli", "Orhangazi", "Osmangazi", "Yenişehir", "Yıldırım"],
    "Ardahan": ["Merkez", "Çıldır", "Göle", "Hanak", "Posof", "Damal", "Ardanuç", "Karakurt"],
    "Kars": ["Merkez", "Arpaçay", "Digor", "Kağızman", "Selim", "Sarıkamış", "Susuz", "Akyaka"],
    "İğdır": ["Merkez", "Aralık", "Tuzluca", "Karakoyunlu"]
}

city_coords = {
    "İstanbul": (41.0082, 28.9784),
    "Ankara": (39.9208, 32.8541),
    "İzmir": (38.4192, 27.1287),
    "Bursa": (40.1828, 29.0665),
    "Adana": (37.0, 35.3213),
    "Ardahan": (41.1108, 42.7023),  # Ardahan koordinatları
    "Kars": (40.6167, 43.0667),  # Kars koordinatları
    "İğdır": (40.6242, 44.0404)  # Iğdır koordinatları

}
from geopy.geocoders import Nominatim
import time

def get_required_district_coords():
    geolocator = Nominatim(user_agent="truck_route_planner")
    coords = {}

    used_cities = sorted(set(p["City"] for p in products))  # Sadece kullanılanlar

    for full_name in used_cities:
        try:
            district, city = full_name.split(" - ")
            location = geolocator.geocode(f"{district}, {city}, Turkey")
            if location:
                coords[full_name] = (location.latitude, location.longitude)
                print(f"✅ {full_name} → {location.latitude}, {location.longitude}")
            else:
                print(f"❌ Not found: {full_name}")
            time.sleep(1)  # OpenStreetMap rate limit
        except Exception as e:
            print(f"⚠️ Error: {full_name} - {e}")
    return coords


def save_district_coords(coords, filename="district_coords.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(coords, f, indent=4)



themes = {
    "Light Default": {"bg": "#f0f0f0", "fg": "#000000", "button_bg": "#d9d9d9", "entry_bg": "#ffffff"},
    "Dark Mode": {"bg": "#121212", "fg": "#e0e0e0", "button_bg": "#333333", "entry_bg": "#1e1e1e"},
    "PyCharm Dracula": {"bg": "#282a36", "fg": "#f8f8f2", "button_bg": "#44475a", "entry_bg": "#44475a"},
    "Solarized Light": {"bg": "#fdf6e3", "fg": "#657b83", "button_bg": "#eee8d5", "entry_bg": "#eee8d5"},
    "Solarized Dark": {"bg": "#002b36", "fg": "#839496", "button_bg": "#073642", "entry_bg": "#073642"},
    "Monokai": {"bg": "#272822", "fg": "#f8f8f2", "button_bg": "#75715e", "entry_bg": "#ffffff"},
    "Gruvbox Dark": {"bg": "#282828", "fg": "#ebdbb2", "button_bg": "#3c3836", "entry_bg": "#3c3836"},
    "Nord": {"bg": "#2e3440", "fg": "#d8dee9", "button_bg": "#4c566a", "entry_bg": "#434c5e"},
    "One Dark": {"bg": "#282c34", "fg": "#abb2bf", "button_bg": "#3e4451", "entry_bg": "#3e4451"},
    "Sweet Pastel": {"bg": "#ffe4e1", "fg": "#5c5c5c", "button_bg": "#ffc0cb", "entry_bg": "#fff0f5"},
}



# Global değişkenler
search_var = tk.StringVar()
selected_city = tk.StringVar()
selected_district = tk.StringVar()
start_city = tk.StringVar()
truck_count = 1
truck_access_type = tk.StringVar(value="arka")  # <- Eklenecek!
rota_tipi_var = tk.StringVar(value="Automatic")


# === DİNAMİK RENK HARİTASI OLUŞTURMA ===
def generate_color(name):
    h = hashlib.md5(name.encode()).hexdigest()
    return f"#{h[:6]}"

def get_color_map():
    color_map = {}
    for city, districts in city_districts.items():
        for district in districts:
            full = f"{city} - {district}"
            color_map[full] = generate_color(full)
    return color_map

color_map = get_color_map()
route_order = list(color_map.keys())



def get_sorted_route(start_city):
    all_coords = get_required_district_coords()
    base_lat, base_lon = city_coords.get(start_city, (0, 0))

    # Sadece ürün olan ilçeler
    used_coords = {
        city: coord for city, coord in all_coords.items()
        if any(p["City"] == city for p in products)
    }

    sorted_route = sorted(
        used_coords.items(),
        key=lambda item: haversine(base_lat, base_lon, item[1][0], item[1][1])
    )

    return [k for k, _ in sorted_route]



def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    return R * 2 * asin(sqrt(a))




def log_placement(kod, sehir, x, y, w, h, rotated, manual, truck_number=1, z=0):
    placement_log.append({
        "Code": kod,
        "City": sehir,
        "X": x,
        "Y": y,
        "Dimension": f"{w}x{h}",
        "Rotated": "Yes" if rotated else "No",
        "Manually?": "Yes" if manual else "No",
        "Truck": truck_number,
        "Z": z
    })


def show_placement_log():
    log_win = tk.Toplevel()
    log_win.title("📋 Placement Log")
    log_win.geometry("700x500")

    # Yeni sütunlar eklendi: Tır ve Z
    columns = ("Code", "City", "Tır", "X", "Y", "Z", "Dimension", "Rotated", "Manually?")
    tree = ttk.Treeview(log_win, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for entry in placement_log:
        tree.insert("", tk.END, values=(
            entry["Code"],
            entry["City"],
            entry.get("Truck",1),
            entry["X"],
            entry["Y"],
            entry.get("Z", 0),
            entry["Dimension"],
            entry["Rotated"],
            entry["Manually?"]
        ))


def open_settings_window():
    def save_settings():
        global truck_length, truck_width,truck_height
        try:
            truck_length = int(length_entry.get())
            truck_width = int(width_entry.get())
            truck_height = int(height_entry.get())
            settings_win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    settings_win = tk.Toplevel()
    settings_win.title("⚙️ Settings")
    settings_win.configure(bg="#f0f4f7")
    tk.Label(settings_win, text="Truck Length (cm):", bg="#f0f4f7").grid(row=0, column=0, pady=5, padx=5)
    tk.Label(settings_win, text="Truck Width (cm):", bg="#f0f4f7").grid(row=1, column=0, pady=5, padx=5)
    tk.Label(settings_win, text="Truck Height (cm):", bg="#f0f4f7").grid(row=2, column=0, pady=5, padx=5)

    length_entry = tk.Entry(settings_win)
    width_entry = tk.Entry(settings_win)
    height_entry = tk.Entry(settings_win)
    length_entry.insert(0, str(truck_length))
    width_entry.insert(0, str(truck_width))
    height_entry.insert(0, str(truck_height))
    length_entry.grid(row=0, column=1, pady=5)
    width_entry.grid(row=1, column=1, pady=5)
    height_entry.grid(row=2, column=1, pady=5)


    tk.Button(settings_win, text="Save", command=save_settings).grid(row=4, column=0, columnspan=2, pady=10)

def load_from_excel():
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        required_cols = {
            "Code", "Width", "Length", "Height",
            "Quantity", "City", "Rotated", "MaxStack"
        }
        if not required_cols.issubset(df.columns):
            messagebox.showerror("Error", f"The Excel file must contain the following columns:\n{', '.join(required_cols)}"
            )
            return

        for _, row in df.iterrows():
            product = {
                "Code": row["Code"],
                "Width": float(row["Width"]),
                "Length": float(row["Length"]),
                "Height": float(row["Height"]),
                "Quantity": int(row["Quantity"]),
                "City": row["City"],
                "Rotated": bool(row["Rotated"]),
                "MaxStack": int(row["MaxStack"])
            }
            products.append(product)
            index = len(products)
            listbox.insert(
                tk.END,
                f"📦 Koli #{index} | 🆔 Code: {product['Code']} | 📏 {product['Width']}x{product['Length']} cm | 📦 Quantity: {product['Quantity']} | ↻ Can be Rotated?: {'✅' if product['Rotated'] else '❌'} | 🏷️ City: {product['City'].split(' - ')[0]} | 📍 District: {product['City'].split(' - ')[1]}"
            )
            listbox.itemconfig(tk.END, {'bg': '#ffffff', 'selectbackground': '#cce5ff'})

        messagebox.showinfo("Success", "Products successfully loaded from Excel!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def show_summary_report():
    def draw_bar():
        fig, ax = plt.subplots(figsize=(6, 4))
        city_counts = defaultdict(int)
        for p in products:
            city_counts[p["City"]] += p["Quantity"]

        labels = list(city_counts.keys())
        values = list(city_counts.values())

        ax.bar(range(len(labels)), values, color='skyblue')
        ax.set_title("Product Distribution by City")
        ax.set_ylabel("Quantity")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        return fig

    def draw_donut():
        fig, ax = plt.subplots(figsize=(6, 4))
        city_counts = defaultdict(int)
        for p in products:
            city_counts[p["City"]] += p["Quantity"]
        wedges, texts, autotexts = ax.pie(city_counts.values(), labels=city_counts.keys(), autopct='%1.1f%%', startangle=90)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title("Donut Chart: Percentage by City")
        return fig

    def draw_histogram():
        fig, ax = plt.subplots(figsize=(6, 4))
        heights = [p["Length"] for p in products for _ in range(p["Quantity"])]
        ax.hist(heights, bins=10, color='coral')
        ax.set_title("Histogram of Product Lengths")
        ax.set_xlabel("Length (cm)")
        ax.set_ylabel("Quantity")
        return fig

    def draw_summary_box(master):
        total_products = sum(p["Quantity"] for p in products)
        lbl = tk.Label(master, text=f"Total Loaded Products: {total_products} items", font=("Segoe UI", 11, "bold"), fg="darkgreen")
        lbl.pack(pady=5)

    summary_win = tk.Toplevel()
    summary_win.title("📊 Loading Summary")

    chart_type = tk.StringVar(value="Bar")

    def update_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()
        if chart_type.get() == "Bar":
            fig = draw_bar()
        elif chart_type.get() == "Donut":
            fig = draw_donut()
        else:
            fig = draw_histogram()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    draw_summary_box(summary_win)
    tk.Label(summary_win, text="Graph Type:").pack()
    chart_options = ttk.Combobox(summary_win, textvariable=chart_type, values=["Bar", "Donut", "Histogram"])
    chart_options.pack()
    tk.Button(summary_win, text="Show", command=update_chart).pack(pady=5)

    chart_frame = tk.Frame(summary_win)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    update_chart()



def show_sustainability_report_with_icons(products, truck_length=1360, truck_width=240, truck_height=270):
    # products → placements dönüştür
    placements = []
    for p in products:
        for _ in range(p["Quantity"]):
            placements.append((0, 0, p["Width"], p["Length"], 0, p["Code"], p["City"], p.get("Rotated", False), p["Height"]))


    # Hesaplama
    truck_volume = truck_length * truck_width * truck_height
    total_box_volume = sum(w * h * height for (_, _, w, h, _, _, _, _, height) in placements)
    utilization = (total_box_volume / truck_volume) * 100
    est_trips = round(total_box_volume / (truck_volume * 0.8), 1)
    co2 = est_trips * 1.2 * 1000
    trees = (co2 / 1000) * 50

    # Bilgiler
    report = [
        ("📦 Total Box Volume", f"{round(total_box_volume / 1e6, 2)} m³"),
        ("🚛 Truck Volume", f"{round(truck_volume / 1e6, 2)} m³"),
        ("📊 Volume Utilization", f"{round(utilization, 2)} %"),
        ("🚌 Estimated Number of Trips", f"{est_trips}"),
        ("🌍 CO₂ Emissions", f"{round(co2, 1)} kg"),
        ("🌳 Tree Equivalent", f"{round(trees, 1)} trees")
    ]

    # Create window
    root = tk.Toplevel()
    root.title("🌱 Sustainability Report")
    root.geometry("460x400")
    root.configure(bg="#f4fdf4")

    # Title and description
    tk.Label(root, text="🌿 Sustainability Report", font=("Segoe UI", 16, "bold"),
             fg="#2e7d32", bg="#f4fdf4").pack(pady=15)

    tk.Label(root, text="This loading operation has been evaluated in terms of environmental impact.",
             font=("Segoe UI", 10), bg="#f4fdf4", fg="#4a4a4a").pack(pady=(0, 10))

    # Info box
    box = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    box.pack(padx=20, pady=10, fill="both", expand=True)

    for label, value in report:
        row = tk.Frame(box, bg="#ffffff")
        row.pack(fill="x", pady=5, padx=10)
        tk.Label(row, text=label, font=("Segoe UI", 11, "bold"), anchor="w", bg="#ffffff", fg="#2e7d32").pack(
            side="left")
        tk.Label(row, text=value, font=("Segoe UI", 11), anchor="e", bg="#ffffff").pack(side="right")

    # Closing message
    tk.Label(root, text="Thank you for contributing to green logistics 🌱",
             font=("Segoe UI", 9, "italic"), fg="#2e7d32", bg="#f4fdf4").pack(pady=(10, 0))

    ttk.Button(root, text="Close", command=root.destroy).pack(pady=10)


"""def simulate_email_send(dummy_file_path):
    win = tk.Toplevel()
    win.title("📧 Email Simulation")
    win.geometry("400x200")

    tk.Label(win, text="Recipient Email Address:").pack(pady=5)
    email_entry = tk.Entry(win, width=40)
    email_entry.pack()

    def fake_send():
        email = email_entry.get()
        if "@" not in email:
            messagebox.showerror("Error", "Invalid email address.")
            return
        messagebox.showinfo("Simulation", f"The file {file_path} was sent to {email} (fake).")
        win.destroy()

    tk.Button(win, text="Send", command=fake_send).pack(pady=10)"""


# === PDF RAPORLAMA FONKSİYONU ===
def export_pdf_report(fig, total_items, elapsed_time, company_name):
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF File", "*.pdf")],
            title="Save as PDF"
        )
        if not file_path:
            return

        # Save figure to memory buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150)
        buf.seek(0)

        # Create PDF
        c = pdfcanvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Company name and report title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Company: {company_name}")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, f"Truck Loading Report - Duration: {elapsed_time:.2f} seconds")
        c.drawString(50, height - 90, f"Total Number of Items: {total_items}")

        # Insert image (bottom section)
        img = ImageReader(buf)
        c.drawImage(img, 50, 200, width=500, preserveAspectRatio=True, mask='auto')

        # Finalize PDF
        c.save()
        messagebox.showinfo("Success", "PDF saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF:\n{e}")


   #simulate_email_send(dummy_file_path)


# === PDF SORUSU EKLİ FONKSİYON ===
def ask_and_export_pdf(fig, total_items, elapsed_time):
    answer = messagebox.askyesno("Create PDF?", "Would you like to export the loading report as a PDF?")
    if answer:
        company_name = simpledialog.askstring("Company Name", "Please enter the company name:")
        if company_name:
            export_pdf_report(fig, total_items, elapsed_time, company_name)
        else:
            messagebox.showwarning("Warning", "PDF could not be generated because the company name was not provided.")


def export_labels_as_individual_files(placements, manual_placements):
    folder = filedialog.askdirectory(title="Select folder to save labels")
    if not folder:
        return

    try:
        for idx, (x, y, w, h, z, code, city, rotated, height) in enumerate(placements):
            manual = any(
                px == x and py == y and pw == w and ph == h and pkod == code
                for (px, py, pw, ph, pkod, pcity, prot) in manual_placements
            )

            # 📛 Safe filename
            safe_code = "".join(c if c.isalnum() else "_" for c in code)
            file_path = f"{folder}/label_{idx+1}_{safe_code}.pdf"

            c = pdfcanvas.Canvas(file_path, pagesize=A6)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(10 * mm, 90 * mm, f"Code: {code}")
            c.setFont("Helvetica", 10)
            c.drawString(10 * mm, 85 * mm, f"City: {city}")
            c.drawString(10 * mm, 80 * mm, f"Size: {w}x{h} cm")
            c.drawString(10 * mm, 75 * mm, f"Position: ({x}, {y})")
            rotated_text = "Yes" if rotated else "No"
            c.drawString(10 * mm, 70 * mm, f"Rotated: {rotated_text}")
            c.drawString(10 * mm, 65 * mm, f"Placement: {'Manual' if manual else 'Automatic'}")

            barcode = code128.Code128(code, barHeight=20 * mm, barWidth=0.5)
            barcode.drawOn(c, 10 * mm, 40 * mm)

            qr = QrCodeWidget(code)
            bounds = qr.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            d = Drawing(40, 40, transform=[40. / width, 0, 0, 40. / height, 0, 0])
            d.add(qr)
            renderPDF.draw(d, c, 100 * mm, 35 * mm)

            c.showPage()
            c.save()

        messagebox.showinfo("Success", f"Labels successfully saved to folder: {folder}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate label files:\n{e}")

def show_color_legend():
    legend_win = tk.Toplevel()
    legend_win.title("🎨 Color Legend")
    legend_win.geometry("300x400")
    legend_win.configure(bg="white")

    canvas = tk.Canvas(legend_win, bg="white", bd=0, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(legend_win, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame, anchor='nw')

    for city, color in color_map.items():
        lbl = tk.Label(frame, text=city, bg=color, fg="black", anchor="w", padx=5)
        lbl.pack(fill=tk.X, pady=2, padx=4)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def show_box_location():
    code = simpledialog.askstring("📦 Box Code", "Enter the code of the box you want to search for:")
    if not code:
        return

    matching = [p for p in placement_log if p["Code"] == code]
    if not matching:
        messagebox.showinfo("No Results", f"No box found with code '{code}'.")
        return

    info = ""
    for p in matching:
        info += (
            f"🆔 Code: {p['Code']}\n"
            f"🚛 Truck No: {p.get('Truck', 1)}\n"
            f"📍 Coordinates: ({p['X']}, {p['Y']}, Z={p.get('Z', 0)})\n"
            f"📏 Dimension: {p['Dimension']}\n"
            f"↻ Rotated: {p['Rotated']}\n"
            f"⚙️ Placement: {'Manual' if p['Manually?'] else 'Automatic'}\n\n"
        )

    messagebox.showinfo("Box Location", info.strip())


def draw_loaded_full_placements():
    if not placement_log:
        messagebox.showinfo("Info", "No saved placement found yet.")
        return

    # === Tırları ayır ===
    trucks_by_index = defaultdict(list)
    for entry in placement_log:
        truck_num = entry.get("Truck", 1)  # Eğer tır numarası logda yoksa 1 olarak al
        trucks_by_index[truck_num].append(entry)

    def draw_truck(truck_entries, truck_index):
        fig, ax = plt.subplots(figsize=(truck_length / 50 + 4, truck_width / 50))
        ax.set_xlim(0, truck_length)
        ax.set_ylim(0, truck_width)
        ax.set_xticks(np.arange(0, truck_length + 1, 200))
        ax.set_yticks(np.arange(0, truck_width + 1, 50))
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.set_aspect('equal')
        ax.set_title(f"Loading Layout for Truck {truck_index}")


        stack_counter = defaultdict(int)
        for entry in truck_entries:
            x = entry["X"]
            y = entry["Y"]
            key = (x, y)
            stack_counter[key] += 1

        for entry in truck_entries:
            x = entry["X"]
            y = entry["Y"]
            w, h = map(int, entry["Dimension"].split('x'))
            kod = entry["Code"]
            city = entry["City"]
            rotated = (entry["Rotated"] == "Yes")
            z = entry.get("Z", 0)

            rect = plt.Rectangle((x, y), w, h, edgecolor="black", facecolor=color_map.get(city, "#cccccc"), lw=1)
            ax.add_patch(rect)

            label = f"{kod}{'*' if rotated else ''}"
            ax.text(x + w / 2, y + h / 2, label, fontsize=8, ha='center', va='center')

            count = stack_counter[(x, y)]
            if count > 1:
                top_z = max(e.get("Z", 0) for e in truck_entries if e["X"] == x and e["Y"] == y)
                if z == top_z:
                    ax.text(x + w / 2, y + h + 10, f"x{count}", fontsize=9, ha='center', va='bottom', weight='bold')

        # Renk Efsanesi
        legend_labels = {}
        for entry in truck_entries:
            city = entry["City"]
            if city not in legend_labels:
                legend_labels[city] = color_map.get(city, "#cccccc")

        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor=legend_labels[city]) for city in legend_labels
        ]
        ax.legend(
            legend_elements, list(legend_labels.keys()),
            title="Cities", loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8
        )

        plt.tight_layout()
        plt.show()


    # === Her tır için ayrı ayrı çiz ===
    for index, entries in trucks_by_index.items():
        draw_truck(entries, index)


def show_truck_canvas_window():
    window = tk.Toplevel()
    window.title("🚛 Truck Visualization Panel")


    selected_truck = tk.StringVar()
    selected_truck.set("Truck 1")

    dropdown = ttk.Combobox(window, textvariable=selected_truck, values=[f"Truck {i+1}" for i in range(len(trucks))])
    dropdown.pack(pady=10)

    canvas_frame = tk.Frame(window)
    canvas_frame.pack(fill="both", expand=True)

    fig, ax = plt.subplots(figsize=(truck_length / 50 + 4, truck_width / 50))
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_selected_truck(event=None):
        truck_index = int(selected_truck.get().split()[-1]) - 1
        truck = trucks[truck_index]

        ax.clear()
        ax.set_title(f"Loading Plan for {selected_truck.get()}")
        ax.set_xlim(0, truck_length)
        ax.set_ylim(0, truck_width)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', linewidth=0.5)

        stack_counter = defaultdict(int)
        for (x, y, _, _, _, _, _, _, _) in truck:
            stack_counter[(x, y)] += 1

        for (x, y, w, h, z, kod, city, rotated, yukseklik) in truck:
            rect = plt.Rectangle((x, y), w, h, edgecolor="black", facecolor=color_map[city], lw=1)
            ax.add_patch(rect)
            label = f"{kod}{'*' if rotated else ''}"
            ax.text(x + w/2, y + h/2, label, fontsize=8, ha='center', va='center')

            count = stack_counter[(x, y)]
            if count > 1:
                top_z = max(pz for (px, py, _, _, pz, _, _, _, _) in truck if px == x and py == y)
                if z == top_z:
                    ax.text(x + w / 2, y + h + 10, f"x{count}", fontsize=9, ha='center', va='bottom', weight='bold')

        for (fx, fy, fw, fh) in forbidden_zones:
            rect = plt.Rectangle((fx, fy), fw, fh, facecolor='gray', edgecolor='black', hatch='//', lw=1)
            ax.add_patch(rect)

        canvas.draw_idle()

    dropdown.bind("<<ComboboxSelected>>", draw_selected_truck)
    draw_selected_truck()  # ilk tırla başla

    window.mainloop()


def save_data():
    try:
        data_to_save = {
            "products": products,
            "manual_placements": manual_placements,
            "placement_log": placement_log,
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Dosyaları", "*.json")], title="Veriyi Kaydet")
        if not file_path:
            return
        with open(file_path, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)
        messagebox.showinfo("✅ Başarılı", "Veriler başarıyla kaydedildi!")
    except Exception as e:
        messagebox.showerror("❌ Hata", f"Veri kaydedilemedi:\n{e}")

# Verileri JSON formatında yükleme fonksiyonu
def load_data():
    try:
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Dosyaları", "*.json")], title="Veri Yükle")
        if not file_path:
            return
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            # Kaydedilen verileri geri yükleme
            global products, manual_placements, placement_log
            products = data.get("products", [])
            manual_placements = data.get("manual_placements", [])
            placement_log = data.get("placement_log", [])
            messagebox.showinfo("Başarılı", "Veriler başarıyla yüklendi!")
            refresh_listbox()  # Listeyi güncelle
    except Exception as e:
        messagebox.showerror("Hata", f"Veri yüklenemedi:\n{e}")

# Listeyi güncelleme fonksiyonu
def refresh_listbox():
    listbox.delete(0, tk.END)

    for i, p in enumerate(products):
        try:
            sehir_il = p['City'].split(' - ')[0]
            sehir_ilce = p['City'].split(' - ')[1]
        except IndexError:
            sehir_il = p['City']
            sehir_ilce = "Unknown"

        label = (
            f"📦 Koli #{i+1} | "
            f"🆔 Code: {p['Code']} | "
            f"📏 {p['Width']}x{p['Length']}xp{['Height']} cm | "
            f"📦 Quantity: {p['Quantity']} | "
            f"↻ Can be Rotated: {'✅' if p.get('Rotated', False) else '❌'} | "
            f"🏷️ City: {sehir_il} | "
            f"📍 District: {sehir_ilce} | "
            f"🗃️ Max Stack Count: {p.get('Max Stack Count', 1)}"
        )

        listbox.insert(tk.END, label)
        listbox.itemconfig(tk.END, {'bg': '#ffffff', 'selectbackground': '#cce5ff'})


from matplotlib import cm
import matplotlib.pyplot as plt
manual_route_list = []

def open_manual_route_window():
    win = tk.Toplevel()
    win.title("🗺️ Set Manual Route")
    win.geometry("300x400")

    # Listbox
    listbox = tk.Listbox(win, selectmode=tk.SINGLE)
    listbox.pack(expand=True, fill="both", padx=10, pady=10)

    # 🔥 Şehirleri ekle
    unique_cities = sorted(set(item["City"] for item in products))
    for city in unique_cities:
        listbox.insert(tk.END, city)

    # 🎯 Drag & Drop işlemleri
    drag_data = {"index": None}

    def on_drag_start(event):
        widget = event.widget
        drag_data["index"] = widget.nearest(event.y)

    def on_drag_motion(event):
        widget = event.widget
        i = widget.nearest(event.y)
        if i != drag_data["index"]:
            items = list(widget.get(0, tk.END))
            dragged_item = items.pop(drag_data["index"])
            items.insert(i, dragged_item)
            widget.delete(0, tk.END)
            for item in items:
                widget.insert(tk.END, item)
            drag_data["index"] = i

    listbox.bind("<ButtonPress-1>", on_drag_start)
    listbox.bind("<B1-Motion>", on_drag_motion)

    # ✅ Rota Kaydet
    def save_manual_route():
        global manual_route_list
        manual_route_list = list(listbox.get(0, tk.END))
        win.destroy()
        messagebox.showinfo("✅ Saved", "📍 Manual Route Order:\n\n" + "\n".join(manual_route_list))

    btn_save = ttk.Button(win, text="✅ Save Route", command=save_manual_route)
    btn_save.pack(pady=5)


def start_placement():
    start_time = time.time()
    global placements, trucks, forbidden_zones, placement_log
    from collections import Counter
    # 💣 Önce temizle
    placements = []
    trucks = []
    placement_log.clear()

    # 🔍 Debug satırları burada
    print("MANUAL:", len(manual_placements))
    print("LOG BEFORE:", len(placement_log))
    print("PRODUCT COUNTS:", Counter([p["Code"] for p in products]))
    print("DEBUG PRODUCT COUNTS:", Counter([p["Code"] for p in products]))



    selected_start_city = start_city.get()
    if not selected_start_city:
        messagebox.showerror("Error", "Please choose the starting city for the route.")
        return

    route_order = get_sorted_route(selected_start_city)
    print(route_order)
    delivery_data = defaultdict(lambda: defaultdict(int))

    for item in products:
        delivery_data[item["City"]][item["Code"]] += item["Quantity"]

    grouped_items = []
    for city in route_order:
        items = []
        for kod, adet in delivery_data[city].items():
            for item in products:
                if item["Code"] == kod:
                    items.append({
                        "Code": item["Code"],
                        "Width": item["Width"],
                        "Length": item["Length"],
                        "Height": item["Height"],
                        "Quantity": adet,
                        "City": city,
                        "Rotated": item.get("Rotated", False),
                        "MaxStack": item.get("Max Stack Count", 1)
                    })
                    break
        grouped_items.append((city, items))

    forbidden_zones = []
    forbidden_zones_array = np.zeros((truck_width, truck_length))
    for fx, fy, fw, fh in forbidden_zones:
        forbidden_zones_array[fy:fy+fh, fx:fx+fw] = 1

    for (x, y, w, h, kod, city, rotated) in manual_placements:
        placements.append((x, y, w, h, 0, kod, city, rotated, 100))

    remaining_items = []
    for city, items in grouped_items:
        for item in items:
            for _ in range(item["Quantity"]):
                remaining_items.append(item)

    truck_index = 1

    while remaining_items:
        print(f"🚛 Loading Truck {truck_index}...")
        occupied = np.zeros((truck_width, truck_length))
        current_truck = []
        unplaced = []

        # Stack bilgileri
        stack_map = defaultdict(int)         # (kod, x, y) → count
        stack_height_map = defaultdict(int)  # (kod, x, y) → total height
        box_base_size = {}                   # (kod, x, y) → (w, h)

        for item in remaining_items:
            en = int(item["Width"])
            boy = int(item["Length"])
            yukseklik = int(item["Height"])
            kod = item["Code"]
            city = item["City"]
            rotated_allowed = item.get("Rotated", False)
            max_stack = item.get("MaxStack", 1)

            orientations = [(boy, en, True)] if rotated_allowed else []
            orientations.append((en, boy, False))

            placed = False

            # 👇 1. Mevcut pozisyonlarda stack denemesi
            for (sx, sy, sw, sh, sz, skod, scity, srot, shy) in current_truck:
                if skod != kod:
                    continue
                key = (kod, sx, sy)
                if stack_map[key] >= max_stack:
                    continue
                if stack_height_map[key] + yukseklik > truck_height:
                    continue
                if box_base_size.get(key, (sw, sh)) != (sw, sh):
                    continue

                z = stack_height_map[key]
                stack_map[key] += 1
                stack_height_map[key] += yukseklik
                box_base_size[key] = (sw, sh)
                current_truck.append((sx, sy, sw, sh, z, kod, city, srot, yukseklik))
                placements.append((sx, sy, sw, sh, z, kod, city, srot, yukseklik))
                #log_placement(kod, city, sx, sy, sw, sh, srot, manual=False, z=z)
                log_placement(kod, city, sx, sy, sw, sh, srot, manual=False, z=z, truck_number=truck_index)

                placed = True
                break

            if placed:
                continue  # stacking yaptıysa geç

            # 👇 2. Yeni boş yer araması
            best_score = -1
            best_pos = None

            for h, w, rotated in orientations:
                for y in range(truck_width - h + 1):
                    for x in range(truck_length - w + 1):
                        if occupied[y:y+h, x:x+w].sum() != 0 or forbidden_zones_array[y:y+h, x:x+w].sum() != 0:
                            continue
                        score = ((w * h) / (truck_width * truck_length)) * 10000 + (x / truck_length * 500)
                        if score > best_score:
                            best_score = score
                            best_pos = (x, y, w, h, rotated)

            if best_pos:
                x, y, w, h, rotated = best_pos
                z = 0
                key = (kod, x, y)

                stack_map[key] = 1
                stack_height_map[key] = yukseklik
                box_base_size[key] = (w, h)

                occupied[y:y+h, x:x+w] = 1
                current_truck.append((x, y, w, h, z, kod, city, rotated, yukseklik))
                placements.append((x, y, w, h, z, kod, city, rotated, yukseklik))
                #log_placement(kod, city, x, y, w, h, rotated, manual=False, z=z)
                log_placement(kod, city, x, y, w, h, rotated, manual=False, z=z, truck_number=truck_index)

            else:
                unplaced.append(item)

        if not current_truck:
            messagebox.showerror("❌ Placement Error", f"Truck {truck_index}: No items could be placed!")
            break

        trucks.append(current_truck)
        remaining_items = unplaced
        truck_index += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    total_items = sum(p["Quantity"] for p in products)
    used_area = sum(w * h for (_, _, w, h, _, _, _, _, _) in placements)
    total_area = truck_length * truck_width * len(trucks)
    usage_pct = (used_area / total_area) * 100
    rotated_count = sum(1 for (_, _, _, _, _, _, _, rotated, _) in placements if rotated)

    messagebox.showinfo(
        "📊 Placement Report",
        f"🚛 Trucks Used: {len(trucks)}\n📦 Total Items: {total_items}\n🔁 Rotated: {rotated_count}\n📐 Used Area: {used_area} / {total_area} cm²\n🎯 Usage: %{usage_pct:.2f}\n⏱️ Time: {elapsed_time:.2f} s"
    )

    # 🔲 Her tır için 2D çizim + PDF + Tooltip
    for i, truck in enumerate(trucks):
        fig, ax = plt.subplots(figsize=(truck_length / 50 + 4, truck_width / 50))
        ax.set_title(f"Truck {i+1} Loading Plan")
        ax.set_xlim(0, truck_length)
        ax.set_ylim(0, truck_width)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', linewidth=0.5)

        stack_counter = defaultdict(int)
        for (x, y, _, _, _, _, _, _, _) in truck:
            stack_counter[(x, y)] += 1

        for (x, y, w, h, z, kod, city, rotated, yukseklik) in truck:
            rect = plt.Rectangle((x, y), w, h, edgecolor="black", facecolor=color_map.get(city, "#cccccc"), lw=1)
            ax.add_patch(rect)

            label = f"{kod}{'*' if rotated else ''}"
            ax.text(x + w / 2, y + h / 2, label, fontsize=8, ha='center', va='center')

            count = stack_counter[(x, y)]
            if count > 1:
                top_z = max(pz for (px, py, _, _, pz, _, _, _, _) in truck if px == x and py == y)
                if z == top_z:
                    ax.text(x + w / 2, y + h + 10, f"x{count}", fontsize=9, ha='center', va='bottom', weight='bold')

        for (fx, fy, fw, fh) in forbidden_zones:
            rect = plt.Rectangle((fx, fy), fw, fh, facecolor='gray', edgecolor='black', hatch='//', lw=1)
            ax.add_patch(rect)

        legend_labels = {city: color_map.get(city, "#cccccc") for (_, _, _, _, _, _, city, _, _) in truck}
        legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=color) for city, color in legend_labels.items()]
        ax.legend(legend_elements, list(legend_labels.keys()), title="Cities", loc='center left', bbox_to_anchor=(1.01, 0.5))

        total_items = sum(p["Quantity"] for p in products)
        ask_and_export_pdf(fig, total_items, elapsed_time)

        cursor = mplcursors.cursor(hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target
            for (px, py, pw, ph, pz, kod, city, rotated, _) in placements:
                if px <= x <= px + pw and py <= y <= py + ph:
                    is_manual = any(
                        mx == px and my == py and mw == pw and mh == ph and mkod == kod
                        for (mx, my, mw, mh, mkod, mcity, mrot) in manual_placements
                    )
                    yerlesim_tipi = "✅ Elle yerleştirildi" if is_manual else "⚙️ Otomatik yerleştirildi"
                    donduruldu_mu = "🔁 Yes" if rotated else "🚫 No"
                    sel.annotation.set(
                        text=(f"✓ Code: {kod}\n"
                              f" Dimension: {pw}x{ph} cm\n"
                              f" City: {city}\n"
                              f"↻ Rotated: {donduruldu_mu}\n"
                              f" {yerlesim_tipi}")
                    )
                    sel.annotation.get_bbox_patch().set(fc="#fffbe6", alpha=0.95)

                    highlight = plt.Rectangle((px, py), pw, ph, edgecolor="gold", linewidth=2.5, facecolor="none", linestyle="--")
                    ax.add_patch(highlight)
                    fig.canvas.draw_idle()
                    break

        plt.tight_layout()
        plt.show()

    kullanılan_alan = sum(w * h for (_, _, w, h, _, _, _, _, _) in placements)
    toplam_alan = truck_length * truck_width * len(trucks)
    doluluk_yuzdesi = (kullanılan_alan / toplam_alan) * 100
    rotated_count = sum(1 for (_, _, _, _, _, _, _, rotated, _) in placements if rotated)

    yerlesemeyenler = [(item["Code"], item["City"]) for item in remaining_items]

    message = (
        f"📦 Placement Completed!\n\n"
        f"🚛 Number of Trucks Used: {len(trucks)}\n"
        f"🔢 Total Number of Items: {total_items}\n"
        f"🔁 Rotated Items: {rotated_count}\n"
        f"📐 Used Area: {kullanılan_alan} / {toplam_alan} cm²\n"
        f"🎯 Fill Rate: %{doluluk_yuzdesi:.2f}\n"
        f"⏱️ Processing Time: {elapsed_time:.2f} seconds\n"
    )
    message += (
        f"\n🚫 Unplaced Boxes: {len(yerlesemeyenler)}" if yerlesemeyenler
        else "\n✅ All products have been successfully placed"
    )

    messagebox.showinfo("📊 Placement Report", message)

    if yerlesemeyenler:
        def show_unplaced():
            win = tk.Toplevel()
            win.title("🚫 Unplaced Boxes")
            win.geometry("400x300")
            text = tk.Text(win, wrap="word")
            text.pack(expand=True, fill="both", padx=10, pady=10)
            text.insert("end", "Code | City\n" + "-"*30 + "\n")
            for kod, city in yerlesemeyenler:
                text.insert("end", f"{kod} | {city}\n")
            text.config(state="disabled")

        ttk.Button(tools_box, text="📋 Unplaced Boxes:", command=show_unplaced).pack(fill="x", pady=2)

    draw_3d_truck_realistic(placements, truck_length, truck_width, truck_height=300)

    import threading
    threading.Thread(
        target=draw_3d_truck_with_full_animation,
        args=(placements, truck_length, truck_width),
        kwargs={"truck_height": 300},
        daemon=True
    ).start()

    choose_visual_mode(placements)



# === ÜRÜN EKLEME ===
donme_var = tk.BooleanVar(value=False)
def add_product():
    try:
        kod = kod_entry.get()
        en = float(en_entry.get())
        boy = float(boy_entry.get())
        yukseklik = float(yukseklik_entry.get())
        adet = int(adet_entry.get())
        istif = int(istif_entry.get())
        city = selected_city.get()
        district = selected_district.get()

        if not city or not district:
            messagebox.showerror("Error", "Please make sure to select a city and a district.")
            return

        sehir = f"{city} - {district}"
        donme_izin = donme_var.get()

        product = {
            "Code": kod,
            "Width": en,
            "Length": boy,
            "Quantity": adet,
            "City": sehir,
            "Rotated": donme_izin,
            "Height": yukseklik,
            "Max Stack Count": istif
        }

        products.append(product)
        index = len(products)
        listbox.insert(
            tk.END,
            f"📦 Koli #{index} | 🆔 Code: {kod} | 📏 {en}x{boy}x{yukseklik} cm | 📦 Quantity: {adet} | ↻ Can be Rotated: {'✅' if donme_izin else '❌'} | 🏷️ City: {city} | 📍 District: {district} | 🧱 Max Stack Count: {istif}"
        )
        listbox.itemconfig(tk.END, {'bg': '#ffffff', 'selectbackground': '#cce5ff'})

        for entry in [kod_entry, en_entry, boy_entry, yukseklik_entry, adet_entry, istif_entry]:
            entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values")



def draw_3d_truck_realistic(placements, truck_length, truck_width, truck_height=300):
    import pyvista as pv
    from matplotlib import cm


    plotter = pv.Plotter(window_size=(1400, 800), notebook=False)
    plotter.set_background("white")
    cmap = cm.get_cmap("tab20")

    def set_isometric_view():
        plotter.camera_position = [(truck_length / 2, -1400, 500),
                                   (truck_length / 2, truck_width / 2, 150),
                                   (0, 0, 1)]
    def set_top_view():
        plotter.camera_position = [(truck_length / 2, truck_width / 2, 1500),
                                   (truck_length / 2, truck_width / 2, 0),
                                   (0, 1, 0)]
    def set_right_view():
        plotter.camera_position = [(truck_length + 1000, truck_width / 2, truck_height / 2),
                                   (truck_length / 2, truck_width / 2, truck_height / 2),
                                   (0, 0, 1)]
    def set_front_view():
        plotter.camera_position = [(truck_length / 2, truck_width + 1000, truck_height / 2),
                                   (truck_length / 2, truck_width / 2, truck_height / 2),
                                   (0, 0, 1)]

    set_isometric_view()
    plotter.enable_eye_dome_lighting()

    light = pv.Light()
    light.set_direction_angle(45, -30)
    light.intensity = 0.9
    light.ambient = 0.4
    plotter.add_light(light)

    wall_thickness = 10
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, 0, truck_width, 0, 5)), color="gray", opacity=0.4)
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, 0, wall_thickness, 0, truck_height)), color="white", opacity=0.1)
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, truck_width - wall_thickness, truck_width, 0, truck_height)), color="white", opacity=0.1)
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, 0, truck_width, truck_height - 5, truck_height)), color="white", opacity=0.05)
    plotter.add_mesh(pv.Box(bounds=(truck_length - 5, truck_length, 0, truck_width, 0, truck_height)), color="gray", opacity=0.15)

    for x in range(0, truck_length, 150):
        beam = pv.Box(bounds=(x, x + 4, truck_width / 2 - 8, truck_width / 2 + 8, -10, 0))
        plotter.add_mesh(beam, color="black", opacity=0.5)

    wheel_positions = [
        (100, -25), (130, -25), (truck_length - 100, -25), (truck_length - 130, -25),
        (100, truck_width + 25), (130, truck_width + 25),
        (truck_length - 100, truck_width + 25), (truck_length - 130, truck_width + 25)
    ]
    for x, y in wheel_positions:
        outer = pv.Cylinder(center=(x, y, 22), direction=(0, 1, 0), radius=30, height=20)
        inner = pv.Cylinder(center=(x, y, 22), direction=(0, 1, 0), radius=15, height=22)
        plotter.add_mesh(outer, color="black")
        plotter.add_mesh(inner, color="dimgray")

    cab_main = pv.Box(bounds=(-140, 0, truck_width / 4, truck_width * 3 / 4, 0, truck_height / 1.8))
    cab_front = pv.Box(bounds=(-160, -140, truck_width / 4, truck_width * 3 / 4, truck_height / 4, truck_height / 1.8))
    glass = pv.Box(bounds=(-155, -140, truck_width / 4, truck_width * 3 / 4, truck_height / 2.5, truck_height / 1.8))
    step1 = pv.Box(bounds=(-140, -130, truck_width / 2 - 10, truck_width / 2 + 10, -10, -5))
    step2 = pv.Box(bounds=(-140, -130, truck_width / 2 - 10, truck_width / 2 + 10, -15, -10))

    plotter.add_mesh(cab_main, color='silver')
    plotter.add_mesh(cab_front, color='gray')
    plotter.add_mesh(glass, color='blue', opacity=0.5)
    plotter.add_mesh(step1, color='darkgray')
    plotter.add_mesh(step2, color='darkgray')

    # === Kutular ===
    label_dict = {}
    for (x, y, w, h, z, kod, city, rotated, yukseklik) in placements:
        #bounds = (truck_length - x - w, truck_length - x, y, y + h, z, z + yukseklik)
        bounds = (x, x + w, y, y + h, z, z + yukseklik)

        box = pv.Box(bounds=bounds)
        color = cmap((hash(city) % 20) / 20)
        plotter.add_mesh(box, color=color, opacity=0.1, show_edges=True, edge_color="black")
        label_dict[id(box)] = f"📦 {kod} | {city} ({w}x{h}x{yukseklik} cm)"

    text_actor = plotter.add_text("", position='upper_right', font_size=10, color="black")

    def hover_callback(picked_mesh):
        if picked_mesh is not None:
            key = id(picked_mesh)
            if key in label_dict:
                text_actor.SetText(0, label_dict[key])
            else:
                text_actor.SetText(0, "❔ Bilgi bulunamadı")
        else:
            text_actor.SetText(0, "")

    plotter.enable_cell_picking(callback=hover_callback, through=False, show_message=False)

    plotter.add_text("📌 Click on a box to view its details", position='lower_edge', font_size=9)
    plotter.add_text("Camera Views: [T] Top • [I] Isometric • [R] Right • [F] Front", position='upper_edge',font_size=9)

    plotter.add_key_event("i", set_isometric_view)
    plotter.add_key_event("t", set_top_view)
    plotter.add_key_event("r", set_right_view)
    plotter.add_key_event("f", set_front_view)

    plotter.add_axes()
    plotter.show_grid(color="lightgray")
    plotter.reset_camera()
    plotter.camera.zoom(1.5)
    plotter.show()



from tkinter import Toplevel, Label
import pyvista as pv
import matplotlib.pyplot as plt
import random
import time


def draw_3d_truck_realistic_animated(placements, truck_length, truck_width, truck_height=300, delay=0.3):
    import pyvista as pv
    from matplotlib import cm
    import time

    plotter = pv.Plotter(window_size=(1400, 800), notebook=False)
    plotter.set_background("white")
    cmap = cm.get_cmap("tab20")

    # === Build truck FIRST ===
    wall_thickness = 10
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, 0, truck_width, 0, 5)), color="gray", opacity=0.4)
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, 0, wall_thickness, 0, truck_height)), color="white", opacity=0.1)
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, truck_width - wall_thickness, truck_width, 0, truck_height)), color="white", opacity=0.1)
    plotter.add_mesh(pv.Box(bounds=(0, truck_length, 0, truck_width, truck_height - 5, truck_height)), color="white", opacity=0.05)
    plotter.add_mesh(pv.Box(bounds=(truck_length - 5, truck_length, 0, truck_width, 0, truck_height)), color="gray", opacity=0.15)

    for x in range(0, truck_length, 150):
        beam = pv.Box(bounds=(x, x + 4, truck_width / 2 - 8, truck_width / 2 + 8, -10, 0))
        plotter.add_mesh(beam, color="black", opacity=0.5)

    wheel_positions = [
        (100, -25), (130, -25), (truck_length - 100, -25), (truck_length - 130, -25),
        (100, truck_width + 25), (130, truck_width + 25),
        (truck_length - 100, truck_width + 25), (truck_length - 130, truck_width + 25)
    ]
    for x, y in wheel_positions:
        outer = pv.Cylinder(center=(x, y, 22), direction=(0, 1, 0), radius=30, height=20)
        inner = pv.Cylinder(center=(x, y, 22), direction=(0, 1, 0), radius=15, height=22)
        plotter.add_mesh(outer, color="black")
        plotter.add_mesh(inner, color="dimgray")

    cab_main = pv.Box(bounds=(-140, 0, truck_width / 4, truck_width * 3 / 4, 0, truck_height / 1.8))
    cab_front = pv.Box(bounds=(-160, -140, truck_width / 4, truck_width * 3 / 4, truck_height / 4, truck_height / 1.8))
    glass = pv.Box(bounds=(-155, -140, truck_width / 4, truck_width * 3 / 4, truck_height / 2.5, truck_height / 1.8))
    step1 = pv.Box(bounds=(-140, -130, truck_width / 2 - 10, truck_width / 2 + 10, -10, -5))
    step2 = pv.Box(bounds=(-140, -130, truck_width / 2 - 10, truck_width / 2 + 10, -15, -10))

    plotter.add_mesh(cab_main, color='silver')
    plotter.add_mesh(cab_front, color='gray')
    plotter.add_mesh(glass, color='blue', opacity=0.5)
    plotter.add_mesh(step1, color='darkgray')
    plotter.add_mesh(step2, color='darkgray')

    # === Ready truck, now show ===
    plotter.show(auto_close=False)  # <- AFTER truck is ready

    # Animate box loading
    for (x, y, w, h, z, kod, city, rotated, yukseklik) in placements:
        #bounds = (truck_length - x - w, truck_length - x, y, y + h, z, z + yukseklik)
        bounds = (x, x + w, y, y + h, z, z + yukseklik)
        box = pv.Box(bounds=bounds)
        color = cmap((hash(city) % 20) / 20)
        plotter.add_mesh(box, color=color, opacity=0.95, show_edges=True, edge_color="black")
        plotter.render()
        time.sleep(delay)

    plotter.show()

def choose_visual_mode(placements):
    mode_win = Toplevel()
    mode_win.title("🎥 Select Visualization Mode")
    mode_win.geometry("420x200")

    Label(mode_win, text="Which visualization mode would you like to use?", font=("Segoe UI", 11)).pack(pady=10)

    ttk.Button(mode_win, text="🖼️ Static 3D View", width=40,
               command=lambda: [
                   mode_win.destroy(),
                   draw_3d_truck_realistic(placements, 1360, 240)
               ]).pack(pady=5)

    ttk.Button(mode_win, text="🎬 3D Animated Loading", width=40,
               command=lambda: [
                   mode_win.destroy(),
                   draw_3d_truck_realistic_animated(placements, 1360, 240)
               ]).pack(pady=5)





def check_overlap(x1, y1, w1, h1, placements):
    for (px, py, pw, ph, _, _, _) in placements:
        if not (x1 + w1 <= px or x1 >= px + pw or y1 + h1 <= py or y1 >= py + ph):
            return True  # Çakışıyor
    return False  # Çakışmıyor

import tkinter as tk
from tkinter import ttk

def show_advanced_user_guide():
    guide_win = tk.Toplevel()
    guide_win.title("📘 User Guide")
    guide_win.geometry("600x500")
    guide_win.configure(bg="white")

    notebook = ttk.Notebook(guide_win)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # === Sekme 1: Başlangıç ===
    start_tab = tk.Frame(notebook, bg="white")
    notebook.add(start_tab, text="🏁 Start")

    start_text = (
        "🚛 Truck Loading Assistant Usage Steps:\n\n"
        "1️⃣ Enter product information (Code, Width, Length, Quantity, City-District) or load from Excel.\n"
        "2️⃣ Manually place products if needed.\n"
        "3️⃣ Select the starting city and click the 'Start Placement' button.\n"
        "4️⃣ After loading, generate a report, export PDF, or save the data.\n"
        "5️⃣ You can reload saved data later.\n"
        "\n✨ Good luck!"
    )
    tk.Label(start_tab, text=start_text, bg="white", justify="left", font=("Segoe UI", 13)).pack(padx=10, pady=10, anchor="nw")

    # === Sekme 2: Hızlı İpuçları ===
    tips_tab = tk.Frame(notebook, bg="white")
    notebook.add(tips_tab, text="🛠️ Quick Tips")

    tips_text = (
        "💡 Tips:\n\n"
        "- Don’t forget to select both City and District when adding products.\n"
        "- Manually placed products affect automatic placement.\n"
        "- Choosing the first city correctly improves the route planning.\n"
        "- It's recommended to use unique product codes.\n"
    )
    tk.Label(tips_tab, text=tips_text, bg="white", justify="left", font=("Segoe UI", 13)).pack(padx=10, pady=10, anchor="nw")

    # === Sekme 3: Sık Sorulan Sorular ===
    faq_tab = tk.Frame(notebook, bg="white")
    notebook.add(faq_tab, text="❓ FAQ")

    faq_text = (
        "❓ Frequently Asked Questions:\n\n"
        "- PDF not generating? ➡️ Check Excel data format.\n"
        "- Theme not changing? ➡️ Check differences between Tkinter/ttk widgets.\n"
        "- Lost your data? ➡️ Use your JSON backup.\n"
    )
    tk.Label(faq_tab, text=faq_text, bg="white", justify="left", font=("Segoe UI", 13)).pack(padx=10, pady=10, anchor="nw")

    # === Sekme 4: Tema Değiştirme ===
    theme_tab = tk.Frame(notebook, bg="white")
    notebook.add(theme_tab, text="🎨 Theme Selection")

    theme_text = (
        "🎨 Theme Options:\n\n"
        "- Use the 'Change Theme' option from the menu.\n"
        "- Try different theme styles from the popup window.\n"
        "- Options include Light / Dark / Soft Pastel themes.\n"
    )
    tk.Label(theme_tab, text=theme_text, bg="white", justify="left", font=("Segoe UI", 13)).pack(padx=10, pady=10, anchor="nw")

    # === Sekme 5: İletişim & Destek ===
    contact_tab = tk.Frame(notebook, bg="white")
    notebook.add(contact_tab, text="📞 Contact")

    contact_text = (
        "📞 Contact & Support:\n\n"
        "- There is currently no support line.\n"
        "- A support and feedback channel will be established in the future.\n"
        "\n📬 Stay tuned!"
    )
    tk.Label(contact_tab, text=contact_text, bg="white", justify="left", font=("Segoe UI", 13)).pack(padx=10, pady=10, anchor="nw")

    # === Alt Mesaj ===
    tk.Label(guide_win, text="Good luck! 👩‍💻👨‍💻", font=("Segoe UI", 10, "italic"), bg="white").pack(pady=5)

def manual_place_selected():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a product.")
        return
    index = selection[0]
    product = products[index]

    win = tk.Toplevel()
    win.title("🛠️ Manual Placement")
    win.geometry("300x250")
    win.configure(bg="#f9f9f9")

    tk.Label(win, text="X coordinate:").pack(pady=2)
    x_entry = tk.Entry(win)
    x_entry.pack()

    tk.Label(win, text="Y coordinate:").pack(pady=2)
    y_entry = tk.Entry(win)
    y_entry.pack()

    tk.Label(win, text="Can be Rotated? (Yes/No)").pack(pady=2)
    rotate_entry = tk.Entry(win)
    rotate_entry.pack()

    def save_manual_placement():
        global manual_placements
        try:
            x = int(x_entry.get())
            y = int(y_entry.get())
            rotated = rotate_entry.get().lower() == "evet"

            width = int(product["Length"]) if rotated else int(product["Width"])
            height = int(product["Width"]) if rotated else int(product["Length"])

            if x + width > truck_length or y + height > truck_width:
                messagebox.showerror("Error", "The product cannot be placed outside the truck boundaries.")
                return
            if check_overlap(x, y, width, height, manual_placements):
                messagebox.showerror("Error", "There is already another product in this area! Overlap detected.")
                return

            manual_placements.append((x, y, width, height, product["Code"], product["City"], rotated))

            # 🔍 Kod bazlı ürün bul ve eksilt
            for p in products:
                if str(p["Code"]) == str(product["Code"]):
                    p["Quantity"] -= 1
                    if p["Quantity"] <= 0:
                        products.remove(p)
                    break
            refresh_listbox()
            kalan_adet = next((p["Quantity"] for p in products if p["Code"] == product["Code"]), 0)
            messagebox.showinfo("Success", f"Manual placement saved! (Remaining quantity: {kalan_adet})")
            win.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers and values.")

    tk.Button(win, text="Save", command=save_manual_placement).pack(pady=10)


def apply_filter():
    keyword = search_var.get().lower()
    listbox.delete(0, tk.END)
    for i, p in enumerate(products):
        if (
            keyword in p["Code"].lower()
            or keyword in p["City"].lower()
        ):
            listbox.insert(
                tk.END,
                f"📦 Koli #{i+1} | 🆔 Code: {p['Code']} | 📏 {p['Width']}x{p['Length']} cm | 📦 Quantity: {p['Quantity']} | ↻ Can be Rotated: {'Yes' if p['Rotated'] else 'No'} | 🏷️ City: {p['City'].split(' - ')[0]} | 📍 District: {p['City'].split(' - ')[1]}"
            )
            listbox.itemconfig(tk.END, {'bg': '#ffffff', 'selectbackground': '#cce5ff'})

def clear_filter():
    search_var.set("")
    listbox.delete(0, tk.END)
    for i, p in enumerate(products):
        listbox.insert(
            tk.END,
            f"📦 Koli #{i+1} | 🆔 Code: {p['Code']} | 📏 {p['Width']}x{p['Length']} cm | 📦 Quantity: {p['Quantity']} | ↻ Can be Rotated: {'Yes' if p['Rotated'] else 'No'} | 🏷️ City: {p['City'].split(' - ')[0]} | 📍 District: {p['City'].split(' - ')[1]}"
        )
        listbox.itemconfig(tk.END, {'bg': '#ffffff', 'selectbackground': '#cce5ff'})

def remove_selected():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a product to delete.")
        return
    index = selection[0]
    listbox.delete(index)
    del products[index]


# Ana pencereyi ayarla
root.geometry("1280x720")
root.title("Welcome")
# Hover Efekti Fonksiyonları
def on_enter(e):
    e.widget.config(bg='#d3d3d3')  # Hover efekti rengi

def on_leave(e):
    e.widget.config(bg='#f0f0f0')  # Normal renk

# Menü Çubuğu
def save_file():
    print("File has been saved.")

def load_file():
    print("File has been loaded.")

def safe_export_labels():
    if not placements:
        messagebox.showwarning("Warning", "You must click 'Start Placement' first..")
        return
    export_labels_as_individual_files(placements, manual_placements)

# === Tema Seçim Combobox'u ===
def apply_theme(theme_name):
    theme = themes.get(theme_name)
    if not theme:
        return
    bg = theme["bg"]
    fg = theme["fg"]
    button_bg = theme["button_bg"]
    entry_bg = theme["entry_bg"]

    # Ana pencereyi güncelle
    root.configure(bg=bg)

    # ttk style'ları güncelle
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=button_bg, foreground=fg)
    style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)
    style.configure("TCombobox", fieldbackground=entry_bg, foreground=fg)
    style.configure("TLabelframe", background=bg, foreground=fg)
    style.configure("TLabelframe.Label", background=bg, foreground=fg)
    style.configure("TFrame", background=bg)

    # tk widget'ları gezip güncelle
    for widget in root.winfo_children():
        recursive_apply(widget, bg, fg, entry_bg)

def recursive_apply(widget, bg, fg, entry_bg):
    try:
        if isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget.configure(bg=bg)
        elif isinstance(widget, (tk.Label, tk.Button, tk.Listbox, tk.Checkbutton, tk.Radiobutton)):
            widget.configure(bg=bg, fg=fg)
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        elif isinstance(widget, (ttk.Entry, ttk.Combobox, ttk.Button, ttk.Label, ttk.Checkbutton)):
            pass  # ttk widgetlara elle bg, fg atamıyoruz (hata verir), onlar Style ile kontrol edilir
        else:
            pass  # Bilinmeyen widget tipleri
    except Exception as e:
        print(f"⚠️ Skipped widget {widget} due to error: {e}")

    for child in widget.winfo_children():
        recursive_apply(child, bg, fg, entry_bg)



def theme_selector():
    top = tk.Toplevel(root)
    top.title("🎨 Theme Selector")
    top.geometry("300x150")
    top.configure(bg="#f0f0f0")

    tk.Label(top, text="Select Theme:", bg="#f0f0f0").pack(pady=10)

    selected_theme = tk.StringVar(value="Light Default")
    combo = ttk.Combobox(top, textvariable=selected_theme, values=list(themes.keys()))
    combo.pack(pady=10)

    def apply():
        apply_theme(selected_theme.get())
        top.destroy()

    tk.Button(top, text="Apply", command=apply).pack(pady=10)

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Save File", command=save_file)
file_menu.add_command(label="Load File", command=load_file)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)
theme_menu = tk.Menu(menubar, tearoff=0)
theme_menu.add_command(label="Change Theme", command=theme_selector)
menubar.add_cascade(label="Themes", menu=theme_menu)





    # === STİL TANIMLARI ===
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f6f8fa", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 12), padding=5)
style.configure("TCombobox", padding=3)
style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

root.withdraw()

def build_main_ui():
    root.title("Truck Loading Assistant")
    root.geometry("1280x720")

    global kod_entry, en_entry, boy_entry, adet_entry, yukseklik_entry, istif_entry, listbox, ilce_combobox

    # === Ana Frame ===
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)

    left_frame = ttk.Frame(main_frame)
    left_frame.pack(side="left", fill="y", padx=(0, 10))

    center_frame = ttk.Frame(main_frame)
    center_frame.pack(side="left", fill="both", expand=True)

    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side="left", fill="y", padx=(10, 0))

    # === ÜRÜN BİLGİLERİ ===
    product_box = ttk.Labelframe(left_frame, text="📦 Product Information", padding=10)
    product_box.pack(fill="x", pady=10)

    for idx, text in enumerate(["Code", "Width", "Length", "Height", "Quantity"]):
        ttk.Label(product_box, text=text).grid(row=idx, column=0, sticky="e", pady=2)

    kod_entry = ttk.Entry(product_box)
    en_entry = ttk.Entry(product_box)
    boy_entry = ttk.Entry(product_box)
    yukseklik_entry = ttk.Entry(product_box)
    adet_entry = ttk.Entry(product_box)

    kod_entry.grid(row=0, column=1)
    en_entry.grid(row=1, column=1)
    boy_entry.grid(row=2, column=1)
    yukseklik_entry.grid(row=3, column=1)
    adet_entry.grid(row=4, column=1)


    ttk.Label(product_box, text="Max Stack Count").grid(row=5, column=0, sticky="e")
    istif_entry = ttk.Entry(product_box)
    istif_entry.grid(row=5, column=1)

    ttk.Label(product_box, text="Can be Rotated?").grid(row=6, column=0, sticky="e")
    donme_checkbox = tk.Checkbutton(product_box,variable=donme_var,onvalue=True,offvalue=False)
    donme_checkbox.grid(row=6, column=1, sticky="w")

    # === KONUM BİLGİLERİ ===
    konum_box = ttk.Labelframe(left_frame, text="📍 Location Information", padding=10)
    konum_box.pack(fill="x", pady=10)

    ttk.Label(konum_box, text="City").grid(row=0, column=0, sticky="e")
    il_combobox = ttk.Combobox(konum_box, textvariable=selected_city, values=list(city_districts.keys()))
    il_combobox.grid(row=0, column=1, pady=2)

    ttk.Label(konum_box, text="District").grid(row=1, column=0, sticky="e")
    ilce_combobox = ttk.Combobox(konum_box, textvariable=selected_district)
    ilce_combobox.grid(row=1, column=1, pady=2)

    def update_districts(event):
        city = selected_city.get()
        ilce_combobox['values'] = city_districts.get(city, [])
        selected_district.set("")

    il_combobox.bind("<<ComboboxSelected>>", update_districts)

    ttk.Label(konum_box, text="	Starting City").grid(row=2, column=0, sticky="e")
    start_city_combobox = ttk.Combobox(konum_box, textvariable=start_city, values=list(city_districts.keys()))
    start_city_combobox.grid(row=2, column=1, pady=2)


    def clear_all_products():
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete all products?"):
            products.clear()
            listbox.delete(0, tk.END)



    # === Butonlar ===
    butonlar_frame = ttk.Frame(left_frame)
    butonlar_frame.pack(fill="x", pady=(5, 0))
    ttk.Button(butonlar_frame, text="➕ Add Product", command=add_product).pack(fill="x", pady=2)
    ttk.Button(butonlar_frame, text="❌ Delete Selected Product", command=remove_selected).pack(fill="x", pady=2)
    ttk.Button(butonlar_frame, text="🧹 Clear All Products", command=clear_all_products).pack(fill="x", pady=2)
    ttk.Button(butonlar_frame, text="🚚 Start Placement", command=start_placement).pack(fill="x", pady=2)
    ttk.Button(butonlar_frame, text="🧭 Set Manual Route", command=open_manual_route_window).pack(fill="x", pady=2)
    ttk.Button(butonlar_frame, text="🛠️ Manual Placement", command=manual_place_selected).pack(fill="x", pady=2)
    ttk.Button(butonlar_frame, text=" ⚙️ Truck Settings", command=open_settings_window).pack(fill="x", pady=2)

    # === ÜRÜN LİSTESİ ===
    listbox = tk.Listbox(center_frame, font=("Segoe UI", 10), bg="white")
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    # === SAĞ PANEL ===
    search_box = ttk.Labelframe(right_frame, text="🔍 Search and Filter", padding=10)
    search_box.pack(fill="x", pady=10)

    ttk.Entry(search_box, textvariable=search_var).pack(fill="x", pady=5)
    ttk.Button(search_box, text="Filter", command=apply_filter).pack(fill="x", pady=2)
    ttk.Button(search_box, text="Clear", command=clear_filter).pack(fill="x", pady=2)

    # === EK ARAÇLAR ===
    extra_box = ttk.Labelframe(right_frame, text="📊 Reporting & Tools", padding=10)
    extra_box.pack(fill="x", pady=10)

    ttk.Button(extra_box, text="📋 Show Reports", command=lambda: show_summary_report()).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="🌱 Sustainability Report",command=lambda: show_sustainability_report_with_icons(products)).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="🧾 Label PDF", command=lambda: export_labels_as_individual_files(placements, manual_placements)).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="📋 Placement Log", command=show_placement_log).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="📦 Box Position", command=show_box_location).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="📁 Import from Excel", command=load_from_excel).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="📥 Load Data", command=load_data).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="📤 Save Data", command=save_data).pack(fill="x", pady=2)
    """ttk.Button(extra_box, text="📧 Email Simulation", command=simulate_email_send(dummy_file_path)).pack(fill="x", pady=2)"""
    ttk.Button(extra_box, text="🖼️ Show 2D Truck View", command=draw_loaded_full_placements).pack(fill="x", pady=2)
    ttk.Button(extra_box, text="🖼️ 3D Visualization Mode", command=lambda: choose_visual_mode(placements)).pack(fill="x", pady=5)
    ttk.Button(extra_box, text="📘 User Guide", command=show_advanced_user_guide).pack(fill="x", pady=2)
    ttk.Label(right_frame, text="© 2025 Truck Loading Assistant", anchor="center").pack(side="bottom", pady=10)


def show_splash_screen():
    splash = tk.Toplevel()
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() - 1200) // 2
    y = (splash.winfo_screenheight() - 1200) // 2
    splash.geometry(f"+{x}+{y}")

    label = tk.Label(splash, text="🚛 Truck Loading Assistant", font=("Segoe UI", 30, "bold"), fg="#4CAF50", bg="white")
    label.pack(pady=30)

    alt_label = tk.Label(splash, text="Loading...", font=("Segoe UI", 16), fg="#555", bg="white")
    alt_label.pack(pady=10)

    progress = ttk.Progressbar(splash, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=30)

    progress["maximum"] = 100
    progress["value"] = 0

    def slow_increase(val=0):
        if val <= 100:
            progress["value"] = val
            splash.after(50, slow_increase, val + 2)  # 5 sn için 50ms aralıklarla +2
        else:
            splash.destroy()
            root.deiconify()  # Ana pencereyi göster
            build_main_ui()  # Ana UI'ı kur

    slow_increase()

# === Program başlat ===
show_splash_screen()
root.mainloop()