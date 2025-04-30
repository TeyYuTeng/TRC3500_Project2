import tkinter as tk
from tkinter import filedialog

# Use tkinter to create a file dialog window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt user to select multiple text files
file_paths = filedialog.askopenfilenames(
    title="Select Text Files to Combine",
    filetypes=[("Text Files", "*.txt")]
)

# Ask user where to save the combined file
output_path = filedialog.asksaveasfilename(
    title="Save Combined File As",
    defaultextension=".txt",
    filetypes=[("Text Files", "*.txt")]
)

# Combine the selected files
if file_paths and output_path:
    with open(output_path, 'w') as outfile:
        for path in file_paths:
            with open(path, 'r') as infile:
                data = infile.read().strip()
                if data:
                    outfile.write(data + ',')  # Add a comma between file contents

    # Remove the trailing comma
    with open(output_path, 'rb+') as f:
        f.seek(-1, 2)
        if f.read(1) == b',':
            f.seek(-1, 2)
            f.truncate()

    print(f"Combined file saved to: {output_path}")
else:
    print("No files selected or save path cancelled.")
