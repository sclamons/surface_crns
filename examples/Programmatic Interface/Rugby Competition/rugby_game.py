from surface_crns import SurfaceCRNQueueSimulator
import sys, os

def main():
    if len(sys.argv) < 3:
        sys.exit("rugby_game.py requires two rugby strategy files as inputs.")

    team_filenames  = [sys.argv[1], sys.argv[2]]
    team_names      = [filename.split(os.path.sep)[-1].split(".")[0] \
                        for filename in team_filenames]
    team_strategies = []

    for filename in team_filenames:
        with open(filename, 'r') as team_file:
            strat = "".join(team_file)
            team_strategies.append(strat)

    team_strategies[1] = team_strategies[1].replace("X", "Y")

    man_filename = os.path.join("temp", "_".join(team_names) + "_manifest.txt")

    with open("templated_rugby_manifest.txt", 'r') as manifest_template:
        with open(man_filename, 'w') as manifest_file:
            for line in manifest_template:
                # Add in team strategy
                if line.startswith("!INCLUDE temp/strategy_insert.txt"):
                    for strat in team_strategies:
                        manifest_file.write(strat)
                # Substitute team names for "X" and "Y" in colormap
                elif line.startswith("{X") or line.startswith("{Y"):
                    team_id = line[1]
                    team_name = team_names[0 if team_id=="X" else 1]
                    line = "{" + team_name + line[2:]
                    manifest_file.write(line)
                else:
                    manifest_file.write(line)

    SurfaceCRNQueueSimulator.simulate_surface_crn(man_filename)

if __name__ == "__main__":
    main()