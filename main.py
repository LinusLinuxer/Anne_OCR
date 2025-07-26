import os
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import random


class OCRApp:
    def __init__(self, root, ocr_folder, background_folder, output_file):
        self.root = root
        self.root.title("OCR Image Viewer")

        self.ocr_folder = ocr_folder
        self.background_folder = background_folder
        self.output_file = output_file

        self.ocr_files = sorted(os.listdir(ocr_folder))
        self.background_files = sorted(os.listdir(background_folder))
        self.image_index = 0

        # GUI Layout
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.status_label = tk.Label(root, text="Starting OCR...", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.root.after(1500, self.process_next_image)

    def process_next_image(self):
        if self.image_index < len(self.ocr_files):
            ocr_filename = self.ocr_files[self.image_index]
            ocr_image_path = os.path.join(self.ocr_folder, ocr_filename)

            # Wähle ein zufälliges Hintergrundbild
            random_bg_filename = random.choice(self.background_files)
            background_image_path = os.path.join(self.background_folder, random_bg_filename)

            try:
                # Lade und zeige das Hintergrundbild
                bg_img = Image.open(background_image_path)
                bg_img.thumbnail((800, 600))
                img_tk = ImageTk.PhotoImage(bg_img)
                self.image_label.configure(image=img_tk)
                self.image_label.image = img_tk

                # Lade das OCR-Bild und führe Texterkennung durch
                with Image.open(ocr_image_path) as ocr_img:
                    extracted_text = pytesseract.image_to_string(ocr_img)

                # Schreibe OCR-Ergebnis in die Datei
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(f"Text from {ocr_filename}:\n")
                    f.write(extracted_text + "\n\n")

                self.status_label.config(text=f"Processed: {ocr_filename}")
            except Exception as e:
                self.status_label.config(text=f"Error with {ocr_filename}: {e}")

            self.image_index += 1
            self.root.after(10, self.process_next_image)
        else:
            self.status_label.config(text="OCR Completed")
            messagebox.showinfo("Done", f"OCR finished.\nText written to: {self.output_file}")
            


if __name__ == "__main__":
    ocr_folder = "OCR_Images"
    background_folder = "OCR_Background"
    output_file = "OCR_Output/data.txt"

    if not os.path.exists(ocr_folder):
        print(f"OCR folder '{ocr_folder}' does not exist.")
    elif not os.path.exists(background_folder):
        print(f"Background folder '{background_folder}' does not exist.")
    else:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        root = tk.Tk()
        app = OCRApp(root, ocr_folder, background_folder, output_file)
        root.mainloop()
