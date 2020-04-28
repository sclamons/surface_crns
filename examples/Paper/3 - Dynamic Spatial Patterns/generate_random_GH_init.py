import random

def main():
    frac_A = 0.1
    frac_R = 0.1

    with open("GH_random_init.txt", 'w') as outfile:
        for row in range(64):
            for col in range(64):
                r = random.random()
                if r < frac_A:
                    state = "A"
                elif r < frac_A + frac_R:
                    state = "R"
                else:
                    state = "Q"
                outfile.write(state + " ")
            if row < 63:
                outfile.write("\n")

if __name__ == "__main__":
    main()