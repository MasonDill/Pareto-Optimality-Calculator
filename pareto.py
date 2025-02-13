import sys
import logging
import argparse as ap

def find_pareto(data, verbose=False):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')
    
    optimal_solutions = data.copy()
    for dataum in data:
        logging.info("\nAnalyzing outcome: %s", str(dataum))
        logging.info("-" * 40)
        
        for other_dataum in data:
            if dataum == other_dataum:
                continue

            not_optimal = True
            logging.info("  Comparing with: %s", str(other_dataum))

            for dim in range(len(dataum)):
                if int(dataum[dim]) < int(other_dataum[dim]):
                    logging.info("    ❌ Not a Pareto improvement: %s < %s at position %d", 
                               str(dataum[dim]), str(other_dataum[dim]), dim + 1)
                    not_optimal = False                    
                    break

            if not_optimal:
                logging.info("    ✓ Found Pareto improvement - removing %s", str(other_dataum))
                try:
                    optimal_solutions.remove(other_dataum)
                except:
                    pass # already removed
            logging.info("")

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
    parser = ap.ArgumentParser(description='Find Pareto optimal solutions from a CSV file.')
    parser.add_argument('input_file', help='Input CSV file containing the data')
    parser.add_argument('-v', '--verbose', action='store_true', 
                      help='Enable verbose debug output')
    
    args = parser.parse_args()
    
    data = read_file(args.input_file)
    solutions = find_pareto(data, args.verbose)
    
    print("SOLUTIONS:")
    for solution in solutions:
        print("\t", solution)
    print()