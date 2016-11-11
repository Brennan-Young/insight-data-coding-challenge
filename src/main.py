from timeit import default_timer as timer

def readBatch(filename):
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
            useful later on.
            ''' 
            
    return adj
    
def sortPayments(adj):
    adj.sort(key=lambda x: x[0]) # sort adjacency list by first element
    numIDs = adj[-1][0]
    adjList = [[] for x in xrange(numIDs)]
    for i in adj:
        adjList[i[0]-1].append(i[1])
    return adjList
    
def readStream(iFile,oFile,adjList,friendDepth = 1):
    with open(iFile, 'rb') as f, open(oFile, 'w') as g:
        next(f)
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
                #if payee in adjList[payer-1]:
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
    '''
    # if friendDepth == 1:
    #     if payee in adjList[payer-1]:
    #         return True
    #     else:
    #         return False
    # else:
    #     #for p in adjList[payer-1]:
    #     return any(inNetwork(adjList,p,payee,friendDepth - 1) for p in adjList[payer-1])
    if payee in adjList[payer-1]:
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
    if payer <= len(adjList) and payee <= len(adjList):
        adjList[payer-1].append(payee)
        adjList[payee-1].append(payer)
    else:
        p = max(payer,payee)
        adjList.extend([[]]*(p-len(adjList)))
        adjList[payer-1].append(payee)
        adjList[payee-1].append(payer)
    return
    

def main():
    start = timer()
    x = readBatch('../insight_testsuite/tests/my_tests/bp1.csv')
    end = timer()
    print(end-start)
    start = timer()
    adjList = sortPayments(x)
    end = timer()
    print(end-start)
    start = timer()
    readStream('../insight_testsuite/tests/my_tests/sp1.csv','./otest.txt',adjList,3)
    end = timer()
    print(end-start)
    #print(adjList)
    print(len(x))
    print(len(adjList))
    print(adjList)
    return
    

if __name__ == "__main__":
    main()