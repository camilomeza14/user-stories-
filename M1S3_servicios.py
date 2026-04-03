# ==============================================================================
# MÓDULO: servicios.py
# DESCRIPCIÓN: Funciones CRUD y estadísticas del inventario
# Cada función recibe el inventario como parámetro para no depender
# de variables globales — buena práctica de modularidad
# ==============================================================================


def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.
    Parámetros:
        inventario (list): lista de diccionarios de productos
        nombre (str): nombre del producto
        precio (float): precio unitario
        cantidad (int): unidades disponibles
    Retorna: None
    """
    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }
    inventario.append(producto)
    print(f"\n✅ '{nombre}' agregado al inventario.")


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario en formato legible.
    Parámetros:
        inventario (list): lista de diccionarios de productos
    Retorna: None
    """
    print("\n" + "─" * 50)
    print("            [INVENTARIO ACTUAL]")
    print("─" * 50)

    # Si la lista está vacía, avisamos y salimos de la función
    if len(inventario) == 0:
        print("⚠️  El inventario está vacío.")
        return

    # Recorremos cada producto con un for y mostramos sus datos
    for i, producto in enumerate(inventario, start=1):
        print(f"{i}. Producto: {producto['nombre']:<20} | "
              f"Precio: ${producto['precio']:<10.2f} | "
              f"Cantidad: {producto['cantidad']}")

    print("─" * 50)


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre (sin distinguir mayúsculas).
    Parámetros:
        inventario (list): lista de diccionarios de productos
        nombre (str): nombre a buscar
    Retorna:
        dict: el producto encontrado, o None si no existe
    """
    # Recorremos buscando coincidencia de nombre (ignorando mayúsculas)
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto

    # Si el for termina sin encontrar nada, retorna None
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza precio y/o cantidad de un producto existente.
    Parámetros:
        inventario (list): lista de diccionarios de productos
        nombre (str): nombre del producto a actualizar
        nuevo_precio (float, opcional): nuevo precio a asignar
        nueva_cantidad (int, opcional): nueva cantidad a asignar
    Retorna: None
    """
    # Reutilizamos buscar_producto — no repetimos lógica
    producto = buscar_producto(inventario, nombre)

    if producto is None:
        print(f"\n❌ Producto '{nombre}' no encontrado.")
        return

    # Solo actualizamos el campo si se pasó un valor nuevo
    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio
    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad

    print(f"\n🔄 '{nombre}' actualizado correctamente.")


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.
    Parámetros:
        inventario (list): lista de diccionarios de productos
        nombre (str): nombre del producto a eliminar
    Retorna: None
    """
    producto = buscar_producto(inventario, nombre)

    if producto is None:
        print(f"\n❌ Producto '{nombre}' no encontrado.")
        return

    # remove() elimina la primera coincidencia del objeto en la lista
    inventario.remove(producto)
    print(f"\n🗑️  '{nombre}' eliminado del inventario.")


def calcular_estadisticas(inventario):
    """
    Calcula estadísticas generales del inventario.
    Parámetros:
        inventario (list): lista de diccionarios de productos
    Retorna:
        dict con claves: unidades_totales, valor_total,
                         producto_mas_caro, producto_mayor_stock
    """
    if len(inventario) == 0:
        return None

    # Lambda para calcular el subtotal de un producto (precio × cantidad)
    subtotal = lambda p: p["precio"] * p["cantidad"]

    # Acumulamos unidades y valor total recorriendo la lista
    unidades_totales = 0
    valor_total = 0
    for producto in inventario:
        unidades_totales = unidades_totales + producto["cantidad"]
        valor_total = valor_total + subtotal(producto)

    # max() con key= evalúa cada producto por el criterio dado
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    # Retornamos todo en un diccionario para fácil acceso
    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock
    }
