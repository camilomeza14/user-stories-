# ==============================================================================
# MÓDULO: archivos.py
# DESCRIPCIÓN: Guardar y cargar inventario desde archivos CSV
# CSV = valores separados por comas. Ejemplo:
#   nombre,precio,cantidad
#   Lápiz,500.0,10
# ==============================================================================

import csv  # Módulo estándar de Python para leer y escribir CSV


def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.
    Parámetros:
        inventario (list): lista de diccionarios de productos
        ruta (str): ruta del archivo destino (ej: "inventario.csv")
        incluir_header (bool): si True, escribe la fila de encabezado
    Retorna: None
    """
    # No tiene sentido guardar si el inventario está vacío
    if len(inventario) == 0:
        print("\n⚠️  El inventario está vacío. No hay nada que guardar.")
        return

    try:
        # Abrimos el archivo en modo escritura
        # newline="" evita líneas en blanco extra en Windows
        # encoding="utf-8" permite caracteres especiales (tildes, ñ)
        with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)

            # Escribimos el encabezado si se pidió
            if incluir_header:
                writer.writerow(["nombre", "precio", "cantidad"])

            # Escribimos una fila por cada producto
            for producto in inventario:
                writer.writerow([
                    producto["nombre"],
                    producto["precio"],
                    producto["cantidad"]
                ])

        print(f"\n✅ Inventario guardado en: {ruta}")

    except PermissionError:
        # Ocurre si el archivo está abierto en otro programa o no hay permisos
        print(f"\n❌ Sin permisos para escribir en '{ruta}'. Cierra el archivo si está abierto.")
    except Exception as e:
        # Cualquier otro error inesperado — lo mostramos pero no cerramos el programa
        print(f"\n❌ Error al guardar: {e}")


def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV al inventario.
    Parámetros:
        ruta (str): ruta del archivo CSV a leer
    Retorna:
        list: lista de productos válidos cargados
              lista vacía si hay error o el archivo no existe
    """
    productos_cargados = []
    filas_invalidas = 0

    try:
        with open(ruta, mode="r", newline="", encoding="utf-8") as archivo:
            reader = csv.reader(archivo)

            # Leemos y validamos el encabezado
            header = next(reader, None)
            if header != ["nombre", "precio", "cantidad"]:
                print(f"\n❌ Encabezado inválido en '{ruta}'.")
                print("   Se esperaba: nombre,precio,cantidad")
                return []

            # Procesamos cada fila del archivo
            for numero_fila, fila in enumerate(reader, start=2):

                # Validamos que la fila tenga exactamente 3 columnas
                if len(fila) != 3:
                    filas_invalidas = filas_invalidas + 1
                    continue  # Saltamos esta fila y seguimos con la siguiente

                try:
                    nombre = fila[0].strip()
                    precio = float(fila[1])
                    cantidad = int(fila[2])

                    # Validamos que los valores no sean negativos
                    if precio < 0 or cantidad < 0:
                        filas_invalidas = filas_invalidas + 1
                        continue

                    # Si todo está bien, armamos el diccionario
                    productos_cargados.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })

                except ValueError:
                    # precio no era float o cantidad no era int
                    filas_invalidas = filas_invalidas + 1
                    continue

    except FileNotFoundError:
        print(f"\n❌ Archivo '{ruta}' no encontrado.")
        return []
    except UnicodeDecodeError:
        print(f"\n❌ El archivo '{ruta}' tiene caracteres que no se pueden leer. Guárdalo en UTF-8.")
        return []
    except Exception as e:
        print(f"\n❌ Error inesperado al leer el archivo: {e}")
        return []

    # Reportamos cuántas filas inválidas se encontraron
    if filas_invalidas > 0:
        print(f"\n⚠️  {filas_invalidas} fila(s) inválida(s) omitida(s).")

    print(f"📥 {len(productos_cargados)} producto(s) cargado(s) desde '{ruta}'.")
    return productos_cargados


def fusionar_inventario(inventario, productos_nuevos):
    """
    Fusiona productos_nuevos al inventario existente.
    Política de fusión:
        - Si el nombre YA existe → suma la cantidad y actualiza el precio al nuevo
        - Si el nombre NO existe → lo agrega como producto nuevo
    Parámetros:
        inventario (list): inventario actual en memoria
        productos_nuevos (list): productos cargados del CSV
    Retorna: None (modifica inventario directamente)
    """
    for nuevo in productos_nuevos:
        # Buscamos si ya existe un producto con ese nombre
        encontrado = False
        for existente in inventario:
            if existente["nombre"].lower() == nuevo["nombre"].lower():
                # Política: sumamos cantidad y actualizamos precio
                existente["cantidad"] = existente["cantidad"] + nuevo["cantidad"]
                existente["precio"] = nuevo["precio"]
                encontrado = True
                break

        # Si no existía, lo agregamos
        if not encontrado:
            inventario.append(nuevo)
