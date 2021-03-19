def main():
    '''
    Converts a game of life state given in gol_state.txt (0s and 1s) into a
    surface CRN logic circuit game of life emulation state, saved in 
    big_GoL_init.txt.
    '''
    gol_lines = []
    with open("GoL_one_site.txt", 'r') as infile:
        for line in infile:
            gol_lines.append(line.strip())

    init_state_lines = []
    with open("gol_state.txt", 'r') as statefile:
        for line in statefile:
            init_state_lines.append(line.strip())

    with open("big_GoL_init.txt", 'w') as init_file:
        for row_num, state_row in enumerate(init_state_lines):
            for cell_row_num, cell_row in enumerate(gol_lines):
                for i, state in enumerate(state_row):
                    write_string = cell_row.replace("?", state)
                    if i == len(state_row)-1:
                        write_string = write_string[:-1]
                    init_file.write(write_string)
                init_file.write("\n")

if __name__ == "__main__":
    main()