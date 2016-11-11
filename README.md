## Dependencies

Source code language: Python 2

Packages used: sys, copy

## Structure of Data

Establishing a connection between two users depends on the user IDs, not the amount paid, the message associated with payment, or the time of payment.  It is natural to want to represent the payment data as an undirected graph G = (V,E), where V the vertices represent users and an edge e in E exists if and only if users with ID u<sub>1</sub> has paid user u<sub>2</sub> or vice-versa.  On such a graph, we can check if a payment between u<sub>1</sub> and u<sub>2</sub> is trusted by checking if there is a path between these users of depth at most n, where n is a positive integer specifying the maximum "degree of friendship" needed for a payment to be trusted.

There are two main ways to represent a graph in data.  We can use an adjacency list, storing every ordered pair of edges in a list (in Python, we can represent an edge as a two-element list, and an adjacency list as a list of these lists). We can alternatively construct a matrix M of size |V| x |V| and set m<sub>i,j</sub>=1 if and only if the pair (u<sub>i</sub>,u<sub>j</sub>) is an edge.  In Python, this can be constructed as a list of lists.  

These two representations have different advantages.  An adjacency list has a low storage cost: we need only store the list of connections, and each connection can be represented by two numbers.  We could thus represent an adjacency list in memory as a list of 2|E| integers, or a list of |E| pairs of integers.  Adding an edge to the graph is similarly easy: simply append a new pair to the list (an O(1) operation).

However, determining if an edge (u,v) exists in this list is more difficult.  If the list is unsorted, we require O(|E|) operations to determine if an edge is in the list.  If the list is sorted (say, lexicographically), then we can perform a binary search, reducing the cost of searching to O(log|E|).  However, adding a new edge requires O(log|E|) operations in this case to ensure that the list remains sorted.

To find if there is a path of length at most 2 between two vertices u and v, we must search for all edges containing u, and then for each w where (u,w) is an edge, check if (v,w) is an edge.

On the other hand, adjacency matrices require O(|V|^2) storage space, but querying whether or not an edge is present in the matrix is a simple O(1) lookup.  

There is a tradeoff here between the time complexity of querying the graph and the storage requirements of the graph.  I chose to skew towards a higher storage-cost, lower time-cost data representation.  The justification for this is that from a user perspective, storage efficiency is irrelevant, but a query that takes a long time to run is a highly negative experience.

Thus, I chose to use an adjacency matrix.  Because the matrix is highly sparse (the number of edges in the graph is far fewer than the number of potential edges, i.e. the number of 1s in the matrix is far fewer than the number of 0s), I made a modification to this that makes the matrix similar to MATLAB's sparse matrix representation.  

In this data representation, every user ID is associated with a row in the adjacency matrix.  Each row is, rather than a 1 x |V| vector of 1s and 0s, is a list of users IDs that the row is directly connected with.  This reduces the storage cost of each row considerably. 

In this implementation, I leave each list within a row unsorted.  It is possible to sort these lists, making searching these lists O(log n) rather than O(n), but because these lists tend to be relatively short, I decided that the overhead incurred in sorting the lists would match any time saved in lookups.  