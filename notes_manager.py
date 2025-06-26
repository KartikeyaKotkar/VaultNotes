import os
import json
import base64
import hashlib
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    """Handles encryption and decryption of notes using AES via Fernet."""
    
    def __init__(self):
        self.salt = None
        self.key = None
        self.fernet = None
    
    def derive_key(self, password: str, salt: bytes = None) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        self.salt = salt
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def set_password(self, password: str, salt: bytes = None):
        """Set the master password and initialize encryption."""
        self.key = self.derive_key(password, salt)
        self.fernet = Fernet(self.key)
    
    def encrypt_data(self, data: str) -> bytes:
        """Encrypt string data."""
        if not self.fernet:
            raise ValueError("Encryption not initialized. Set password first.")
        return self.fernet.encrypt(data.encode())
    
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt data back to string."""
        if not self.fernet:
            raise ValueError("Encryption not initialized. Set password first.")
        return self.fernet.decrypt(encrypted_data).decode()


class Note:
    """Represents a single note with metadata."""
    
    def __init__(self, title: str, content: str, tags: List[str] = None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = None
        self.modified_at = None
    
    def to_dict(self) -> Dict:
        """Convert note to dictionary for serialization."""
        return {
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Note':
        """Create note from dictionary."""
        note = cls(data['title'], data['content'], data.get('tags', []))
        note.created_at = data.get('created_at')
        note.modified_at = data.get('modified_at')
        return note


class NotesVault:
    """Manages the encrypted notes vault."""
    
    def __init__(self, vault_path: str = "notes_vault.enc"):
        self.vault_path = vault_path
        self.salt_path = vault_path + ".salt"
        self.encryption_manager = EncryptionManager()
        self.notes: Dict[str, Note] = {}
        self.is_unlocked = False
    
    def _save_salt(self):
        """Save salt to file."""
        if self.encryption_manager.salt:
            with open(self.salt_path, 'wb') as f:
                f.write(self.encryption_manager.salt)
    
    def _load_salt(self) -> Optional[bytes]:
        """Load salt from file."""
        if os.path.exists(self.salt_path):
            with open(self.salt_path, 'rb') as f:
                return f.read()
        return None
    
    def create_vault(self, master_password: str) -> bool:
        """Create a new vault with master password."""
        try:
            self.encryption_manager.set_password(master_password)
            self._save_salt()
            self.notes = {}
            self.is_unlocked = True
            self.save_vault()
            return True
        except Exception as e:
            print(f"Error creating vault: {e}")
            return False
    
    def unlock_vault(self, master_password: str) -> bool:
        """Unlock existing vault with master password."""
        try:
            if not os.path.exists(self.vault_path):
                return False
            
            salt = self._load_salt()
            if salt is None:
                return False
            
            self.encryption_manager.set_password(master_password, salt)
            self.load_vault()
            self.is_unlocked = True
            return True
        except Exception as e:
            print(f"Error unlocking vault: {e}")
            return False
    
    def save_vault(self):
        """Save encrypted vault to file."""
        if not self.is_unlocked:
            raise ValueError("Vault is locked")
        
        notes_data = {
            note_id: note.to_dict() 
            for note_id, note in self.notes.items()
        }
        
        json_data = json.dumps(notes_data)
        encrypted_data = self.encryption_manager.encrypt_data(json_data)
        
        with open(self.vault_path, 'wb') as f:
            f.write(encrypted_data)
    
    def load_vault(self):
        """Load and decrypt vault from file."""
        if not os.path.exists(self.vault_path):
            self.notes = {}
            return
        
        with open(self.vault_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = self.encryption_manager.decrypt_data(encrypted_data)
        notes_data = json.loads(decrypted_data)
        
        self.notes = {
            note_id: Note.from_dict(note_data)
            for note_id, note_data in notes_data.items()
        }
    
    def add_note(self, note: Note) -> str:
        """Add a new note to the vault."""
        if not self.is_unlocked:
            raise ValueError("Vault is locked")
        
        note_id = hashlib.md5(f"{note.title}_{len(self.notes)}".encode()).hexdigest()
        import datetime
        now = datetime.datetime.now().isoformat()
        note.created_at = now
        note.modified_at = now
        
        self.notes[note_id] = note
        self.save_vault()
        return note_id
    
    def update_note(self, note_id: str, note: Note):
        """Update an existing note."""
        if not self.is_unlocked:
            raise ValueError("Vault is locked")
        
        if note_id in self.notes:
            import datetime
            note.created_at = self.notes[note_id].created_at
            note.modified_at = datetime.datetime.now().isoformat()
            self.notes[note_id] = note
            self.save_vault()
    
    def delete_note(self, note_id: str):
        """Delete a note from the vault."""
        if not self.is_unlocked:
            raise ValueError("Vault is locked")
        
        if note_id in self.notes:
            del self.notes[note_id]
            self.save_vault()
    
    def search_notes(self, query: str) -> List[Tuple[str, Note]]:
        """Search notes by title, content, or tags."""
        if not self.is_unlocked:
            raise ValueError("Vault is locked")
        
        results = []
        query_lower = query.lower()
        
        for note_id, note in self.notes.items():
            if (query_lower in note.title.lower() or 
                query_lower in note.content.lower() or 
                any(query_lower in tag.lower() for tag in note.tags)):
                results.append((note_id, note))
        
        return results
    
    def get_all_notes(self) -> List[Tuple[str, Note]]:
        """Get all notes in the vault."""
        if not self.is_unlocked:
            raise ValueError("Vault is locked")
        
        return list(self.notes.items())
    
    def lock_vault(self):
        """Lock the vault."""
        self.is_unlocked = False
        self.notes = {}
        self.encryption_manager.key = None
        self.encryption_manager.fernet = None
