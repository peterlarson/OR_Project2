'''
Project 2. 

By: Peter Larson and Abhimayu Yadav
'''


#Here we open the data file to use. 
file = open("data7.dat", 'r')
line1 = file.readline()
N,R,C = line1.split(" ")

#Line1 contained the number of ports, and the rows and columns of the ship. 
N,R,C = int(N), int(R), int(C)

#This matrix, the transportation matrix, stores the data for how much must be shipped between ports in a way that easily accessible. 
#Matrix format is: tMatrix[sourcePort][destinationPort] = quantity 
tMatrix = []

#cMatrix is the Cargo Matrix storing the state of the ship as it travels between virtual ports. 
#Matrix is [Row][Column]
cMatrix = []

#Here we populate the transportation matrix with 0's
for port in range(N):
    tMatrix.append([0]*N)

#Here we populate the transportation matrix with data from the file. 
for line in file:
    source, destination, quantity = [int(i) for i in line.split(" ")]
    tMatrix[source-1][destination-1] = quantity

#Here we populate the cargo matrix. 
for i in range(R):
    cMatrix.append([0]*C)



#This function unloads the cargo from the ship at a given port. 
#It returns a list of the additional containers that needed to be removed in order to get everything out 
#for the current port. 
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


#This function loads the cargo (a list of destinations) in the manner described in our report. 
#First the cargo is sorted by destination, and then the ship is loaded from bottom to top with cargo for far destinations before
#cargo for near destinations.
def load_cargo(cargo_matrix, cargo):
    sorted_cargo = sorted(cargo)
    for row in range(R-1, -1, -1):
        for column in range(C):
            if(len(sorted_cargo) > 0 and cargo_matrix[row][column] == 0):
                cargo_matrix[row][column] = sorted_cargo.pop()


#This function takes the transportation matrix and a port number and returns a list of all the cargo to be put on the ship from that port. 
def get_new_cargo(transportation_matrix, port):
    t_row = transportation_matrix[port-1]
    new_cargo = []
    for dest_port in range(len(t_row)):
        amount = t_row[dest_port]
        for i in range(amount):
            new_cargo.append(dest_port+1)
    return new_cargo


#This is where the brunt of the logic takes place. 

#This variable keeps track of how many containers needed to be removed and replaced on the ship. 
extra_removals = 0

#This is the initial cargo to be loaded. 
cargo = get_new_cargo(tMatrix, 1)

#This loads the initial cargo on the ship. 
load_cargo(cMatrix, cargo)

#Loop over intermediate ports. 
for port in range(2, N):
    #print(cMatrix)
    #extra holds the cargo that needed to be removed to get the cargo out for this port. 
    #The extra cargo must be put back on the ship. 
    extra = unload_cargo(cMatrix, port)

    #We count how many pieces of cargo had to be removed. 
    extra_removals = extra_removals + len(extra)

    #The new cargo from this port. 
    cargo = get_new_cargo(tMatrix, port)

    #This loads the cargo on the ship. 
    load_cargo(cMatrix, cargo + extra)


#Missing at the end here is a final removal from the ship. At this point the ship will have only cargo for the last destination. 
#The final removal will not change the number of extra removals, so we do not do it. 

#print(cMatrix)
print(extra_removals)
