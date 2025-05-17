import tkinter as tk
from tkinter import filedialog
import time
import threading
import os
from PIL import Image, ImageTk

# Set up main
root = tk.Tk()
root.title("Narrow.One Trainer")
root.geometry("500x300")
root.configure(bg="#1e1e1e")

file_path = None
file_paths = []
mistral_output = ""
index = 0
index_submit = 0

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def image_viewer(folder_path):
    global ai
    clear_screen()
    root.geometry('600x600')

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'png', 'jpeg'))]
    index = 0

    image_label = tk.Label(root)
    image_label.pack()

    img_index = tk.Label(root, anchor="s", bg="#1e1e1e", fg="white")
    img_index.pack(pady=10)

    def show_image():
        img_path = os.path.join(folder_path, image_files[index])
        img = Image.open(img_path)
        img = img.resize((600, 400))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        img_index.config(text=f"{index + 1} / {len(image_files)}")

    def next_image():
        nonlocal index
        index = (index + 1) % len(image_files)
        show_image()

    def prev_image():
        nonlocal index
        index = (index - 1) % len(image_files)
        show_image()

    tk.Button(root, text="<<", command=prev_image).pack(side="left", padx=20, pady=10)
    tk.Button(root, text=">>", command=next_image).pack(side="right", padx=20, pady=10)
    ai = tk.Button(root, text="Analyse with AI ✨", command=lambda: analyse())
    ai.pack(side="right", padx=20, pady=10)
    ai = tk.Button(root, text="Analyse stats table", command=lambda: analyse_table())
    ai.pack(side="right", padx=20, pady=10)
    


    show_image()



def analyse_table():
            with open(r"C:\Users\nshei\Desktop\youtube code\Expert System\stats_table.py", "r") as f:
                contents = f.read()
                exec(contents, globals())

                root.after(0, show_mistral_output(f"""
    Kill Contribution %: {kill_contribution_percentage}
    Assist Contribution %: {assist_contribution_percentage}
    Combat Focus Ratio: {combat_focus_ratio}
    Score per Kill: {score_per_kill}
    Score per Assist: {score_per_assist}
    Kill accuracy: {kill_accuracy}
    \nPerformance Score: {score:.1f}/10
    """))


def people_keys():
    try:
        globals_dict = globals().copy()
        globals_dict.update({
            'mistral_output': None,
            'index': 0,
            'index_submit': 0
        })
        
        with open(r"C:\Users\nshei\Desktop\youtube code\Expert System\people_keys.py", "r") as f:
            contents = f.read()
            # Pass the updated globals dictionary to exec
            exec(contents, globals_dict)
            image_viewer(r"C:\Users\nshei\Desktop\youtube code\Expert System\people_moments")
    except Exception as e:
        print(f"❌ Error in people_keys: {e}")

def show_mistral_output(output_text: str):
    """Open a styled Toplevel window that shows the AI analysis text."""
    top = tk.Toplevel(root)
    top.title("AI Analysis")
    top.configure(bg="#1e1e1e")

    # --- window sizing & centring ---
    top.update_idletasks()
    w, h = 600, 400                      # desired inner size
    x = (top.winfo_screenwidth()  - w) // 2
    y = (top.winfo_screenheight() - h) // 3
    top.geometry(f"{w}x{h}+{x}+{y}")
    top.minsize(400, 250)                # reasonable minimum

    # outer frame gives us padding
    frame = tk.Frame(top, bg="#1e1e1e", padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    # scrollable, read-only text widget
    text_box = tk.Text(
        frame,
        wrap="word",
        bg="#1e1e1e",
        fg="#f5f5f5",
        insertbackground="#f5f5f5",      # caret colour
        relief="flat",
        font=("Helvetica", 12),
        borderwidth=0,
        highlightthickness=0
    )
    text_box.insert("1.0", output_text)
    text_box.configure(state="disabled")          # read-only
    text_box.pack(side="left", expand=True, fill="both")

    scroll = tk.Scrollbar(frame, command=text_box.yview, bg="#1e1e1e")
    scroll.pack(side="right", fill="y")
    text_box.configure(yscrollcommand=scroll.set)

    # neat close button at the bottom
    tk.Button(
        top,
        text="Close",
        command=top.destroy,
        font=("Helvetica", 10, "bold"),
        bg="#444",
        fg="#ffffff",
        activebackground="#333",
        activeforeground="#ffffff",
        bd=0,
        padx=12,
        pady=6
    ).pack(pady=(10, 20))


def analyse():
    global mistral_output

    ai.destroy()

    #overlay
    loading_frame = tk.Frame(root, bg="#1e1e1e")
    loading_frame.place(relx=0.5, rely=0.5, anchor="center")

    loading_label = tk.Label(
        loading_frame,
        text="Analysing",
        font=("Helvetica", 14, "bold"),
        bg="#1e1e1e",
        fg="#25c1b9"
    )
    loading_label.pack(padx=20, pady=10)
    
    def animate(i=[0]):
        loading_label.config(text="Analysing" + "." * (i[0] % 4))
        i[0] += 1
        loading_frame.after(450, animate)           # every 450 ms

    animate()

    def worker():
        try:
            with open(r"C:\Users\nshei\Desktop\youtube code\Expert System\ollama images feed.py", "r") as f:
                contents = f.read()
                exec(contents, globals())

            root.after(0, on_success)

        except Exception as e:
            print(f"❌ Error in analyse(): {e}")
            root.after(0, lambda: loading_label.config(text="❌ Error – see console"))

    def on_success():
        loading_frame.destroy()                     # remove the overlay
        image_viewer(r"C:\Users\nshei\Desktop\youtube code\Expert System\people_moments")
        show_mistral_output(mistral_output)

    threading.Thread(target=worker, daemon=True).start()

def run_in_thread():
    with open(r"C:\Users\nshei\Desktop\youtube code\Expert System\key_moments.txt", "r") as f:
        contents = f.read()
        exec(contents)
        people_keys()

def analyse_key_moments():
    clear_screen()

    main_label = tk.Label(
    root,
    text="Narrow.One Trainer\n\nAnalysing video...",
    font=("Helvetica", 16, "bold"),
    bg="#1e1e1e",
    fg="#f5f5f5",
    justify="center"
    )
    main_label.pack(pady=(30, 10))

    threading.Thread(target=run_in_thread).start()



# Function to handle file import
def import_file(file_type):
    global file_path , file_paths
    if file_type == "vid":
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("MP4 Video", "*.mp4"), ("All files", "*.*")]
        )
        if file_path:
            print("Selected video file:", file_path)
            selected_file_label.config(text=f"📁 {file_path.split('/')[-1]}")
            file_paths.append(file_path)
            import_button.config(
                text="Choose game statistics table",
                command=lambda: import_file("img")
            )
            main_label.config(
                text="Narrow.One Trainer\n\nUpload your endscreen statistics table (.png)"
            )
            back_button.pack(pady=5)
    else:
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("PNG Image", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            print("Selected image file:", file_path)
            selected_file_label.config(text=f"📁 {file_path.split('/')[-1]}")
            file_paths.append(file_path)
            continue_button.pack()

# Function to go back to video upload step
def go_back():
    import_button.config(
        text="Choose Video",
        command=lambda: import_file("vid")
    )
    main_label.config(
        text="Narrow.One Trainer\n\nUpload your gameplay video (.mp4)"
    )
    back_button.pack_forget()
    selected_file_label.config(text="")

# Main label
main_label = tk.Label(
    root,
    text="Narrow.One Trainer\n\nUpload your gameplay video (.mp4)",
    font=("Helvetica", 16, "bold"),
    bg="#1e1e1e",
    fg="#f5f5f5",
    justify="center"
)
main_label.pack(pady=(30, 10))

# Button to import file
import_button = tk.Button(
    root,
    text="Choose Video",
    command=lambda: import_file("vid"),
    font=("Helvetica", 13),
    bg="#007acc",
    fg="white",
    padx=20,
    pady=10,
    bd=0,
    activebackground="#005f99",
    activeforeground="white"
)
import_button.pack(pady=10)

# Back button (initially hidden)
back_button = tk.Button(
    root,
    text="<- Back",
    command=go_back,
    font=("Helvetica", 10),
    bg="#444",
    fg="white",
    padx=10,
    pady=5,
    bd=2,
    activebackground="#333",
    activeforeground="white"
)

continue_button = tk.Button(
    root,
    text="Continue ->",
    command= analyse_key_moments,
    font=("Helvetica", 10),
    bg="#444",
    fg="#25c1b9",
    pady=5,
    bd=2,
    activebackground="#333",
    activeforeground="white"
)

# Label to show selected file
selected_file_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 10),
    bg="#1e1e1e",
    fg="#bbbbbb",
    wraplength=400
)
selected_file_label.pack(pady=(10, 0))

# Start GUI loop
root.mainloop()
