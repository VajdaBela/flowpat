# flowpat
This is a helper project. There is a project implemented in c that controls the pattern of lights on the flower (see picture). Sadly the patterns are specified in c structures. It's inconvenient to have to write the pattern like this. Hence this project. flowpat provides an easier syntax for specifying patterns.
![](flower.jpg)

To call the program:

    flowpat.py <in_file> <out_file>

in_file should contain the pattern, out_file should be the name of the c file used in the other project.

## Pattern specification
 - pattern:
```
time1|value1,diode1,diode2,...,diodeN|value2,diode1,diode2,...,diodeM/time2|value1,diode1,diode2,...,diodeN|value2,diode1,diode2,...,diodeM
```
Every line containes a pattern that follows the aformentioned syntax.
A pattern contains any number of frames. A frames contains any number of instructions. Both frames and instructions are shown above but here they are on their own:
 - frame:
```
time1|value1,diode1,diode2,...,diodeN
```
 - instruction:
 ```
 value1,diode1,diode2,...,diodeN
 ```

patterns.txt is an example of some patterns.
