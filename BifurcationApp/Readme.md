# Bifurcation App

<!-- TOC -->
<!-- TOC:BEGIN -->
- [Bifurcation App Dependency Installation Guide](#bifurcation-app-dependency-installation-guide)
  - [Step 1: Install WSL (Windows Subsystem for Linux)](#step-1-install-wsl-windows-subsystem-for-linux)
  - [Step 2: Update and Install Required Packages in Ubuntu](#step-2-update-and-install-required-packages-in-ubuntu)
  - [Step 3: Set Up a Virtual Environment](#step-3-set-up-a-virtual-environment)
  - [Step 4: Install Jupyter Notebook](#step-4-install-jupyter-notebook)
  - [Step 5: Reopen Terminal and Install Additional Tools for the Application](#step-5-reopen-terminal-and-install-additional-tools-for-the-application)
  - [Step 6: Visualize the Application](#step-6-visualize-the-application)
  - [Step 7 (When Needed): Debug the Application Code](#step-7-when-needed-debug-the-application-code)
- [Bifurcation Application: Functionalities](#bifurcation-application-functionalities)
- [Bifurcation Application: Outlook](#bifurcation-application-outlook)
<!-- TOC:END -->

## Bifurcation App Dependency Installation Guide

### Step 1: Install WSL (Windows Subsystem for Linux)

1. Open PowerShell as Administrator:
   - Right-click on the Start Menu and select **Windows PowerShell (Admin)**.
   - Alternatively, search for **PowerShell** in the Start menu, right-click, and run it as Administrator.

2. Run the WSL installation command in PowerShell:
   ```
   wsl --install
   ```
   This command enables WSL, installs WSL 2, and installs the default Linux distribution (usually Ubuntu).

3. Set up your username and password for the Linux environment.

4. If necessary, reboot your system: After installation, PowerShell may prompt you to restart your computer. Once rebooted, Ubuntu will automatically be installed, and you’ll be prompted to set up your username and password for the Linux environment.

### Step 2: Update and Install Required Packages in Ubuntu

1. Open Ubuntu (WSL) Terminal: Once Ubuntu is installed, you can open it either from the Start menu or by typing ubuntu in the Windows search bar. This will open a Linux terminal.

2. Update the package list: It’s always a good practice to update the package list before installing anything. Run:
   ```
   sudo apt update
   ```

3. Install Python and development packages: Now, install Python-related packages that will help you set up Jupyter and virtual environments:
   ```
   sudo apt install python3-pip python3-dev
   ```
   - `python3-pip`: The package installer for Python 3.
   - `python3-dev`: Essential development headers for compiling Python modules.

### Step 3: Set Up a Virtual Environment

1. Install virtualenv: Install virtualenv, which is used to create isolated Python environments:
   ```
   sudo apt install virtualenv
   ```

2. Create a new directory for your project: Create a directory where you will set up your virtual environment and project files:
   ```
   mkdir ~/myprojects
   cd ~/myprojects
   ```

3. Create a virtual environment: Use virtualenv to create a virtual environment named BifurcationApp:
   ```
   virtualenv BifurcationApp
   ```
   This creates a directory `myprojects` containing a clean Python environment.

4. Activate the virtual environment: Once the environment is created, activate it using:
   ```
   source BifurcationApp/bin/activate
   ```
   After activation, the terminal will show `(BifurcationApp)` before the prompt, indicating the virtual environment is active.

### Step 4: Install Jupyter Notebook

Jupyter Notebook is an interactive web-based tool that allows you to create and share documents with live code, equations, visualizations, and narrative text.

- Interactive Coding: Run code in real-time and see results instantly, making it great for exploration and debugging.
- Data Visualization: Supports inline charts and graphs for data analysis with libraries like Matplotlib and Seaborn.

1. Install Jupyter Notebook: While the virtual environment is active, install Jupyter Notebook using pip:
   ```
   pip install jupyter
   ```

2. Launch Jupyter Notebook: After installation, run Jupyter Notebook:
   ```
   jupyter notebook
   ```
   This will open Jupyter Notebook in your default web browser, allowing you to create and run Python notebooks.

3. Close the Terminal: When you're done using Jupyter Notebook, you can simply close the terminal window, or stop Jupyter using `Ctrl+C` in the terminal.

### Step 5: Reopen Terminal and Install Additional Tools for the Application

1. Open Ubuntu (WSL) again: You can reopen the terminal from the Start menu or using the command `ubuntu` in the search bar.

2. Activate the virtual environment: Make sure to activate your virtual environment again:
   ```
   source ~/myprojects/BifurcationApp/bin/activate
   ```

3. Install gfortran: gfortran is the GNU Fortran compiler, and you’ll need it to work with Fortran-based projects:
   ```
   sudo apt install gfortran
   ```

4. Install Bifurcation App needed Python libraries:
   ```
   pip install -r requirements.txt
   ```

### Step 6: Visualize the Application

1. Open Ubuntu (WSL) again

2. Activate the virtual environment: Make sure to activate your virtual environment again:
   ```
   source ~/myprojects/BifurcationApp/bin/activate
   ```

3. Run command: 
   ```
   streamlit run BifurcationUI.py
   ```

### Step 7 (When Needed): Debug the Application Code

1. Open Ubuntu (WSL) in a new window

2. Activate the virtual environment: Make sure to activate your virtual environment again:
   ```
   source ~/myprojects/BifurcationApp/bin/activate
   ```

3. Run command: 
   ```
   jupyter notebook
   ```

4. Search for the code file "BifurcationUI.py" in the Jupyter Notebook folder.

## Bifurcation Application: Functionalities

The Bifurcation App provides several functionalities to analyze and visualize bifurcation problems. Below are the main features:

1. **Stability Analysis**:
   - Allows users to input a description and upload a sketch of the bifurcation problem.
   - Users can define the energy formula, parameter, maximum parameter value, and constants.
   - Generates and displays a bifurcation plot.
   - Provides an option to generate a PDF report containing the description, sketch, energy formula, parameters, constants, and bifurcation plot.

2. **Asymmetric Bifurcation**:
   - Visualizes the asymmetric bifurcation case with an image.
   - Allows users to input parameters such as length, stiffness, and load.
   - Calculates and plots the bifurcation plot for the asymmetric case.
   - Displays a data table of load vs. displacement.
   - Plots the deformation of the system and displays the vertical and horizontal displacements.

3. **Stable Symmetric Bifurcation**:
   - Visualizes the stable symmetric bifurcation case with an image.
   - Allows users to input parameters such as length, stiffness, and load.
   - Calculates and plots the bifurcation plot for the stable symmetric case.
   - Displays a data table of load vs. displacement.
   - Plots the deformation of the system and displays the horizontal displacement and angle.

4. **Unstable Symmetric Bifurcation**:
   - Visualizes the unstable symmetric bifurcation case with an image.
   - Allows users to input parameters such as length, stiffness, and load.
   - Calculates and plots the bifurcation plot for the unstable symmetric case.
   - Displays a data table of load vs. displacement.
   - Plots the deformation of the system and displays the horizontal displacement and center joint position.

5. **Limit Point / Saddle-node**:
   - Visualizes the limit point/saddle-node bifurcation case with an image.
   - Allows users to input parameters such as length, stiffness, load, and initial angle.
   - Calculates and plots the deformation of the 2D system with a spring.
   - Displays the vertical and horizontal displacements and the new angle after deformation.

## Bifurcation Application: Outlook

### Improvements

1. **Enhanced User Interface**:
   - Improve the user interface for better usability and aesthetics.
   - Add more interactive elements and visual aids to help users understand the bifurcation concepts better.

2. **Error Handling and Validation**:
   - Implement more robust error handling and input validation to ensure the application runs smoothly and provides meaningful error messages.

3. **Performance Optimization**:
   - Optimize the performance of the application, especially for complex calculations and large datasets.

4. **Documentation and Tutorials**:
   - Provide comprehensive documentation and tutorials to help users understand how to use the application effectively.

### Adding More Cases

To implement more pages for additional bifurcation cases, follow these steps:

1. **Define the New Case**:
   - Identify the new bifurcation case you want to add and define its parameters, energy formula, and any specific calculations required.

2. **Create a New Page**:
   - In the `BifurcationUI.py` file, add a new section for the new case. Use the existing cases as a template.
   - Define the input fields, calculations, and plots for the new case.

3. **Add Navigation**:
   - Update the sidebar navigation to include the new case. Add a new option to the `st.sidebar.radio` function.

4. **Implement Calculations and Plots**:
   - Implement the necessary calculations and plots for the new case. Use the existing helper functions or create new ones as needed.

5. **Test the New Case**:
   - Thoroughly test the new case to ensure it works correctly and provides accurate results.

By following these steps, you can extend the Bifurcation App to include more bifurcation cases and provide a more comprehensive tool for analyzing and visualizing bifurcation problems.