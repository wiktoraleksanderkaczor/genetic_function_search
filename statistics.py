def normalize(value, minimum, maximum):
    try:
        normalized = (value - minimum) / (maximum - minimum)
    except:
        normalized = 1

    return normalized