import streamlit as st
import pyfurc as pf
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import shutil
import pandas as pd

# Directory to save images and plots
SAVE_DIR = "stability_analysis_files"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
#######################################################################################################################################
# Helping Functions
def set_custom_theme():
    custom_css = f"""
    <style>
        /* Background color */
        .stApp {{
            background-color: #FFFFF;
        }}
        
        /* Primary color (buttons, highlights) */
        .stButton>button {{
            background-color: #5AB4BB !important;
            color: white !important;
            border-radius: 8px;
        }}
        
        /* Navigation bar color */
        .stSidebar {{
            background-color: #5AB4BB !important;
        }}

        
        /* Text color adjustments */
        .stMarkdown, .stTextInput, .stSelectbox, .stSlider, .stRadio {{
            color: black !important;
        }}
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
    
def plot_bifurcation(P_max, parameter, energy_formula, constants):
    try:
        q = pf.Dof(parameter)
        P = pf.Load("P")
        theta = q
        for key, value in constants.items():
            globals()[key] = float(value)
    
        V = pf.Energy(eval(energy_formula))
        bf = pf.BifurcationProblem(V, name="bifurcation_solution")
        bf.set_parameter("RL1", P_max)
        
        solver = pf.BifurcationProblemSolver(bf)
        solver.solve()
        
        # Plot the Bifurcation Plot
        fig, ax = plt.subplots()
        for branch in bf.solution.raw_data:
            ax.plot(branch["U(1)"], branch["PAR(1)"])
        
        ax.set_xlabel(parameter)
        ax.set_ylabel("P")
        ax.set_title("Bifurcation Plot")
        
        # Save plot to session state and folder
        plot_path = os.path.join(SAVE_DIR, "bifurcation_plot.png")
        fig.savefig(plot_path)
        plt.close(fig)
        
        # Store the plot path in session state
        st.session_state.plot_path = plot_path
        st.session_state.plot_ready = True

    except Exception as e:
        st.error(f"An error occurred: {e}")

def save_pdf(description, uploaded_image_path, energy_formula, parameter, P_max, constants, plot_path):
    pdf_path = os.path.join(SAVE_DIR, "bifurcation_report.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Define starting positions and page dimensions
    text_y = 750
    text_x = 100
    line_height = 14  # Height of each text line
    bottom_margin = 50  # Margin to avoid text running into the footer or plot
    page_width = letter[0] - 2 * text_x

    # Function to add text and handle page breaks with word wrapping
    def add_text(text, font_size):
        nonlocal text_y
        c.setFont("Helvetica", font_size)
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                lines.append("")
                continue
            while line:
                if c.stringWidth(line, "Helvetica", font_size) <= page_width:
                    lines.append(line)
                    break
                # Split line by words to fit within page width
                split_point = len(line)
                while c.stringWidth(line[:split_point], "Helvetica", font_size) > page_width:
                    split_point = line.rfind(' ', 0, split_point)
                if split_point == -1:
                    split_point = len(line)
                lines.append(line[:split_point])
                line = line[split_point:].strip()

        for line in lines:
            if text_y <= bottom_margin:
                c.showPage()
                c.setFont("Helvetica", font_size)
                text_y = 750
            c.drawString(text_x, text_y, line)
            text_y -= line_height

    # Add the description to the PDF
    add_text("Stability Analysis:\n", 20)
    add_text("Description:", 16)
    add_text("\n" + description, 12)
    add_text("\nSketch:", 16)

    # Add uploaded image to PDF, check if there's space, else create a new page
    if uploaded_image_path:
        if text_y - 300 <= bottom_margin:
            c.showPage()
            text_y = 750
        c.drawImage(uploaded_image_path, text_x, text_y - 300, width=400, height=300)
        text_y -= 320

    # Add text for the inputs below the image, with space check
    add_text("\nEnergy Formula:\n", 12)
    add_text(f"V = {energy_formula}", 12)
    add_text(f"Parameter = {parameter}", 12)
    add_text(f"Max Parameter (P_max) = {P_max}", 12)
    for key, value in constants.items():
        add_text(f"{key} = {value}", 12)
    # Add the plot to the PDF, check if there's space, else create a new page
    if text_y - 300 <= bottom_margin:
        c.showPage()
        text_y = 750
    add_text("\nPlot:", 16)
    c.drawImage(plot_path, text_x, text_y - 300, width=400, height=300)

    # Save the PDF
    c.save()

    return pdf_path

def delete_bifurcation_folders():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    for folder in os.listdir(script_dir):
        folder_path = os.path.join(script_dir, folder)
        if os.path.isdir(folder_path) and folder.startswith("bifurcation_solution"):
            shutil.rmtree(folder_path)

def show_image(filename):
    """Displays an image in a Streamlit app."""
    try:
        image = Image.open(filename)  # Open the image file
        st.image(image, caption="Uploaded Image", use_container_width =True)  # Show the image
    except Exception as e:
        st.error(f"Error loading image: {e}")

#######################################################################################################################################
#######################################################################################################################################
##################################################### Bifurcation App #################################################################
#######################################################################################################################################
#######################################################################################################################################
# Streamlit UI
set_custom_theme()
st.title("Bifurcation App")

# Sidebar for Navigation
page = st.sidebar.radio("Navigation", ["Stability Analysis","Stable Symmetric Bifurcation", "Unstable Symmetric Bifurcation", "Asymmetric Bifurcation", "Limit Point / Saddle-node"])

# Define pages
if page == "Stability Analysis":
    delete_bifurcation_folders()
    st.subheader("Stability Analysis")
    # Description Input Section
    st.subheader("Description")
    description_input = st.text_area(
        "Enter a description for your bifurcation problem.",
        help="This description will be included at the beginning of the PDF report."
    )
    
    if st.button("Save Description"):
        st.session_state.description = description_input
        st.success("Description saved successfully!")
    
    # Image Upload Section
    st.subheader("Sketch Upload")
    uploaded_file = st.file_uploader(
        "Upload an Image", 
        type=["png", "jpg", "jpeg"],
        help="Upload an image (sketch) to visualize the problem setup."
    )
    
    # Display uploaded image
    uploaded_image_path = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        uploaded_image_path = os.path.join(SAVE_DIR, "uploaded_image.png")
        image.save(uploaded_image_path)
        st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Inputs
    st.subheader("Input Parameters")
    energy_formula = st.text_input(
        "Energy Formula V", 
        "(1 / 2) * k * (q ** 2) * l ** 2 - 2 * P * l * (1 - sp.sqrt(1 - q ** 2))",
        help="Define the energy formula (V). Use sp.cos(x), sp.sin(x), and sp.sqrt(x) for cosine(x), sine(x), and √x functions respectively. Use P as a force variable"
    )
    
    parameter = st.text_input(
        "Parameter (Degree of Freedom)", 
        "q",
        help="Enter the name of the parameter (degree of freedom) to use in the formula, `q` for translation, or `theta` for rotation."
    )
    P_max = st.number_input(
        "Max Parameter (P_max)", 
        min_value=0.0, 
        value=1.0, 
        step=0.1,
        help="Specify the maximum value for the parameter (P_max). This affects the Bifurcation Plot."
    )
    constants = st.text_input(
        "Constants", 
        "{'l': 1, 'k': 1}", 
        help="Enter the constant variables of the system. Syntax: `{'constant_name_1': value_1, constant_name_2': value_2, ...}`"
    )
    constants = eval(constants)
    if 'q' in constants:
        st.error("Constants should not contain 'q'. Please remove it.")
    elif 'theta' in constants:
        st.error("Constants should not contain 'theta'. Please remove it.")
                
        
    # Track if the plot and PDF are ready
    if "plot_ready" not in st.session_state:
        st.session_state.plot_ready = False
    
    # Plot Section
    st.subheader("Plot")
    
    # Buttons
    if st.button("Plot"):
        plot_bifurcation(P_max, parameter, energy_formula, constants)
    
    if st.button("Clear Plot"):
        st.write("Plot cleared.")
        st.session_state.plot_ready = False
    
    # Display the plot once it is generated and stored
    if st.session_state.plot_ready:
        st.image(st.session_state.plot_path, caption="Bifurcation Plot", use_container_width=True)
    
    # Automatically generate and download PDF once everything is ready
    if st.session_state.plot_ready:
        if os.path.exists(SAVE_DIR):
            plot_path = st.session_state.plot_path
            if os.path.exists(plot_path):
                pdf_path = save_pdf(
                    st.session_state.get("description", ""),
                    uploaded_image_path,
                    energy_formula,
                    parameter,
                    P_max,
                    constants,
                    plot_path
                )
                
                # Automatically trigger the download after generating the PDF
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Generate Report",  # Renamed the button
                        data=f,
                        file_name="bifurcation_report.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("Please generate the plot before downloading the PDF.")
#######################################################################################################################################
############################################### Asymmetric Bifurcation ################################################################    
elif page == "Asymmetric Bifurcation":
    delete_bifurcation_folders()
    
    st.subheader("Asymmetric Bifurcation")
    
    show_image("images/asymmetric_case.jpeg")
    
    def calculate_and_plot_q_asym_bifurc(load, length, stiffness):
        try:
            l = length
            q = pf.Dof("q")
            P = pf.Load("P")
            k = stiffness
            
            V = pf.Energy(eval("k*l*(1-sp.sqrt(1+q))**2 - P*l*(1-sp.sqrt(1-q**2))"))
            bf = pf.BifurcationProblem(V, name="bifurcation_solution")
            bf.set_parameter("RL1", 3)
            
            solver = pf.BifurcationProblemSolver(bf)
            solver.solve()
            
            # Plot the Bifurcation Plot
            fig, ax = plt.subplots()
            corresponding_q = None
            print(bf.solution.raw_data)
            raw_data_list = []
            for branch in bf.solution.raw_data:
                ax.plot(branch["U(1)"], branch["PAR(1)"])
            
                # print(branch["U(1)"], branch["PAR(1)"])
                # Convert raw_data to a pandas DataFrame
                
                # Search for the load in PAR(1) and find the corresponding q in U(1)
                for par_value, u_value in zip(branch["PAR(1)"], branch["U(1)"]):
                    raw_data_list.append({"Load (P)": par_value, "Displacement (q)": u_value})
                    if abs(par_value - load) < 1e-2:  # Tolerance for floating-point comparison
                        corresponding_q = u_value

            if corresponding_q is not None:
                # Highlight the identified point on the plot
                ax.scatter(corresponding_q, load, color="red", label=f"Point ({corresponding_q:.3f}, {load:.3f})", zorder=5)

            ax.set_xlabel("Displacement (q)")
            ax.set_ylabel("Load (P)")
            ax.set_title("Bifurcation Plot")
            ax.legend()
        
            if corresponding_q is not None:
                st.success(f"The corresponding q for load {load} is {corresponding_q:.6f}")
            else:
                st.warning(f"No corresponding q found for load {load}")
    
            return corresponding_q, fig, raw_data_list
    
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None


    def calculate_vertical_displacement(P, k):
        return P / k  # Hooke's law: displacement = force / spring constant

    def plot_deformation(L, k, P, q):
        # Compute displacements
        delta = calculate_vertical_displacement(P, k)
    
        # Initial coordinates
        x1, y1 = 0, 0
        x2, y2 = L, 0
        x3, y3 = L, L
    
        # Deformed coordinates
        x3_def = L + q * L  # Top node moves horizontally
        y3_def = L - delta  # Top node moves vertically
    
        # Plot the initial and deformed system
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot([x1, x3, x2], [y1, y3, y2], 'o-', label='Initial Configuration', color='blue')
        ax.plot([x1, x3_def, x2], [y1, y3_def, y2], 'o--', label='Deformed Configuration', color='red')
    
        # Plot settings
        ax.set_title("Deformation of the 2 Rigid Links with Spring embedded in the left one")
        ax.set_xlabel("X (cm)")
        ax.set_ylabel("Y (cm)")
        ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
        ax.legend()
        ax.grid(True)
        ax.axis('equal')
    
        return fig, delta, q * L    
    
    L = st.number_input("L (cm):", value=2.0, step=0.1)
    k = st.number_input("k (N/cm):", value=1.0, step=0.1)
    
        
    P = st.number_input("P (N):", value=1.41, step=0.1)
    # q = st.number_input("q (ratio):", value=0.2, step=0.01)
    # if st.button("Get Data Table"):
    q, fig,raw_data_list = calculate_and_plot_q_asym_bifurc(P, L, k)
    df = pd.DataFrame(raw_data_list)

    # Display the table in Streamlit
    st.subheader("Data Table (P vs. q)")
    st.dataframe(df)
    
        
    st.subheader("Plots")
    if st.button("Update Plots"):
        # q, fig = calculate_and_plot_q_asym_bifurc(P, L)
        st.pyplot(fig)
        if q:
            fig2, delta, qL = plot_deformation(L, k, P, q)
            st.pyplot(fig2)
            st.write(f"**Vertical displacement of the top node (delta):** {delta:.2f} cm")
            st.write(f"**Horizontal displacement of the top node (q*L):** {qL:.2f} cm")

#######################################################################################################################################
########################################## Stable Symmetric Bifurcation ###############################################################
elif page == "Stable Symmetric Bifurcation":
    delete_bifurcation_folders()
    
    def calculate_and_plot_theta_sym_bifurc(load, length, stiffness):
        try:
            l = length
            theta = pf.Dof("theta")
            P = pf.Load("P")
            c = stiffness
            
            V = pf.Energy(eval("2 * c * theta**2 - 2 * P * L * (1 - sp.cos(theta))"))
            bf = pf.BifurcationProblem(V, name="bifurcation_solution")
            bf.set_parameter("RL1", 3)
            
            solver = pf.BifurcationProblemSolver(bf)
            solver.solve()
            
            # Plot the Bifurcation Plot
            fig, ax = plt.subplots()
            corresponding_theta = None
            print(bf.solution.raw_data)
            raw_data_list = []
            for branch in bf.solution.raw_data:
                ax.plot(branch["U(1)"], branch["PAR(1)"])
            
                # print(branch["U(1)"], branch["PAR(1)"])
                # Convert raw_data to a pandas DataFrame
                
                # Search for the load in PAR(1) and find the corresponding q in U(1)
                for par_value, u_value in zip(branch["PAR(1)"], branch["U(1)"]):
                    raw_data_list.append({"Load (P)": par_value, "Displacement (theta)": u_value})
                    if abs(par_value - load) < 1e-2:  # Tolerance for floating-point comparison
                        corresponding_theta = u_value

            if corresponding_theta is not None:
                # Highlight the identified point on the plot
                ax.scatter(corresponding_theta, load, color="red", label=f"Point ({corresponding_theta:.3f}, {load:.3f})", zorder=5)

            ax.set_xlabel("Displacement (theta)")
            ax.set_ylabel("Load (P)")
            ax.set_title("Bifurcation Plot")
            ax.legend()
        
            if corresponding_theta is not None:
                st.success(f"The corresponding q for load {load} is {corresponding_theta:.6f}")
            else:
                st.warning(f"No corresponding q found for load {load}")
    
            return corresponding_theta, fig, raw_data_list
    
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None
            
    st.subheader("Stable Symmetric Bifurcation")
    
    show_image("images/stable_symmetric_case.jpeg")
    
    # Input fields using Streamlit widgets
    L = st.number_input("Enter L (cm):", value=2.0, step=0.1)
    c = st.number_input("Enter c (N*cm/rad):", value=1.0, step=0.1)
    P = st.number_input("Enter P (N):", value=1.31, step=0.1)
    
    theta_sym, fig,raw_data_list = calculate_and_plot_theta_sym_bifurc(P, L, c)
    df = pd.DataFrame(raw_data_list)

    # Display the table in Streamlit
    st.subheader("Data Table (P vs. Theta)")
    st.dataframe(df)
    
        
    st.subheader("Plots")
    # Compute Delta
    Delta = L * (1 - np.cos(theta_sym))
    
    # Initial coordinates
    x1, y1 = 0, 0
    x2, y2 = L, 0
    x3, y3 = 2 * L, 0
    
    # Deformed coordinates
    x1_def, y1_def = Delta, 0
    x2_def, y2_def = L + Delta / 2, abs(L * np.sin(theta_sym/1.5))
    x3_def, y3_def = x3, y3
    if st.button("Update Plot"):
        st.pyplot(fig)
        if theta_sym:
            # Plot the initial and deformed system
            fig2, ax = plt.subplots(figsize=(5, 4))
            
            ax.plot([x1, x2, x3], [y1, y2, y3], 'o-', label='Initial Configuration', color='blue')
            ax.plot([x1_def, x2_def, x3_def], [y1_def, y2_def, y3_def], 'o--', label='Deformed Configuration', color='red')
            
            # Plot settings
            ax.set_title("Deformation of 2 Rigid Links with Torsional Spring")
            ax.set_xlabel("X (cm)")
            ax.set_ylabel("Y (cm)")
            ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
            ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
            ax.legend()
            ax.grid(True)
            ax.axis('equal')
            
            # Display the plot
            st.pyplot(fig2)
            
            # Display results
            st.write(f"Applied force (P): {P} N")
            st.write(f"Angle (Theta): {np.degrees(theta_sym):.2f} degrees")
            st.write(f"Horizontal displacement of left cart (Delta): {Delta:.2f} cm")

#######################################################################################################################################
################################## Unstable Symmetric Bifurcation #####################################################################
elif page == "Unstable Symmetric Bifurcation":
    delete_bifurcation_folders()
    st.subheader("Unstable Symmetric Bifurcation")

    show_image("images/unstable_symmetric_case.jpeg")
    
    def calculate_and_plot_q_unstable_sym_bifurc(load, length, stiffness):
        try:
            l = length
            q = pf.Dof("q")
            P = pf.Load("P")
            k = stiffness
            
            V = pf.Energy(eval("(1/2) * k * q**2 * l**2 - 2 * P * l * (1 - sp.sqrt(1 - q**2))"))
            bf = pf.BifurcationProblem(V, name="bifurcation_solution")
            bf.set_parameter("RL1", 3)
            
            solver = pf.BifurcationProblemSolver(bf)
            solver.solve()
            
            # Plot the Bifurcation Plot
            fig, ax = plt.subplots()
            corresponding_q = None
            print(bf.solution.raw_data)
            raw_data_list = []
            for branch in bf.solution.raw_data:
                ax.plot(branch["U(1)"], branch["PAR(1)"])
            
                # print(branch["U(1)"], branch["PAR(1)"])
                # Convert raw_data to a pandas DataFrame
                
                # Search for the load in PAR(1) and find the corresponding q in U(1)
                for par_value, u_value in zip(branch["PAR(1)"], branch["U(1)"]):
                    raw_data_list.append({"Load (P)": par_value, "Displacement (q)": u_value})
                    if abs(par_value - load) < 1e-2:  # Tolerance for floating-point comparison
                        corresponding_q = u_value

            if corresponding_q is not None:
                # Highlight the identified point on the plot
                ax.scatter(corresponding_q, load, color="red", label=f"Point ({corresponding_q:.3f}, {load:.3f})", zorder=5)

            ax.set_xlabel("Displacement (q)")
            ax.set_ylabel("Load (P)")
            ax.set_title("Bifurcation Plot")
            ax.legend()
        
            if corresponding_q is not None:
                st.success(f"The corresponding q for load {load} is {corresponding_q:.6f}")
            else:
                st.warning(f"No corresponding q found for load {load}")
    
            return corresponding_q, fig, raw_data_list
    
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None
            
    def calculate_displacement(P, k):
        return P / k  # Hooke's law: displacement = force / spring constant
    
    
    
    # Input fields
    L = st.number_input("L (cm):", value=1.0)
    k = st.number_input("k (N/cm):", value=3.0)
    P = st.number_input("P (N):", value=0.857)
    # q = st.number_input("q (ratio):", value=0.5)
    q_unstable, fig,raw_data_list = calculate_and_plot_q_unstable_sym_bifurc(P, L, k)
    df = pd.DataFrame(raw_data_list)

    # Display the table in Streamlit
    st.subheader("Data Table (P vs. q)")
    st.dataframe(df)
    
        
    st.subheader("Plots")
    if st.button("Update Plots"):
        st.pyplot(fig)
        if q_unstable:
            # Compute displacements
            delta_x1 = calculate_displacement(P, k)
        
            # Initial coordinates
            x1, y1 = 0, 0
            x2, y2 = L, 0
            x3, y3 = 2 * L, 0
        
            # Deformed coordinates
            x1_def, y1_def = delta_x1, 0
            x2_def = L + delta_x1 / 2
            y2_def = abs(q_unstable * L)  # Vertical displacement of the center joint
            x3_def, y3_def = x3, y3
        
            # Plot the initial and deformed system
            fig2, ax = plt.subplots(figsize=(5, 4))
            ax.plot([x1, x2, x3], [y1, y2, y3], 'o-', label='Initial Configuration', color='blue')
            ax.plot([x1_def, x2_def, x3_def], [y1_def, y2_def, y3_def], 'o--', label='Deformed Configuration', color='red')
        
            # Plot settings
            ax.set_title("Deformation of the 2 Rigid Links with Spring")
            ax.set_xlabel("X (cm)")
            ax.set_ylabel("Y (cm)")
            ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
            ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
            ax.legend()
            ax.grid(True)
            ax.axis('equal')
        
            st.pyplot(fig2)
        
            # Display results
            st.write(
                f"**Applied force (P):** {P} N\n\n"
                f"**Horizontal displacement of the left cart (Delta):** {delta_x1:.2f} cm\n\n"
                f"**Center joint position:** X = {x2_def:.2f} cm, Y = {y2_def:.2f} cm"
            )

#######################################################################################################################################
############################################# Limit Point / Saddle-node ###############################################################

elif page == "Limit Point / Saddle-node":
    delete_bifurcation_folders()
            
    def calculate_vertical_displacement(P, k, theta):
        theta_rad = np.radians(theta)
        return P / (2 * k * np.cos(theta_rad))  # Hooke's law and geometry
    
    def calculate_horizontal_displacement(L, delta, theta):
        theta_rad = np.radians(theta)
        return delta * np.tan(theta_rad)  # Based on geometry of the system
    

    # Input fields
    st.subheader("Limit Point / Saddle-node")
    show_image("images/limit_point_case.jpeg")
    
    L = st.number_input("L (cm):", value=2.0, step=0.1)
    k = st.number_input("k (N/cm):", value=1.0, step=0.1)
    P = st.number_input("P (N):", value=1.13, step=0.1)
    theta_initial = st.number_input("Initial angle θ = α (degrees):", value=30.0, step=0.1)

    
    st.subheader("2D Deformation with Spring")
    if st.button("Update Plot"):
        # st.pyplot(fig4)
        # Compute displacements
        delta = calculate_vertical_displacement(P, k, theta_initial)
        x1_def = -calculate_horizontal_displacement(L, delta, theta_initial)  # Carriage moves left
        x3_def = L + x1_def  # Top node moves horizontally as the carriage moves

        # Initial coordinates
        x1, y1 = 0, 0  # Bottom-left node (carriage)
        x2, y2 = 2 * L, 0  # Bottom-right fixed node
        x3, y3 = L, L * np.tan(np.radians(theta_initial))  # Top node (initial position)

        # Deformed coordinates
        y3_def = y3 - delta  # Top node moves vertically by delta

        # Calculate the new angle theta after deformation
        new_theta = np.degrees(np.arctan((y3_def - y1) / (x3_def - x1_def)))

        # Plot the initial and deformed system
        fig, ax = plt.subplots()
        ax.plot([x1, x3, x2], [y1, y3, y2], 'o-', label='Initial Configuration', color='blue')
        ax.plot([x1_def, x3_def, x2], [y1, y3_def, y2], 'o--', label='Deformed Configuration', color='red')

        # Plot settings
        ax.set_title("Deformation of the 2D System with Spring")
        ax.set_xlabel("X (cm)")
        ax.set_ylabel("Y (cm)")
        ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
        ax.legend()
        ax.grid(True)
        ax.axis('equal')

        # Display the plot
        st.pyplot(fig)

        # Display results
        st.text((
            f"The vertical displacement (delta) is: {delta:.2f} cm\n"
            f"The horizontal displacement of the carriage is: {abs(x1_def):.2f} cm\n"
            f"The new horizontal position of the top node is: {x3_def:.2f} cm\n"
            f"The new angle theta after deformation is: {new_theta:.2f} degrees"
        ))
##############################################################################################################################################
##############################################################################################################################################