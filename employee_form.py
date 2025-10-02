import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


# NOTA: En la integración real, este formulario recibirá el DBManager y el objeto Usuario

class EmployeeForm(tk.Toplevel):
    """Ventana emergente para crear o editar un Empleado."""

    def __init__(self, master, empleado_id: Optional[int] = None, callback=None):
        super().__init__(master)
        self.depto_combo = None
        self.depto_var = None
        self.role_combo = None
        self.role_var = None
        self.entries = None
        self.master = master
        self.empleado_id = empleado_id
        self.callback = callback

        self.title_text = "Crear Nuevo Empleado" if empleado_id is None else f"Editar Empleado ID: {empleado_id}"
        self.title(self.title_text)
        self.geometry("650x600")  # Aumentamos más el tamaño
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        # Estilo para la ventana Toplevel
        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TButton', font=('Helvetica', 10, 'bold'))
        style.configure('Accent.TButton', background='#48BB78', foreground='white')
        style.map('Accent.TButton', background=[('active', '#38A169')])

        self.crear_widgets()

        if self.empleado_id is not None:
            # Aquí iría la carga REAL de datos desde la DB
            self.cargar_datos_simulados(self.empleado_id)

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="30")  # Más padding
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=self.title_text, font=("Helvetica", 16, "bold"),
                  foreground='#2D3748').grid(row=0, column=0, columnspan=2, pady=(0, 25), sticky="w")

        # Configuración de la cuadrícula
        main_frame.grid_columnconfigure(0, weight=0)  # Etiqueta fija
        main_frame.grid_columnconfigure(1, weight=1)  # Entrada expandible

        # Campos de texto y entrada
        campos = [
            ("Nombre Completo:", "nombre"),
            ("Dirección:", "direccion"),
            ("Teléfono:", "telefono"),
            ("Email:", "email"),
            ("Salario (ej. 65000.00):", "salario"),
            ("Fecha de Inicio (YYYY-MM-DD):", "fecha_de_inicio"),
            ("Username (Login):", "username"),
            ("Contraseña (solo en creación/cambio):", "contrasena")
        ]

        self.entries = {}
        row_num = 1
        for label_text, key in campos:

            ttk.Label(main_frame, text=label_text, width=30).grid(row=row_num, column=0, sticky="w", pady=7)  # Más pady

            entry = ttk.Entry(main_frame, width=50)  # Mayor ancho
            entry.grid(row=row_num, column=1, sticky="ew", pady=7)
            self.entries[key] = entry

            if key == "contrasena":
                entry.config(show="*")

            row_num += 1

        # Campos con Select (Combobox)
        ttk.Label(main_frame, text="Rol:", width=30).grid(row=row_num, column=0, sticky="w", pady=7)
        self.role_var = tk.StringVar()
        self.role_combo = ttk.Combobox(main_frame, textvariable=self.role_var,
                                       values=["1 - Administrador", "2 - Empleado Regular", "3 - Gerente"],
                                       state='readonly')
        self.role_combo.grid(row=row_num, column=1, sticky="ew", pady=7)
        self.role_combo.current(0)
        row_num += 1

        ttk.Label(main_frame, text="Departamento:", width=30).grid(row=row_num, column=0, sticky="w", pady=7)
        self.depto_var = tk.StringVar()
        self.depto_combo = ttk.Combobox(main_frame, textvariable=self.depto_var,
                                        values=["101 - I+D", "102 - Ventas", "103 - Marketing", "104 - Gerencia"],
                                        state='readonly')
        self.depto_combo.grid(row=row_num, column=1, sticky="ew", pady=7)
        self.depto_combo.current(0)
        row_num += 1

        # Botón Guardar (con estilo Accent)
        btn_guardar = ttk.Button(main_frame, text="Guardar Cambios" if self.empleado_id else "Crear Empleado",
                                 command=self.guardar_empleado, style='Accent.TButton')
        btn_guardar.grid(row=row_num, column=0, columnspan=2, pady=30, sticky="n")

    def cargar_datos_simulados(self, empleado_id: int):
        """Simula la carga de datos de un empleado para edición."""
        print(f"Cargando datos del empleado ID {empleado_id}...")

        datos_simulados = {
            "nombre": "Ana Gómez",
            "direccion": "Calle Falsa 123",
            "telefono": "555-1234",
            "email": "ana.g@ecotechs.com",
            "salario": "65000.00",
            "fecha_de_inicio": "2023-01-15",
            "username": "ana.gomez",
            "contrasena": ""
        }

        for key, value in datos_simulados.items():
            if key in self.entries and key != "contrasena":
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, value)

        self.role_var.set("1 - Administrador")
        self.depto_var.set("104 - Gerencia")

    def guardar_empleado(self):
        """Valida y simula el guardado de los datos."""
        data = {key: entry.get() for key, entry in self.entries.items()}

        # Requisito: Validación de Entradas Seguras
        if not all([data['nombre'], data['email'], data['username'], data['salario']]):
            messagebox.showerror("Error de Validación",
                                 "Los campos Nombre, Email, Username y Salario son obligatorios.")
            return

        # Lógica de persistencia REAL (Crear/Actualizar en DB) iría aquí (usando la clase Usuario y DBManager)

        if self.empleado_id is None:
            messagebox.showinfo("Éxito", "¡Empleado creado correctamente! (Simulación)")
        else:
            messagebox.showinfo("Éxito", "¡Empleado actualizado correctamente! (Simulación)")

        if self.callback:
            self.callback()  # Refresca el listado en el Dashboard

        self.destroy()
