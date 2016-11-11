import sys
import copy

def readBatch(filename):
    '''
    Reads a file line by line, extracting the useful information (for us, just 
    the payment ids) and placing these into a list.  Holds only one line in 
    memory at a time.
    '''
    adj = []
    with open(filename, "rb") as f:
        next(f) # skip the header
        for line in f:
            l = [s.strip() for s in line.split(',')]
            adj.append([int(l[1]),int(l[2])])
            adj.append([int(l[2]),int(l[1])])
            ''' 
            If id x pays id y, add both the pair (x,y) and the pair (y,x)
            to an adjacency list.  This is not explicitly needed, but will be 
            useful.  See top level README.md for details.
            ''' 
            
    return adj
    
def sortPayments(adj):
    '''
    Restructures the list of connections, originally formatted a list of ordered
    pairs (lists), into a list of lists similar to MATLAB's sparse matrix 
    representation.  Each list corresponds to a user ID.  Within each list are
    IDs of users that the given user has a connection with (either as payer or
    payee).  
    '''
    adj.sort(key=lambda x: x[0]) # sort adjacency list by first element
    numIDs = adj[-1][0]
    adjList = [[] for x in xrange(numIDs)]
    for i in adj:
        adjList[i[0]-1].append(i[1])
    return adjList
    
def readStream(iFile,oFile,adjList,friendDepth = 1):
    '''
    Reads a stream input and writes to a file whether each payment in the stream
    is trusted or unverified.  Permits arbitrary "depth" of 
    '''
    with open(iFile, 'rb') as f, open(oFile, 'w') as g:
        next(f) #skip header
        for line in f:
            l = [s.strip() for s in line.split(',')]
            payer = int(l[1])
            payee = int(l[2])
            ''' 
            Sometimes the payer may have an ID higher than the current 
            largest ID.  In such a case, this transaction will always be 
            unverified, as they have no transactions.  
            '''
            if payer <= len(adjList):
                if inNetwork(adjList,payer,payee,friendDepth):
                    g.write('trusted\n')
                else:
                    g.write('unverified\n')
                    graphAdd(adjList,payer,payee)
            else: 
                g.write('unverified\n')
                graphAdd(adjList,payer,payee) # connect the payer and payee
    return

def inNetwork(adjList,payer,payee,friendDepth):
    '''
    Recursive function to decide if there is a connection between two users of 
    depth at most friendDepth.  First, we check if there is a direct connection
    between the payer and payee.  If not, we search recursively through the 
    payer's connections until a link to the payee is found or the maximum
    depth is reached.
    
    Remark: this is a breadth-first approach to looking for a connection.
    '''
    if payee in adjList[payer-1]: # "early stopping"
        return True
    else:
        if friendDepth > 1:
            '''
            Main recursion.  A connection is established if any of the payer's
            connections connect to the payee in one fewer steps than the 
            maximum depth.
            '''
            return any(inNetwork(adjList,p,payee,friendDepth - 1) for p in adjList[payer-1])
        else:
            return False
            
def graphAdd(adjList,payer,payee):
    '''
    Upon seeing a transaction, make the two users involved connected.  
    '''
    if payer <= len(adjList) and payee <= len(adjList): 
        adjList[payer-1].append(payee)
        adjList[payee-1].append(payer)
    else: # happens when one of the user IDs is larger than the largest ID in 
    # the current adjacency matrix.  In such a case, new rows need to be added.
        p = max(payer,payee)
        adjList.extend([[]]*(p-len(adjList)))
        adjList[payer-1].append(payee)
        adjList[payee-1].append(payer)
    return
    

def main(argv):
    x = readBatch(argv[0])
    adjList = sortPayments(x)
    # deep copies of this list
    l2 = copy.deepcopy(adjList)
    l3 = copy.deepcopy(adjList)
    
    readStream(argv[1],argv[2],adjList,1)
    readStream(argv[1],argv[3],l2,2)
    readStream(argv[1],argv[4],l3,4)
    return
    

if __name__ == "__main__":
    main(sys.argv[1:])