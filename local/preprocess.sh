#!/bin/bash

tail -n6662 000001.csv | awk -F',' '{print $1,$4}' > tmp.csv