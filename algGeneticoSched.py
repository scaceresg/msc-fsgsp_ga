# Algoritmo genético para el FSGSP

import numpy as np


class AlgGeneticoSched:

    # Método 0. Constructor con los parámetros de GA

    def __init__(self, tam_poblacion, num_generaciones, tam_torneo, prob_cruce, prob_mutacion):
        self.tam_poblacion = tam_poblacion
        self.num_generaciones = num_generaciones
        self.tam_torneo = tam_torneo
        self.prob_cruce = prob_cruce
        self.prob_mutacion = prob_mutacion

    # Método 1. Crear individuos de la población inicial

    def poblacion_inicial(self, group_scheduling):

        # 1.1 Estructuras necesarias para el método

        poblacion = []

        for ind in range(self.tam_poblacion):
            individuo = []
            arr_grupos = np.random.permutation(group_scheduling.grupos)
            individuo.append(arr_grupos)

            for j in group_scheduling.trabajos_grupos:
                arr_trabajos = np.random.permutation(j)
                individuo.append(arr_trabajos)

            poblacion.append(individuo)

        # print("Población de individuos: \n", poblacion)

        return poblacion

    # Método 2. Evaluar los individuos de la población de acuerdo con la fitness

    def obtener_mejor(self, group_scheduling, poblacion):

        best = 99999999
        best_ind = 0
        for ind in poblacion:
            fitness_ind = group_scheduling.fitness(ind)
            if fitness_ind < best:
                best = fitness_ind
                best_ind = ind

        print("El mejor individuo de la población es: \n", best_ind,
              "\nCon un Fitness de: \n", best)

        return best, best_ind

    # Método 3. Seleccionar individuos a cruzar según torneo

    def seleccion(self, group_scheduling, poblacion):

        # Tournament Selection

        ganador = 0
        ganador_pos = 999
        ganadores = []

        # 3.1 Elegir aleatoriamente individuos para el toreno

        ganador_torneo1 = 999
        for torneo in range(2):

            fit_ganador = 99999999
            pos_elegidas = []
            for k in range(self.tam_torneo):

                # Identificar posición aleatoria para participante
                pos = np.random.randint(0, len(poblacion), 1)[0]
                while pos in pos_elegidas or pos == ganador_torneo1:
                    pos = np.random.randint(0, len(poblacion), 1)[0]
                pos_elegidas.append(pos)

                # Actualizar el mejor del torneo según función objetivo

                fit_participante = group_scheduling.fitness(poblacion[pos])

                if fit_participante < fit_ganador:
                    fit_ganador = fit_participante
                    ganador = poblacion[pos]
                    ganador_pos = pos

            # Agregar al ganador del torneo a la lista ganadores
            ganadores.append(ganador)
            ganador_torneo1 = ganador_pos

        return ganadores

    # Método 4. Cruzar individuos seleccionados para generar nueva población

    def cruce(self, padres):

        # Partially Matched Crossover (PMX)

        hijos = []
        hijo1, hijo2 = [], []
        padre1, padre2 = padres[0], padres[1]

        # 5.1 Evaluar probabilidad de cruce entre los padres

        if np.random.rand() <= self.prob_cruce:

            # 5.2 Encontrar sección de cromosoma y cruzar padres

            for ind_s, s in enumerate(padre1):
                t = padre2[ind_s]

                # Encontrar posición de cortes para cruce

                cortes = np.random.randint(0, len(s), 2)
                cortes = np.sort(cortes)

                while cortes[0] == cortes[1]:
                    cortes = np.random.randint(0, len(s), 2)
                    cortes = np.sort(cortes)

                # Realizar cruce entre padres mediante PMX

                for i in range(cortes[0], cortes[1]):

                    # Identificar los genes en las posiciones de corte

                    gen1 = s[i]
                    gen2 = t[i]

                    if gen1 != gen2:

                        # Se cambia el gen1 por el gen2 en los cromosomas padre

                        pos_g = 0
                        suma = 0
                        for g in s:
                            if g == gen1:
                                s[pos_g] = gen2
                                suma += 1
                            if g == gen2:
                                s[pos_g] = gen1
                                suma += 1
                            pos_g += 1
                            if suma == 2:
                                suma = 0
                                break

                        pos_h = 0
                        for h in t:
                            if h == gen1:
                                t[pos_h] = gen2
                                suma += 1
                            if h == gen2:
                                t[pos_h] = gen1
                                suma += 1
                            pos_h += 1
                            if suma == 2:
                                break

                # 5.3 Añadir cada sección de cromosoma cruzada en el nuevo individiuo

                hijo1.append(s)
                hijo2.append(t)
        else:

            hijo1 = padre1
            hijo2 = padre2
        # 5.4 Añadir los individuos cruzados

        hijos.append(hijo1)
        hijos.append(hijo2)

        return hijos

    # Método 6. Realizar mutación de individuos de acuerdo con operador de mutación

    def mutacion(self, hijos):

        # 6.1 Evaluar la probabilidad de mutación de los dos hijos

        if np.random.rand() <= self.prob_mutacion:

            # 6.2 Mutar dos genes de los individuos hijos en cada sección

            for son in hijos:
                for section in son:

                    genes = np.random.randint(0, len(section), 2)
                    while genes[0] == genes[1]:
                        genes = np.random.randint(0, len(section), 2)

                    gen1 = section[genes[0]]
                    gen2 = section[genes[1]]

                    section[genes[0]] = gen2
                    section[genes[1]] = gen1

        return hijos

    # Método 7. Sustituir los peores individuos de la población actual por los nuevos individuos

    def sustitucion(self, group_scheduling, poblacion, hijos):

        # 7.1 Evaluar la función objetivo y eliminar los dos peores individuo

        for i in range(2):

            fit_peor = 0
            pos_peor = 999

            for index, ind in enumerate(poblacion):

                fit_ind = group_scheduling.fitness(ind)

                if fit_ind >= fit_peor:
                    fit_peor = fit_ind
                    pos_peor = index

            del poblacion[pos_peor]

        # 7.2 Incluir los nuevos individuos a la población

        for hijo in hijos:
            poblacion.append(hijo)

        return poblacion
