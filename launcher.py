#!/usr/bin/env python3
"""
Cross-platform launcher for Encrypted Notes Manager
Works on Windows, Linux, macOS, and other systems with Python
"""

import os
import sys
import subprocess
import platform

def find_python():
    """Find the best Python executable"""
    python_commands = ['python3', 'python', 'py']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return cmd
        except FileNotFoundError:
            continue
    
    print("❌ Python not found! Please install Python 3.6+")
    sys.exit(1)

def run_command(python_cmd, script, args=""):
    """Run a Python script with the given Python command"""
    cmd = f"{python_cmd} {script} {args}"
    try:
        if platform.system() == "Windows":
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        return False
    return True

def main():
    print("🔒 Encrypted Notes Manager")
    print("==========================")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("")
    
    python_cmd = find_python()
    print(f"Using Python: {python_cmd}")
    print("")
    
    while True:
        print("Choose interface:")
        print("1. GUI (Graphical Interface) - Default")
        print("2. CLI (Command Line Interface)")
        print("3. Run Demo")
        print("4. Setup Dependencies")
        print("5. Exit")
        print("")
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
        
        if choice == "1" or choice == "":
            print("Starting GUI mode...")
            if run_command(python_cmd, "main.py", "--gui"):
                break
        elif choice == "2":
            print("Starting CLI mode...")
            if run_command(python_cmd, "main.py", "--cli"):
                break
        elif choice == "3":
            print("Running demo...")
            run_command(python_cmd, "demo.py")
        elif choice == "4":
            print("Setting up dependencies...")
            run_command(python_cmd, "setup.py")
        elif choice == "5":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-5.")
        
        print("")

if __name__ == "__main__":
    main()
