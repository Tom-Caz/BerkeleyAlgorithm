# BerkeleyAlgorithm

This implements the Berkely Algorithm for clock synchronization

First run Server.py then Client.py

Each client thread generates random amounts of drift. The local (incorrect) clock time is then averaged and updated for each client.

Two graphs are generated comparing the clock drift with and without the Berkeley Algorithm.
