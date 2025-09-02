# ORTOOLS
This is just a boilerplate with some examples. 
* The python example should have a customized VRP-PDPTW problem setup.
* C++ is just the VRPTW sample given [here](https://developers.google.com/optimization/routing/vrptw).

# Versions
The samples come in both C++ and Python.

## Python
Simply install using `pip`. Current version is `ortools==9.14.6206`
```bash
pip install ortools~=9.14
```
## C++
I couldn't get the binary install to work. The `make test` was failing because of some unsigned issues.

### Brew
I have a Mac Pro M3 15.6. I currently use Python 3.12 and brew or-tools version 9.14.
```bash
brew install or-tools
```

### Build from Source
Follow instructions [here](https://developers.google.com/optimization/install/cpp/source_mac).  

I haven't successfully built it from source, not because it fails but because it takes too long and the brew version is up-to-date (9.14) as of September 2025.

# Samples

## Python Sample
```bash
python scripts/capacity.py

#output
Search parameters set, starting solve...
Objective: 80036
Routing Status: 1
Route for vehicle 0:
0 Load(0) Time(0,0) -> 7 Load(0) Time(2,2) -> 5 Load(1) Time(5,5) -> 8 Load(2) Time(7,7) -> 9 Load(1) Time(10,10) -> 0 Load(0) Time(12,12)
Maximum load of the route: 2
Time of the route: 12min

Route for vehicle 1:
0 Load(0) Time(0,0) -> 13 Load(0) Time(4,4) -> 12 Load(1) Time(6,6) -> 0 Load(0) Time(10,10)
Maximum load of the route: 1
Time of the route: 10min

Route for vehicle 2:
0 Load(0) Time(0,0) -> 16 Load(0) Time(7,7) -> 14 Load(1) Time(9,9) -> 0 Load(0) Time(14,14)
Maximum load of the route: 1
Time of the route: 14min

Skipped 4 pickup/delivery requests:
  Request 1: pickup 1 -> delivery 6
  Request 2: pickup 2 -> delivery 10
  Request 3: pickup 4 -> delivery 3
  Request 6: pickup 15 -> delivery 11
Total time of all routes: 36min
Total load of all routes: 4
```

## C++ Sample
```bash
mkdir build
cd build
cmake ..
make -j4
./ortools_example

# Output
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1756826952.934630 28036930 ortools.cpp:74] Route for Vehicle 0:
I0000 00:00:1756826952.936046 28036930 ortools.cpp:87] 0 Load(0) -> 7 Load(8) -> 3 Load(10) -> 4 Load(14) -> 1 Load(15) -> 0
I0000 00:00:1756826952.936049 28036930 ortools.cpp:88] Distance of the route: 1552m
I0000 00:00:1756826952.936051 28036930 ortools.cpp:89] Load of the route: 15
I0000 00:00:1756826952.936053 28036930 ortools.cpp:74] Route for Vehicle 1:
I0000 00:00:1756826952.936056 28036930 ortools.cpp:87] 0 Load(0) -> 14 Load(4) -> 16 Load(12) -> 10 Load(14) -> 9 Load(15) -> 0
I0000 00:00:1756826952.936058 28036930 ortools.cpp:88] Distance of the route: 1552m
I0000 00:00:1756826952.936059 28036930 ortools.cpp:89] Load of the route: 15
I0000 00:00:1756826952.936060 28036930 ortools.cpp:74] Route for Vehicle 2:
I0000 00:00:1756826952.936064 28036930 ortools.cpp:87] 0 Load(0) -> 12 Load(2) -> 11 Load(3) -> 15 Load(11) -> 13 Load(15) -> 0
I0000 00:00:1756826952.936065 28036930 ortools.cpp:88] Distance of the route: 1552m
I0000 00:00:1756826952.936066 28036930 ortools.cpp:89] Load of the route: 15
I0000 00:00:1756826952.936067 28036930 ortools.cpp:74] Route for Vehicle 3:
I0000 00:00:1756826952.936070 28036930 ortools.cpp:87] 0 Load(0) -> 8 Load(8) -> 2 Load(9) -> 6 Load(13) -> 5 Load(15) -> 0
I0000 00:00:1756826952.936072 28036930 ortools.cpp:88] Distance of the route: 1552m
I0000 00:00:1756826952.936073 28036930 ortools.cpp:89] Load of the route: 15
I0000 00:00:1756826952.936110 28036930 ortools.cpp:93] Total distance of all routes: 6208m
I0000 00:00:1756826952.936112 28036930 ortools.cpp:94] Total load of all routes: 60
I0000 00:00:1756826952.936114 28036930 ortools.cpp:95] 
I0000 00:00:1756826952.936115 28036930 ortools.cpp:96] Advanced usage:
I0000 00:00:1756826952.936116 28036930 ortools.cpp:97] Problem solved in 1003ms
```

