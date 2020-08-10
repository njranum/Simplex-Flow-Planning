''' Nicholas Ranum
    This program generates and runs a CPLEX linear problem file for a load
    balancing problem on transit nodes between a series of source and
    destination nodes.
'''


import subprocess
import sys

def demand(sources,transit,dests):
 ''' Create demand constraints for the demand between each source and dest node '''
     demandLines = []
     for i in range(sources):
         i += 1
         for j in range(dests):
             j += 1
             line = ""
             for k in range(transit):
                 k += 1
                 line += "x{}{}{} + ".format(i,k,j)
             line = line[0:-3]
             line += " = {}".format(i+j)
             demandLines.append(line)
     return demandLines

def capacity(sources,transit,dests):
     ''' Creade capacity constraints for the capacity of each source-transit and
     each transit-dest node '''
     capacityLines = []
     y = 1
     # Linj capacities for source -> transit links
     for i in range(sources):
         i += 1
         for k in range(transit):
             k +=1
             line = ""
             for j in range(dests):
                 j += 1
                 line += "x{}{}{} + ".format(i,k,j)
             line = line[0:-3]
             line += " - c{}{} = 0".format(i,k)
             capacityLines.append(line)
             y += 1
     # Link capacities for transit -> destination links
     for k in range(transit):
         k += 1
         for j in range(dests):
             j +=1
             line = ""
             for i in range(sources):
                 i += 1
                 line += "x{}{}{} + ".format(i,k,j)
            line = line[0:-3]
            line += " - d{}{} = 0".format(k,j)
            capacityLines.append(line)
            y += 1
    return capacityLines

def bounds(sources,transit,dests):
 ''' Generates bounds for all demand volumes and auxiliary variable r '''
     boundLines = []
     boundLines.append("\nBounds")
     for i in range(sources):
         i += 1
         for k in range(transit):
             k += 1
             boundLines.append("c{}{} >= 0".format(i,k))
     for k in range(transit):
         k += 1
         for j in range(dests):
             j += 1
             boundLines.append("d{}{} >= 0".format(k,j))
     for i in range(sources):
         i += 1
         for k in range(transit):
             k += 1
             for j in range(dests):
                    j += 1
                    boundLines.append("0 <= x{}{}{}".format(i,k,j))
     boundLines.append("0 <= r")
     return boundLines

def splitLimit(sources,transit,dests,splits):
     ''' Constrains the binary variable to be the number of demand volume splits '''
     splitLines = []
     splitLines.append("")
     for i in range(sources):
         i += 1
         for j in range(dests):
             j += 1
             line = ""
             for k in range(transit):
                 k += 1
                 line += "u{}{}{} + ".format(i,k,j)
             line = line[0:-3]
             line += " = {}".format(splits)
             splitLines.append(line)
     return splitLines

def binary(sources,transit,dests):
     ''' Bounds each of the integer based decision variables to a 1 or 0 '''
     binaryLines = []
     binaryLines.append("\nBIN")
     for i in range(sources):
         i += 1
         for k in range(transit):
             k += 1
             for j in range(dests):
                j += 1
                 binaryLines.append("u{}{}{}".format(i,k,j))
     return binaryLines

     def halfFlow(sources,transit,dests):
         ''' Constrains a path to take half of the demand volume if it takes any at all '''
         halfLines = []
         halfLines.append("")
         for i in range(sources):
             i += 1
             for k in range(transit):
                 k += 1
                 for j in range(dests):
                     j += 1
                     halfLines.append("2 x{}{}{} - {} u{}{}{} = 0".format(i,k,j,i+j,i,k,j))
         return halfLines

def auxiliary(sources,transit,dests):
     ''' Introduces auxiliary variable r representing the value of the objective
     function. '''
     auxLines = []
     for k in range(transit):
         k += 1
         line = ""
         for i in range(sources):
             i += 1
             for j in range(dests):
                 j += 1
                 line += "x{}{}{} + ".format(i,k,j)
         line = line[0:-3]
         line += " -r <= 0"
         auxLines.append(line)
     return auxLines

def main():
 # Number of sources, destinations and transit nodes
 sources = int(sys.argv[1])
 transit = int(sys.argv[2])
 dests = int(sys.argv[3])
 splits = 2 # amount of paths the demand volume can take

 lines = []
 file_ = open("flow.lp","w

 # Adds objective function to the lp file
 lines.append("Minimize\nr")
 lines.append("Subject to

 # Generates and adds the demand constraints to the lp file list
 lines.append("\nDemand:")
 demandLines = demand(sources,transit,dests)
 for line in demandLines:
     lines.append(line

 # Generates and adds the capacity constraints to the lp file list
 lines.append("\nCapacity:")
 capacityLines = capacity(sources,transit,dests) # Link capacity constraints
 for line in capacityLines:
     lines.append(line

 # Generates and adds the binary value constraints to the lp file list
 splitLines = splitLimit(sources,transit,dests,splits)
 for line in splitLines:
     lines.append(line

 # Generates and adds constraint for a demand flow to take half of the
 # demand volume to the lp file list
 halfLines = halfFlow(sources,transit,dests)
 for line in halfLines:
     lines.append(line

 # Generates and adds the auxiliary file constraints to the lp file list
 auxLines = auxiliary(sources,transit,dests)
 for line in auxLines:
     lines.append(line

 # Generates and adds the bounds to the lp file list
 boundsLines = bounds(sources,transit,dests)
 for line in boundsLines:
     lines.append(line)

 # Generates and adds the binary bounds to the lp file list
 binaryLines = binary(sources,transit,dests)
 for line in binaryLines:
     lines.append(line)
    lines.append("End

 # Write each of the lp file list to the actual lp file
 for line in lines:
     file_.write(line + "\n")
 sol_file = open("flow_sol.txt","w")

 # Runs the cplex command lines in the terminal and writes the stdout to
 # flow_sol.txt.
 out = subprocess.Popen("./cplex -c \" read flow.lp\" \"optimize\" \"display solution variables -
\"",shell=True, stdout = sol_file)
 sol_file.close()
 file_.close()

if __name__ == "__main__":
    main()
