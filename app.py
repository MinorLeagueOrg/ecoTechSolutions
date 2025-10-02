import tkinter as tk
from tkinter import ttk, messagebox

# --- Importaciones de módulos (Necesarias) ---
from admin_dashboard import AdminDashboard


# from employee_dashboard import EmployeeDashboard # Lo crearíamos para el rol Empleado
# from db_manager import DBManager # Desactivado por ahora para enfocarnos en la GUI

class LoginWindow(tk.Toplevel):
    """Ventana de inicio de sesión"""

    def __init__(self, master):
        super().__init__(master)
        self.pass_entry = None
        self.user_entry = None
        self.master = master
        self.title("Inicio de Sesión")
        self.geometry("400x250")
        self.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill='both')

        # Título
        lbl_titulo = ttk.Label(main_frame, text="EcoTechSolutions - Login", font=("Helvetica", 14, "bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=15)

        # Usuario
        ttk.Label(main_frame, text="Usuario:", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.user_entry = ttk.Entry(main_frame, width=35)
        self.user_entry.grid(row=1, column=1, pady=5)

        # Contraseña
        ttk.Label(main_frame, text="Contraseña:", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", pady=5,
                                                                               padx=5)
        self.pass_entry = ttk.Entry(main_frame, width=35, show="*")
        self.pass_entry.grid(row=2, column=1, pady=5)

        # Botón de Login
        btn_login = ttk.Button(main_frame, text="Iniciar Sesión", command=self.handle_login)
        btn_login.grid(row=3, column=0, columnspan=2, pady=20)

        # Configuraciones para centrar
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def handle_login(self):
        """Maneja la lógica de inicio de sesión (actualmente simulada)."""
        username = self.user_entry.get()
        password = self.pass_entry.get()

        rol = None
        if username == "admin" and password == "123":
            rol = "Administrador"
        elif username == "empleado" and password == "123":
            rol = "Empleado"

        if rol:
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {username}! Acceso de {rol}.")
            self.destroy()  # Cierra la ventana de login
            self.master.mostrar_ventana_principal(rol, username)
        else:
            messagebox.showerror("Error de Login",
                                 "Usuario o Contraseña incorrectos. Intenta con 'admin'/'123' o 'empleado'/'123'")

class AppGestionEmpresarial(tk.Tk):
    """Contenedor principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Empresarial")
        self.geometry("800x600")

        # --- Configuración de Base de Datos (Comentada) ---
        # self.db = DBManager()
        # self.db.connect()

        self.withdraw()  # Oculta la ventana principal hasta que el login sea exitoso
        self.current_window = None  # Referencia al frame de contenido principal

        # Iniciar el flujo con la ventana de Login
        # LA CLASE LoginWindow ESTÁ DEFINIDA ARRIBA, ASÍ QUE ESTO ES CORRECTO.
        self.login_window = LoginWindow(self)

    def mostrar_ventana_principal(self, rol: str, username: str):
        """Muestra la ventana principal con el dashboard según el rol."""
        self.deiconify()  # Muestra la ventana principal

        # Limpiar el contenido anterior si existe
        if self.current_window:
            self.current_window.destroy()

        if rol == "Administrador":
            self.current_window = AdminDashboard(self)
            self.title(f"Sistema de Gestión Empresarial - Administrador ({username})")
        elif rol == "Empleado":
            # Si existiera la clase EmployeeDashboard, se usaría aquí
            self.current_window = ttk.Label(self,
                                            text=f"Panel de Empleado para {username}\n(Funcionalidad en desarrollo)",
                                            font=("Helvetica", 16))
            self.current_window.pack(expand=True, fill='both')
            self.title(f"Sistema de Gestión Empresarial - Empleado ({username})")

    def on_closing(self):
        """Se ejecuta al cerrar la aplicación para cerrar la conexión de DB."""
        # if self.db:
        #     self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = AppGestionEmpresarial()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
