# Simulator Controller

## 1 Install python

### Windows

Do a google search for Python. Install the latest version.
During the set-up process, check the box that says "Add python.exe to PATH".

### macOS

Install from python.org or if using the Homebrew package manager, open a terminal and run:

brew install python

### Linux

Update your package index and install python 3 along with it's package manager via the terminal:

sudo apt update
sudo apt install python3 python3-pip python3-venv

## 2. Upgrade the package manager Pip

In a terminal run:

python -m pip install --upgrade pip

Note: Use python3 if required by your operating system.

## 3. Download this repository

From a terminal run: git clone xxx

## 4 Create and activate a virtual python environment

From a terminal run: python -m venv venv

### Activate for Windows (Command Promnpt)

venv\Scripts\activate.bat

### Activate for Windows (PowerShell)

venv\Scripts\Activate.ps1

### Activate for macOS/Linux

source venv/bin/activate

### Deactivate when ready

deactivate

## 5 Install Dependencies

pip install -r requirements.txt

## 6 Install headless browsers into Playwright

To install all 3: playright install
To install Chromium: playright install chromium
Or select which browser you want: playright install chromium firefox webkit

## 7 Launch the browser manually using a debugging port
        
### Windows

chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\xxx\Chrome_Profile"
    
### Mac

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/playwright_profile"

### Linux

google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

## 8. Run the script

python sim-control.py