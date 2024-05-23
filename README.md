OptiFile: File Optimization Application

OptiFile is an open-source file optimization application designed to reduce the size of images, videos, PDF files, text files, and audio files. It helps to save space on your device and improve the efficiency of your data storage and transfer processes.

## Installation
Installation of OptiFile is straightforward. You can choose one of the following methods:

## Downloading Releases
Simply download the release zip file for your system from the Releases page on GitHub. Extract the zip file and run the executable binary.

## Building From Source
If you prefer to build from source, ensure you have Python 3 installed on your system. Clone the OptiFile repository using Git:
git clone https://github.com/arp4zrex/OptiFile.git

Navigate to the cloned directory and install the required dependencies:
cd OptiFile
pip install -r requirements.txt
Once dependencies are installed, you can run OptiFile using:
python optifile.py

## Usage
After starting OptiFile, the user interface will open. Here, you can select the files you want to optimize. Follow the on-screen instructions to complete the optimization process.
Once you're in the interface, select "Select File".
Then you can choose "Optimize File" to start the optimization process.
Once completed, select "Open Optimized Folder" to navigate to the "Optimized Files" directory where you'll find the optimized files

## Create Executable in Windows
If you want to create an executable .exe file in Windows for the optifile.py script, you can follow these steps:

Open the Command Prompt (cmd) on your system.

Navigate to the directory where the optifile.py file is located using the cd command. For example: cd C:\path\to\the\directory

Once in the correct directory, run the following command:
pyinstaller --onefile --windowed optifile.py

This command tells PyInstaller to create a single-file executable (--onefile) and not to show a console window (--windowed). optifile.py is the name of the script you want to convert into an executable.
PyInstaller will start working and create a folder named dist in the current directory.
Inside the dist folder, you will find an executable file with the same name as your script but with a .exe extension.
Now users can create a shortcut to this executable file on the desktop if they wish. To do this, they can right-click on the .exe file, select "Create shortcut," and then drag that shortcut to the desktop.
By following these steps, users will be able to convert the optifile.py script into an .exe executable file and create a desktop shortcut to easily run it.

##Contributions
Contributions to OptiFile are welcome! If you have any improvements or bug fixes, feel free to submit a pull request.

##Issues and Suggestions
If you encounter any problems or have suggestions for improving OptiFile, please open an issue on the GitHub repository. Your feedback is valuable in helping us improve the application.

##License
OptiFile is licensed under the Apache License. Feel free to use and modify the code according to the terms of the license.
