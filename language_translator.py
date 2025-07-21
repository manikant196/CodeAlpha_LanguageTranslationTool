import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyttsx3
from gtts import gTTS
import playsound
import tempfile

# Setup TTS engine
offline_tts = pyttsx3.init()

# Languages supported by GoogleTranslator (simplified)
LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Kannada': 'kn',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh-CN',
    'Arabic': 'ar',
    'Russian': 'ru',
    'Japanese': 'ja',
}

lang_names = list(LANGUAGES.keys())

def get_lang_code(name):
    return LANGUAGES.get(name, 'en')

def translate_text():
    src = get_lang_code(src_lang.get())
    dest = get_lang_code(dest_lang.get())
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "Please enter some text to translate.")
        return

    try:
        translated = GoogleTranslator(source=src, target=dest).translate(text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

def copy_output():
    translated = output_text.get("1.0", tk.END).strip()
    if translated:
        root.clipboard_clear()
        root.clipboard_append(translated)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

def speak_output_offline():
    text = output_text.get("1.0", tk.END).strip()
    if text:
        offline_tts.say(text)
        offline_tts.runAndWait()

def speak_output_online():
    text = output_text.get("1.0", tk.END).strip()
    lang = get_lang_code(dest_lang.get())
    if text:
        try:
            tts = gTTS(text=text, lang=lang)
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
                tts.save(fp.name)
                playsound.playsound(fp.name)
        except Exception as e:
            messagebox.showerror("TTS Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Language Translator")
root.geometry("700x550")

# Language selection
tk.Label(root, text="Source Language:", font=("Arial", 12)).pack(pady=(10, 0))
src_lang = ttk.Combobox(root, values=lang_names, width=50)
src_lang.set("English")
src_lang.pack()

tk.Label(root, text="Target Language:", font=("Arial", 12)).pack(pady=(10, 0))
dest_lang = ttk.Combobox(root, values=lang_names, width=50)
dest_lang.set("Hindi")
dest_lang.pack()

# Input text
tk.Label(root, text="Enter Text:", font=("Arial", 12)).pack(pady=(15, 0))
input_text = tk.Text(root, height=6, width=70)
input_text.pack()

# Translate Button
tk.Button(root, text="Translate", font=("Arial", 12), bg="#4CAF50", fg="white", command=translate_text).pack(pady=10)

# Output text
tk.Label(root, text="Translated Text:", font=("Arial", 12)).pack()
output_text = tk.Text(root, height=6, width=70)
output_text.pack()

# Buttons frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Copy", width=15, command=copy_output).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Speak (Offline)", width=15, command=speak_output_offline).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Speak (Online)", width=15, command=speak_output_online).grid(row=0, column=2, padx=10)

root.mainloop()
