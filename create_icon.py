"""
Icon creation utility for the Encrypted Notes Manager
"""
import tkinter as tk
from tkinter import Canvas
import os

def create_lock_icon():
    """Create a simple lock icon using Tkinter Canvas."""
    
    # Create a temporary window to draw the icon
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create canvas for drawing
    canvas = Canvas(root, width=32, height=32, bg='white')
    canvas.pack()
    
    # Draw a simple lock icon
    # Lock body (rectangle)
    canvas.create_rectangle(8, 14, 24, 28, fill='#2c3e50', outline='#34495e', width=2)
    
    # Lock shackle (semicircle)
    canvas.create_arc(12, 6, 20, 18, start=0, extent=180, outline='#2c3e50', width=3, style='arc')
    
    # Keyhole
    canvas.create_oval(14, 18, 18, 22, fill='#ecf0f1', outline='#bdc3c7')
    canvas.create_rectangle(15, 21, 17, 25, fill='#ecf0f1', outline='#bdc3c7')
    
    # Save as PostScript and convert to other formats if needed
    try:
        canvas.postscript(file="assets/lock_icon.eps")
        print("Icon created as lock_icon.eps")
    except Exception as e:
        print(f"Could not save icon: {e}")
    
    root.destroy()

def create_text_icon():
    """Create a simple text-based icon representation."""
    icon_data = """
/* XPM */
static char * lock_icon_xpm[] = {
"16 16 3 1",
" 	c None",
".	c #2c3e50",
"+	c #ecf0f1",
"                ",
"      ....      ",
"     .    .     ",
"    .      .    ",
"    .      .    ",
"   ..........   ",
"   .++++++++.   ",
"   .+++..+++.   ",
"   .+++..+++.   ",
"   .++....++.   ",
"   .++....++.   ",
"   .++++++++.   ",
"   ..........   ",
"                ",
"                ",
"                "};
"""
    
    with open("assets/lock_icon.xpm", "w") as f:
        f.write(icon_data)
    print("Created XPM icon file")

if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    create_lock_icon()
    create_text_icon()
