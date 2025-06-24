import random
import interfazAlternativa


def calcular_ausentismo(probabilidades_acumuladas, num_obreros_aus):
    aleatorio = random.random()
    for indice, prob_acumulada in enumerate(probabilidades_acumuladas):
        if aleatorio < prob_acumulada:
            return num_obreros_aus[indice]
    return num_obreros_aus[-1]


def calcular_beneficio_diario(presentes, ingreso_diario, costo_total):
    ingreso_total = 0
    if presentes >= 20:
        ingreso_total = ingreso_diario
    return ingreso_total - costo_total


def calcular_distribucion(datos_ausentismo):
    distribucion = []
    total = sum(datos_ausentismo)
    for dato in datos_ausentismo:
        probabilidad = dato / total
        distribucion.append(probabilidad)
    return distribucion


def calcular_acumulada(distribucion):
    probabilidades_acumuladas = []
    for i in range(len(distribucion)):
        probabilidades_acumuladas.append(sum(distribucion[:i + 1]))
    return probabilidades_acumuladas


def simular(conductores_totales, ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i, j):
    distribucion = calcular_distribucion(datos_ausentismo)
    probabilidades_acumuladas = calcular_acumulada(distribucion)
    beneficio_acumulado = 0
    ultima_fila = None

    for dia in range(1, n + 1):
        # Obtener el RND para el ausentismo
        rnd_ausentismo = random.random()
        ausentes = calcular_ausentismo(probabilidades_acumuladas, [0, 1, 2, 3, 4, 5])
        presentes = conductores_totales - ausentes

        # Calcular columnas
        ingreso_total = 0
        costo_salario = conductores_totales * salario
        costo_total = costo_operativo + costo_salario

        # Calcular beneficio diario
        beneficio = calcular_beneficio_diario(presentes, ingreso_diario, costo_total)
        beneficio_acumulado += beneficio
        fila = {
                'Día': dia,
                'RND Ausentismo': rnd_ausentismo,
                'Ausentes': ausentes,
                'Presentes': presentes,
                'Ingreso': ingreso_total,
                'Costo_Operativo': costo_operativo,
                'Costo_Salario': costo_salario,
                'Costo_Total': costo_total,
                'Beneficio_Diario': beneficio,
                'Beneficio_Acumulado': beneficio_acumulado
            }
        if j <= dia <= min(i + j - 1, n):
            interfazAlternativa.imprimir_fila(fila)
        if dia == n:
            ultima_fila = fila
    return {
        'ultima_fila': ultima_fila,
        'distribucion': distribucion,
        'probabilidades_acumuladas': probabilidades_acumuladas
    }

