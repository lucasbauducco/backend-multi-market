# backend-multi-market
Bienvenido a multi-market, tu destino definitivo de compras en línea con una diversa gama de tiendas.

En multi-market, creemos en ofrecerte una experiencia de compra sin igual, reuniendo una amplia variedad de tiendas y marcas bajo un mismo techo digital. Nuestra plataforma de multi tiendas te permite explorar y comprar productos de numerosas categorías, desde tecnología de punta y moda hasta artículos para el hogar y productos gourmet, todo desde la comodidad de tu hogar.

Características Únicas:

    Variedad Inigualable: Con tiendas que abarcan múltiples categorías, encontrarás exactamente lo que buscas, ya sean últimas tendencias en moda, los gadgets más recientes o ese artículo especial para decorar tu hogar.

    Compras Seguras: Priorizamos tu seguridad y privacidad. Todas las transacciones se realizan a través de métodos de pago seguros y protegidos, asegurando una experiencia de compra confiable.

    Facilidad de Uso: Nuestra interfaz amigable e intuitiva hace que navegar por las distintas tiendas y productos sea un paseo. Busca, compara y compra con solo unos clics.

    Ofertas y Promociones Exclusivas: Accede a ofertas especiales y descuentos exclusivos disponibles solo para usuarios de multi-market, permitiéndote ahorrar en grande en tus marcas favoritas.

    Envíos a Todo el Mundo: Con opciones de envío flexibles, llevamos tus productos favoritos directamente a tu puerta, sin importar en qué parte del mundo te encuentres.

    Soporte al Cliente Excepcional: Nuestro dedicado equipo de atención al cliente está aquí para ayudarte con cualquier pregunta o inquietud que puedas tener, garantizando una experiencia de compra satisfactoria.

En multi-market, estamos comprometidos a ofrecerte no solo productos de calidad y una selección incomparable, sino también a construir una comunidad de compradores y vendedores apasionados por las buenas ofertas y las últimas tendencias. Únete a nosotros hoy y descubre el placer de comprar en una plataforma que entiende verdaderamente la diversidad de tus necesidades de compra.

¡Explora multi-market ahora y transforma tu experiencia de compra en línea!

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

