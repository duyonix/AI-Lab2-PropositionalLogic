from copy import deepcopy
import os

###   UTILITY SECTION   ###


def negative_literal(x):
    # sample: A -> -A and vice versa
    return x.replace("-", "") if "-" in x else "-" + x


def negative_alpha(alpha):
    clause = []

    # remove duplicates and sort literals by alphabet in alpha
    alpha = sorted(
        set(alpha),
        key=lambda literal: literal.replace("-", "") if "-" in literal else literal,
    )

    # Negative all literals in alpha and convert to 2D list
    for literal in alpha:
        clause.append([negative_literal(literal)])

    # sample:
    # alpha = ["A", "B", "-C"]
    # clause = [["-A"], ["-B"], ["C"]]
    return clause


def pl_resolve(clause_x, clause_y):
    resolvent = clause_x + clause_y

    # remove tautology clause
    # sample: resolvent has both A and -A
    for literal in resolvent:
        if negative_literal(literal) in resolvent:
            resolvent.remove(literal)
            resolvent.remove(negative_literal(literal))
            break

    # if still have tautology clause then return None
    # sample: resolvent = ["B", "-B", "C"], this mean B OR -B OR C = TRUE OR C = TRUE
    for literal in resolvent:
        if negative_literal(literal) in resolvent:
            return None

    # if nothing changed then return None
    if len(resolvent) == len(clause_x) + len(clause_y):
        return None

    # remove duplicates and sort literals by alphabet in clause
    resolvent = sorted(
        set(resolvent),
        key=lambda literal: literal.replace("-", "") if "-" in literal else literal,
    )

    return list(resolvent)


def resolve_clause(_kb):
    kb = deepcopy(_kb)
    new = []

    for clause_x in kb:
        # copy kb without clause_x
        clone = deepcopy(kb)
        clone.remove(clause_x)
        for clause_y in clone:
            # Apply pl_resolve for clause_x and clause_y
            resolvent = pl_resolve(clause_x, clause_y)

            # check condition for resolvent
            isNone = resolvent is None
            isInKB = None
            isInNew = None
            if not isNone:
                isInKB = resolvent in kb
                isInNew = resolvent in new

            # if ok then append to new clause else skip
            if (not isNone) and (not isInKB) and (not isInNew):
                new.extend([resolvent])

    return new


def pl_resolution(_kb, _alpha, result):
    kb = deepcopy(_kb)
    alpha = deepcopy(_alpha)

    # remove duplicates and sort literals by alphabet in each clause of KB
    kb = [
        sorted(
            set(clause),
            key=lambda literal: literal.replace("-", "") if "-" in literal else literal,
        )
        for clause in kb
    ]

    # Add negative alpha to KB
    clauses = kb + negative_alpha(alpha)

    while True:
        new = resolve_clause(clauses)

        # append number of clause in each loop to result
        result.append("{}".format(len(new)))

        # append new clause to result
        for literal in new:
            if literal == []:
                result.append("{}")
            else:
                result.append(" OR ".join(literal))

        # Check finish pl_resolution
        clauses.extend(new)

        # Success case
        if [] in clauses:
            result.append("YES")
            return True

        # Fail case
        if len(new) == 0:
            result.append("NO")
            return False


def read_input(filename):
    # Init variables
    alpha = []
    kb = []

    file = open(filename, "r")

    # Read alpha
    line = file.readline()
    clause = [literal.strip() for literal in line.split(" OR ")]
    alpha.extend(clause)

    # Read KB
    kb_count = int(file.readline())
    for _ in range(kb_count):
        line = file.readline()
        clause = [[literal.strip() for literal in line.split(" OR ")]]
        kb.extend(clause)

    file.close()

    # sample:
    # alpha = ["A", "B", "-C"]
    # kb = [["-A", "B"], ["-B", "D"], ["C", "-A"]]
    return alpha, kb


def write_output(filename, result):
    # sample result: ['3', '-A', 'B', '-C', '4', '-B OR C', 'A OR C', 'A OR -B', '{}', 'YES']
    file = open(filename, mode="w+", newline="\n")
    file.write("\n".join(result))
    file.close()


###     MAIN SECTION    ###

# Declare path for input and output
BASE_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = BASE_PATH + "/input"
OUTPUT_PATH = BASE_PATH + "/output"


def main():
    # loop for each test case in input folder
    for input_filename in os.listdir(INPUT_PATH):
        if input_filename.endswith(".txt"):
            # get data from input file
            input_file = INPUT_PATH + "/" + input_filename
            alpha, kb = read_input(input_file)

            # solve pl_resolution
            result = []
            pl_r = pl_resolution(kb, alpha, result)

            # write result to output file
            output_filename = input_filename.replace("input", "output")
            output_file = OUTPUT_PATH + "/" + output_filename
            write_output(output_file, result)

            # print result if kb entails alpha to console
            entail = "YES" if pl_r else "NO"
            print("Result for", input_filename, "->", output_filename, ":", entail)


if __name__ == "__main__":
    main()