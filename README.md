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

Step 6: Select "droplet-analysis" conda virtual environment as python interpreter by clicking blue strip in bottom left-hand corner and selecting "droplet-analysis" from dropdown menu


