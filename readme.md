# 02226 Network Embedded Systems Project
This project is the final project of the course 02226 Network Embedded Systems at DTU. You find here the worst-case delay analysis tool for asynchronous traffic shaping. 

The repository includes all the code along with multiple correctness tests. Furthermore it contains all analysis and plotting code used for our analysis. The results of the OMNeT++ simulations were too large to include here.

# Running the analysis tool
Navigate to the root and execute
```
python src/main.py [path/to/topology.csv] [path/to/streams.csv]
```

# Executing the tests
The automatic tests can be executed via
```
pip install -r requirements.txt
python setup.py develop
pytest
```
