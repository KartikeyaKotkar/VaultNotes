#!/usr/bin/env python3
"""
Demo script to showcase the Encrypted Notes Manager functionality
"""

import os
import sys
import tempfile
from notes_manager import NotesVault, Note

def demo_encryption_features():
    """Demonstrate the core encryption features."""
    print("🔒 ENCRYPTED NOTES MANAGER DEMO")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    vault_path = os.path.join(temp_dir, "demo_vault.enc")
    
    print(f"📁 Demo vault location: {vault_path}")
    print()
    
    vault = NotesVault(vault_path)
    
    print("1️⃣ Creating new vault with master password...")
    master_password = "demo_password_123"
    if vault.create_vault(master_password):
        print("✅ Vault created successfully!")
    else:
        print("❌ Failed to create vault!")
        return
    
    print(f"📊 Vault status: {'🔓 UNLOCKED' if vault.is_unlocked else '🔒 LOCKED'}")
    print()
    
    print("2️⃣ Adding sample notes...")
    
    notes_data = [
        {
            "title": "Meeting Notes - Q1 Planning",
            "content": "Discussed quarterly goals:\n- Increase revenue by 15%\n- Launch new product line\n- Hire 3 new developers\n\nNext meeting: Friday 2PM",
            "tags": ["meeting", "planning", "Q1", "business"]
        },
        {
            "title": "Personal - Grocery List",
            "content": "Weekly shopping:\n- Milk\n- Bread\n- Eggs\n- Chicken\n- Vegetables (broccoli, carrots)\n- Fruit (apples, bananas)",
            "tags": ["personal", "shopping", "grocery"]
        },
        {
            "title": "Tech Notes - Python Best Practices",
            "content": "Key principles:\n1. Follow PEP 8 style guide\n2. Use meaningful variable names\n3. Write docstrings for functions\n4. Handle exceptions properly\n5. Use virtual environments",
            "tags": ["tech", "python", "programming", "best-practices"]
        },
        {
            "title": "Book Ideas",
            "content": "Potential books to read:\n- 'Clean Code' by Robert Martin\n- 'The Pragmatic Programmer'\n- 'Design Patterns'\n- 'Effective Python'",
            "tags": ["books", "learning", "programming"]
        }
    ]
    
    note_ids = []
    for note_data in notes_data:
        note = Note(note_data["title"], note_data["content"], note_data["tags"])
        note_id = vault.add_note(note)
        note_ids.append(note_id)
        print(f"  ✅ Added: {note_data['title']}")
    
    print(f"📊 Total notes in vault: {len(vault.notes)}")
    print()
    
    # Demo 3: Search functionality
    print("3️⃣ Testing search functionality...")
    
    search_queries = ["python", "meeting", "personal"]
    for query in search_queries:
        results = vault.search_notes(query)
        print(f"🔍 Search '{query}': {len(results)} result(s)")
        for note_id, note in results:
            print(f"  - {note.title}")
    print()
    
    print("4️⃣ Testing vault locking/unlocking...")
    print("🔒 Locking vault...")
    vault.lock_vault()
    print(f"📊 Vault status: {'🔓 UNLOCKED' if vault.is_unlocked else '🔒 LOCKED'}")
    
    print("🔓 Unlocking vault with master password...")
    if vault.unlock_vault(master_password):
        print("✅ Vault unlocked successfully!")
    else:
        print("❌ Failed to unlock vault!")
    
    print(f"📊 Vault status: {'🔓 UNLOCKED' if vault.is_unlocked else '🔒 LOCKED'}")
    print(f"📊 Notes accessible: {len(vault.notes)}")
    print()
    
    print("5️⃣ Updating a note...")
    if note_ids:
        note_id = note_ids[0]
        note = vault.notes[note_id]
        original_title = note.title
        note.title = f"{original_title} (UPDATED)"
        note.content += "\n\n[UPDATE] This note was modified in the demo."
        vault.update_note(note_id, note)
        print(f"✅ Updated note: {original_title}")
    print()
    
    print("6️⃣ Verifying file encryption...")
    print(f"📁 Vault file exists: {os.path.exists(vault.vault_path)}")
    print(f"📁 Salt file exists: {os.path.exists(vault.salt_path)}")
    
    if os.path.exists(vault.vault_path):
        with open(vault.vault_path, 'rb') as f:
            encrypted_content = f.read()[:100]
        
        print(f"📄 Encrypted file size: {len(encrypted_content)} bytes (showing first 100)")
        print(f"🔒 Encrypted content (hex): {encrypted_content.hex()}")
    print()
    
    print("7️⃣ Testing wrong password protection...")
    vault.lock_vault()
    wrong_password = "wrong_password_456"
    print(f"🔐 Attempting unlock with wrong password: '{wrong_password}'")
    if vault.unlock_vault(wrong_password):
        print("❌ Security issue: Wrong password accepted!")
    else:
        print("✅ Security working: Wrong password rejected!")
    
    print(f"🔐 Unlocking with correct password...")
    vault.unlock_vault(master_password)
    print()
    
    print("8️⃣ Final vault contents:")
    all_notes = vault.get_all_notes()
    for i, (note_id, note) in enumerate(all_notes, 1):
        tags_str = f" [Tags: {', '.join(note.tags)}]" if note.tags else ""
        print(f"  {i}. {note.title}{tags_str}")
        # Show content preview
        preview = note.content[:80] + "..." if len(note.content) > 80 else note.content
        print(f"     {preview}")
        print()
    
    print("🧹 Cleaning up demo files...")
    vault.lock_vault()
    try:
        os.remove(vault.vault_path)
        os.remove(vault.salt_path)
        os.rmdir(temp_dir)
        print("✅ Demo files cleaned up!")
    except Exception as e:
        print(f"⚠️ Cleanup warning: {e}")
    
    print("\n🎉 Demo completed successfully!")
    print("\nKey features demonstrated:")
    print("✅ AES encryption with master password")
    print("✅ Secure note storage and retrieval")
    print("✅ Search functionality")
    print("✅ Tag support")
    print("✅ Vault locking/unlocking")
    print("✅ Password protection")
    print("✅ Local file encryption")


if __name__ == "__main__":
    demo_encryption_features()
