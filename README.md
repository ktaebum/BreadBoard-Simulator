# BreadBoard Simulator

![Half-Adder Example](https://i.imgur.com/JErshPj.png)

## Description
This program is interactive breadboard simulator for logic design  
```
Author: Taebum Kim
Version: 1.0.0
Last Updated: 2018-3-23
Contact: phya.ktaebum@gmail.com
```

## How to Use

> $ git clone https://github.com/ktaebum/BreadBoard-Simulator.git  
$ cd BreadBoard-Simulator  
$ python -m breadboard  
(breadboard)$ (Type your command)

*Optional Arguments*

| Argument | Description|
| :---: | :---|
| -i/--input=filename | pre-set commands file |
| -v/--verbose | make program print every internal calculation information |

## Prerequisite

Following python packages are needed

- numpy
- matplotlib 

## Supporting Commands

| Command | Parameters | Description|
| :---: | :---: | :--- |
|`input`| `(input_name, target_position)` | Insert input variable in target_position | 
|`output`| `(from_variable(position), output_name, target_position)` | Insert output variable from from_variable(position) to target_position | 
|`chip`| `(lowest_position, chip_number)` | Insert chip in target position | 
|`line`| `(from_position(variable), target_position)` | Insert wire from from_position to target_position | 
|`connect`| `(from_position, chip_number, gate_number)` | Connect to gate. Chip number is denoted in leftmost text in chip picture, gate number is labeling in row-major order | 
|`save`| `(filename)` | Save all command log into file | 

## Example
Following example is command for full-adder logic circuit which is shown at the top-most picture (Not uploaded yet)
```
input A 1I
input B 3G
chip 5E 7400
chip 15E 7400
chip 25E 7400
connect A 0 1
connect A 0 2
connect B 0 1
connect B 0 4
connect 8F 0 2
connect 8F 0 4
connect 11F 1 1
connect 10E 1 1
input Cin 23I
connect Cin 1 2
connect 18F 1 2
connect 18F 1 4
connect 21F 1 4
connect 21F 2 1
connect Cin 2 1
connect 20E 2 2
connect 28F 2 2
connect 21F 2 4
connect 8F 2 4
output 31F S 40I
output 30E Cout 40C
```