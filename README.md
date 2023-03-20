## Genetic algorithm for the Flow-Shop Group Scheduling Problem (FSGSP)

Contains the following files:

* `group_scheduling.py`: Contains the class for defining the FSGSP. It contains the following methods:
  - Decoding schedule
  - Compute fitness function
  - Compute makespan, total completion time of jobs
  - Build and optimize MILP formulation using `PuLP`
  
* `algGeneticoSched.py`: Contains the class that defines the operators for the Genetic Algorithm (GA) to be applied to the FSGSP.

* `fsgsp_confeccion_cmax.py`: Contains the application of the GA for the FSGSP through the case study for the garment industry.
