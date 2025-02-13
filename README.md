# Pareto Optimality Calculator

A Python tool for finding Pareto optimal solutions from a set of multi-dimensional data points. This tool helps identify solutions where no improvement can be made to one dimension without making another dimension worse off.

For more information about Pareto efficiency, visit the [Wikipedia page on Pareto efficiency](https://en.wikipedia.org/wiki/Pareto_efficiency).

## Overview

The calculator takes a CSV file containing multi-dimensional data points and identifies the Pareto optimal solutions among them. A solution is considered Pareto optimal when there exists no other solution that improves at least one dimension without making any other dimension worse.

## Usage

```bash
python pareto.py input_file.csv [-v]
```

### Arguments:
- `input_file.csv`: Path to the input CSV file containing the data points
- `-v, --verbose`: (Optional) Enable verbose debug output

### Input File Format
The input file should be a CSV file where:
- Each line represents one solution
- Values within each line are comma-separated
- All values should be numeric
- Each column represents a dimension to be optimized

### Example: Prisoners' Dilemma

Consider the classic prisoners' dilemma where two suspects are being interrogated separately. Each value pair represents the years in prison for Prisoner A and Prisoner B respectively. Negative numbers represent years in prison (the higher/less negative the better).

Input file `prisoners.csv`:
```
-1,-1    # Both remain silent
-5,0     # A silent, B betrays
0,-5     # A betrays, B silent
-2,-2    # Both betray
```

Running the command:
```bash
python pareto.py prisoners.csv
```

Will output the Pareto optimal solutions from this dataset. In this case, it will identify which outcomes are such that neither prisoner could improve their situation without making the other's worse.

To see detailed comparison information during processing, use the verbose flag:
```bash
python pareto.py prisoners.csv -v
```

## Notes
- The tool assumes higher values are better in all dimensions (in the prisoners' example, less negative numbers are "better" outcomes)
- All values are treated as integers during comparison
- Duplicate solutions are handled appropriately 