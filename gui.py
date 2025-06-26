import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import threading
from typing import Optional, Tuple
from notes_manager import NotesVault, Note


class PasswordDialog:
    """Custom password dialog."""
    
    def __init__(self, parent, title="Enter Password", prompt="Password:"):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        try:
            self.dialog.iconbitmap(parent.iconbitmap())
        except:
            pass
        self.dialog.transient(parent)
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=prompt).pack(pady=(0, 10))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.pack(pady=(0, 20))
        self.password_entry.focus()
        
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT)
        
        self.password_entry.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
    
    def ok_clicked(self):
        self.result = self.password_var.get()
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()


class NotesManagerGUI:
    """Main GUI for the Encrypted Notes Manager."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Encrypted Notes Manager")
        self.root.geometry("800x600")
        
        self.set_window_icon()
        
        self.vault = NotesVault()
        self.current_note_id = None
        self.notes_list = []
        
        self.setup_gui()
        self.update_ui_state()
    
    def set_window_icon(self):
        """Set custom window icon."""
        try:
            self.root.title("🔒 Encrypted Notes Manager")
        except Exception as e:
            print(f"Could not load custom icon: {e}")
            pass
    
    def setup_gui(self):
        """Set up the main GUI components."""
        self.create_menu()
        
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.RIGHT)
        
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(list_frame, text="Notes:").pack(anchor=tk.W)
        
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.notes_listbox = tk.Listbox(list_container)
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.notes_listbox.yview)
        self.notes_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.new_note_btn = ttk.Button(buttons_frame, text="New Note", command=self.new_note)
        self.new_note_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.delete_note_btn = ttk.Button(buttons_frame, text="Delete", command=self.delete_note)
        self.delete_note_btn.pack(side=tk.LEFT)
        
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        title_frame = ttk.Frame(right_frame)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(title_frame, text="Title:").pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, textvariable=self.title_var)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.title_entry.bind('<KeyRelease>', self.on_title_change)
        
        tags_frame = ttk.Frame(right_frame)
        tags_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(tags_frame, text="Tags:").pack(side=tk.LEFT)
        self.tags_var = tk.StringVar()
        self.tags_entry = ttk.Entry(tags_frame, textvariable=self.tags_var)
        self.tags_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.tags_entry.bind('<KeyRelease>', self.on_tags_change)
        
        ttk.Label(tags_frame, text="(comma-separated)", font=("TkDefaultFont", 8)).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Label(right_frame, text="Content:").pack(anchor=tk.W)
        self.content_text = ScrolledText(right_frame, wrap=tk.WORD, height=20)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.content_text.bind('<KeyRelease>', self.on_content_change)
        
        save_frame = ttk.Frame(right_frame)
        save_frame.pack(fill=tk.X)
        
        self.save_btn = ttk.Button(save_frame, text="Save Note", command=self.save_note)
        self.save_btn.pack(side=tk.RIGHT)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Vault is locked. Use File menu to unlock or create vault.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New Vault", command=self.new_vault)
        file_menu.add_command(label="Open Vault", command=self.open_vault)
        file_menu.add_separator()
        file_menu.add_command(label="Lock Vault", command=self.lock_vault)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def update_ui_state(self):
        """Update UI state based on vault status."""
        is_unlocked = self.vault.is_unlocked
        
        controls = [
            self.search_entry, self.notes_listbox, self.new_note_btn,
            self.delete_note_btn, self.title_entry, self.tags_entry,
            self.content_text, self.save_btn
        ]
        
        state = tk.NORMAL if is_unlocked else tk.DISABLED
        for control in controls:
            control.config(state=state)
        
        if is_unlocked:
            self.status_var.set(f"Vault unlocked - {len(self.vault.notes)} notes")
            self.refresh_notes_list()
        else:
            self.status_var.set("Vault is locked")
            self.notes_listbox.delete(0, tk.END)
            self.clear_editor()
    
    def new_vault(self):
        """Create a new vault."""
        password_dialog = PasswordDialog(self.root, "Create New Vault", "Enter master password:")
        self.root.wait_window(password_dialog.dialog)
        
        if password_dialog.result:
            password = password_dialog.result
            if len(password) < 6:
                messagebox.showwarning("Weak Password", "Password should be at least 6 characters long.")
                return
            
            confirm_dialog = PasswordDialog(self.root, "Confirm Password", "Confirm master password:")
            self.root.wait_window(confirm_dialog.dialog)
            
            if confirm_dialog.result == password:
                if self.vault.create_vault(password):
                    messagebox.showinfo("Success", "Vault created successfully!")
                    self.update_ui_state()
                else:
                    messagebox.showerror("Error", "Failed to create vault.")
            else:
                messagebox.showerror("Error", "Passwords do not match.")
    
    def open_vault(self):
        """Open an existing vault."""
        password_dialog = PasswordDialog(self.root, "Open Vault", "Enter master password:")
        self.root.wait_window(password_dialog.dialog)
        
        if password_dialog.result:
            password = password_dialog.result
            if self.vault.unlock_vault(password):
                messagebox.showinfo("Success", "Vault unlocked successfully!")
                self.update_ui_state()
            else:
                messagebox.showerror("Error", "Invalid password or vault not found.")
    
    def lock_vault(self):
        """Lock the current vault."""
        if self.vault.is_unlocked:
            self.vault.lock_vault()
            self.update_ui_state()
            messagebox.showinfo("Locked", "Vault has been locked.")
    
    def refresh_notes_list(self):
        """Refresh the notes list."""
        self.notes_listbox.delete(0, tk.END)
        self.notes_list = self.vault.get_all_notes()
        
        for note_id, note in self.notes_list:
            self.notes_listbox.insert(tk.END, note.title)
    
    def on_search(self, event=None):
        """Handle search functionality."""
        if not self.vault.is_unlocked:
            return
        
        query = self.search_var.get().strip()
        if query:
            results = self.vault.search_notes(query)
            self.notes_listbox.delete(0, tk.END)
            self.notes_list = results
            for note_id, note in results:
                self.notes_listbox.insert(tk.END, note.title)
        else:
            self.refresh_notes_list()
    
    def clear_search(self):
        """Clear search and show all notes."""
        self.search_var.set("")
        self.refresh_notes_list()
    
    def on_note_select(self, event=None):
        """Handle note selection."""
        selection = self.notes_listbox.curselection()
        if selection and self.notes_list:
            index = selection[0]
            if index < len(self.notes_list):
                note_id, note = self.notes_list[index]
                self.load_note_to_editor(note_id, note)
    
    def load_note_to_editor(self, note_id: str, note: Note):
        """Load a note into the editor."""
        self.current_note_id = note_id
        self.title_var.set(note.title)
        self.tags_var.set(", ".join(note.tags))
        
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, note.content)
    
    def clear_editor(self):
        """Clear the note editor."""
        self.current_note_id = None
        self.title_var.set("")
        self.tags_var.set("")
        self.content_text.delete(1.0, tk.END)
    
    def new_note(self):
        """Create a new note."""
        self.clear_editor()
        self.title_entry.focus()
    
    def save_note(self):
        """Save the current note."""
        if not self.vault.is_unlocked:
            return
        
        title = self.title_var.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        tags_str = self.tags_var.get().strip()
        
        if not title:
            messagebox.showwarning("Missing Title", "Please enter a title for the note.")
            return
        
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        note = Note(title, content, tags)
        
        try:
            if self.current_note_id:
                self.vault.update_note(self.current_note_id, note)
                messagebox.showinfo("Saved", "Note updated successfully!")
            else:
                note_id = self.vault.add_note(note)
                self.current_note_id = note_id
                messagebox.showinfo("Saved", "Note created successfully!")
            
            self.refresh_notes_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save note: {e}")
    
    def delete_note(self):
        """Delete the current note."""
        if not self.current_note_id:
            messagebox.showwarning("No Selection", "Please select a note to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?"):
            try:
                self.vault.delete_note(self.current_note_id)
                self.clear_editor()
                self.refresh_notes_list()
                messagebox.showinfo("Deleted", "Note deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete note: {e}")
    
    def on_title_change(self, event=None):
        pass
    
    def on_tags_change(self, event=None):
        pass
    
    def on_content_change(self, event=None):
        pass
    
    def show_about(self):
        """Show about dialog."""
        about_text = """Encrypted Notes Manager
        
A secure notes application with local encryption.

Features:
• AES encryption using master password
• Create, edit, save, and delete notes
• Search functionality
• Tag support
• Local vault storage

Built with Python, Tkinter, and cryptography library."""
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = NotesManagerGUI()
    app.run()
