import tkinter as tk
from tkinter import messagebox

# Mors Alfabesi Sözlüğü
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}

def text_to_binary(text):
    text = text.upper()
    binary_result = ""
    for char in text:
        if char in MORSE_CODE_DICT:
            mors = MORSE_CODE_DICT[char]
            if mors == '/':
                binary_result += "0000000"
            else:
                for symbol in mors:
                    if symbol == '.': binary_result += "1"
                    elif symbol == '-': binary_result += "111"
                    binary_result += "0"
                binary_result += "00"
    return binary_result.strip('0')

def binary_to_text(binary):
    try:
        binary = binary.strip()
        reverse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
        decoded_text = ""
        # 7 tane sıfır kelime boşluğudur
        words = binary.split("0000000")
        for word in words:
            # 3 tane sıfır harf boşluğudur
            chars = word.split("000")
            for char in chars:
                mors_char = ""
                # Tek sıfır sembol boşluğudur
                symbols = char.split("0")
                for symbol in symbols:
                    if symbol == "1": mors_char += "."
                    elif symbol == "111": mors_char += "-"
                if mors_char:
                    decoded_text += reverse_dict.get(mors_char, "?")
            decoded_text += " "
        return decoded_text.strip()
    except Exception:
        return "Geçersiz İkili Kod!"

# Buton Fonksiyonları
def metni_koda_cevir():
    metin = entry_text_in.get()
    if not metin:
        messagebox.showwarning("Uyarı", "Lütfen bir metin girin!")
        return
    sonuc = text_to_binary(metin)
    text_binary_out.delete(1.0, tk.END)
    text_binary_out.insert(tk.END, sonuc)

def kodu_metne_cevir():
    kod = entry_binary_in.get("1.0", tk.END).strip()
    if not kod:
        messagebox.showwarning("Uyarı", "Lütfen 1 ve 0'lardan oluşan kodu girin!")
        return
    sonuc = binary_to_text(kod)
    label_text_out.config(text=sonuc)

# Arayüz Ayarları
root = tk.Tk()
root.title("Mors - Binary Çift Yönlü Çevirici")
root.geometry("600x600")

# --- ÜST BÖLÜM: YAZIDAN KODA ---
frame_top = tk.LabelFrame(root, text="Yazıdan İkili Koda (1-0)", padx=10, pady=10, fg="blue")
frame_top.pack(fill="both", expand="yes", padx=20, pady=10)

tk.Label(frame_top, text="Metni Girin:").pack(anchor="w")
entry_text_in = tk.Entry(frame_top, width=60)
entry_text_in.pack(pady=5)

btn_to_binary = tk.Button(frame_top, text="Koda Dönüştür ↓", command=metni_koda_cevir, bg="#e1e1e1")
btn_to_binary.pack(pady=5)

text_binary_out = tk.Text(frame_top, height=5, width=60)
text_binary_out.pack(pady=5)

# --- ALT BÖLÜM: KODDAN YAZIYA ---
frame_bottom = tk.LabelFrame(root, text="İkili Koddan (1-0) Yazıya", padx=10, pady=10, fg="green")
frame_bottom.pack(fill="both", expand="yes", padx=20, pady=10)

tk.Label(frame_bottom, text="1 ve 0 Kodlarını Yapıştırın:").pack(anchor="w")
entry_binary_in = tk.Text(frame_bottom, height=5, width=60)
entry_binary_in.pack(pady=5)

btn_to_text = tk.Button(frame_bottom, text="Yazıya Dönüştür ↓", command=kodu_metne_cevir, bg="#e1e1e1")
btn_to_text.pack(pady=5)

tk.Label(frame_bottom, text="Çözülen Metin:", font=("Arial", 10, "bold")).pack(anchor="w")
label_text_out = tk.Label(frame_bottom, text="...", font=("Arial", 14, "bold"), fg="darkgreen")
label_text_out.pack(pady=10)

root.mainloop()