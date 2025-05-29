# interfaz.py

# Asegúrate de que el archivo con la lógica de simulación se llame 'logica_simulacion.py'
# y esté en el mismo directorio que este archivo 'interfaz.py'.
try:
    from montecarlo_terminal import ejecutar_simulacion
except ImportError:
    print("Error: No se pudo encontrar el archivo 'logica_simulacion.py'.")
    print("Asegúrate de que el archivo con la lógica principal se llame así y esté en el mismo directorio.")
    exit()

def obtener_numero_positivo(mensaje, tipo_dato=float):
    """Solicita al usuario un número positivo del tipo especificado."""
    while True:
        try:
            valor = tipo_dato(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo. Inténtalo de nuevo.")
            else:
                return valor
        except ValueError:
            print(f"Entrada inválida. Debes ingresar un número. Inténtalo de nuevo.")

def obtener_lista_enteros(mensaje, longitud_esperada):
    """Solicita al usuario una lista de enteros de una longitud específica."""
    while True:
        try:
            entrada_str = input(mensaje)
            elementos_str = entrada_str.split(',')
            if len(elementos_str) != longitud_esperada:
                print(f"Debes ingresar exactamente {longitud_esperada} números separados por coma.")
                continue

            lista_enteros = [int(e.strip()) for e in elementos_str]
            if any(n < 0 for n in lista_enteros):
                print("Todos los números en la lista deben ser no negativos. Inténtalo de nuevo.")
                continue
            return lista_enteros
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar números enteros separados por coma (ej: 20,30,15,10,5,2).")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

def mostrar_resultados_simulacion(resultados, n_dias):
    """Muestra los resultados finales de la simulación."""
    print("\n" + "="*50)
    print("RESUMEN DE LA SIMULACIÓN")
    print("="*50)

    conductores_opciones = [21, 22, 23, 24]

    for i, (beneficio_acum, ultima_fila) in enumerate(resultados):
        conductores_actuales = conductores_opciones[i]
        print(f"\n--- Escenario con {conductores_actuales} Conductores Totales ---")
        print(f"Beneficio total acumulado en {n_dias} días: ${beneficio_acum:,.2f}")

        if ultima_fila:
            print(f"\nDetalles del último día simulado (Día {ultima_fila['Día']}):")
            print(f"  Ausentes:             {ultima_fila['Ausentes']}")
            print(f"  Presentes:            {ultima_fila['Presentes']}")
            print(f"  Ingreso Diario:       ${ultima_fila['Ingreso']:,.2f}")
            print(f"  Costo Operativo:      ${ultima_fila['Costo_Operativo']:,.2f}")
            print(f"  Costo Salario:        ${ultima_fila['Costo_Salario']:,.2f}")
            print(f"  Costo Total Diario:   ${ultima_fila['Costo_Total']:,.2f}")
            print(f"  Beneficio Diario:     ${ultima_fila['Beneficio_Diario']:,.2f}")
            print(f"  Beneficio Acumulado:  ${ultima_fila['Beneficio_Acumulado']:,.2f}")
        else:
            print("No se generaron datos para el último día (esto no debería ocurrir si n > 0).")
        print("-"*50)

    # Determinar la mejor opción
    mejor_beneficio = -float('inf')
    mejor_opcion_conductores = 0
    for i, (beneficio_acum, _) in enumerate(resultados):
        if beneficio_acum > mejor_beneficio:
            mejor_beneficio = beneficio_acum
            mejor_opcion_conductores = conductores_opciones[i]

    print("\n--- CONCLUSIÓN ---")
    if mejor_opcion_conductores > 0:
        print(f"La política de contratación que maximiza el beneficio es tener {mejor_opcion_conductores} conductores,")
        print(f"generando un beneficio acumulado de ${mejor_beneficio:,.2f} en {n_dias} días.")
    else:
        print("No se pudo determinar una política óptima con los datos proporcionados.")
    print("="*50)


def main():
    print("Bienvenido al Simulador de Beneficios de Empresa de Transporte")
    print("="*60)
    print("Por favor, ingresa los datos para la simulación:")

    ingreso_diario = obtener_numero_positivo("Ingreso diario si hay 20 o más conductores presentes (ej: 3000): ", float)
    costo_operativo = obtener_numero_positivo("Costo operativo diario (ej: 1200): ", float)
    salario = obtener_numero_positivo("Salario diario por conductor (ej: 60): ", float)

    print("\nDatos de ausentismo (frecuencia observada para 0, 1, 2, 3, 4, 5 ausentes):")
    print("Ejemplo: si para 0 ausentes se observó 20 veces, para 1 ausente 30 veces, etc.")
    datos_ausentismo = obtener_lista_enteros(
        "Ingresa las frecuencias separadas por coma (6 valores) (ej: 20,30,25,15,7,3): ",
        6
    )

    print("\nParámetros de la simulación:")
    n = obtener_numero_positivo("Número total de días a simular (N) (ej: 365): ", int)

    print("\nParámetros de visualización de filas durante la simulación:")
    print("La simulación imprimirá las filas desde el día 'j' hasta el día 'j+i-1'.")
    i_display = obtener_numero_positivo("Número de filas a mostrar consecutivamente (i) (ej: 5): ", int)
    j_display = obtener_numero_positivo("Día de inicio para mostrar filas (j) (ej: 1): ", int)
    if j_display > n :
        print(f"Advertencia: El día de inicio para mostrar filas ({j_display}) es mayor que el total de días ({n}). No se mostrarán filas intermedias.")
    if j_display + i_display -1 > n:
        print(f"Advertencia: El rango de visualización ({j_display} a {j_display+i_display-1}) excede el número total de días ({n}). Se mostrarán filas hasta el día {n}.")


    print("\n" + "-"*30)
    print("Iniciando simulación...")
    print("Las filas intermedias (si 'i' y 'j' están en rango) se mostrarán a continuación:")
    print("Ten en cuenta que se ejecutarán 4 simulaciones (para 21, 22, 23 y 24 conductores).")
    print("-"*30 + "\n")

    # Ejecutar la simulación
    # Los prints de las filas intermedias ocurren dentro de la función 'simular' importada
    resultados_completos = ejecutar_simulacion(
        ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i_display, j_display
    )

    # Mostrar el resumen final
    mostrar_resultados_simulacion(resultados_completos, n)

    print("\nSimulación completada.")

if __name__ == "__main__":
    main()
