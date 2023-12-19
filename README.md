# Thesis_code
Code for Thesis

To start with make sure that you have python installed on your system.

## Instructions

### Virtual environment

Create a virtual environment for this project. I created one using the virtualenv module installed by default in python.

```{python}
virtualenv venv
```
Once the virtualenv is created, activate it using

```{python}
venv\Scripts\Activate
```

on Windows. Activate using source command if on Linux.

### Dependencies

Now we can install the packages required for this project using the requirements.txt


```{python}
pip install -r requirements.txt
```
This might take some time. Once the installation is done, you can start exploring the notebooks in the notebook folder.

## Things to do

- Make a django webpage
- add nodes and relationships to the graph
- display the graph in the app
