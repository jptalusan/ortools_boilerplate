# ORTOOLS
This is just a boilerplate with some examples. 
* The python example should have a customized VRP-PDPTW problem setup.
* C++ is just the VRPTW sample given [here](https://developers.google.com/optimization/routing/vrptw).

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


