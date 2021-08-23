

ENCODING = 'windows-1251'
SEPARATOR = '\t'

class Line:

    def __init__(self, id, text):
        self.id = int(id)
        self.text = text

    @property
    def id_bytes(self):
        return (self.id).to_bytes(4, 'little')
    
    @property
    def text_bytes(self):
        return str.encode(self.text, encoding=ENCODING)

    def __repr__(self):
        return f'{self.id} {self.text}'

class TxtToDef:
    BLOCK_SIZE = 8
    HEADER_START_POS = 8

    def process(self, txt_path, def_path):
        lines = self.__read_txt(txt_path)
        total_lines = len(lines)
        header_size = self.BLOCK_SIZE*total_lines
        target_bytes = self.__int_to_bytes(total_lines) + bytes(4)
        str_bytes = bytes()
        for line in lines:
            text_pos = self.BLOCK_SIZE + header_size + len(str_bytes)
            target_bytes += line.id_bytes + self.__int_to_bytes(text_pos)
            str_bytes += line.text_bytes + bytes(1)

        target_bytes += str_bytes
        self.__write_def(target_bytes, def_path)

    def __int_to_bytes(self, number):
        return (number).to_bytes(4, 'little')

    def __write_def(self, def_bytes, path):
        with open(path, 'wb') as f:
            f.write(def_bytes)

    def __read_txt(self, path):
        with open(path, 'r') as f:
            raw_lines = f.readlines()

        lines_dict = dict()
        sorted_ids = list()

        for line in raw_lines:
            line = line.split(SEPARATOR)
            lines_dict[int(line[0])] = line[1].replace('\n', '').replace('\r', '')
            sorted_ids.append(int(line[0]))

        sorted_ids.sort()
        return [Line(id, lines_dict[id]) for id in sorted_ids]

        

class DefToTxt:

    BLOCK_SIZE = 8
    HEADER_START_POS = 8

    def process(self, def_path, txt_path):
        def_bytes = self.__read_bytes(def_path)
        total_lines = self.__get_lines_count(def_bytes)
        lines = self.__get_lines(def_bytes, total_lines)
        self.__lines_to_txt(lines, txt_path)

    def __read_bytes(self, path):
        with open(path, 'rb') as f:
            return f.read()

    def __bytes_to_int(self, bytes_arr):
        return int.from_bytes(bytes_arr, 'little')

    def __get_lines_count(self, file_bytes):
        return self.__bytes_to_int(file_bytes[:4])

    def __get_lines(self, file_bytes, total_strings):
        header_bytes = file_bytes[self.HEADER_START_POS : (total_strings*self.BLOCK_SIZE) + self.BLOCK_SIZE]
        lines = []
        for i in range(total_strings):
            STEP = i * self.BLOCK_SIZE
            id = self.__bytes_to_int(header_bytes[STEP: STEP+int(self.BLOCK_SIZE/2)])
            text_start_pos = self.__bytes_to_int(header_bytes[STEP+int(self.BLOCK_SIZE/2): STEP+self.BLOCK_SIZE])
            text_end_pos = self.__bytes_to_int(header_bytes[STEP+int(self.BLOCK_SIZE*3/2): STEP+self.BLOCK_SIZE*2]) - 1
            text = file_bytes[text_start_pos:text_end_pos].decode(ENCODING)
            lines.append(Line(id, text))

        return lines

    def __lines_to_txt(self, lines, txt_path):
        with open(txt_path, 'w+') as f:
            for line in lines:
                f.write(f'{line.id}{SEPARATOR}{line.text}\n')
        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Script that can convert Mafia textdb_xx.def to txt and txt to textdb_xx.def.')
    parser.add_argument('--i', default='textdb_en.def', type=str, help='input file (required)')
    parser.add_argument('--o', default='textdb_en.txt', type=str, help='output file (required)')
    parser.add_argument('--d', default='def2txt', type=str, help='def2txt or txt2def (required)')
    args = parser.parse_args()
    if args.d == 'def2txt':
        def_to_txt = DefToTxt()
        def_to_txt.process(args.i, args.o)
        print('x`')
    elif args.d == 'txt2def':
        txt_to_def = TxtToDef()
        txt_to_def.process(args.i, args.o)
    else:
        print('unknown convert direction.')
