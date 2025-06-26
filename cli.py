#!/usr/bin/env python3
"""
Command Line Interface for the Encrypted Notes Manager
"""

import os
import sys
import getpass
from typing import List, Tuple
from notes_manager import NotesVault, Note


class NotesManagerCLI:
    """Command Line Interface for the Encrypted Notes Manager."""
    
    def __init__(self):
        self.vault = NotesVault()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("         🔒 ENCRYPTED NOTES MANAGER 🔒")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print the main menu."""
        print("📋 MAIN MENU:")
        print("-" * 30)
        if not self.vault.is_unlocked:
            print("1. Create New Vault")
            print("2. Open Existing Vault")
        else:
            print("1. List All Notes")
            print("2. Search Notes")
            print("3. Create New Note")
            print("4. Edit Note")
            print("5. Delete Note")
            print("6. Lock Vault")
        print("0. Exit")
        print("-" * 30)
    
    def get_password(self, prompt: str = "Enter password: ") -> str:
        """Get password input securely."""
        return getpass.getpass(prompt)
    
    def get_input(self, prompt: str) -> str:
        return input(prompt).strip()
    
    def wait_for_key(self):
        input("\nPress Enter to continue...")
    
    def create_vault(self):
        """Create a new vault."""
        print("\n🔐 CREATE NEW VAULT")
        print("-" * 30)
        
        password = self.get_password("Enter master password: ")
        if len(password) < 6:
            print("❌ Password should be at least 6 characters long.")
            self.wait_for_key()
            return
        
        confirm_password = self.get_password("Confirm master password: ")
        if password != confirm_password:
            print("❌ Passwords do not match.")
            self.wait_for_key()
            return
        
        if self.vault.create_vault(password):
            print("✅ Vault created successfully!")
        else:
            print("❌ Failed to create vault.")
        
        self.wait_for_key()
    
    def open_vault(self):
        """Open an existing vault."""
        print("\n🔓 OPEN VAULT")
        print("-" * 30)
        
        if not os.path.exists(self.vault.vault_path):
            print("❌ No vault found. Please create a new vault first.")
            self.wait_for_key()
            return
        
        password = self.get_password("Enter master password: ")
        
        if self.vault.unlock_vault(password):
            print("✅ Vault unlocked successfully!")
        else:
            print("❌ Invalid password.")
        
        self.wait_for_key()
    
    def list_notes(self):
        """List all notes."""
        print("\n📝 ALL NOTES")
        print("-" * 50)
        
        notes = self.vault.get_all_notes()
        if not notes:
            print("No notes found.")
            self.wait_for_key()
            return
        
        for i, (note_id, note) in enumerate(notes, 1):
            tags_str = f" [Tags: {', '.join(note.tags)}]" if note.tags else ""
            print(f"{i}. {note.title}{tags_str}")
            if note.content:
                preview = note.content[:100] + "..." if len(note.content) > 100 else note.content
                print(f"   {preview}")
            print()
        
        self.wait_for_key()
    
    def search_notes(self):
        """Search notes."""
        print("\n🔍 SEARCH NOTES")
        print("-" * 30)
        
        query = self.get_input("Enter search query: ")
        if not query:
            return
        
        results = self.vault.search_notes(query)
        if not results:
            print("No notes found matching your query.")
            self.wait_for_key()
            return
        
        print(f"\nFound {len(results)} result(s):")
        print("-" * 40)
        
        for i, (note_id, note) in enumerate(results, 1):
            tags_str = f" [Tags: {', '.join(note.tags)}]" if note.tags else ""
            print(f"{i}. {note.title}{tags_str}")
            if note.content:
                preview = note.content[:100] + "..." if len(note.content) > 100 else note.content
                print(f"   {preview}")
            print()
        
        self.wait_for_key()
    
    def create_note(self):
        """Create a new note."""
        print("\n✏️  CREATE NEW NOTE")
        print("-" * 30)
        
        title = self.get_input("Enter note title: ")
        if not title:
            print("❌ Title is required.")
            self.wait_for_key()
            return
        
        print("Enter note content (press Ctrl+D or Ctrl+Z to finish):")
        content_lines = []
        try:
            while True:
                line = input()
                content_lines.append(line)
        except EOFError:
            pass
        
        content = "\n".join(content_lines)
        
        tags_input = self.get_input("Enter tags (comma-separated, optional): ")
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        note = Note(title, content, tags)
        note_id = self.vault.add_note(note)
        
        print(f"✅ Note '{title}' created successfully!")
        self.wait_for_key()
    
    def edit_note(self):
        """Edit an existing note."""
        print("\n📝 EDIT NOTE")
        print("-" * 30)
        
        notes = self.vault.get_all_notes()
        if not notes:
            print("No notes found.")
            self.wait_for_key()
            return
        
        # List notes for selection
        print("Select a note to edit:")
        for i, (note_id, note) in enumerate(notes, 1):
            print(f"{i}. {note.title}")
        
        try:
            choice = int(self.get_input("Enter note number: "))
            if 1 <= choice <= len(notes):
                note_id, note = notes[choice - 1]
                self.edit_note_content(note_id, note)
            else:
                print("❌ Invalid selection.")
                self.wait_for_key()
        except ValueError:
            print("❌ Please enter a valid number.")
            self.wait_for_key()
    
    def edit_note_content(self, note_id: str, note: Note):
        """Edit the content of a specific note."""
        print(f"\n📝 EDITING: {note.title}")
        print("-" * 40)
        
        print("Current content:")
        print(note.content)
        print("-" * 40)
        
        new_title = self.get_input(f"New title (current: {note.title}): ")
        if new_title:
            note.title = new_title
        
        print("Enter new content (press Ctrl+D or Ctrl+Z to finish, leave empty to keep current):")
        content_lines = []
        try:
            while True:
                line = input()
                content_lines.append(line)
        except EOFError:
            pass
        
        if content_lines:
            note.content = "\n".join(content_lines)
        
        current_tags = ", ".join(note.tags) if note.tags else ""
        new_tags_input = self.get_input(f"New tags (current: {current_tags}): ")
        if new_tags_input:
            note.tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
        
        self.vault.update_note(note_id, note)
        print("✅ Note updated successfully!")
        self.wait_for_key()
    
    def delete_note(self):
        """Delete a note."""
        print("\n🗑️  DELETE NOTE")
        print("-" * 30)
        
        notes = self.vault.get_all_notes()
        if not notes:
            print("No notes found.")
            self.wait_for_key()
            return
        
        # List notes for selection
        print("Select a note to delete:")
        for i, (note_id, note) in enumerate(notes, 1):
            print(f"{i}. {note.title}")
        
        try:
            choice = int(self.get_input("Enter note number: "))
            if 1 <= choice <= len(notes):
                note_id, note = notes[choice - 1]
                
                confirm = self.get_input(f"Are you sure you want to delete '{note.title}'? (y/N): ")
                if confirm.lower() == 'y':
                    self.vault.delete_note(note_id)
                    print("✅ Note deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
        
        self.wait_for_key()
    
    def lock_vault(self):
        """Lock the vault."""
        self.vault.lock_vault()
        print("🔒 Vault locked.")
        self.wait_for_key()
    
    def run(self):
        """Run the CLI application."""
        while self.running:
            self.clear_screen()
            self.print_header()
            
            if self.vault.is_unlocked:
                print(f"🔓 Vault Status: UNLOCKED ({len(self.vault.notes)} notes)")
            else:
                print("🔒 Vault Status: LOCKED")
            
            print()
            self.print_menu()
            
            try:
                choice = self.get_input("Enter your choice: ")
                
                if choice == "0":
                    self.running = False
                    print("👋 Goodbye!")
                    break
                elif not self.vault.is_unlocked:
                    if choice == "1":
                        self.create_vault()
                    elif choice == "2":
                        self.open_vault()
                    else:
                        print("❌ Invalid choice.")
                        self.wait_for_key()
                else:
                    if choice == "1":
                        self.list_notes()
                    elif choice == "2":
                        self.search_notes()
                    elif choice == "3":
                        self.create_note()
                    elif choice == "4":
                        self.edit_note()
                    elif choice == "5":
                        self.delete_note()
                    elif choice == "6":
                        self.lock_vault()
                    else:
                        print("❌ Invalid choice.")
                        self.wait_for_key()
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                self.running = False
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                try:
                    self.wait_for_key()
                except (EOFError, KeyboardInterrupt):
                    self.running = False
                    break


if __name__ == "__main__":
    app = NotesManagerCLI()
    app.run()
