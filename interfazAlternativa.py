import tkinter as tk
from tkinter import ttk, messagebox

import montecarloAlternativa
COLUMN_ORDER= None
#target_treeview = None

output_ultima_fila_detail_frames = []
output_filas_treeviews = []

TREEVIEW_COLUMNS_CONFIG = {
    "Día": {"width": 40, "anchor": tk.CENTER},
    "Ausentes": {"width": 60, "anchor": tk.CENTER},
    "Presentes": {"width": 65, "anchor": tk.CENTER},
    "Ingreso": {"width": 80, "anchor": tk.E},
    "Costo_Operativo": {"width": 110, "anchor": tk.E},
    "Costo_Salario": {"width": 100, "anchor": tk.E},
    "Costo_Total": {"width": 100, "anchor": tk.E},
    "Beneficio_Diario": {"width": 110, "anchor": tk.E},
    "Beneficio_Acumulado": {"width": 130, "anchor": tk.E}
}

COLUMN_ORDER = list(TREEVIEW_COLUMNS_CONFIG.keys())


def on_simulate_click(param_entries, ausentismo_entries_list):
    try:
        ingreso_diario = float(param_entries['ingreso_diario'].get())
        costo_operativo = float(param_entries['costo_operativo'].get())
        salario = float(param_entries['salario'].get())
        n_days = int(param_entries['n'].get())
        i_rows_to_show = int(param_entries['i'].get())
        j_start_day = int(param_entries['j'].get())

        datos_ausentismo_freq = []
        for aus_entry in ausentismo_entries_list:
            val = aus_entry.get()
            datos_ausentismo_freq.append(int(val) if val else 0)  # Treat empty as 0

        if n_days <= 0:
            messagebox.showerror("Error de Entrada", "N (Número de Días) debe ser mayor que 0.")
            return
        if i_rows_to_show < 0:
            messagebox.showerror("Error de Entrada", "I (Número de Filas a Mostrar) no puede ser negativo.")
            return
        if j_start_day <= 0:
            messagebox.showerror("Error de Entrada", "J (Día de Inicio) debe ser mayor que 0.")
            return
        if sum(datos_ausentismo_freq) != 100:
            messagebox.showerror("Error de Entrada", "La suma de las frecuencias observadas debe ser igual a 100.")
            return

    except ValueError:
        messagebox.showerror("Error de Entrada", "Por favor, ingrese números válidos en todos los campos.")
        return
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")
        return

    # Clear previous results from the GUI
    for frame in output_ultima_fila_detail_frames:
        for widget in frame.winfo_children():
            widget.destroy()

    for tree in output_filas_treeviews:
        for item in tree.get_children():
            tree.delete(item)

    # Realizar las 4 simulaciones
    for indice, cantidad_conductores in enumerate([21, 22, 23, 24]):
        target_treeview = output_filas_treeviews[indice]
        ultima_fila = montecarloAlternativa.simular(cantidad_conductores, ingreso_diario, costo_operativo, salario,   
                                      datos_ausentismo_freq, n_days, i_rows_to_show, j_start_day,target_treeview)

        # --- Display Last Day N Data (ultima_fila) ---
        target_frame_for_last_day = output_ultima_fila_detail_frames[indice]

        # Custom labels for "ultima_fila" section for clarity
        ultima_fila_labels_map = {
            'Día': f"Día ({ultima_fila.get('Día', n_days)}):",
            'Ausentes': "Ausentes:",
            'Presentes': "Presentes:",
            'Ingreso': "Ingreso:",
            'Costo_Operativo': "Costo Operativo:",
            'Costo_Salario': "Costo de Salarios:",
            'Costo_Total': "Costo Total:",
            'Beneficio_Diario': "Beneficio Diario:",
            'Beneficio_Acumulado': "Beneficio Acumulado Total:"
        }

        for row_idx, data_key in enumerate(COLUMN_ORDER):
            if data_key not in ultima_fila_labels_map:
                continue

            label_text = ultima_fila_labels_map[data_key]
            raw_value_from_dict = ultima_fila.get(data_key, "N/A") # Get original value for logic

            # Format value for display
            if isinstance(raw_value_from_dict, (int, float)):
                value_to_display = f"{raw_value_from_dict:,.2f}" if isinstance(raw_value_from_dict, float) else f"{raw_value_from_dict:,}"
            else:
                value_to_display = str(raw_value_from_dict)

            lbl_key = ttk.Label(target_frame_for_last_day, text=label_text, anchor="w")
            lbl_key.grid(row=row_idx, column=0, padx=2, pady=1, sticky=tk.W)

            lbl_val = ttk.Label(target_frame_for_last_day, text=value_to_display, anchor="e")
            lbl_val.grid(row=row_idx, column=1, padx=2, pady=1, sticky=tk.EW)
            target_frame_for_last_day.grid_columnconfigure(1, weight=1)

            if data_key == 'Beneficio_Acumulado':
                lbl_key.configure(font=('TkDefaultFont', 9, 'bold'))

                text_color = "blue" # Default color if not numeric (e.g. "N/A")
                if isinstance(raw_value_from_dict, (int, float)): # Check the original, unformatted value
                    if raw_value_from_dict >= 0:
                        text_color = "green"
                    else:
                        text_color = "red"
                lbl_val.configure(font=('TkDefaultFont', 9, 'bold'), foreground=text_color)

        # --- Populate TreeView for I rows from J ---
        
        


def imprimir_fila(fila,target_treeview):
    
    ordered_values = []
    for col_key in COLUMN_ORDER:
        val = fila.get(col_key, "")
        if isinstance(val, (int, float)):  # Basic formatting for numbers in tree
            ordered_values.append(f"{val:,.2f}" if isinstance(val, float) else f"{val:,}")
        else:
            ordered_values.append(val)
    target_treeview.insert("", tk.END, values=ordered_values)

def setup_gui_layout(app_root):
    """
    Sets up the main layout of the Tkinter GUI.
    """
    app_root.title("Simulador de Beneficios de Flota de Transporte v3.2b")
    app_root.geometry("1200x750")  # Adjusted for potentially wide tables

    # --- Input Frame ---
    input_controls_frame = ttk.LabelFrame(app_root, text="Parámetros de Simulación")
    input_controls_frame.pack(padx=10, pady=(10, 5), fill=tk.X, side=tk.TOP)

    # Parameter entries dictionary
    param_entries = {}

    # Basic parameters
    basic_params_frame = ttk.Frame(input_controls_frame)
    basic_params_frame.pack(pady=5, padx=5, fill=tk.X)

    param_definitions = {
        "ingreso_diario": ("Ingreso Diario Potencial:", "4000"),
        "costo_operativo": ("Costo Operativo Diario Fijo:", "2400"),
        "salario": ("Salario Diario por Conductor:", "30"),
        "n": ("Número de Días a Simular (N):", "10000"),
        "i": ("Número de Filas a Mostrar (I):", "10"),
        "j": ("Día de Inicio para Mostrar (J):", "1")
    }

    col_idx = 0
    for key, (text, default_val) in param_definitions.items():
        ttk.Label(basic_params_frame, text=text).grid(row=0, column=col_idx, padx=5, pady=2, sticky=tk.W)
        entry = ttk.Entry(basic_params_frame, width=10)
        entry.insert(0, default_val)
        entry.grid(row=0, column=col_idx + 1, padx=5, pady=2, sticky=tk.EW)
        param_entries[key] = entry
        basic_params_frame.grid_columnconfigure(col_idx + 1, weight=1)  # Allow entry to expand
        col_idx += 2  # Move to next pair of label/entry

    # Ausentismo data input (table-like)
    ausentismo_input_frame = ttk.LabelFrame(input_controls_frame,
                                            text="Frecuencia de Ausentismo (X días en un periodo de 100 días)")
    ausentismo_input_frame.pack(pady=5, padx=5, fill=tk.X)

    ausentismo_entries_list = []
    ausentismo_labels_text = ["0 Ausentes:", "1 Ausente:", "2 Ausentes:", "3 Ausentes:", "4 Ausentes:",
                              "5 o más Ausentes:"]
    # Example: In a 100-day period, 0 absences occurred on 10 days, 1 absence on 20 days, etc.
    default_ausentismo_values = ["36", "38", "19", "6", "1", "0"]

    for i, label_text in enumerate(ausentismo_labels_text):
        ttk.Label(ausentismo_input_frame, text=label_text).grid(row=0, column=i * 2, padx=(10, 2), pady=5, sticky=tk.W)
        entry = ttk.Entry(ausentismo_input_frame, width=6)
        entry.insert(0, default_ausentismo_values[i])
        entry.grid(row=0, column=i * 2 + 1, padx=(0, 10), pady=5, sticky=tk.EW)
        ausentismo_entries_list.append(entry)
        ausentismo_input_frame.grid_columnconfigure(i * 2 + 1, weight=1)

    # --- Simulation Button ---
    simulate_btn = ttk.Button(app_root, text="Ejecutar Simulación",
                              command=lambda: on_simulate_click(param_entries, ausentismo_entries_list))
    simulate_btn.pack(pady=(5, 10), fill=tk.X, padx=10)

    # --- Output Display Area ---
    output_main_frame = ttk.LabelFrame(app_root, text="Resultados de Simulación")
    output_main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    num_simulations = 4
    sim_conductors = [21, 22, 23, 24]  # As per simulation_logic.py

    for i in range(num_simulations):
        # Create a column frame for each simulation's results
        sim_result_column_frame = ttk.Frame(output_main_frame)
        sim_result_column_frame.grid(row=0, column=i, padx=5, pady=5, sticky=tk.NSEW)
        output_main_frame.grid_columnconfigure(i, weight=1)  # Allow columns to expand

        # Title for this simulation column
        ttk.Label(sim_result_column_frame, text=f"Simulación: {sim_conductors[i]} Conductores",
                  font=('TkDefaultFont', 10, 'bold')).pack(pady=(0, 5), fill=tk.X)

        # Frame for "ultima_fila" (Last Day N details)
        last_day_details_frame = ttk.LabelFrame(sim_result_column_frame, text="Resumen del Día N Final")
        # CORRECTED LINE:
        last_day_details_frame.pack(pady=5, fill=tk.X, expand=False)  # Don't expand this part too much
        output_ultima_fila_detail_frames.append(last_day_details_frame)

        # TreeView for "i filas desde j"
        ttk.Label(sim_result_column_frame, text="Detalle Días Seleccionados:").pack(pady=(10, 2), anchor=tk.W)

        tree_container_frame = ttk.Frame(sim_result_column_frame)  # To hold treeview and scrollbars
        tree_container_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_container_frame, columns=tuple(COLUMN_ORDER), show='headings', height=7)

        for col_key in COLUMN_ORDER:
            col_config = TREEVIEW_COLUMNS_CONFIG[col_key]
            tree.heading(col_key, text=col_key)
            tree.column(col_key, width=col_config["width"], anchor=col_config["anchor"],
                        stretch=tk.YES)  # Allow stretch

        # Scrollbars for the treeview
        ysb = ttk.Scrollbar(tree_container_frame, orient=tk.VERTICAL, command=tree.yview)
        xsb = ttk.Scrollbar(tree_container_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        xsb.pack(side=tk.BOTTOM, fill=tk.X)  # Place X scrollbar below Y scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        output_filas_treeviews.append(tree)

    output_main_frame.grid_rowconfigure(0, weight=1)  # Allow row containing results to expand


def iniciar_interfaz():
    root = tk.Tk()
    # Use a modern theme if available
    style = ttk.Style(root)
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")
    elif "vista" in available_themes:  # For Windows
        style.theme_use("vista")
    elif "aqua" in available_themes:  # For macOS
        style.theme_use("aqua")

    setup_gui_layout(root)
    root.mainloop()
