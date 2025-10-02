import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


class EmployeeForm(tk.Toplevel):
    """Ventana emergente para crear o editar un Empleado."""

    def __init__(self, master, empleado_id: Optional[int] = None, callback=None):
        super().__init__(master)
        self.master = master
        self.empleado_id = empleado_id
        self.callback = callback

        self.title_text = "Crear Nuevo Empleado" if empleado_id is None else f"Editar Empleado ID: {empleado_id}"
        self.title(self.title_text)
        self.geometry("550x550")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.crear_widgets()

        if self.empleado_id is not None:
            self.cargar_datos_empleado(self.empleado_id)

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text=self.title_text, font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                         pady=10)

        # Campos de texto y entrada
        campos = [
            ("Nombre:", "nombre"),
            ("Dirección:", "direccion"),
            ("Teléfono:", "telefono"),
            ("Email:", "email"),
            ("Salario:", "salario"),
            ("Fecha de Inicio (YYYY-MM-DD):", "fecha_de_inicio"),
            ("Username (Usuario de Login):", "username"),
            ("Contraseña (solo en creación/cambio):", "contrasena")
        ]

        self.entries = {}
        for i, (label_text, key) in enumerate(campos):
            row_num = i + 1

            ttk.Label(main_frame, text=label_text, width=25).grid(row=row_num, column=0, sticky="w", pady=5)

            entry = ttk.Entry(main_frame, width=40)
            entry.grid(row=row_num, column=1, sticky="ew", pady=5)
            self.entries[key] = entry

            if key == "contrasena" and self.empleado_id is None:
                entry.config(show="*")
            elif key == "contrasena":
                entry.config(show="*")  # También oculta en edición

        # Campos con Select (Combobox) para Relaciones (Roles y Departamentos)
        ttk.Label(main_frame, text="Rol:", width=25).grid(row=len(campos) + 1, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar()
        self.role_combo = ttk.Combobox(main_frame, textvariable=self.role_var,
                                       values=["Administrador", "Empleado Regular"], state='readonly', width=38)
        self.role_combo.grid(row=len(campos) + 1, column=1, sticky="ew", pady=5)
        self.role_combo.current(0)

        ttk.Label(main_frame, text="Departamento:", width=25).grid(row=len(campos) + 2, column=0, sticky="w", pady=5)
        self.depto_var = tk.StringVar()
        self.depto_combo = ttk.Combobox(main_frame, textvariable=self.depto_var,
                                        values=["I+D", "Ventas", "Marketing", "Gerencia"], state='readonly', width=38)
        self.depto_combo.grid(row=len(campos) + 2, column=1, sticky="ew", pady=5)
        self.depto_combo.current(0)

        # Botón Guardar
        btn_guardar = ttk.Button(main_frame, text="Guardar Cambios" if self.empleado_id else "Crear Empleado",
                                 command=self.guardar_empleado)
        btn_guardar.grid(row=len(campos) + 3, column=0, columnspan=2, pady=20)

        main_frame.grid_columnconfigure(1, weight=1)

    def cargar_datos_empleado(self, empleado_id: int):
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

        for key, entry in self.entries.items():
            if key in datos_simulados and key != "contrasena":
                entry.delete(0, tk.END)
                entry.insert(0, datos_simulados[key])

        self.role_var.set("Administrador")
        self.depto_var.set("Gerencia")

    def guardar_empleado(self):
        """Valida y simula el guardado de los datos."""
        data = {key: entry.get() for key, entry in self.entries.items()}

        if not all([data['nombre'], data['email'], data['username']]):
            messagebox.showerror("Error de Validación", "Los campos Nombre, Email y Username son obligatorios.")
            return

        # Lógica de persistencia REAL (Crear/Actualizar en DB) iría aquí

        if self.empleado_id is None:
            print(f"Creando nuevo empleado...")
            messagebox.showinfo("Éxito", "¡Empleado creado correctamente!")
        else:
            print(f"Actualizando empleado ID {self.empleado_id}...")
            messagebox.showinfo("Éxito", "¡Empleado actualizado correctamente!")

        if self.callback:
            self.callback()

        self.destroy()
