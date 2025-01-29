import tkinter as tk
from tkinter import filedialog
from tesserocr import PyTessBaseAPI
from tesserocr import get_languages

tessdata_path = "/usr/share/tesseract-ocr/4.00/tessdata"

def add_text():
    """Dynamically adds text to the screen."""
    new_label = tk.Label(frame, text=entry.get(), font=("Arial", 12))
    new_label.pack(pady=5)  # Adds space between labels
    entry.delete(0, tk.END)  # Clear the entry box after submission



# Function to open file dialog
def open_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        file_label.config(text=f"Selected File:\n{file_path}")
        print("File path: ", file_path)
        try:
            with PyTessBaseAPI(path= tessdata_path) as api:
                print("✅ Tesseract initialized successfully!")
                print(get_languages(tessdata_path))  # or any other path that applies to your system
                img = file_path
                api.SetImageFile(img)
                text_output = api.GetUTF8Text()
                print(text_output)
                # Insert long text to show scrolling
                text_widget.insert("1.0", text_output)
                # Automatically adjust the window to fit the content
                

        except Exception as e:
            print("❌ Failed to initialize Tesseract:", e)
            


def copy_to_clipboard():
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(text_widget.get("1.0", "end-1c"))  # Copy text
    root.update()  # Ensures the clipboard is updated
                
# Create main Tkinter window
root = tk.Tk()
root.title("File Selector")
root.geometry("400x200") 

# Create a button to open file dialog
button = tk.Button(root, text="Select File", command=open_file)
button.pack(pady=20)

# Label to display selected file
# file_selected = True
file_label = tk.Label(root, text="No file selected", wraplength=350)
file_label.pack(pady=10)


# Label to display selected file
output_label = tk.Label(root, text="Your OCR Text Output", wraplength=350)
output_label.pack(pady=10)

# Button to copy text
copy_button = tk.Button(root, text="Copy Text", command=copy_to_clipboard)
copy_button.pack(pady=5)

# Frame to contain the text widget and scrollbar
frame = tk.Frame(root)
frame.pack(expand=True, fill="both", padx=10, pady=10)

# Create a Text widget
text_widget = tk.Text(frame, wrap="word", height=400, width=300)
text_widget.pack(side="left", fill="both", expand=True)
width = min(400, text_widget.winfo_reqwidth())  # Limit width to 400px
height = min(500, text_widget.winfo_reqheight())  # Limit height to 500px
root.geometry(f"{width}x{height}")

# Create a Scrollbar
scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
scrollbar.pack(side="right", fill="y")

# Link the scrollbar to the text widget
text_widget.config(yscrollcommand=scrollbar.set)


# Run the application
root.mainloop()
