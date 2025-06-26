#!/usr/bin/env python3
"""
Main entry point for the Encrypted Notes Manager
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import NotesManagerGUI
from cli import NotesManagerCLI


def main():
    parser = argparse.ArgumentParser(description='Encrypted Notes Manager')
    parser.add_argument('--cli', action='store_true', 
                       help='Run in command line interface mode')
    parser.add_argument('--gui', action='store_true', 
                       help='Run in graphical user interface mode (default)')
    
    args = parser.parse_args()
    
    if args.cli:
        print("Starting Encrypted Notes Manager - CLI Mode")
        app = NotesManagerCLI()
        app.run()
    else:
        print("Starting Encrypted Notes Manager - GUI Mode")
        try:
            app = NotesManagerGUI()
            app.run()
        except ImportError as e:
            print(f"GUI mode failed: {e}")
            print("Falling back to CLI mode...")
            app = NotesManagerCLI()
            app.run()


if __name__ == "__main__":
    main()
