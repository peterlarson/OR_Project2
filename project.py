file = open("data7.dat", 'r')
line1 = file.readline()
N,R,C = line1.split(" ")
N,R,C = int(N), int(R), int(C)
tMatrix = []

for port in range(N):
    tMatrix.append([0]*N)

for line in file:
    source, destination, quantity = [int(i) for i in line.split(" ")]
    tMatrix[source-1][destination-1] = quantity

cMatrix = []
for i in range(R):
    cMatrix.append([0]*C)

#Matrix is [Row][Column]

def unload_cargo(cargo_matrix, port_number):
    removed_cargo = []
    for column in range(C):
        removing = False
        for row in range(R-1,-1,-1):
            if(cargo_matrix[row][column] == port_number):
                removing = True
                cargo_matrix[row][column] = 0
            elif(removing and not cargo_matrix[row][column] == 0):
                removed_cargo.append(cargo_matrix[row][column])
                cargo_matrix[row][column] = 0

    return removed_cargo

def load_cargo(cargo_matrix, cargo):
    sorted_cargo = sorted(cargo)
    for row in range(R-1, -1, -1):
        for column in range(C):
            if(len(sorted_cargo) > 0 and cargo_matrix[row][column] == 0):
                cargo_matrix[row][column] = sorted_cargo.pop()

def get_new_cargo(transportation_matrix, port):
    t_row = transportation_matrix[port-1]
    new_cargo = []
    for dest_port in range(len(t_row)):
        amount = t_row[dest_port]
        for i in range(amount):
            new_cargo.append(dest_port+1)
    return new_cargo


extra_removals = 0
cargo = get_new_cargo(tMatrix, 1)
load_cargo(cMatrix, cargo)
for port in range(2, N):
    #print(cMatrix)
    extra = unload_cargo(cMatrix, port)
    extra_removals = extra_removals + len(extra)
    cargo = get_new_cargo(tMatrix, port)
    load_cargo(cMatrix, cargo + extra)

#print(cMatrix)
#print(extra_removals)
