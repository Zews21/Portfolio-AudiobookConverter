import os
from gtts import gTTS
import pdfplumber
import tkinter as tk
from tkinter import filedialog, messagebox


# Function to extract text from a PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ''
            for page in pdf.pages:
                full_text += page.extract_text()
            return full_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


# Function to convert text to speech and save as MP3
def convert_text_to_speech(text, output_mp3):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_mp3)
    except Exception as e:
        print(f"Error generating MP3: {e}")


# Function to handle PDF to MP3 conversion
def pdf_to_mp3(pdf_path, output_mp3):
    text = extract_text_from_pdf(pdf_path)

    if text:
        convert_text_to_speech(text, output_mp3)
        messagebox.showinfo("Success", f"MP3 saved as: {output_mp3}")
    else:
        messagebox.showerror("Error", "No text found in the PDF or failed to extract text.")


# Function to open file dialog and get PDF file
def browse_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Choose a PDF file"
    )
    pdf_path_var.set(file_path)


# Function to select output location and name for MP3
def save_mp3():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")],
        title="Save as"
    )
    mp3_path_var.set(file_path)


# Function to trigger the conversion on button click
def convert():
    pdf_path = pdf_path_var.get()
    mp3_path = mp3_path_var.get()

    if not pdf_path or not os.path.exists(pdf_path):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return

    if not mp3_path:
        messagebox.showerror("Error", "Please specify a valid output MP3 file.")
        return

    # Perform the conversion
    pdf_to_mp3(pdf_path, mp3_path)


# Setting up the Tkinter window
root = tk.Tk()
root.title("PDF to Audiobook Converter")

# Variables to store file paths
pdf_path_var = tk.StringVar()
mp3_path_var = tk.StringVar()

# Labels and Buttons for PDF selection, MP3 saving, and conversion
tk.Label(root, text="Select PDF File:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=pdf_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_pdf).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Save MP3 As:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=mp3_path_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Save", command=save_mp3).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Convert to Audiobook", command=convert, bg='green', fg='white').grid(row=2, column=1, pady=20)

# Run the application
root.mainloop()
