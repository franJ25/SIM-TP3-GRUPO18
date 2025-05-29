import random


def calcular_ausentismo(probabilidades_acumuladas, num_obreros_aus):
    aleatorio = random.random()
    for indice, prob_acumulada in enumerate(probabilidades_acumuladas):
        if aleatorio < prob_acumulada:
            return num_obreros_aus[indice]
    return num_obreros_aus[-1]


def calcular_beneficio_diario(conductores_totales, presentes, ingreso_diario, costo_operativo, salario):
    ingreso_total = 0
    costo_salario = conductores_totales * salario
    costo_total = costo_operativo + costo_salario

    if presentes >= 20:
        ingreso_total = ingreso_diario
    return ingreso_total - costo_total, costo_salario, costo_total, ingreso_total


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
        ausentes = calcular_ausentismo(probabilidades_acumuladas, [0, 1, 2, 3, 4, 5])
        presentes = conductores_totales - ausentes
        beneficio, costo_salario, costo_total, ingreso_total = calcular_beneficio_diario(conductores_totales, presentes,
                                                                                         ingreso_diario,
                                                                                         costo_operativo, salario)
        beneficio_acumulado += beneficio
        fila = {
                'Día': dia,
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
            print("fila: ", fila, flush=True)
        if dia == n:
            ultima_fila = fila
    return beneficio_acumulado, ultima_fila


def ejecutar_simulacion(ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i, j):
    resultado1 = simular(21, ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i, j)
    resultado2 = simular(22, ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i, j)
    resultado3 = simular(23, ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i, j)
    resultado4 = simular(24, ingreso_diario, costo_operativo, salario, datos_ausentismo, n, i, j)
    return resultado1, resultado2, resultado3, resultado4
