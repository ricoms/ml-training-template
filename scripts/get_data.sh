#!/bin/bash

wget https://archive.ics.uci.edu/ml/machine-learning-databases/00497/divorce.rar -P ml/input/data/training/
cd ml/input/data/training/ && unrar e divorce.rar
cd ml/input/data/training/ && rm divorce.rar && rm divorce.xlsx
