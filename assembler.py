class Assembler(object):
    def __init__(self):
        """Create a new Assembler instance."""
        self.calcs = {'ADD': '01000100', 'SUB': '01000101', 'AND': '01000011', 'NOR': '01000010', 'NAND': '01000001', 'OR': '01000000'}
        self.registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'IN': '110', 'OUT': '110'}
        self.cmp1 = {'NIL': '11000000', 'JEQ': '11000001', 'JLT': '11000010', 'JLE': '11000011', 'JMP': '11000100', 'JME': '11000101', 'JGE': '11000110', 'JGT': '11000111', 'JNE':'11000101'}

    def remove_comments(self, lines):
        no_comments = []
        for line in lines:
            cindex = line.find('#')
            new_line = line
            if cindex >= 0:
                new_line = line[:cindex]
            new_line = new_line.strip()
            if len(new_line) > 0:
                no_comments.append(new_line)
        return no_comments

    def assemble(self, asm_ins):
        bin_ins = []
        label = {}
        line_num = 0
        something_i_want = []

        for char in asm_ins:
            if '(' in char and ')' in char:
                label[char[1:-1]] = line_num
            else:
                something_i_want.append(char)
                line_num += 1

        for ins in something_i_want:
            bins = ins
            if '@' in ins: 
                if ins[1:] in label:
                    num = label[ins[1:]]
                    bins = '{:08b}'.format(num)
                else:
                    num = bins.replace('@', '')
                    num = int(num)
                    bins = '{:08b}'.format(num)
            if ins in self.cmp1:
                bins = self.cmp1[ins]
            if ins in self.calcs:
                bins = self.calcs[ins]
            if '->' in ins:
                point = ins.find('->')
                src = ins[:point]  # source
                dst = ins[point + 2:]  # destination
                bins = '10' + self.registers[dst] + self.registers[src]
            bin_ins.append(bins)
        return bin_ins

    def assemble_file(self, asm_filename):
        """Open the asm_filename for the .over file and create the assembled .ture file."""
        with open(asm_filename, 'r') as asm_file:
            lines = asm_file.readlines()

        no_comments = self.remove_comments(lines)
        binary_instructions = self.assemble(no_comments)


        output_filename = asm_filename.replace('.over', '.ture')
        with open(output_filename, 'w') as output_file:
            output_file.writelines('\n'.join(binary_instructions))



if __name__ == "__main__":
    assembler = Assembler()
    assembler.assemble_file('input.over')