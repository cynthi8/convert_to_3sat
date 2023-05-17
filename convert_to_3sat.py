import os
import sys

def read_CNF(cnf_file_path):
    clauses = []
    with open(cnf_file_path, 'r') as file:
        for line in file:
            if line.startswith('c'):
                continue  # Skip comment lines
            elif line.startswith('p'):
                continue  # Skip problem line
            else:
                clause = [int(literal) for literal in line.strip().split()[:-1]]
                if clause:
                    clauses.append(clause)
    return clauses

def write_CNF(clauses, cnf_file_path):
    with open(cnf_file_path, 'w') as file:
        file.write(f"p cnf {largest_variable(clauses)} {len(clauses)}\n")
        for clause in clauses:
            literal_str = ' '.join(str(literal) for literal in clause)
            file.write(literal_str + ' 0\n')

def largest_variable(clauses):
    return max([abs(variable) for clause in clauses for variable in clause])

def split_clause(clause, new_glue_variable):
    if len(clause) <= 3:
        return clause, None
    
    clause3 = [clause[0], clause[1], new_glue_variable]
    clause_rest = [-new_glue_variable] + clause[2:]
    return clause3, clause_rest

def expand_clause(clause):
    while len(clause) < 3:
        clause.append(clause[0])
    return clause
    
def convert_clauses_to_3sat(clauses):
    final_clauses = []

    largest_var = largest_variable(clauses)
    free_var = largest_var + 1

    for clause in clauses:
        clause_left, clause_right = split_clause(clause, free_var)
        final_clauses.append(expand_clause(clause_left))
        while clause_right:
            free_var += 1
            clause_left, clause_right = split_clause(clause_right, free_var)
            final_clauses.append(expand_clause(clause_left))

    return final_clauses

def convert_to_3sat(cnf_file_path):
    clauses = read_CNF(cnf_file_path)
    new_clauses = convert_clauses_to_3sat(clauses)
    output_file_path = os.path.splitext(cnf_file_path)[0] + "_3sat.cnf"
    write_CNF(new_clauses, output_file_path) 

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        convert_to_3sat(sys.argv[1])
    else:
        convert_to_3sat("test.cnf")
