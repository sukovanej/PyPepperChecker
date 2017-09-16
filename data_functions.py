

def getOutputVector(output, output_size):
    """
    vrati vektor vystupu
    :param output: cislo v rozmezi 0 - (pocet druhy papircek)
    :return: vector vysledku
    """
    result = list()

    for i in range(output_size):
        if output == i:
            result.append(1)
        else:
            result.append(0)

    return result


def getInputVector(input):
    """
    vrati vektor vstupu
    :param input:
    :return:
    """
    result = list()

    for rgb in input:
        result.append(rgb[0])
        result.append(rgb[1])
        result.append(rgb[2])

    return result