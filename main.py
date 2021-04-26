
from deap import creator, base, tools, algorithms, gp
import multiprocessing
import numpy

from config import \
    INPUTS, \
    OUTPUTS, \
    MAX_EXPR_ELEMENTS, \
    MAX_GENERATIONS, \
    MAX_POPULATION, \
    CONSTANTS, \
    FUNCTIONS, \
    validate


def main():
    # Define the function
    INPUT_KEYS = list(INPUTS[0].keys())
    pset = gp.PrimitiveSet("main", len(INPUT_KEYS))
    
    # Setting for code generation
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)
    
    # Rename arguments
    for num, name in zip(range(len(INPUT_KEYS)), INPUT_KEYS):
        exec("pset.renameArguments(ARG{}='{}')".format(num, name))

    for name, val in CONSTANTS.items():
        pset.addTerminal(val, name=name)

    # Get num args per function and add to set.
    from functions import num_args_for_function
    function_and_num_args = num_args_for_function(FUNCTIONS)
    for name, func, num_args in function_and_num_args:
        pset.addPrimitive(func, num_args)

    # Define model by registering functions.
    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genGrow, pset, min_=1, max_=MAX_EXPR_ELEMENTS)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    """
    Then, we decorate the mate and mutate method to limit the height of generated individuals. 
    This is done to avoid an important draw back of genetic programming : bloat. Koza in his book 
    on genetic programming suggest to use a max depth of 17.
    """
    from operator import attrgetter
    toolbox.decorate("mate", gp.staticLimit(key=attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=attrgetter("height"), max_value=17))

    def EVALUATE(individual, max_complexity):
        num_parts = len(individual)
        func = toolbox.compile(expr=individual)
        total = []
        for arguments, actual in zip(INPUTS, OUTPUTS):
            #arg = list(arguments.values())
            error = 0
            try:
                predicted = func(**arguments)
            except:
                predicted = None
                error = 1
            
            if predicted:
                error = validate(predicted, actual, OUTPUTS)
            else:
                error = 1

            total.append(error)

        # If working model;
        if error == 0:
            # If smallest ever;
            if num_parts > max_complexity:
                total.append(1)
            else:
                exec("")
                #print("WORKING MODEL")

        # Scale by number of errors calculated, zero to one only.
        total = sum(total) / len(total)
        return tuple([total])

    toolbox.register("evaluate", EVALUATE, max_complexity=MAX_EXPR_ELEMENTS)

    # Set up statistics tracking
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    # Concurrency
    """
    from pathos.pools import ProcessPool
    pool = ProcessPool(nodes=24)
    toolbox.register("map", pool.imap)
    """
    from multiprocessing.pool import ThreadPool as Pool
    pool = Pool(4)
    toolbox.register("map", pool.imap)


    # Launch evaluation
    pop = toolbox.population(n=MAX_POPULATION)
    hof = tools.HallOfFame(1)
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, MAX_GENERATIONS, 
                                   halloffame=hof, verbose=True, stats=mstats)

    # Select the top one best program after finishing.
    top1 = tools.selBest(pop, k=1)
    
    # Show graph
    from graph import graph_expr
    graph_expr(top1[0])
    exit(0)

if __name__ == "__main__":
    main()