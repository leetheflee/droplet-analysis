# Droplet analysis

The following steps are for Windows installation

Step 1: Download miniconda for Windows https://docs.conda.io/en/latest/miniconda.html
Install using default configurations
EXCEPT: select "add miniconda to my PATH enivironment variable" (ignore warning)

Step 2: Download droplet-analysis repository as .zip file
Extract in appropriate location on PC

Step 3: Install VSCode for Windows: https://code.visualstudio.com/download
Open VSCode from Start menu
VS Code will prompt you to install python extension, do this.
select miniconda as python interpreter in VS Code

Step 4: In VSCode: click file>open folder (droplet-analysis)

Step 5: Open a terminal in VS Code from top toolbar
Paste the following command into the terminal: `conda create --name droplet-analysis --file requirements.txt python=3.9` - this will create a virtual environment for us to run our code in.
After installation of packages is complete restart VS Code

Step 6: Run `conda init droplet-analysis` in the powershell terminal in VSCode

Step 7: If you see the following the error in your terminal:  File C:\Users\User\Documents\WindowsPowerShell\profile.ps1 cannot be loaded because running scripts is
    disabled on this system. For more information, see about_Execution_Policies at
    https:/go.microsoft.com/fwlink/?LinkID=135170.
    
    Open your Windows Powershell as administrator and run the following command: set-executionpolicy remotesigned

Step 8: Select "droplet-analysis" conda virtual environment as python interpreter by clicking blue strip in bottom left-hand corner and selecting "droplet-analysis" from dropdown menu

Step 9: Change the input variable in the script you want to use to 'input'

Step 10: Place directories with numbers as file names (e.g. protein concentration in µM or PEG %) and hit run
