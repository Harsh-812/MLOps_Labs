# MLOps_Lab1

##  Overview
The goal was to understand how to structure a Python project, manage dependencies, write unit tests, and set up automation using GitHub Actions.

- Creating a virtual environment  
- Git and GitHub for version control  
- Organizing project folders (data, src, test)  
- Write and run tests using **Pytest** and **Unittest**  
- Automate test execution using **GitHub Actions**

---

##  Step 1: Virtual Environment
A virtual environment was created to isolate dependencies and maintain a clean setup.

---

##  Step 2: Script – `stats_utils.py`
The main Python file, located in the `src/` folder, contains basic statistical functions such as:

- **mean()** → calculates the average  
- **median()** → finds the middle value  
- **mode()** → identifies the most frequent value  
- **variance()** → measures data spread  

Each function includes input validation and raises errors for empty or invalid lists.

---

##  Step 3: Testing
Tests written using the `pytest` framework, focusing on verifying correct outputs and error handling.

## Example usage
```python
from src.stats_utils import mean, median, mode, variance

print(mean([1, 2, 3, 4, 5]))   # Output: 3
print(median([1, 3, 2]))       # Output: 2
print(mode([1, 2, 2, 3]))      # Output: 2
print(variance([1, 2, 3]))     # Output: 0.6666
```

## CI (GitHub Actions)
- Two workflows in `.github/workflows/` run on **push** and **pull_request** to `main`.
- They set up Python 3.8, install deps, run tests, and upload results.


