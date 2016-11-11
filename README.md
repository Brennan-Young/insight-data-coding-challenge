## Dependencies

Source code language: Python 2

Packages used: sys, copy

## Structure of Data

Establishing a connection between two users depends on the user IDs, not the amount paid, the message associated with payment, or the time of payment.  It is natural to want to represent the payment data as a graph G = (V,E), where V the vertices represent users and an edge e in E exists if and only if users with ID u<sub>1</sub> has paid user u<sub>2</sub> or vice-versa.  