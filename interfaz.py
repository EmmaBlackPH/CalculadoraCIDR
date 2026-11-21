"""
Módulo: interfaz.py
Descripción: Interfaz gráfica de usuario para la calculadora CIDR.
Dependencias: tkinter (estándar de Python) y cidr.py (módulo local).
"""
# Declaracion de dependencias
import tkinter as tk
from tkinter import ttk, messagebox
from cidr import calcular_cidr

# Clase principal de la aplicación GUI
class CalculadoraCIDRApp:
    # Inicializa la ventana principal y configura los widgets.
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Calculadora IP (CIDR)")
        self.root.resizable(False, False)
        self.root.configure(padx=16, pady=16)
        self._crear_widgets()

    # Crea y organiza todos los elementos gráficos en la ventana.
    def _crear_widgets(self):
        # --- Sección de Entradas ---
        frame_entrada = ttk.LabelFrame(self.root, text="Datos de entrada", padding=10)
        frame_entrada.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(frame_entrada, text="IP o IP/Prefijo:").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_ip = ttk.Entry(frame_entrada, width=30)
        self.entry_ip.grid(row=0, column=1, padx=(8, 0), pady=4)
        self.entry_ip.insert(0, "192.168.1.0/24")

        ttk.Label(frame_entrada, text="Máscara (opcional):").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_mascara = ttk.Entry(frame_entrada, width=30)
        self.entry_mascara.grid(row=1, column=1, padx=(8, 0), pady=4)

        self.var_binario = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_entrada,
            text="Mostrar equivalencia en binario",
            variable=self.var_binario,
            command=self._alternar_binario,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # --- Botones ---
        frame_botones = ttk.Frame(self.root)
        frame_botones.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ttk.Button(frame_botones, text="Calcular", command=self.calcular).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(frame_botones, text="Limpiar", command=self.limpiar).pack(side="left", expand=True, fill="x", padx=(4, 0))

        # --- Sección de Resultados ---
        frame_resultados = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        frame_resultados.grid(row=2, column=0, sticky="ew")

        campos = [
            ("Dirección de Red:", "red"),
            ("Rango de Hosts:", "rango_hosts"),
            ("Dirección Broadcast:", "broadcast"),
            ("Máscara Decimal:", "mascara_decimal"),
            ("Prefijo CIDR:", "prefijo"),
            ("Hosts Disponibles:", "hosts_disponibles"),
        ]

        self.salidas = {}
        for i, (etiqueta, clave) in enumerate(campos):
            ttk.Label(frame_resultados, text=etiqueta).grid(row=i, column=0, sticky="w", pady=3)
            var = tk.StringVar()
            entry = ttk.Entry(frame_resultados, textvariable=var, width=34, state="readonly")
            entry.grid(row=i, column=1, padx=(8, 0), pady=3)
            self.salidas[clave] = var

        # --- Sección Binaria (oculta por defecto) ---
        self.frame_binario = ttk.LabelFrame(self.root, text="Representación Binaria", padding=10)
        campos_bin = [("Red (bin):", "red"), ("Máscara (bin):", "mascara"), ("Broadcast (bin):", "broadcast")]
        self.salidas_bin = {}
        for i, (etiqueta, clave) in enumerate(campos_bin):
            ttk.Label(self.frame_binario, text=etiqueta).grid(row=i, column=0, sticky="w", pady=3)
            var = tk.StringVar()
            entry = ttk.Entry(self.frame_binario, textvariable=var, width=38, state="readonly")
            entry.grid(row=i, column=1, padx=(8, 0), pady=3)
            self.salidas_bin[clave] = var

        # Permitir calcular presionando Enter
        self.root.bind("<Return>", lambda event: self.calcular())

    # Esta funcion alterna la visibilidad de la seccion binaria segun el estado del checkbox.
    def _alternar_binario(self):
        if self.var_binario.get():
            self.frame_binario.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        else:
            self.frame_binario.grid_forget()

    # Esta funcion calcula los datos CIDR usando la funcion calcular_cidr y actualiza los campos de salida. 
    # Maneja errores de validacion mostrando un mensaje emergente.
    def calcular(self):
        try:
            datos = calcular_cidr(self.entry_ip.get(), self.entry_mascara.get())
            self.salidas["red"].set(datos["red"])
            self.salidas["rango_hosts"].set(datos["rango_hosts"])
            self.salidas["broadcast"].set(datos["broadcast"])
            self.salidas["mascara_decimal"].set(datos["mascara_decimal"])
            self.salidas["prefijo"].set(datos["prefijo"])
            self.salidas["hosts_disponibles"].set(f"{datos['hosts_disponibles']:,}")

            self.salidas_bin["red"].set(datos["binario"]["red"])
            self.salidas_bin["mascara"].set(datos["binario"]["mascara"])
            self.salidas_bin["broadcast"].set(datos["binario"]["broadcast"])
        except ValueError as err:
            messagebox.showerror("Error de validación", str(err))

    # Esta funcion limpia los campos de entrada y salida, y coloca el foco en el campo de IP.
    def limpiar(self):
        self.entry_ip.delete(0, tk.END)
        self.entry_mascara.delete(0, tk.END)
        for var in self.salidas.values():
            var.set("")
        for var in self.salidas_bin.values():
            var.set("")
        self.entry_ip.focus()

# Función principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraCIDRApp(root)
    root.mainloop()