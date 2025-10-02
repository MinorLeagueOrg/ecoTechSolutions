import tkinter as tk
from tkinter import ttk, messagebox

# --- Importaciones de módulos ---
from admin_dashboard import AdminDashboard


# from db_manager import DBManager # Descomentar cuando integremos el CRUD real


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

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))

        self.crear_widgets()

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill='both')

        # Título
        lbl_titulo = ttk.Label(main_frame, text="EcoTechSolutions - Login", font=("Helvetica", 16, "bold"),
                               foreground='#48BB78')  # Color de la empresa
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=15)

        # Usuario
        ttk.Label(main_frame, text="Usuario:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.user_entry = ttk.Entry(main_frame, width=35)
        self.user_entry.grid(row=1, column=1, pady=5)

        # Contraseña
        ttk.Label(main_frame, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.pass_entry = ttk.Entry(main_frame, width=35, show="*")
        self.pass_entry.grid(row=2, column=1, pady=5)

        # Botón de Login
        btn_login = ttk.Button(main_frame, text="Iniciar Sesión", command=self.handle_login,
                               style='Accent.TButton')  # Estilo de botón principal
        btn_login.grid(row=3, column=0, columnspan=2, pady=20)

        # Configuraciones para centrar
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Añadir un tema para el botón principal
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', background='#48BB78', foreground='white', font=('Helvetica', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#38A169')])

    def handle_login(self):
        """Maneja la lógica de inicio de sesión (actualmente simulada)."""
        username = self.user_entry.get()
        password = self.pass_entry.get()

        rol = None
        # Simulación de autenticación (debe ser reemplazada por Autenticación Segura de la DB)
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
        self.title("Sistema de Gestión Empresarial - EcoTech Solutions")
        self.geometry("1200x700")  # Aumentamos el tamaño para el dashboard

        # --- Configuración de Base de Datos (Comentada) ---
        # self.db_manager = DBManager()

        self.withdraw()  # Oculta la ventana principal hasta que el login sea exitoso
        self.current_window = None

        # Iniciar el flujo con la ventana de Login
        self.login_window = LoginWindow(self)

    def mostrar_ventana_principal(self, rol: str, username: str):
        """Muestra la ventana principal con el dashboard según el rol."""
        self.deiconify()  # Muestra la ventana principal

        if self.current_window:
            self.current_window.destroy()

        if rol == "Administrador":
            # Pasamos el gestor de DB si estuviera inicializado: self.db_manager
            self.current_window = AdminDashboard(self)
            self.title(f"Sistema de Gestión Empresarial - Administrador ({username})")
        elif rol == "Empleado":
            # Vista de Empleado (pendiente de desarrollo)
            self.current_window = ttk.Label(self,
                                            text=f"Panel de Empleado para {username}\n(Funcionalidad en desarrollo)",
                                            font=("Helvetica", 16))
            self.current_window.pack(expand=True, fill='both')
            self.title(f"Sistema de Gestión Empresarial - Empleado ({username})")

    def on_closing(self):
        """Se ejecuta al cerrar la aplicación para cerrar la conexión de DB (cuando esté implementada)."""
        # if hasattr(self, 'db_manager') and self.db_manager:
        #     self.db_manager.close()
        self.destroy()


if __name__ == "__main__":
    app = AppGestionEmpresarial()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
