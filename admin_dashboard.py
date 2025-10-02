import tkinter as tk
from tkinter import ttk, messagebox
from employee_form import EmployeeForm

class AdminDashboard(ttk.Frame):
    """Panel principal para el Administrador, con menú y contenido dinámico."""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill='both')
        self.current_view = None

        self.crear_diseno()
        self.mostrar_vista("Inicio")  # Muestra la vista inicial

    def crear_diseno(self):
        # 1. Menú Lateral (Frame a la izquierda)
        menu_frame = ttk.Frame(self, width=180, relief='raised')
        menu_frame.pack(side='left', fill='y', padx=10, pady=10)

        ttk.Label(menu_frame, text="Menú Admin", font=("Helvetica", 12, "bold")).pack(pady=10)

        botones = [
            ("Inicio", "Inicio"),
            ("Usuarios", "Gestionar Usuarios"),
            ("Departamentos", "Gestionar Deptos"),
            ("Proyectos", "Gestionar Proyectos"),
            ("Informes", "Generar Informes")
        ]

        for texto, vista in botones:
            btn = ttk.Button(menu_frame, text=texto, command=lambda v=vista: self.mostrar_vista(v))
            btn.pack(fill='x', padx=5, pady=5)

        # 2. Área de Contenido Principal (Frame a la derecha)
        self.content_frame = ttk.Frame(self, padding="10")
        self.content_frame.pack(side='right', fill='both', expand=True)

    def limpiar_contenido(self):
        """Elimina todos los widgets del área de contenido."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_vista(self, vista: str):
        """Carga el widget correspondiente a la vista seleccionada."""
        self.limpiar_contenido()

        ttk.Label(self.content_frame, text=vista, font=("Helvetica", 16, "bold")).pack(pady=10, anchor='w')

        if vista == "Inicio":
            ttk.Label(self.content_frame,
                      text="Bienvenido al Panel de Administración.\nSelecciona una opción del menú lateral.",
                      font=("Helvetica", 12)).pack(pady=50)

        elif vista == "Gestionar Usuarios":
            self.crear_panel_gestion_usuarios()

        elif vista == "Gestionar Proyectos":
            ttk.Label(self.content_frame,
                      text="Aquí se gestionarán los proyectos de la empresa (Crear, Editar, Eliminar).").pack(pady=10)

        elif vista == "Gestionar Deptos":
            ttk.Label(self.content_frame, text="Aquí se gestionarán los departamentos de la empresa.").pack(pady=10)

        elif vista == "Generar Informes":
            ttk.Label(self.content_frame, text="Aquí se generarán los informes PDF y Excel.").pack(pady=10)

    def crear_panel_gestion_usuarios(self):
        """Crea la interfaz para gestionar Empleados/Usuarios con Treeview y CRUD."""

        listado_frame = ttk.LabelFrame(self.content_frame, text="Empleados Registrados", padding="10")
        listado_frame.pack(fill='both', expand=True, pady=10)

        columnas = ("id", "nombre", "rol", "departamento", "email")
        self.empleados_tree = ttk.Treeview(listado_frame, columns=columnas, show='headings')

        self.empleados_tree.heading("id", text="ID")
        self.empleados_tree.heading("nombre", text="Nombre Completo")
        self.empleados_tree.heading("rol", text="Rol")
        self.empleados_tree.heading("departamento", text="Departamento")
        self.empleados_tree.heading("email", text="Email")

        self.empleados_tree.column("id", width=50, anchor=tk.CENTER)
        self.empleados_tree.column("nombre", width=150)
        self.empleados_tree.column("rol", width=100)
        self.empleados_tree.column("departamento", width=120)
        self.empleados_tree.column("email", width=180)

        self.empleados_tree.pack(fill='both', expand=True)

        botones_frame = ttk.Frame(self.content_frame, padding="10")
        botones_frame.pack(fill='x', pady=5)

        ttk.Button(botones_frame, text="➕ Agregar Empleado", command=self.abrir_formulario_crear).pack(side='left',
                                                                                                       padx=5)
        ttk.Button(botones_frame, text="✏️ Editar Empleado", command=self.abrir_formulario_editar).pack(side='left',
                                                                                                        padx=5)
        ttk.Button(botones_frame, text="❌ Eliminar Empleado", command=self.eliminar_empleado).pack(side='left', padx=5)

        self.cargar_datos_simulados()  # Cargar datos iniciales al mostrar el panel

    def cargar_datos_simulados(self):
        """Función temporal para poblar el Treeview con datos de ejemplo."""
        self.empleados_tree.delete(*self.empleados_tree.get_children())

        datos_ejemplo = [
            (1, "Ana Gómez", "Admin", "Gerencia", "ana.g@ecotechs.com"),
            (2, "Juan Pérez", "Desarrollador", "I+D", "juan.p@ecotechs.com"),
            (3, "Marta Ríos", "Marketing", "Ventas", "marta.r@ecotechs.com")
        ]

        for item in datos_ejemplo:
            self.empleados_tree.insert('', tk.END, values=item)

    def abrir_formulario_crear(self):
        """Abre la ventana para crear un nuevo empleado."""
        # Se pasa la función de refresco (callback)
        EmployeeForm(self.master, empleado_id=None, callback=self.cargar_datos_simulados)

    def abrir_formulario_editar(self):
        """Abre la ventana para editar el empleado seleccionado."""
        seleccion = self.empleados_tree.selection()
        if seleccion:
            empleado_id = self.empleados_tree.item(seleccion)['values'][0]
            EmployeeForm(self.master, empleado_id=empleado_id, callback=self.cargar_datos_simulados)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para editar.")

    def eliminar_empleado(self):
        """Simula la eliminación de un empleado."""
        seleccion = self.empleados_tree.selection()
        if seleccion:
            id_empleado = self.empleados_tree.item(seleccion)['values'][0]
            if messagebox.askyesno("Confirmar Eliminación",
                                   f"¿Estás seguro de que deseas eliminar al empleado ID {id_empleado}?"):
                print(f"Simulando eliminación de empleado ID: {id_empleado}...")
                # Lógica de eliminación REAL en DB iría aquí
                self.cargar_datos_simulados()  # Refrescar la tabla
        else:
            messagebox.showwarning("Advertencia", "Selecciona un empleado para eliminar.")
