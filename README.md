# 🚚 Plataforma de Gestión de Domicilios

Aplicación de escritorio desarrollada en **Python y Flet**, orientada a la administración y gestión de solicitudes de domicilios, asignación automática de domiciliarios y seguimiento de entregas.

El sistema cuenta con tres tipos de usuarios: administrador, restaurantes y domiciliarios. Cada uno dispone de una interfaz con funcionalidades específicas según su rol.

## 🎯 Objetivo del proyecto

Desarrollar una plataforma que facilite la gestión de domicilios mediante la automatización de procesos como la asignación de solicitudes, el control de entregas, la administración de usuarios y el registro de pagos.

## ⚙️ Tecnologías utilizadas

- **Python:** lenguaje principal de programación.
- **Flet:** desarrollo de la interfaz gráfica.
- **SQLite:** almacenamiento y gestión de información.
- **Programación orientada a objetos (POO):** organización del código mediante clases y objetos.
- **Git y GitHub:** control de versiones y gestión del repositorio.

## 👥 Tipos de usuarios

### 1. Administrador
- Crear y administrar cuentas de restaurantes.
- Registrar y gestionar domiciliarios.
- Supervisar las solicitudes de domicilios.
- Consultar asignaciones y entregas.
- Gestionar pagos y comisiones.
- Configurar el porcentaje de comisión de la plataforma.

### 2. Restaurante
- Registrar solicitudes de domicilios.
- Ingresar los datos del destinatario.
- Consultar el estado de las solicitudes.
- Visualizar el domiciliario asignado.
- Consultar el historial de solicitudes.
- Gestionar la información relacionada con los pagos.

### 3. Domiciliario
- Activar y desactivar su disponibilidad.
- Recibir solicitudes automáticamente.
- Aceptar o rechazar asignaciones.
- Consultar la información de las entregas.
- Actualizar el estado de los domicilios.
- Consultar su historial de entregas.

## 🔄 Sistema de asignación automática

La plataforma implementa un sistema de asignación basado en una cola de domiciliarios disponibles.

Su funcionamiento es el siguiente:

1. Se registra una nueva solicitud de domicilio.
2. El sistema identifica los domiciliarios disponibles.
3. Se selecciona el domiciliario que lleva más tiempo en la cola.
4. El domiciliario dispone de 30 segundos para aceptar la solicitud.
5. Si rechaza o no responde dentro del tiempo establecido, el sistema busca otro domiciliario.
6. Si no hay domiciliarios disponibles, la solicitud queda pendiente.

Cada domiciliario puede tener hasta dos entregas activas simultáneamente.

## 💰 Gestión financiera

La plataforma contempla un sistema de gestión financiera que permite:

- Registrar los pagos asociados a las entregas.
- Calcular las comisiones de la plataforma.
- Consultar los valores correspondientes al domiciliario.
- Administrar el porcentaje de comisión.

El porcentaje inicial de comisión es del 20 %, con posibilidad de reducirse hasta un mínimo del 10 % mediante la gestión del administrador.

## 📁 Estructura del proyecto

```text
Proyecto_Domicilios/
│
├── main.py
│
├── interfaz/
│   ├── __init__.py
│   ├── login.py
│   ├── administrador.py
│   ├── restaurante.py
│   └── domiciliario.py
│
├── modelos/
│   ├── __init__.py
│   └── usuario.py
│
├── logica/
│   ├── __init__.py
│   └── autenticacion.py
│
├── recursos/
│   └── logo.png
│
└── usuarios.db
```

### Organización del código

- **main.py:** punto de entrada de la aplicación.
- **interfaz/:** contiene las interfaces gráficas de cada tipo de usuario.
- **modelos/:** contiene las clases y modelos del sistema.
- **logica/:** contiene los procesos y operaciones principales de la plataforma.
- **recursos/:** almacena los elementos gráficos utilizados por la aplicación.
- **usuarios.db:** base de datos SQLite utilizada para almacenar la información.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Ingresar a la carpeta

```bash
cd Proyecto_Domicilios
```

### 3. Crear un entorno virtual (opcional)

```bash
python -m venv venv
```

Activar el entorno virtual en Windows:

```bash
venv\Scripts\activate
```

### 4. Instalar Flet

```bash
pip install flet
```

### 5. Ejecutar la aplicación

```bash
python main.py
```

## 📌 Estado del proyecto

El proyecto cuenta actualmente con:

- Inicio de sesión y diferenciación de roles.
- Interfaces independientes para administrador, restaurante y domiciliario.
- Registro y consulta de solicitudes.
- Asignación automática de domiciliarios.
- Cola de disponibilidad.
- Aceptación y rechazo de solicitudes con límite de tiempo.
- Control de entregas activas.
- Gestión de pagos y comisiones.

## 🔮 Mejoras futuras

- Integración con dispositivos ESP32.
- Comunicación entre sensores físicos y la plataforma.
- Implementación de notificaciones en tiempo real.
- Ampliación de los reportes administrativos.
- Mejoras en el seguimiento de las entregas.

---

**Desarrollado con Python y Flet.**

Proyecto académico enfocado en la automatización y gestión de servicios de domicilios.
