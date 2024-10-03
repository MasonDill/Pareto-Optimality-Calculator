import sys
import logging

def find_pareto(data, verbose=False):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level)
    
    optimal_solutions = data.copy()
    for dataum in data:
        for other_dataum in data:
            if dataum == other_dataum:
                continue

            not_optimal = True
            logging.info("Comparing " + str(dataum) + " to " + str(other_dataum))

            for dim in range(len(dataum)):
                if int(dataum[dim]) < int(other_dataum[dim]):
                    logging.info("since " + str(dataum[dim]) + " < " + str(other_dataum[dim]) + " at index " + str(dim + 1) + " of " + str(dataum) + " is not a pareto improvement\n")
                    not_optimal = False                    
                    break

            if not_optimal:
                logging.info("it is a pareto improvement, we can remove" + str(other_dataum) +"\n")
                try:
                    optimal_solutions.remove(other_dataum)
                except:
                    pass # already removed

    return optimal_solutions
            

def read_file(file_name):
    data = []
    with open(file_name, 'r') as file:
        lines = file.readlines()

        for line in lines:
            values = line.strip().split(',')
            data.append(values)
    return data

if __name__ == "__main__":
    data = read_file(sys.argv[1])
    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    solutions = find_pareto(data, verbose)
    print("SOLUTIONS:")
    for solution in solutions:
        print("\t", solution)
    print()