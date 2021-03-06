
class PacketDecoder:
    def __init__(self, hexa):
        self.version = 0
        self.i = 0
        self.binary_data = self.conv_hexa_binary(self.data_loader())
    
    def data_loader(self):
        with open("inputs/input.txt", "r") as f:
            return f.read()

    def conv_hexa_binary(self, hexa):
        hexBin = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', 
        '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
        binary = ""
        for c in hexa:
            binary += hexBin[c]
        return binary

    def get(self, size):
        val = int(self.binary_data[self.i:self.i+size],2)
        self.i += size
        return val
    
    def get_binary(self, size):
        b = self.binary_data[self.i:self.i+size]
        self.i+=size
        return b

    def parse_literal(self):
        binary = ""
        while True:
            A = self.get_binary(5)
            binary += A[1:]
            if A[0] == '0':
                break
        return int(binary, 2)

    def parse_operator(self, typ):
        initialMap = {0: 0, 1:1, 2: 10000, 3:-10000, 5: [], 6: [], 7:[]}
        initial = initialMap[typ]
        len_id = self.get(1)
        if len_id==0:
            num_bits = self.get(15)
            starting_bit = self.i
            while self.i-starting_bit<num_bits:
                val = self.parser()
                if typ==0:
                    initial += val
                elif typ==1:
                    initial*=val
                elif typ==2:
                    initial = min(initial, val)
                elif typ==3:
                    initial = max(initial, val)
                else:
                    initial.append(val)
        else:
            num_subpackets = self.get(11)
            for _ in range(num_subpackets):
                val = self.parser()
                if typ==0:
                    initial += val
                elif typ==1:
                    initial*=val
                elif typ==2:
                    initial = min(initial, val)
                elif typ==3:
                    initial = max(initial, val)
                else:
                    initial.append(val)
        if typ==5:
            return 1 if initial[0]>initial[1] else 0
        elif typ==6:
            return 1 if initial[0]<initial[1] else 0
        elif typ==7:
            return 1 if initial[0]==initial[1] else 0
        return initial
    def parser(self):
        self.version += self.get(3)
        pid = self.get(3)
        if pid==4:
            return self.parse_literal()
        return self.parse_operator(pid)
    def run(self):
        return self.parser()
    
if __name__ == '__main__':
    s = PacketDecoder(None)
    print(f'the sum of the packet versions: {s.version}') # part 1
    print(f'the result of parsing the hexadecimal: {s.run()}') # part 2
