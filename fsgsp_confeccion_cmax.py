# Optimización del problema FSGSP mediante algoritmo genético para el caso del sector de la confección
# de prendas de vestir de la ciudad de Cúcuta, Colombia
# Minimizar el Tiempo de Terminación Total y el Makespan


from group_scheduling import *
from algGeneticoSched import *
import pandas as pd
from copy import deepcopy

# Datos de entrada para FSGSP:

datos_fsgsp = pd.read_excel("Input_sched_propuesto.xlsx")
cols_fsgsp = datos_fsgsp.columns.values

# Datos para la celda de manufactura 1 (CM1):

# Número de grupos (g)
grupos_cm1 = list(datos_fsgsp["G_CM1"].dropna().astype(int))

# Trabajos en cada grupo (G_k)
trabajos_grupos_cm1 = []
trab_cont = 1
for gr in grupos_cm1:
    n_trab = int(datos_fsgsp["J_CM1"][gr - 1])
    trabs = list(range(trab_cont, trab_cont + n_trab))
    trabajos_grupos_cm1.append(trabs)
    trab_cont += n_trab

# Número de máquinas (m)
maquinas_cm1 = list(range(1, 4 + 1))

# Número de trabajos (N)
num_trabajos_cm1 = trabajos_grupos_cm1[-1][-1]

# Número de trabajos en grupo k (n_k)
num_trabajos_k_cm1 = list(datos_fsgsp["J_CM1"].dropna().astype(int))

# Tiempo de procesamiento de trabajos (P_ji)
t_proc = datos_fsgsp[cols_fsgsp[1:5]].dropna()
t_procesamiento_cm1 = []
for ind in t_proc.index:
    t_procesamiento_cm1.append(list(t_proc.iloc[ind]))

# Tiempo de preparación de los grupos en máquinas (s_tki)
t_prep = datos_fsgsp[cols_fsgsp[33:37]].dropna()
t_prep_maq = []
t_preparacion_cm1 = []
for ind in t_prep.index:
    t_prep_maq.append(list(t_prep.iloc[ind]))
for maq in maquinas_cm1:
    t_preparacion_cm1.append(t_prep_maq)

# Datos para la celda de manufactura 2 (CM2):

# Número de grupos (g)
grupos_cm2 = list(datos_fsgsp["G_CM2"].dropna().astype(int))

# Trabajos en cada grupo (G_k)
trabajos_grupos_cm2 = []
trab_cont = 1
for gr in grupos_cm2:
    n_trab = int(datos_fsgsp["J_CM2"][gr - 1])
    trabs = list(range(trab_cont, trab_cont + n_trab))
    trabajos_grupos_cm2.append(trabs)
    trab_cont += n_trab

# Número de máquinas (m)
maquinas_cm2 = list(range(1, 9 + 1))

# Número de trabajos (N)
num_trabajos_cm2 = trabajos_grupos_cm2[-1][-1]

# Número de trabajos en grupo k (n_k)
num_trabajos_k_cm2 = list(datos_fsgsp["J_CM2"].dropna().astype(int))

# Tiempo de procesamiento de trabajos (P_ji)
t_proc = datos_fsgsp[cols_fsgsp[6:15]].dropna()
t_procesamiento_cm2 = []
for ind in t_proc.index:
    t_procesamiento_cm2.append(list(t_proc.iloc[ind]))

# Tiempo de preparación de los grupos en máquinas (s_tki)
t_prep = datos_fsgsp[cols_fsgsp[38:41]].dropna()
t_prep_maq = []
t_preparacion_cm2 = []
for ind in t_prep.index:
    t_prep_maq.append(list(t_prep.iloc[ind]))
for maq in maquinas_cm2:
    t_preparacion_cm2.append(t_prep_maq)

# Datos para la celda de manufactura 3 (CM3):

# Número de grupos (g)
grupos_cm3 = list(datos_fsgsp["G_CM3"].dropna().astype(int))

# Trabajos en cada grupo (G_k)
trabajos_grupos_cm3 = []
trab_cont = 1
for gr in grupos_cm3:
    n_trab = int(datos_fsgsp["J_CM3"][gr - 1])
    trabs = list(range(trab_cont, trab_cont + n_trab))
    trabajos_grupos_cm3.append(trabs)
    trab_cont += n_trab

# Número de máquinas (m)
maquinas_cm3 = list(range(1, 4 + 1))

# Número de trabajos (N)
num_trabajos_cm3 = trabajos_grupos_cm3[-1][-1]

# Número de trabajos en grupo k (n_k)
num_trabajos_k_cm3 = list(datos_fsgsp["J_CM3"].dropna().astype(int))

# Tiempo de procesamiento de trabajos (P_ji)
t_proc = datos_fsgsp[cols_fsgsp[16:20]].dropna()
t_procesamiento_cm3 = []
for ind in t_proc.index:
    t_procesamiento_cm3.append(list(t_proc.iloc[ind]))

# Tiempo de preparación de los grupos en máquinas (s_tki)
t_prep = datos_fsgsp[cols_fsgsp[42:]].dropna()
t_prep_maq = []
t_preparacion_cm3 = []
for ind in t_prep.index:
    t_prep_maq.append(list(t_prep.iloc[ind]))
for maq in maquinas_cm3:
    t_preparacion_cm3.append(t_prep_maq)


# Clases para determinar el problema de scheduling

# Clase GroupScheduling para el problema FSGSP: Celda de Manufactura 1
sched_cm1 = GroupScheduling(grupos=grupos_cm1, maquinas=maquinas_cm1,
                            num_trabajos=num_trabajos_cm1,
                            trabajos_grupos=trabajos_grupos_cm1,
                            num_trab_grupo=num_trabajos_k_cm1,
                            t_procesamiento=t_procesamiento_cm1,
                            t_preparacion=t_preparacion_cm1,
                            objetivo="makespan")

# Clase GroupScheduling para el problema FSGSP: Celda de Manufactura 2
sched_cm2 = GroupScheduling(grupos=grupos_cm2, maquinas=maquinas_cm2,
                            num_trabajos=num_trabajos_cm2,
                            trabajos_grupos=trabajos_grupos_cm2,
                            num_trab_grupo=num_trabajos_k_cm2,
                            t_procesamiento=t_procesamiento_cm2,
                            t_preparacion=t_preparacion_cm2,
                            objetivo="makespan")

# Clase GroupScheduling para el problema FSGSP: Celda de Manufactura 3
sched_cm3 = GroupScheduling(grupos=grupos_cm3, maquinas=maquinas_cm3,
                            num_trabajos=num_trabajos_cm3,
                            trabajos_grupos=trabajos_grupos_cm3,
                            num_trab_grupo=num_trabajos_k_cm3,
                            t_procesamiento=t_procesamiento_cm3,
                            t_preparacion=t_preparacion_cm3,
                            objetivo="makespan")

# Algoritmo genético para el FSGSP (conjunto de parámetros 3)
ga_fsgsp = AlgGeneticoSched(tam_poblacion=100, num_generaciones=300, tam_torneo=2,
                            prob_cruce=0.9, prob_mutacion=0.1)

# Optimización de FSGSP para el caso de estudio mediante GA:
# Minimizar el Tiempo de Terminación Total (TCT):

n_iteraciones = 1

# cm1_sched_sol = []
# cm2_sched_sol = []
# cm3_sched_sol = []

iter_cm1 = [0] * n_iteraciones
iter_cm2 = [0] * n_iteraciones
iter_cm3 = [0] * n_iteraciones

iteracion = 0
while iteracion < n_iteraciones:

    cmax_cm1 = [0] * ga_fsgsp.num_generaciones
    cmax_cm2 = [0] * ga_fsgsp.num_generaciones
    cmax_cm3 = [0] * ga_fsgsp.num_generaciones

    # Optimización de la secuenciación para las celdas de manufactura del caso de estudio

    # Celda de manufactura 1 (CM1)
    poblacion_cm1 = ga_fsgsp.poblacion_inicial(sched_cm1)
    best_cm1, best_ind_cm1 = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el FSGSP - CM1
    while gen < ga_fsgsp.num_generaciones:

        for q in range(int(ga_fsgsp.tam_poblacion / 2)):
            # Selección
            padres_cm1 = ga_fsgsp.seleccion(sched_cm1, poblacion_cm1)
            parents_cm1 = deepcopy(padres_cm1)

            # Cruce
            children_cm1 = ga_fsgsp.cruce(parents_cm1)

            # Mutación
            children_cm1 = ga_fsgsp.mutacion(children_cm1)

            # Sustitución
            poblacion_cm1 = ga_fsgsp.sustitucion(sched_cm1, poblacion_cm1, children_cm1)

        # Mejor FO e individuo
        best_cm1, best_ind_cm1 = ga_fsgsp.obtener_mejor(sched_cm1, poblacion_cm1)
        print("Group Scheduling - CM1 - Cmax:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardar mejores y el promedio de la generación
        if cmax_cm1[gen] == 0 or best_cm1 < cmax_cm1[gen]:
            cmax_cm1[gen] = best_cm1

        gen += 1

    # Guardar solución y resultados del GA para la CM1
    # cm1_sched_sol.append(best_ind_cm1)
    iter_cm1[iteracion] = cmax_cm1

    # Celda de manufactura 2 (CM2)
    poblacion_cm2 = ga_fsgsp.poblacion_inicial(sched_cm2)
    best_cm2, best_ind_cm2 = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el FSGSP - CM2
    while gen < ga_fsgsp.num_generaciones:

        for k in range(int(ga_fsgsp.tam_poblacion / 2)):
            # Selección
            padres_cm2 = ga_fsgsp.seleccion(sched_cm2, poblacion_cm2)
            parents_cm2 = deepcopy(padres_cm2)

            # Cruce
            children_cm2 = ga_fsgsp.cruce(parents_cm2)

            # Mutación
            children_cm2 = ga_fsgsp.mutacion(children_cm2)

            # Sustitución
            poblacion_cm2 = ga_fsgsp.sustitucion(sched_cm2, poblacion_cm2, children_cm2)

        # Mejor FO e individuo
        best_cm2, best_ind_cm2 = ga_fsgsp.obtener_mejor(sched_cm2, poblacion_cm2)
        print("Group Scheduling - CM2 - Cmax:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardar mejores y el promedio de la generación
        if cmax_cm2[gen] == 0 or best_cm2 < cmax_cm2[gen]:
            cmax_cm2[gen] = best_cm2

        gen += 1

    # Guardar solución y resultados del GA para la CM2
    # cm2_sched_sol.append(best_ind_cm2)
    iter_cm2[iteracion] = cmax_cm2

    # Celda de manufactura 3 (CM3)
    poblacion_cm3 = ga_fsgsp.poblacion_inicial(sched_cm3)
    best_cm3, best_ind_cm3 = 0, 0
    gen = 0

    # Inicio del algoritmo genético para el FSGSP - CM3
    while gen < ga_fsgsp.num_generaciones:

        for s in range(int(ga_fsgsp.tam_poblacion / 2)):
            # Selección
            padres_cm3 = ga_fsgsp.seleccion(sched_cm3, poblacion_cm3)
            parents_cm3 = deepcopy(padres_cm3)

            # Cruce
            children_cm3 = ga_fsgsp.cruce(parents_cm3)

            # Mutación
            children_cm3 = ga_fsgsp.mutacion(children_cm3)

            # Sustitución
            poblacion_cm3 = ga_fsgsp.sustitucion(sched_cm3, poblacion_cm3, children_cm3)

        # Mejor FO e individuo
        best_cm3, best_ind_cm3 = ga_fsgsp.obtener_mejor(sched_cm3, poblacion_cm3)
        print("Group Scheduling - CM3 - Cmax:\n Gen N°: {}, Iter: {}".format(gen, iteracion))

        # Guardar mejores y el promedio de la generación
        if cmax_cm3[gen] == 0 or best_cm3 < cmax_cm3[gen]:
            cmax_cm3[gen] = best_cm3

        gen += 1

    # Guardar solución y resultados del GA para la CM3
    # cm3_sched_sol.append(best_ind_cm3)
    iter_cm3[iteracion] = cmax_cm3

    iteracion += 1

# df = pd.DataFrame({'cm1_iter0': iter_cm1[0], 'cm2_iter0': iter_cm2[0], 'cm3_iter0': iter_cm3[0]})
# df.to_excel('results_cmax_iter0.xlsx')
df_cm1 = pd.DataFrame()
for it in range(n_iteraciones):
    df_cm1[f'iter_{it}'] = iter_cm1[it]

df_cm1.to_excel('results_cmax_cm1.xlsx')

df_cm2 = pd.DataFrame()
for it in range(n_iteraciones):
    df_cm2[f'iter_{it}'] = iter_cm2[it]

df_cm2.to_excel('results_cmax_cm2.xlsx')

df_cm3 = pd.DataFrame()
for it in range(n_iteraciones):
    df_cm3[f'iter_{it}'] = iter_cm3[it]

df_cm3.to_excel('results_cmax_cm3.xlsx')

# df = pd.DataFrame([cmax_cm1, cmax_cm2, cmax_cm3])

# df.to_excel("results_conf_cmax_2022.xlsx")

# df2 = pd.DataFrame([cm1_sched_sol, cm2_sched_sol, cm3_sched_sol])

# df2.to_excel("results_conf_sols_cmax_2022.xlsx")

# print(cmax_cm1, "\n", cmax_cm2, "\n", cmax_cm3)
