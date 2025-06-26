# Cross-platform launcher for Encrypted Notes Manager (PowerShell version)
# Works on Windows PowerShell and PowerShell Core

Write-Host "🔒 Encrypted Notes Manager" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

function Find-Python {
    $pythonCommands = @('python3', 'python', 'py')
    
    foreach ($cmd in $pythonCommands) {
        try {
            $result = & $cmd --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                return $cmd
            }
        }
        catch {
            continue
        }
    }
    
    Write-Host "❌ Python not found! Please install Python 3.6+" -ForegroundColor Red
    exit 1
}

function Run-PythonScript {
    param([string]$PythonCmd, [string]$Script, [string]$Args = "")
    
    try {
        if ($Args) {
            & $PythonCmd $Script $Args
        } else {
            & $PythonCmd $Script
        }
        return $LASTEXITCODE -eq 0
    }
    catch {
        Write-Host "❌ Error running $Script`: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

$pythonCmd = Find-Python
Write-Host "Using Python: $pythonCmd" -ForegroundColor Green
Write-Host ""

do {
    Write-Host "Choose interface:"
    Write-Host "1. GUI (Graphical Interface) - Default"
    Write-Host "2. CLI (Command Line Interface)"
    Write-Host "3. Run Demo"
    Write-Host "4. Setup Dependencies"
    Write-Host "5. Exit"
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-5)"
    
    switch ($choice) {
        "1" {
            Write-Host "Starting GUI mode..." -ForegroundColor Yellow
            if (Run-PythonScript $pythonCmd "main.py" "--gui") {
                break
            }
        }
        "2" {
            Write-Host "Starting CLI mode..." -ForegroundColor Yellow
            if (Run-PythonScript $pythonCmd "main.py" "--cli") {
                break
            }
        }
        "3" {
            Write-Host "Running demo..." -ForegroundColor Yellow
            Run-PythonScript $pythonCmd "demo.py"
        }
        "4" {
            Write-Host "Setting up dependencies..." -ForegroundColor Yellow
            Run-PythonScript $pythonCmd "setup.py"
        }
        "5" {
            Write-Host "Goodbye!" -ForegroundColor Green
            exit 0
        }
        default {
            Write-Host "Invalid choice. Starting GUI mode by default..." -ForegroundColor Yellow
            if (Run-PythonScript $pythonCmd "main.py" "--gui") {
                break
            }
        }
    }
    
    Write-Host ""
} while ($true)

Write-Host ""
Read-Host "Press Enter to exit"
