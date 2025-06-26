#!/bin/bash
echo "🔒 Encrypted Notes Manager"
echo "=========================="
echo ""
echo "Choose interface:"
echo "1. GUI (Graphical Interface) - Default"
echo "2. CLI (Command Line Interface)"
echo "3. Run Demo"
echo "4. Setup Dependencies"
echo "5. Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Starting GUI mode..."
        python3 main.py --gui 2>/dev/null || python main.py --gui
        ;;
    2)
        echo "Starting CLI mode..."
        python3 main.py --cli 2>/dev/null || python main.py --cli
        ;;
    3)
        echo "Running demo..."
        python3 demo.py 2>/dev/null || python demo.py
        ;;
    4)
        echo "Setting up dependencies..."
        python3 setup.py 2>/dev/null || python setup.py
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Starting GUI mode by default..."
        python3 main.py --gui 2>/dev/null || python main.py --gui
        ;;
esac

echo ""
read -p "Press Enter to exit..."
