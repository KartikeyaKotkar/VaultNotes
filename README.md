# 🔒 Encrypted Notes Manager with Local Vault

A secure desktop notes application with local encryption and password protection, built with Python.

## 🎯 Features

- **🔐 AES Encryption**: All notes are encrypted using AES via the `cryptography` library
- **🔑 Master Password**: Single master password protects your entire vault
- **📝 Note Management**: Create, edit, save, and delete notes with ease
- **🔍 Search Functionality**: Search through notes by title, content, or tags
- **🏷️ Tag Support**: Organize notes with customizable tags
- **💾 Local Storage**: All data stored locally in encrypted format
- **🖥️ Dual Interface**: Both GUI (Tkinter) and CLI modes available
- **🔒 Automatic Locking**: Secure vault locking when done

## 🚀 Installation & Quick Start

### Method 1: One-Click Setup (Recommended)
Choose the launcher that works best for your system:

**Universal Python Launcher**
```bash
python launcher.py
```
Works on all platforms with Python installed.

**Windows**
- Batch: Double-click `run.bat`
- PowerShell: Right-click `run.ps1` → "Run with PowerShell"

**Linux/macOS/Unix**
```bash
./run.sh
```
Make executable first: `chmod +x run.sh`

### Method 2: Manual Installation
1. **Install dependencies**: `python setup.py`
2. **Run the application**: Choose your preferred mode below

## 🎮 Usage

### GUI Mode (Default)
```bash
python main.py
```
or
```bash
python main.py --gui
```

### CLI Mode
```bash
python main.py --cli
```

### Direct Access
- **GUI only**: `python gui.py`
- **CLI only**: `python cli.py`

## 🔧 How It Works

### Encryption
- Uses **PBKDF2** with SHA-256 for key derivation
- **100,000 iterations** for strong password protection
- **AES encryption** via Fernet (cryptography library)
- **Random salt** generation for each vault
- `notes_vault.enc` - Encrypted notes storage
- `notes_vault.enc.salt` - Salt file for key derivation

### Security Features
- Master password required for all vault operations
- Notes are never stored in plain text
- Salt ensures unique encryption keys
- Memory is cleared when vault is locked

## 📋 GUI Features

### Main Interface
- **Notes List**: Browse all notes with search functionality
- **Note Editor**: Rich text editing with title and tags
- **Menu System**: File operations and help
- **Status Bar**: Vault status and note count

### Vault Operations
- **New Vault**: Create encrypted vault with master password
- **Open Vault**: Unlock existing vault
- **Lock Vault**: Secure vault when done

### Note Operations
- **Create**: New notes with title, content, and tags
- **Edit**: Modify existing notes
- **Delete**: Remove notes with confirmation
- **Search**: Find notes by any text or tag

## 💻 CLI Features

### Menu-Driven Interface
- Clean, intuitive command-line interface
- Numbered menu options
- Secure password input (hidden typing)

### Available Commands
1. **Create New Vault** - Set up encrypted storage
2. **Open Existing Vault** - Unlock with master password
3. **List All Notes** - View all notes with previews
4. **Search Notes** - Find notes by keyword
5. **Create New Note** - Add new note with multi-line input
6. **Edit Note** - Modify existing notes
7. **Delete Note** - Remove notes with confirmation
8. **Lock Vault** - Secure the vault

## 🛡️ Security Considerations

### Strong Practices
- **Minimum 6-character passwords** (recommend 12+ characters)
- **Unique master password** not used elsewhere
- **Regular backups** of vault files
- **Secure deletion** of temporary files

### Threat Model
- Protects against casual access to files
- Secures notes against basic file system browsing
- Requires master password for any access

### Limitations
- No protection against memory dumps while unlocked
- No network security (local storage only)
- Relies on local system security

##  Technical Details

### Dependencies
- **cryptography**: AES encryption and key derivation
- **tkinter**: GUI framework (included with Python)
- **hashlib**: Password hashing utilities
- **json**: Data serialization
- **base64**: Encoding utilities

### Classes
- **`EncryptionManager`**: Handles AES encryption/decryption
- **`Note`**: Represents individual notes with metadata
- **`NotesVault`**: Manages encrypted storage and operations
- **`NotesManagerGUI`**: Tkinter-based graphical interface
- **`NotesManagerCLI`**: Command-line interface

## ️ Future Enhancements

Potential improvements:
- **Cloud sync** with end-to-end encryption
- **Multiple vaults** support
- **Export/import** functionality
- **Note sharing** with encryption
- **Advanced search** with filters
- **Themes and customization**
- **Backup and recovery** tools

