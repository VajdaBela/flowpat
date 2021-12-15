#!/usr/bin/python3

import sys

"""
A pattern consists of multiple frames. A frame consists of multiple instructions. An instruction says which
diode has to achieve which brightness value. Max brightness is 255, min is 0. A frame says under what time
the instruction has to be fulfilled. And a pattern is just a collection of frames..
"""
#TODO remove folder names from out file

class Instruction:
    all_instructions = []
    def __init__(self, diode, final_value):
        self.diode = diode
        self.final_value = final_value

        Instruction.all_instructions.append(self)

    @staticmethod
    def make_instructions_from_line(line):
        """
        Used to make multiple instructions from a str line. Puts the Instructions into all_instructions.
        input:
            line - A str line containing data for the instructions. The line has the following format:
                value,diode1,diode2,diode3,...,diodeN
        output:
            number of instructions created
        """
        parts = line.split(",")

        final_value = int(parts[0])

        for diode in parts[1:]:
            Instruction(int(diode), final_value)

        return len(parts) - 1

class Frame:
    all_frames = []
    def __init__(self, time, first_instruction_idx, instruction_num):
        self.time = time
        self.first_instruction_idx = first_instruction_idx
        self.instruction_num = instruction_num

        Frame.all_frames.append(self)

    @staticmethod
    def make_frame_from_line(line):
        """
        Used to make a frame from a str line. Puts the Frame into all_frames.
        input:
            line - A str line containing data for the Frame. The line has the following format:
                time|instruction_line
                see line from Instruction
        output:
            NA
        """
        parts = line.split("|")

        time = int(parts[0])

        first_instruction_idx = len(Instruction.all_instructions)

        instruction_num = 0
        for instruction_part in parts[1:]:
            instruction_num += Instruction.make_instructions_from_line(instruction_part)

        Frame(time, first_instruction_idx, instruction_num)

class Pattern:
    all_patterns = []
    def __init__(self, first_frame_idx, frame_num):
        self.first_frame_idx = first_frame_idx
        self.frame_num = frame_num

        Pattern.all_patterns.append(self)

    @staticmethod
    def make_pattern_from_line(line):
        """
        Used to make a pattern from a str line. Puts the Pattern into all_patterns.
        input:
            line - A str line containing multiple Frames separated with /. The line has the following format:
                frame_line1/frame_line2/.../frame_line3
                see line from Frame
        output:
            NA
        """
        parts = line.split("/")

        first_frame_idx = len(Frame.all_frames)

        frame_num = len(parts)

        for frame_part in parts:
            Frame.make_frame_from_line(frame_part)

        Pattern(first_frame_idx, frame_num)

def generate_c_code(out_file):
    """
    Used for writing out the structures and arrays for the c program
    input:
        out_file - opened file for writing
    output:
        NA
    """
    def to_file_print(string):
        print(string, file=out_file)

    define_word = out_file.name.upper().replace(".","_")

    #the ifndef of c header files
    to_file_print("#ifndef " + define_word)
    to_file_print("#define " + define_word)

    #declaration of types for c
    to_file_print("#define PATTERN_NUMBER " + str(len(Pattern.all_patterns)))
    to_file_print("typedef struct {")
    to_file_print("uint8_t diode;")
    to_file_print("uint8_t finalValue;")
    to_file_print("} Instruction;")
    to_file_print("typedef struct {")
    to_file_print("uint32_t time;")
    to_file_print("uint8_t instLen;")
    to_file_print("Instruction* insts;")
    to_file_print("} Frame;")
    to_file_print("typedef struct {")
    to_file_print("uint8_t frameLen;")
    to_file_print("Frame* frames;")
    to_file_print("} Pattern;")

    #writing out all instructions
    to_file_print("const Instruction instructions[] = {")
    for instruction in Instruction.all_instructions:
        to_file_print("{" + str(instruction.diode) + "," + str(instruction.final_value) + "},")
    to_file_print("};")

    #writing out all frames
    to_file_print("const Frame frames[] = {")
    for frame in Frame.all_frames:
        to_file_print("{" + str(frame.time) + "," + str(frame.instruction_num) + ",&instructions[" + 
                str(frame.first_instruction_idx) + "]},")
    to_file_print("};")

    #writing out all patterns
    to_file_print("const Pattern patterns[] = {")
    for pattern in Pattern.all_patterns:
        to_file_print("{" + str(pattern.frame_num) + ",&frames[" + str(pattern.first_frame_idx) + "]},")
    to_file_print("};")

    #end of ifndef of c header files
    to_file_print("#endif")

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: <infile> <outfile>")
        sys.exit(1)

    in_file = open(sys.argv[1], 'r')
    out_file = open(sys.argv[2], 'w')

    try:
        for line in in_file:
            line = line.strip()
            if not line:
                continue
            Pattern.make_pattern_from_line(line)

        generate_c_code(out_file)
    except ValueError as err:
        print("ERROR: not integer values found")
        print("exception:")
        print(repr(err))
    finally:
        out_file.close()
        in_file.close()
