import sys

def main():
    '''
    Converts a cellular automata state given in a file specified by the first
    argument into an emulation where each cell is replaced by a block defined
    in a file specified by the second argument. The result is printed to a
    file given by the third argument.

    The original automaton's states must be single characters. No spaces or
    commas.
    '''
    if len(sys.argv) < 4:
        raise ValueError("This program needs three arguments: 1) a file "
                    "containing automaton to emulate, 2) a file containing a"
                    " specification for an emulation cell, and 3) an output "
                    "location.")

    automaton_lines = []
    with open(sys.argv[1], 'r') as infile:
        for line in infile:
            automaton_lines.append(line.strip())

    init_state_lines = []
    with open(sys.argv[2], 'r') as statefile:
        for line in statefile:
            init_state_lines.append(line.strip())

    with open(sys.argv[3], 'w') as init_file:
        for row_num, state_row in enumerate(init_state_lines):
            for cell_row_num, cell_row in enumerate(automaton_lines):
                for i, state in enumerate(state_row):
                    write_string = cell_row.replace("?", state)
                    if i == len(state_row)-1:
                        write_string = write_string[:-1]
                    init_file.write(write_string)
                init_file.write("\n")

if __name__ == "__main__":
    main()