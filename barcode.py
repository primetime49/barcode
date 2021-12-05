from tkinter import Canvas, Tk
import csv

class Barcode(Canvas):
    def __init__(self, code):
        super().__init__(height=270, width=400)
        self.code = code
        self.init_struct()
        self.init_encoding()
        
    def init_struct(self):
        filename = 'struct.csv'
        with open(filename, 'r') as f:
            reader = csv.reader(f,delimiter =';')
            your_list = list(reader)
        self.struct = []
        for s in your_list:
            st = dict()
            st['first'] = s[1][:6]
            st['last'] = s[2][:6]
            self.struct.append(st)
            
    def init_encoding(self):
        filename = 'encode.csv'
        with open(filename, 'r') as f:
            reader = csv.reader(f,delimiter =';')
            your_list = list(reader)
        self.encoding = []
        for s in your_list:
            st = dict()
            st['L'] = s[1][:7]
            st['G'] = s[2][:7]
            st['R'] = s[3][:7]
            self.encoding.append(st)
    
    def split_code(self):
        return [int(self.code[0]),self.code[1:7],self.code[7:13]]
    
    def draw_bit(self, byte, pointer):
        for b in byte:
            if b == '0':
                self.create_rectangle(pointer, 10, pointer+4, 235, outline="#fff", fill="#fff")
            elif b == '1':
                self.create_rectangle(pointer, 10, pointer+4, 235, outline="#fff", fill="#000")
            pointer = pointer+4
        return pointer
    
    def draw_m(self, pointer): # draw middle
        for i in range(0,5):
            if i%2 == 0:
                self.create_rectangle(pointer, 10, pointer+4, 260, outline="#fff", fill="#fff")
            else:
                self.create_rectangle(pointer, 10, pointer+4, 260, outline="#fff", fill="#000")
            pointer = pointer+4
        return pointer
    
    def draw_edge(self, pointer):
        for i in range(0,3):
            if i%2 == 0:
                self.create_rectangle(pointer, 10, pointer+4, 260, outline="#fff", fill="#000")
            else:
                self.create_rectangle(pointer, 10, pointer+4, 260, outline="#fff", fill="#fff")
            pointer = pointer+4
        return pointer
    
    def draw_bits(self, struct, digits, pointer):
        for i in range(0,6):
            s = struct[i] # L,R, or G
            d = int(digits[i]) # bit from the barcode
            encode = self.encoding[d][s] # get the bits, e.g. 1011100
            pointer = self.draw_bit(encode, pointer)
        return pointer
    
    def generate(self):
        comp = self.split_code()
        first_dig = comp[0]
        pointer = 10 # pointer x-buffer start
        
        pointer = self.draw_edge(pointer)
        
        six = self.struct[first_dig]['first']
        digits = comp[1]
        pointer = self.draw_bits(six,digits,pointer)
        
        pointer = self.draw_m(pointer)
        
        six = self.struct[first_dig]['last']
        digits = comp[2]
        pointer = self.draw_bits(six,digits,pointer)
        
        pointer = self.draw_edge(pointer)
        
        self.pack()
        
        #save to eps
        self.update()
        self.postscript(file="barcode1.eps", colormode='color')

def main():
    screen = Tk()

    brc = Barcode('8997029809979')
    brc.generate()

    screen.mainloop()

if __name__ == "__main__":
    main()