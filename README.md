# 🏨 Scraper de Hoteles con Selenium

## 🚀 Descripción

Este proyecto utiliza **Selenium** para automatizar la navegación en la página de [Booking.com](https://www.booking.com) y extraer una lista de hoteles disponibles en una búsqueda específica. Los datos obtenidos se almacenan en formatos **TXT** y **JSON**.

## 🛠 Tecnologías Utilizadas

- 🐍 **Python** (Automatización y manejo de datos)
- 🌐 **Selenium** (Automatización del navegador)
- 🏎 **Google Chrome** + **ChromeDriver** (Ejecución del navegador)

## 📦 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```
2. Instala las dependencias necesarias:
```bash
pip install selenium
```

3. Descarga y configura **ChromeDriver**:

- Descarga la versión compatible desde [aquí](https://sites.google.com/chromium.org/driver)
- Guarda el ejecutable en la carpeta del proyecto o configura su PATH

## 🔧 Uso

Ejecuta el script con:
```bash
python scraper.py
```
El script:

- Abre **Booking.com** y realiza una búsqueda específica.

- Rechaza cookies (si es necesario).

- Hace scroll y carga todos los resultados disponibles.

- Extrae los nombres de los hoteles y los guarda en hoteles.txt y hoteles.json.

## 📂 Archivos generados

- ``: Lista de hoteles en texto plano. **TXT**

- ``: Lista de hoteles en formato **JSON**.

## ⚠️ Consideraciones

- Asegúrate de tener **Google Chrome** instalado y actualizado.

- Este script está diseñado para fines educativos y personales. El scraping automatizado puede violar los términos de servicio de algunos sitios web.

- Evita sobrecargar servidores ejecutando demasiadas solicitudes en poco tiempo.

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**.

💡 Desarrollado con Selenium para automatizar la recopilación de datos de hoteles de Booking.com.


