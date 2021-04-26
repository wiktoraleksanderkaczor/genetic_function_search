def f(a, b, c):
    return (b + c * a) * a 

# List of dicts with each dict containing named arguments.
INPUTS = [{"a": a, "b": b, "c": c} for a, b, c in zip(list(range(30)), list(range(30, 60)), list(range(60, 90)))]
OUTPUTS = [f(**item) for item in INPUTS]

MAX_EXPR_ELEMENTS = 30
MAX_GENERATIONS = 500
MAX_POPULATION = 150
CONSTANTS = {} #{"PI": 3.14} # Ephemeral constant, evaluated at call time, name to value
from operator import truediv, mul, add, sub
FUNCTIONS = [truediv, mul, add, sub]

# Between 1 and 0
# For all inputs to all outputs
from statistics import normalize
def validate(predicted, actual, OUTPUTS):
    worst = max(OUTPUTS)
    return normalize(value=abs(predicted - actual), minimum=0, maximum=worst)
