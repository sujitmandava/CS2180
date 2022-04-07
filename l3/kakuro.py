import imp
from pickletools import read_unicodestring1
import queue
import sys
import copy
import itertools
from time import time


def createMatrix(rows, columns):
    mat = [[0]*columns]*rows
    return mat


class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.currentDomains = {variable: list(self.domains[variable]) for variable in self.variables}

    def conflicts(self, variable, value, assignment):
        # Returns number of conflicts
        number = 0
        for var in assignment:
            if self.constraints(variable, value, var, assignment[var]) == False:
                number += 1
        return number
    
    def conflict(self, var1, val1, var2, val2): #BW TWO VARS
        if self.constraints(var1, val1, var2, val2) == False:
            return False
        return True

    def assignVar(self, variable, value, assignment):
        assignment[variable] = value

    def removeVar(self, var, assignment):
        del assignment[var]

    # Keeps track of list of integers from domain that are deleted i.e, keeps track of assuumption
    def btassumption(self, var, value):
        domainDeletions = [(var, t) for t in self.currentDomains[var] if t != value]
        # print(domainDeletions)
        self.currentDomains[var] = [value]  # Assumption
        # print(self.currentDomains[var])
        return domainDeletions

    def restoreAssumption(self, deletions):
        for var, value in deletions:
            # if var not in self.currentDomains:
                # self.currentDomains[var] = []
            self.currentDomains[var].append(value)

    def displayAssignemt(self, assignment):
        print(assignment)

    def domainValues(self, var):
        return self.currentDomains[var]

    # Selects unassigned variable in the current assignment of the CSP
    def newVariable(self, assignment):
        uVar = [var for var in self.variables if var not in assignment]
        # print(uVar[0])
        return uVar[0]

    def goalTest(self, assignment):
        if len(assignment) == len(self.variables) and all(self.conflicts(var, assignment[var], assignment) == 0 for var in self.variables):
            return True
        return False
    
    def allArcs(self):
        allArcs = []
        for var in self.variables:
            # print(d1,d2)
            if var[0] == 'V':
                for nei in self.neighbors[var]:
                    # print(var, nei)
                    allArcs.append((var, nei))
                # allArcs.append((var, (nei for nei in self.neighbors[var])))
        return allArcs


class Kakuro(CSP):
    def __init__(self, puzzleH, puzzleV):
        rows = len(puzzleH)
        columns = len(puzzleH[0])

        tph = copy.deepcopy(puzzleH)
        tpv = copy.deepcopy(puzzleV)

        # Converting into one matrix
        for i in range(rows):
            for j in range(columns):
                if tph[i][j] != tpv[i][j] or tph[i][j] != '0':
                    newElement = list()
                    newElement.append(tph[i][j])
                    newElement.append(tpv[i][j])
                    tph[i][j] = newElement

        self.puzzleValues = copy.deepcopy(tph)  # tph has the combined matrix

        puzzleVariables = createMatrix(rows, columns)
        blanks = []
        constraintInfo = []
        variables = []
        variableDomains = {}
        variableNeighbors = {}

        # Defining variables, blank cells('#')
        for i in range(rows):
            for j in range(columns):
                v = 'V'+str(i)+","+str(j)
                puzzleVariables[i][j] = 'V'+str(i)+","+str(j)

                if tph[i][j] == '0':  # Variables
                    self.puzzleValues[i][j] = 0
                    variables.append(v)
                    variableDomains[v] = list(range(1,10))
                    variableNeighbors[v] = []

                elif tph[i][j] == "#":  # Blank Cells
                    blanks.append('B'+str(i)+","+str(j))

                else:  # Sum right and sum down in a list element; At least one has a value
                    # print(tph[i][j])
                    constraintInfo.append((tph[i][j]))

        self.rows = rows
        self.columms = columns
        self.variables = variables
        self.blanks = blanks
        self.constraintInfo = constraintInfo

        # Defining constraits by creating row and column constraints
        for i in range(rows):
            for j in range(columns):
                if tph[i][j] in constraintInfo:     
                # Horizontal sum constraint present // Defined such that sum is sum of cells to the right
                    if tph[i][j][0] != "#":
                        # Hidden variable for right side sum
                        hv = "CR"+str(i)+","+str(j)
                        variables.append(hv)

                        cells = 0  # Number of cells in the row sums
                        for t in range(j+1, columns):
                            # Discontinuity; Cells after this do not participate in constraint
                            if tph[i][t] != "0":
                                break

                            cells += 1
                            currentVar = 'V'+str(i)+","+str(t)

                            # Add hv and currentVar to each others neighbors according to constraint
                            if hv not in variableNeighbors:
                                variableNeighbors[hv] = []
                            variableNeighbors[hv].append(currentVar)

                            if currentVar not in variableNeighbors:
                                variableNeighbors[currentVar] = []
                            variableNeighbors[currentVar].append(hv)

                            # Domain is all the permutations of numbers such that sum is the given value and no number is repeated
                        possibleAssignments = list(itertools.permutations('123456789', cells))
                        for assignment in possibleAssignments:
                            if sum(int(x) for x in assignment) == int(tph[i][j][0]):
                                if hv not in variableDomains:
                                    variableDomains[hv] = []
                                variableDomains[hv].append(assignment)

                    # Repeated for vertical/Downward sum
                    if tph[i][j][1] != "#":  # Vertical sum
                        hv = "CD"+str(i)+","+str(j)
                        variables.append(hv)
                        cells = 0
                        for t in range(i+1, rows):
                            if tph[t][j] != "0":
                                break
                            
                            cells += 1
                            currentVar = 'V'+str(t) + ","+str(j)

                            if hv not in variableNeighbors:
                                variableNeighbors[hv] = []
                            variableNeighbors[hv].append(currentVar)

                            if currentVar not in variableNeighbors:
                                variableNeighbors[currentVar] = []
                            variableNeighbors[currentVar].append(hv)

                        possibleAssignments = list(itertools.permutations('123456789', cells))
                        for assignment in possibleAssignments:
                            if sum(int(x) for x in assignment) == int(tph[i][j][1]):
                                if hv not in variableDomains:
                                    variableDomains[hv] = []
                                variableDomains[hv].append(assignment)

        self.variableDomains = variableDomains
        self.variableNeighbors = variableNeighbors

        super().__init__(variables, variableDomains, variableNeighbors, self.constraint)

    ''' 
    Function to decode constraints using previously generated data. A, B are of three types: Cell, Row sum or Column sum.
    Returns true if value of a particular cell in row/column sum and the given value of the cell is the same (if one is cell and other is row/column sum) (Satisfied)
    Returns false otherwise
    '''

    def constraint(self, A, a, B, b):
        if A[0] == "V" and B[0] == "C": 
            if A not in self.variableNeighbors[B]:
                return True
            Vi = int(A[1:A.index(",")])
            Vj = int(A[A.index(",") + 1:])

            Ci = int(B[2:B.index(",")])
            Cj = int(B[B.index(",") + 1:])

            if B[1] == 'R':
                index = Vj - Cj - 1
                if int(b[index]) == a:
                    return True
            else:
                index = Vi - Ci - 1
                if int(b[index]) == a:
                    return True
                
        elif B[0] == "V" and A[0] == "C":
            if B not in self.variableNeighbors[A]:
                return True
            Vi = int(B[1:B.index(",")])
            Vj = int(B[B.index(",") + 1:])

            Ci = int(A[2:A.index(",")])
            Cj = int(A[A.index(",") + 1:])
            # print('here')
            if A[1] == 'R':
                index = Vj - Cj - 1
                # print(index)
                # print(B,A)
                if int(a[index]) == b:
                    return True
            else:
                index = Vi - Ci - 1
                if int(a[index]) == b:
                    return True
        return False

# Define AC3 and BS algorithms
def AC3v2(csp: CSP, q=None):
    # for t in range(4):
    if q is None:
        q = {(var, nei) for var in csp.variables for nei in csp.neighbors[var]}
    checks = 0
    while q:
        (var, nei) = q.pop()
        revised, checks = revisev2(csp, var, nei, checks)
        if revised:
            if not csp.currentDomains[var]:
                return False, checks
            for nei2 in csp.neighbors[var]:
                if nei2[0] == 'V':
                    q.add((nei2,var))
                else:
                    q.add((var,nei2))
    return True, checks
            
def revisev2(csp: CSP, var1, var2, checks):
    revised = False
    cdom1 = copy.deepcopy(csp.currentDomains[var1])
    cdom2 = copy.deepcopy(csp.currentDomains[var2])
    
    for d1 in cdom1:
        valPresent = False
        for d2 in cdom2:
            if csp.conflict(var1, d1, var2,d2):
                valPresent = True
            checks+=1
            if valPresent:
                break
        if not valPresent:
            csp.currentDomains[var1].remove(d1)
            revised = True      
    return revised, checks

# def backtracking_search(csp: CSP):
#     def backtrack(assignment):
#         if len(assignment) == len(csp.variables):
#             return assignment
        
#         var = csp.newVariable(assignment)
#         for value in csp.currentDomains[var]:
#             if csp.conflicts(var,value,assignment) == 0:
#                 csp.assignVar(var, value, assignment)
#                 result = backtrack(assignment)
#                 if result is not None:
#                     return result
#                 csp.removeVar(var, assignment)
                    
#     result = backtrack({})
#     assert result is None or csp.goalTest(result)
#     return result

# def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
#                         order_domain_values=unordered_domain_values, inference=no_inference):
#     """[Figure 6.5]"""

#     def backtrack(assignment):
#         if len(assignment) == len(csp.variables):
#             return assignment
#         var = select_unassigned_variable(assignment, csp)
#         for value in order_domain_values(var, assignment, csp):
#             if 0 == csp.nconflicts(var, value, assignment):
#                 csp.assign(var, value, assignment)
#                 removals = csp.suppose(var, value)
#                 if inference(csp, var, value, assignment, removals):
#                     result = backtrack(assignment)
#                     if result is not None:
#                         return result
#                 csp.restore(removals)
#         csp.unassign(var, assignment)
#         return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result


if __name__ == '__main__':
    argList = sys.argv
    if len(argList) != 3:
        print("Invalid execution (Format = python3 kakuro.py <input file> <output file>)\n")

    fin = open(argList[1], 'r')
    fout = open(argList[2], 'w')

    L = fin.readlines()

    count = 0
    rows = 0
    columns = 0
    i = j = 0

    for line in L:
        if count == 0:
            count += 1
            rows = int(line[line.index('=') + 1:line.index('\n')])
            fout.write(str(rows) + " ")
        elif count == 1:
            count += 1
            columns = int(line[line.index('=') + 1:line.index('\n')])
            fout.write(str(columns))
        else:
            break

    matH = createMatrix(rows, columns)
    matV = createMatrix(rows, columns)

    for i in range(rows):
        L[3+i] = L[3+i].replace("\n", "")
        L[4+rows+i] = L[4+rows+i].replace("\n", "")
        matH[i] = L[3+i].split(",")
        matV[i] = L[4+rows+i].split(",")

    tph = copy.deepcopy(matH)
    tpv = copy.deepcopy(matV)

    KakuroProblem = Kakuro(tph, tpv)
    q = None
    # AC3
    for i in range(4):
        AC3v2(KakuroProblem, q)
    print(KakuroProblem.currentDomains)
    # Backtracking Search
    initTime = time()
    # btResult = backtracking_search(KakuroProblem)
    finalTime = time() - initTime
    # print(btResult)
    print(finalTime)
    
    fin.close()
    fout.close()
