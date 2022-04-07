import itertools

possibleAssignments = list(itertools.permutations('123456789', 3))
varAsgn = []
for assignment in possibleAssignments:
    if sum(int(x) for x in assignment) == 6:
        varAsgn.append(''.join(assignment))
        
print(varAsgn)
