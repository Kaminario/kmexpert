# kmexpert

The Kaminario kmexpert library provides an infrastructure for building interactive decision trees (procedures) in python code. The resulting procedures can be run as a shell command and can be used via the command-line interface. The interactive decision trees are a good alternative to the document style step by step instructions, for example, troubleshooting instructions.

The library philosophy is to combine the raw python code flexibility with the simple procedure definition syntax, making the procedure both readable and as flexible as python can be.

# Installation
The library code may be directly sourced or Kmexpert-<version>.tar.gz archive can be created by running:

    make build

 The resulting tar.gz file will be located in the created dist folder

# Usage
See the main_example.py and example_procedure.py for the example usage.
![Help interface](https://github.com/Kaminario/kmexpert/blob/master/example1.py)

![Run example](https://github.com/Kaminario/kmexpert/blob/master/example2.py)

# Architecture
Each procedure step is represented by a python class. During the procedure evaluation, the stack of step objects is built up and the execution context is updated and propagated forward. Each step object on the stack preserves its execution context copy, thus enabling step back operations.

