from pulp import *


# Creación de la clase Group Scheduling


class GroupScheduling:

    # Método 0. Constructor de problema de FlowShop Group Scheduling

    def __init__(self, grupos, maquinas, num_trabajos, trabajos_grupos, num_trab_grupo,
                 t_procesamiento, t_preparacion, fechas_entrega=None, costos_tardanza=None,
                 objetivo="tct"):
        self.grupos = grupos
        self.maquinas = maquinas
        self.num_trabajos = num_trabajos
        self.trabajos_grupos = trabajos_grupos
        self.num_trab_k = num_trab_grupo
        self.t_procesamiento = t_procesamiento
        self.t_preparacion = t_preparacion
        self.fechas_entrega = fechas_entrega
        self.costos_tardanza = costos_tardanza
        self.objetivo = objetivo
        self.M = 999999

    # Método 1. Mostrar por pantalla los atributos actuales de la clase

    def obtener_atributos(self):
        print("\nATRIBUTOS DE LA CLASE:\n"
              "Grupos/Familias: {}\n".format(self.grupos),
              "Máquinas: {}\n".format(self.maquinas),
              "Número total de trabajos: {}\n".format(self.num_trabajos),
              "Trabajos que pertenecen a cada grupo: {}\n".format(self.trabajos_grupos),
              "Número de trabajos en cada grupo: {}\n".format(self.num_trab_k),
              "Tiempo de procesamiento de trabajos en máquinas:\n{}\n".format(self.t_procesamiento),
              "Tiempo de preparación de grupos en máquinas:\n{}\n".format(self.t_preparacion),
              "Fechas de entrega de los trabajos:\n{}\n".format(self.fechas_entrega),
              "Costos de penalización por tardanza de los trabajos:\n{}\n".format(self.costos_tardanza),
              "Función objetivo:\n{}\n".format(self.objetivo))

    # Método 2. Decodificar cromosoma de solución del FSGSP

    def decodificar_schedule(self, individuo):

        # 2.1 Definir lista inicial para recopilar tiempos de preparación, inicio y terminación de trabajos

        jobs_times = []  # jobs_times[job - 1][machine - 1] = [[setup_start_time, setup_time], [start_run, finish_run]]
        grupo_ant = 0
        t_term_trab_ant_maq = [0] * len(self.maquinas)

        # 2.2 Calcular el tiempo de inicio y terminación de cada trabajo en cada máquina

        for g in individuo[0]:
            for j in individuo[g]:
                t_trabajos_maqs = []
                t_term_trab_maq_ant = 0

                for i in self.maquinas:

                    t_inicio = max(t_term_trab_maq_ant,
                                   t_term_trab_ant_maq[i - 1] + self.t_preparacion[i - 1][grupo_ant][g - 1])
                    t_terminacion = t_inicio + self.t_procesamiento[j - 1][i - 1]
                    t_ini_term = [t_inicio, t_terminacion]

                    if grupo_ant != g:
                        t_prep = [t_term_trab_ant_maq[i - 1], self.t_preparacion[i - 1][grupo_ant][g - 1]]
                    else:
                        t_prep = [0, 0]

                    t_trabajos_maqs.append([t_prep, t_ini_term])

                    t_term_trab_maq_ant = t_terminacion
                    t_term_trab_ant_maq[i - 1] = t_terminacion

                grupo_ant = g
                jobs_times.append(t_trabajos_maqs)

        return jobs_times

    # Método 3. Definir método para obtener fitness: makespan, total completion time, total weighted tardiness

    def fitness(self, individuo):

        tiempos_trabajos = self.decodificar_schedule(individuo)
        fitness = 0

        if self.objetivo == "makespan":

            fitness = tiempos_trabajos[-1][-1][-1][-1]

        elif self.objetivo == "tct":

            for i in tiempos_trabajos:
                fitness += i[-1][-1][-1]

        elif self.objetivo == "twt":

            indice = 0
            for grupo in individuo[0]:
                for trab in individuo[grupo]:
                    tardanza = max(tiempos_trabajos[indice][-1][-1][-1] - self.fechas_entrega[trab - 1], 0)
                    fitness += self.costos_tardanza[trab - 1] * tardanza
                    indice += 1

        return fitness

    # Método. Definir método para obtener makespan

    def makespan(self, individuo):

        tiempos_trabajos = self.decodificar_schedule(individuo)
        compl_max = tiempos_trabajos[-1][-1][-1][-1]

        return compl_max

    # Método. Definir método para obtener total completion time

    def total_completion(self, individuo):

        tiempos_trabajos = self.decodificar_schedule(individuo)
        total_completion_time = 0

        for i in tiempos_trabajos:
            total_completion_time += i[-1][-1][-1]

        return total_completion_time

    # Método 4. Optimizar modelo MILP del FSGSP para los objetivos de TCT y Cmax mediante PuLP
    # Retrieved from Naderi & Salmasi, 2012 (Model 2)

    def optimizar_milp(self, objetivo="tct"):

        # 4.1 Definir el problema con PuLP

        prob = LpProblem("Flowshop Group Scheduling", sense=LpMinimize)
        print("El problema se ha definido con PuLP")

        # 4.2 Definir las variables del modelo

        # (X_jl) job j occupies lth position of group k
        x_job_sequence = LpVariable.dicts("X", ((j, l) for k in self.grupos
                                                for j in self.trabajos_grupos[k - 1]
                                                for l in range(1, self.num_trab_k[k - 1] + 1)),
                                          cat="Binary")

        # (U_tk) group k is processed immediately after group p
        u_group_sequence = LpVariable.dicts("U", ((t, k) for t in range(len(self.grupos) + 1)
                                                  for k in self.grupos
                                                  if t != k),
                                            cat="Binary")

        # (F_ki) finishing time of the last job of group k on machine i
        f_finishing_group = LpVariable.dicts("F", ((k, i) for k in range(len(self.grupos) + 1)
                                                   for i in self.maquinas),
                                             lowBound=0, upBound=None, cat="Continuous")

        # (S_ki) starting time of the first job of group k on machine i
        s_starting_group = LpVariable.dicts("S", ((k, i) for k in self.grupos
                                                  for i in self.maquinas),
                                            lowBound=0, upBound=None, cat="Continuous")

        # (C_kli) completion time of the job in the lth position of group k on machine i
        c_completion_job = LpVariable.dicts("C", ((k, l, i) for k in self.grupos
                                                  for l in range(1, self.num_trab_k[k - 1] + 1)
                                                  for i in range(len(self.maquinas) + 1)),
                                            lowBound=0, upBound=None, cat="Continuous")

        # 4.3 Definir la función objetivo del modelo

        if objetivo == "tct":
            prob += lpSum(c_completion_job[k, l, self.maquinas[-1]]
                          for k in self.grupos
                          for l in range(1, self.num_trab_k[k - 1] + 1))
        elif objetivo == "makespan":
            prob += lpSum(c_completion_job[k, self.num_trab_k[k - 1], self.maquinas[-1]]
                          for k in self.grupos)

        # 4.4 Definir las restricciones del modelo

        # (12) each group on each machine starts processing after last job of the immediately previous
        # group is finished
        for t in range(len(self.grupos) + 1):
            for k in self.grupos:
                if t != k:
                    for i in self.maquinas:

                        if t == 0:
                            f_finishing_group[t, i] = 0

                        prob += s_starting_group[k, i] >= f_finishing_group[t, i] + \
                            self.t_preparacion[i - 1][t][k - 1] - (1 - u_group_sequence[t, k]) * self.M

        # (13) each group should have exactly one group as the previous processed group on each machine
        for k in self.grupos:
            prob += lpSum(u_group_sequence[t, k] for t in range(len(self.grupos) + 1)
                          if t != k) == 1

        # (14) each group has at most one successor group
        for t in range(len(self.grupos) + 1):
            prob += lpSum(u_group_sequence[t, k] for k in self.grupos
                          if t != k) <= 1

        # (15) the reference group -group zero- is assigned to the first slot
        prob += lpSum(u_group_sequence[0, k] for k in self.grupos) == 1

        # (16) each group can be processed before or after another group
        for t in self.grupos[:-1]:
            k = t + 1

            prob += u_group_sequence[t, k] + u_group_sequence[k, t] <= 1

        # (22) each job occupies exactly one slot in the group it belongs
        for k in self.grupos:
            for j in self.trabajos_grupos[k - 1]:
                prob += lpSum(x_job_sequence[j, l] for l in range(1, self.num_trab_k[k - 1] + 1)) == 1

        # (23) each slot of any group is assigned to one of the jobs in that group
        for k in self.grupos:
            for l in range(1, self.num_trab_k[k - 1] + 1):
                prob += lpSum(x_job_sequence[j, l] for j in self.trabajos_grupos[k - 1]) == 1

        # (24) processing of a job can start if processing of the job in the previous slot is finished
        for k in self.grupos:
            for l in range(2, self.num_trab_k[k - 1] + 1):
                for i in self.maquinas:
                    prob += c_completion_job[k, l, i] >= c_completion_job[k, l - 1, i] + \
                            lpSum(x_job_sequence[j, l] * self.t_procesamiento[j - 1][i - 1]
                                  for j in self.trabajos_grupos[k - 1])

        # (25) processing of each job starts after the processing of the job is concluded
        # on the previous machine
        for k in self.grupos:
            for l in range(1, self.num_trab_k[k - 1] + 1):
                for i in self.maquinas:

                    if i == 1:
                        c_completion_job[k, l, 0] = 0

                    prob += c_completion_job[k, l, i] >= c_completion_job[k, l, i - 1] + \
                        lpSum(x_job_sequence[j, l] * self.t_procesamiento[j - 1][i - 1]
                              for j in self.trabajos_grupos[k - 1])

        # (26) processing of a job in the first slot of each group starts after
        # the starting point of the group
        for k in self.grupos:
            for i in self.maquinas:
                prob += c_completion_job[k, 1, i] >= s_starting_group[k, i] + \
                        lpSum(x_job_sequence[j, 1] * self.t_procesamiento[j - 1][i - 1]
                              for j in self.trabajos_grupos[k - 1])

        # (27) completion time of a group is greater than or equal to the completion
        # time of the job in the last slot
        for k in self.grupos:
            for i in self.maquinas:
                prob += f_finishing_group[k, i] >= c_completion_job[k, self.num_trab_k[k - 1], i]

        # 4.5 Resolver el problema y mostrar respuesta: Solver: CBC MILP Solver(v. 2.9.0)

        print(prob)
        # prob.solve()
        prob.solve(solver=CPLEX_CMD())

        # Mostrar variables con sus respectivos valores
        for v in prob.variables():
            print(v.name, " = ", v.varValue)

        # Mostrar valor de la función objetivo
        objective_value = 0
        if objetivo == "tct":
            objective_value = value(prob.objective)
        elif objetivo == "makespan":
            completion_j = []
            for k in self.grupos:
                completion_j.append(c_completion_job[k, self.num_trab_k[k - 1], self.maquinas[-1]].varValue)
            objective_value = max(completion_j)

        print("Status: ", LpStatus[prob.status])
        print("Objective Function Value = ", objective_value)

        return objective_value

    # Método 5. Optimizar modelo MILP del FSGSP para el objetivo de Total Weighted Tardiness mediante PuLP
    # Retrieved from Naderi & Salmasi, 2012 (Model 1)

    def optimizar_milp_twt(self):

        # 5.1 Definir el problema con PuLP

        prob = LpProblem("Flowshop Group Scheduling", sense=LpMinimize)
        print("El problema se ha definido con PuLP")

        # 5.2 Definir las variables del modelo

        # (X_lj) job j is processed after job l
        x_job_sequence = LpVariable.dicts("X", ((l, j) for k in self.grupos
                                                for j in self.trabajos_grupos[k - 1]
                                                for l in self.trabajos_grupos[k - 1]
                                                if j > l),
                                          cat="Binary")

        # (U_tk) group k is processed immediately after group p
        u_group_sequence = LpVariable.dicts("U", ((t, k) for t in range(len(self.grupos) + 1)
                                                  for k in self.grupos
                                                  if t != k),
                                            cat="Binary")

        # (F_ki) finishing time of the last job of group k on machine i
        f_finishing_group = LpVariable.dicts("F", ((k, i) for k in range(len(self.grupos) + 1)
                                                   for i in self.maquinas),
                                             lowBound=0, upBound=None, cat="Continuous")

        # (S_ki) starting time of the first job of group k on machine i
        s_starting_group = LpVariable.dicts("S", ((k, i) for k in self.grupos
                                                  for i in self.maquinas),
                                            lowBound=0, upBound=None, cat="Continuous")

        # (C_ji) completion time of the job j on machine i
        c_completion_job = LpVariable.dicts("C", ((j, i) for k in self.grupos
                                                  for j in self.trabajos_grupos[k - 1]
                                                  for i in range(len(self.maquinas) + 1)),
                                            lowBound=0, upBound=None, cat="Continuous")

        # (T_j) tardiness of the job j
        t_tardiness_job = LpVariable.dicts("T", ((j) for k in self.grupos
                                                 for j in self.trabajos_grupos[k - 1]),
                                           lowBound=0, upBound=None, cat="Continuous")

        # 5.3 Definir la función objetivo del modelo

        prob += lpSum(self.costos_tardanza[j - 1] * t_tardiness_job[j] for k in self.grupos
                      for j in self.trabajos_grupos[k - 1])

        # 5.4 Definir las restricciones del modelo

        # (7) completion time of a job on a machine should be greater than its completion time
        # on the previous machine
        for k in self.grupos:
            for j in self.trabajos_grupos[k - 1]:
                for i in self.maquinas:

                    if i == 1:
                        c_completion_job[j, i - 1] = 0

                    prob += c_completion_job[j, i] >= c_completion_job[j, i - 1] + self.t_procesamiento[j - 1][i - 1]

        # (8 and 9) jobs are not processed simultaneously on each machine
        for k in self.grupos:
            for j in self.trabajos_grupos[k - 1]:
                for l in self.trabajos_grupos[k - 1]:
                    for i in self.maquinas:
                        if j > l:
                            # (8)
                            prob += c_completion_job[j, i] >= (c_completion_job[l, i] +
                                                               self.t_procesamiento[j - 1][i - 1] -
                                                               ((1 - x_job_sequence[l, j]) * self.M))
                            # (9)
                            prob += c_completion_job[l, i] >= (c_completion_job[j, i] +
                                                               self.t_procesamiento[l - 1][i - 1] -
                                                               x_job_sequence[l, j] * self.M)

        # (10 and 11) jobs should start and finish between starting and finishing times of the group it
        # belongs to
        for k in self.grupos:
            for j in self.trabajos_grupos[k - 1]:
                for i in self.maquinas:
                    # (10)
                    prob += c_completion_job[j, i] >= s_starting_group[k, i] + self.t_procesamiento[j - 1][i - 1]

                    # (11)
                    prob += f_finishing_group[k, i] >= c_completion_job[j, i]

        # (12) each group on each machine starts processing after last job of the immediately previous
        # group is finished
        for t in range(len(self.grupos) + 1):
            for k in self.grupos:
                if t != k:
                    for i in self.maquinas:

                        if t == 0:
                            f_finishing_group[t, i] = 0

                        prob += s_starting_group[k, i] >= f_finishing_group[t, i] + \
                            self.t_preparacion[i - 1][t][k - 1] - (1 - u_group_sequence[t, k]) * self.M

        # (13) each group should have exactly one group as the previous processed group on each machine
        for k in self.grupos:
            prob += lpSum(u_group_sequence[t, k] for t in range(len(self.grupos) + 1)
                          if t != k) == 1

        # (14) each group has at most one successor group
        for t in range(len(self.grupos) + 1):
            prob += lpSum(u_group_sequence[t, k] for k in self.grupos
                          if t != k) <= 1

        # (15) the reference group -group zero- is assigned to the first slot
        prob += lpSum(u_group_sequence[0, k] for k in self.grupos) == 1

        # (16) each group can be processed before or after another group
        for t in self.grupos[:-1]:
            k = t + 1

            prob += u_group_sequence[t, k] + u_group_sequence[k, t] <= 1

        # (17) tardiness of a job is the difference between completion time of the job and its due date
        for k in self.grupos:
            for j in self.trabajos_grupos[k - 1]:

                prob += t_tardiness_job[j] >= c_completion_job[j, self.maquinas[-1]] - self.fechas_entrega[j - 1]

        # 5.5 Resolver el problema y mostrar respuesta: Solver: CBC MILP Solver(v. 2.9.0)

        # prob.solve()
        prob.solve(solver=CPLEX_CMD())

        for v in prob.variables():
            print(v.name, " = ", v.varValue)
        print("Status: ", LpStatus[prob.status])
        print("Objective function value: ", value(prob.objective))

        return value(prob.objective)
