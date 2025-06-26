#!/usr/bin/env python3
"""
Setup script for the Encrypted Notes Manager
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages."""
    print("🔧 Setting up Encrypted Notes Manager...")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        return False
    
    print("📦 Installing dependencies...")
    
    try:
        print("   Installing cryptography...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
        print("   ✅ cryptography installed successfully")
        
        print("\n🧪 Testing installation...")
        try:
            from cryptography.fernet import Fernet
            print("   ✅ cryptography import test passed")
        except ImportError as e:
            print(f"   ❌ Import test failed: {e}")
            return False
        
        try:
            from notes_manager import NotesVault, Note
            print("   ✅ notes_manager import test passed")
        except ImportError as e:
            print(f"   ❌ notes_manager import test failed: {e}")
            return False
        
        print("\n🎉 Setup completed successfully!")
        print("\nYou can now run the application using:")
        print("  • python main.py          (GUI mode)")
        print("  • python main.py --cli    (CLI mode)")
        print("  • python demo.py          (Demo)")
        
        if os.name == 'nt':
            print("  • run.bat                 (Windows launcher)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False


if __name__ == "__main__":
    success = install_dependencies()
    if not success:
        sys.exit(1)
