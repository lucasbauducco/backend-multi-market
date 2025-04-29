# Multi-Market – Plataforma de Compras en Línea con Múltiples Tiendas

**multi-market**, destino definitivo de compras en línea. Esta plataforma fue desarrollada con el objetivo de reunir múltiples tiendas en un solo lugar, brindando una experiencia de compra cómoda, segura y diversa para los usuarios.

## ¿Qué es Multi-Market?

**Multi-Market** es una plataforma de e-commerce tipo "marketplace", donde diferentes tiendas pueden ofrecer sus productos a través de un entorno digital compartido. Desde tecnología y moda hasta artículos para el hogar y productos gourmet, en multi-market encontrarás una amplia variedad de categorías, todo accesible desde cualquier lugar.

## Características principales

- **Variedad de tiendas y productos:** Podés explorar y comprar entre múltiples marcas y categorías, todo en un solo sitio.
- **Navegación amigable:** Interfaz clara, intuitiva y moderna para una experiencia de usuario fluida.
- **Carrito de compras unificado:** Agregá productos de diferentes tiendas y gestioná tu compra desde un solo lugar.
- **Seguridad en transacciones:** Procesamiento de pagos seguro con soporte para múltiples métodos de pago.
- **Promociones exclusivas:** Ofertas y descuentos especiales para usuarios registrados.
- **Envíos internacionales:** Comprá desde cualquier parte del mundo con opciones de envío flexibles.
- **Soporte al cliente:** Atención personalizada para resolver tus consultas en cada etapa del proceso de compra.

---

# Instalar Proyecto


## Pre-requisitos

Asegúrate de tener instalado Python 3.x y pip en tu sistema. Este proyecto también requiere Django y Django Rest Framework, que se instalarán a través de `pip`.

## Configuración del entorno

Es recomendable utilizar un entorno virtual para Python para evitar conflictos de dependencias. Puedes configurar uno con:

```bash
python3 -m venv mi_entorno_virtual
source mi_entorno_virtual/bin/activate  # En Windows usa `mi_entorno_virtual\Scripts\activate`
```
## Descargar proyecto
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

## Instalar requisitos
```bash
pip install -r requirements.txt
```
## configurar db "setting.py"
Este proyecto utiliza SQLite por defecto. Si necesitas configurar otra base de datos, modifica el archivo settings.py en el directorio del proyecto:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
## Ejecutar las migraciones
```bash
python manage.py migrate
```

## Crear un superusuario
```bash
python manage.py createsuperuser
```

## Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

