# ==============================================================================
# PROGRAMA: INVENTARIO AVANZADO CON PERSISTENCIA CSV
# AUTOR: Camilo - Python Apprentice
# ARCHIVO: app.py — Motor principal del sistema
# MÓDULOS: servicios.py (CRUD + estadísticas) | archivos.py (CSV)
# TEMAS: listas, diccionarios, tuplas, funciones, módulos, manejo de errores
# ==============================================================================

# Importamos las funciones de nuestros módulos
import servicios
import archivos

# --- INVENTARIO EN MEMORIA: lista de diccionarios ---
inventario = []


# ==============================================================================
# FUNCIONES DE INTERFAZ — conectan el menú con los módulos
# ==============================================================================

def interfaz_agregar():
    """Pide datos al usuario y llama a servicios.agregar_producto()"""
    print("\n" + "─" * 40)
    print("         [AGREGAR PRODUCTO]")
    print("─" * 40)

    nombre = ""
    while nombre == "":
        nombre = input("Nombre del producto: ").strip()
        if nombre == "":
            print("❌ El nombre no puede estar vacío.")

    precio = -1
    while precio < 0:
        try:
            precio = float(input("Precio: "))
            if precio < 0:
                print("❌ El precio no puede ser negativo.")
        except ValueError:
            print("❌ Ingresa un número válido.")
            precio = -1

    cantidad = -1
    while cantidad < 0:
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad < 0:
                print("❌ La cantidad no puede ser negativa.")
        except ValueError:
            print("❌ Ingresa un número entero válido.")
            cantidad = -1

    servicios.agregar_producto(inventario, nombre, precio, cantidad)


def interfaz_buscar():
    """Pide nombre al usuario y muestra resultado de búsqueda"""
    print("\n--- [BUSCAR PRODUCTO] ---")
    nombre = input("Nombre a buscar: ").strip()
    resultado = servicios.buscar_producto(inventario, nombre)

    if resultado:
        print(f"\n🔍 Encontrado: {resultado['nombre']} | "
              f"Precio: ${resultado['precio']:.2f} | "
              f"Cantidad: {resultado['cantidad']}")
    else:
        print(f"\n🚫 '{nombre}' no está en el inventario.")


def interfaz_actualizar():
    """Pide datos y llama a servicios.actualizar_producto()"""
    print("\n--- [ACTUALIZAR PRODUCTO] ---")
    nombre = input("Nombre del producto a actualizar: ").strip()

    # Verificamos que exista antes de pedir nuevos datos
    if servicios.buscar_producto(inventario, nombre) is None:
        print(f"\n❌ '{nombre}' no encontrado.")
        return

    print("(Presiona Enter para conservar el valor actual)")

    # Nuevo precio — opcional
    nuevo_precio = None
    entrada_precio = input("Nuevo precio: ").strip()
    if entrada_precio != "":
        try:
            nuevo_precio = float(entrada_precio)
            if nuevo_precio < 0:
                print("⚠️  Precio negativo ignorado.")
                nuevo_precio = None
        except ValueError:
            print("⚠️  Precio inválido ignorado.")

    # Nueva cantidad — opcional
    nueva_cantidad = None
    entrada_cantidad = input("Nueva cantidad: ").strip()
    if entrada_cantidad != "":
        try:
            nueva_cantidad = int(entrada_cantidad)
            if nueva_cantidad < 0:
                print("⚠️  Cantidad negativa ignorada.")
                nueva_cantidad = None
        except ValueError:
            print("⚠️  Cantidad inválida ignorada.")

    servicios.actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)


def interfaz_eliminar():
    """Pide nombre, confirma y llama a servicios.eliminar_producto()"""
    print("\n--- [ELIMINAR PRODUCTO] ---")
    nombre = input("Nombre del producto a eliminar: ").strip()

    if servicios.buscar_producto(inventario, nombre) is None:
        print(f"\n❌ '{nombre}' no encontrado.")
        return

    confirmar = input(f"¿Eliminar '{nombre}'? (s/n): ").lower().strip()
    if confirmar == "s":
        servicios.eliminar_producto(inventario, nombre)
    else:
        print("⚠️  Eliminación cancelada.")


def interfaz_estadisticas():
    """Muestra las estadísticas calculadas por servicios.calcular_estadisticas()"""
    stats = servicios.calcular_estadisticas(inventario)

    if stats is None:
        print("\n⚠️  El inventario está vacío. No hay estadísticas.")
        return

    print("\n" + "─" * 40)
    print("           [ESTADÍSTICAS]")
    print("─" * 40)
    print(f"📦 Unidades totales     : {stats['unidades_totales']}")
    print(f"💰 Valor total          : ${stats['valor_total']:.2f}")
    print(f"💎 Producto más caro    : {stats['producto_mas_caro']['nombre']} "
          f"(${stats['producto_mas_caro']['precio']:.2f})")
    print(f"📊 Mayor stock          : {stats['producto_mayor_stock']['nombre']} "
          f"({stats['producto_mayor_stock']['cantidad']} unidades)")
    print("─" * 40)


def interfaz_guardar():
    """Pide ruta y llama a archivos.guardar_csv()"""
    print("\n--- [GUARDAR CSV] ---")
    ruta = input("Ruta del archivo (ej: inventario.csv): ").strip()
    if ruta == "":
        ruta = "inventario.csv"
    archivos.guardar_csv(inventario, ruta)


def interfaz_cargar():
    """Pide ruta, carga el CSV y pregunta si sobrescribir o fusionar"""
    print("\n--- [CARGAR CSV] ---")
    ruta = input("Ruta del archivo CSV a cargar: ").strip()

    # Intentamos cargar — la función ya maneja los errores internamente
    productos_nuevos = archivos.cargar_csv(ruta)

    # Si no se cargó nada, no hay nada que hacer
    if len(productos_nuevos) == 0:
        print("⚠️  No se cargaron productos.")
        return

    # Preguntamos la política de carga
    print(f"\n¿Qué deseas hacer con los {len(productos_nuevos)} producto(s) cargado(s)?")
    print("  S = Sobrescribir inventario actual")
    print("  N = Fusionar (suma cantidades, actualiza precios)")

    decision = ""
    while decision not in ["s", "n"]:
        decision = input("Elige (S/N): ").lower().strip()

    if decision == "s":
        # Sobrescribir: vaciamos la lista y cargamos los nuevos
        # clear() elimina todos los elementos de la lista
        inventario.clear()
        for p in productos_nuevos:
            inventario.append(p)
        print(f"\n✅ Inventario reemplazado con {len(inventario)} producto(s).")

    else:
        # Fusionar: la función de archivos.py maneja la lógica
        antes = len(inventario)
        archivos.fusionar_inventario(inventario, productos_nuevos)
        print(f"\n✅ Fusión completada. "
              f"Antes: {antes} producto(s) → Ahora: {len(inventario)} producto(s).")
        print("   Política aplicada: cantidad sumada, precio actualizado al nuevo.")


# ==============================================================================
# MOTOR PRINCIPAL — menú con while hasta que el usuario elija salir
# ==============================================================================

opcion = ""
while opcion != "9":

    print("\n" + "═" * 40)
    print("      SISTEMA DE INVENTARIO AVANZADO")
    print("═" * 40)
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Estadísticas")
    print("7. Guardar CSV")
    print("8. Cargar CSV")
    print("9. Salir")

    opcion = input("\nElige una opción (1-9): ").strip()

    # Procesamos la opción con if/elif/else
    if opcion == "1":
        interfaz_agregar()
    elif opcion == "2":
        servicios.mostrar_inventario(inventario)
    elif opcion == "3":
        interfaz_buscar()
    elif opcion == "4":
        interfaz_actualizar()
    elif opcion == "5":
        interfaz_eliminar()
    elif opcion == "6":
        interfaz_estadisticas()
    elif opcion == "7":
        interfaz_guardar()
    elif opcion == "8":
        interfaz_cargar()
    elif opcion == "9":
        print("\n👋 Sistema cerrado. ¡Hasta luego!")
    else:
        print(f"\n⚠️  '{opcion}' no es válida. Elige entre 1 y 9.")

# ==============================================================================
# RESUMEN DE LA SEMANA:
# Construimos un inventario modular con persistencia en CSV.
# Aplicamos listas de diccionarios, funciones con docstrings,
# módulos separados (servicios.py, archivos.py), manejo de errores
# con try/except, y lectura/escritura de archivos reales.
# El sistema sobrevive entradas inválidas y datos corruptos sin cerrarse.
# ==============================================================================
