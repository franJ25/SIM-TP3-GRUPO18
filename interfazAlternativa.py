import tkinter as tk
from tkinter import ttk, messagebox
import montecarloAlternativa

# --- Variables Globales para los Widgets de la GUI que necesitan ser accedidos globalmente ---
tree_distribucion = None
tree_filas_simulacion = None
last_day_details_frame = None

# --- Configuración de Columnas para la Tabla de Resultados de la Simulación ---
TREEVIEW_COLUMNS_CONFIG = {
    "Día": {"width": 40, "anchor": tk.CENTER},
    "RND Ausentismo": {"width": 110, "anchor": tk.CENTER},
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
    """Se ejecuta al hacer clic en el botón de simulación."""
    try:
        # Recoger y validar todos los parámetros de entrada de la GUI
        conductores_totales = int(param_entries['conductores_totales'].get())
        ingreso_diario = float(param_entries['ingreso_diario'].get())
        costo_operativo = float(param_entries['costo_operativo'].get())
        salario = float(param_entries['salario'].get())
        n_days = int(param_entries['n'].get())
        i_rows_to_show = int(param_entries['i'].get())
        j_start_day = int(param_entries['j'].get())

        datos_ausentismo_freq = [int(entry.get() or 0) for entry in ausentismo_entries_list]

        if conductores_totales < 20:
            messagebox.showerror("Error de Entrada", "La cantidad de conductores debe ser mayor o igual que 20.")
            return
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

    # Limpiar resultados anteriores
    for item in tree_distribucion.get_children():
        tree_distribucion.delete(item)
    for widget in last_day_details_frame.winfo_children():
        widget.destroy()
    for item in tree_filas_simulacion.get_children():
        tree_filas_simulacion.delete(item)

    # Ejecutar simulación
    resultados = montecarloAlternativa.simular(
        conductores_totales, ingreso_diario, costo_operativo, salario,
        datos_ausentismo_freq, n_days, i_rows_to_show, j_start_day
    )

    # Rellenar Tabla de Distribución
    cota_inferior = 0.0
    num_obreros_aus_posibles = [0, 1, 2, 3, 4, 5]
    for i, prob in enumerate(resultados['distribucion']):
        if prob == 0:
            continue
        prob_acum = resultados['probabilidades_acumuladas'][i]
        cota_superior = prob_acum - 0.01
        intervalo_rnd = f"{cota_inferior:.2f} - {cota_superior:.2f}"
        if i == len(resultados['distribucion']) - 1:
            intervalo_rnd = f"{cota_inferior:.2f} - 0.99"

        row_data = (f"{num_obreros_aus_posibles[i]}", f"{prob:.2f}", f"{prob_acum:.2f}", intervalo_rnd)
        tree_distribucion.insert("", tk.END, values=row_data)
        cota_inferior = prob_acum

    # Rellenar Resumen del Día N
    ultima_fila = resultados['ultima_fila']
    if ultima_fila:
        summary_data_keys = ['Día', 'Ausentes', 'Presentes', 'Ingreso', 'Costo_Total', 'Beneficio_Diario', 'Beneficio_Acumulado']
        for row_idx, data_key in enumerate(summary_data_keys):
            label_text = data_key.replace('_', ' ').title() + ":"
            raw_value = ultima_fila.get(data_key, "N/A")
            value_display = f"{raw_value:,.2f}" if isinstance(raw_value, float) else f"{raw_value:,}"

            lbl_key = ttk.Label(last_day_details_frame, text=label_text, anchor="w")
            lbl_key.grid(row=row_idx, column=0, padx=2, pady=1, sticky=tk.W)
            lbl_val = ttk.Label(last_day_details_frame, text=value_display, anchor="e")
            lbl_val.grid(row=row_idx, column=1, padx=2, pady=1, sticky=tk.EW)

            if data_key == 'Beneficio_Acumulado':
                lbl_key.configure(font=('TkDefaultFont', 9, 'bold'))
                color = "green" if raw_value >= 0 else "red"
                lbl_val.configure(font=('TkDefaultFont', 9, 'bold'), foreground=color)
        last_day_details_frame.grid_columnconfigure(1, weight=1)

def imprimir_fila(fila):
    """Inserta una fila de datos en la tabla de simulación, truncando el RND a 2 decimales."""
    if not tree_filas_simulacion: return

    ordered_values = []
    for col_key in COLUMN_ORDER:
        val = fila.get(col_key, "")
        if col_key == 'RND Ausentismo':
            # --- CAMBIO IMPORTANTE: Truncar en lugar de redondear ---
            # Multiplica por 100, convierte a entero (corta decimales) y divide de nuevo
            truncated_val = int(val * 100) / 100.0
            # Formatea para asegurar que siempre se muestren 2 decimales (e.g., 0.5 -> "0.50")
            ordered_values.append(f"{truncated_val:.2f}")
        elif isinstance(val, float):
            ordered_values.append(f"{val:,.2f}")
        elif isinstance(val, int):
            ordered_values.append(f"{val:,}")
        else:
            ordered_values.append(val)
    tree_filas_simulacion.insert("", tk.END, values=ordered_values)

def setup_gui_layout(app_root):
    """Configura la estructura visual y los widgets de la GUI de Tkinter."""
    global tree_distribucion, tree_filas_simulacion, last_day_details_frame
    app_root.title("Simulador de Flota v8.0 - Truncado")
    app_root.geometry("1250x800")

    # --- Frame de Entradas (Superior) ---
    input_controls_frame = ttk.LabelFrame(app_root, text="Parámetros de Simulación")
    input_controls_frame.pack(padx=10, pady=10, fill=tk.X, side=tk.TOP)

    param_entries = {}
    params_grid_frame = ttk.Frame(input_controls_frame)
    params_grid_frame.pack(pady=5, padx=5, fill=tk.X)

    param_definitions = {
        "conductores_totales": ("Cantidad de Conductores:", "22"),
        "ingreso_diario": ("Ingreso Diario Potencial:", "4000"),
        "costo_operativo": ("Costo Operativo Fijo:", "2400"),
        "salario": ("Salario por Conductor:", "30"),
        "n": ("Nº Días a Simular:", "10000"),
        "i": ("Nº Filas a Mostrar:", "20"),
        "j": ("Día Inicio a Mostrar:", "1")
    }
    for i, (key, (text, default_val)) in enumerate(param_definitions.items()):
        ttk.Label(params_grid_frame, text=text).grid(row=0, column=i*2, padx=5, pady=2, sticky=tk.W)
        entry = ttk.Entry(params_grid_frame, width=10)
        entry.insert(0, default_val)
        entry.grid(row=0, column=i*2 + 1, padx=(0,15), pady=2, sticky=tk.EW)
        param_entries[key] = entry
        params_grid_frame.grid_columnconfigure(i*2 + 1, weight=1)

    ausentismo_input_frame = ttk.LabelFrame(input_controls_frame, text="Frecuencia de Ausentismo (días en un periodo de 100)")
    ausentismo_input_frame.pack(pady=5, padx=5, fill=tk.X)
    ausentismo_entries_list = []
    ausentismo_labels_text = ["0 Ausentes:", "1 Ausente:", "2 Ausentes:", "3 Ausentes:", "4 Ausentes:", "5+ Ausentes:"]
    default_ausentismo_values = ["36", "38", "19", "6", "1", "0"]
    for i, label_text in enumerate(ausentismo_labels_text):
        ttk.Label(ausentismo_input_frame, text=label_text).grid(row=0, column=i*2, padx=(10, 2), pady=5, sticky=tk.W)
        entry = ttk.Entry(ausentismo_input_frame, width=6)
        entry.insert(0, default_ausentismo_values[i])
        entry.grid(row=0, column=i*2 + 1, padx=(0, 10), pady=5, sticky=tk.EW)
        ausentismo_entries_list.append(entry)
        ausentismo_input_frame.grid_columnconfigure(i*2 + 1, weight=1)

    # --- Botón de Simulación ---
    simulate_btn = ttk.Button(app_root, text="Ejecutar Simulación", command=lambda: on_simulate_click(param_entries, ausentismo_entries_list))
    simulate_btn.pack(pady=(0, 10), fill=tk.X, padx=10)

    # --- ÁREA DE RESULTADOS ---
    output_main_frame = ttk.Frame(app_root)
    output_main_frame.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

    output_main_frame.grid_columnconfigure(0, weight=1)
    output_main_frame.grid_columnconfigure(1, weight=3)
    output_main_frame.grid_rowconfigure(0, weight=2)
    output_main_frame.grid_rowconfigure(1, weight=1)

    # --- Columna Izquierda, Fila Superior: Tabla de Distribución ---
    dist_frame = ttk.LabelFrame(output_main_frame, text="Tabla de Distribución de Ausentismo")
    dist_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 5))

    dist_cols = ("Ausentes", "Prob.", "Acum.", "Intervalo RND")
    tree_distribucion = ttk.Treeview(dist_frame, columns=dist_cols, show='headings', height=7)
    tree_distribucion.column("Ausentes", anchor=tk.CENTER, width=60)
    tree_distribucion.column("Prob.", anchor=tk.CENTER, width=60)
    tree_distribucion.column("Acum.", anchor=tk.CENTER, width=60)
    tree_distribucion.column("Intervalo RND", anchor=tk.CENTER, width=110)
    for col in dist_cols:
        tree_distribucion.heading(col, text=col)
    tree_distribucion.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- Columna Izquierda, Fila Inferior: Resumen Día N ---
    last_day_details_frame = ttk.LabelFrame(output_main_frame, text="Resumen del Día N Final")
    last_day_details_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

    # --- Columna Derecha: Tabla de Filas (ocupa 2 filas de alto) ---
    sim_rows_frame = ttk.LabelFrame(output_main_frame, text="Detalle de Días Seleccionados")
    sim_rows_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(5, 0))

    tree_container = ttk.Frame(sim_rows_frame)
    tree_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    tree_filas_simulacion = ttk.Treeview(tree_container, columns=tuple(COLUMN_ORDER), show='headings')
    for col_key in COLUMN_ORDER:
        cfg = TREEVIEW_COLUMNS_CONFIG[col_key]
        tree_filas_simulacion.heading(col_key, text=col_key)
        tree_filas_simulacion.column(col_key, width=cfg["width"], anchor=cfg["anchor"], stretch=tk.YES)

    ysb = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=tree_filas_simulacion.yview)
    xsb = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=tree_filas_simulacion.xview)
    tree_filas_simulacion.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    ysb.pack(side=tk.RIGHT, fill=tk.Y)
    xsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree_filas_simulacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

def iniciar_interfaz():
    """Inicializa y ejecuta la aplicación de la GUI."""
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    setup_gui_layout(root)
    root.mainloop()
