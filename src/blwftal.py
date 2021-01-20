from modules.waveformTable import WaveformTable
import sys

if __name__ == "__main__":
    compact = False
    waveform_table = WaveformTable()
    if len(sys.argv) < 2:
        print('blwftal: missing operand\ntry \'blwftal --help\' for more information')
        sys.exit()
    
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--compact':
            compact = True
        else:
            print(f'blwftal: unknown operand \'{sys.argv[2]}\'\ntry \'blwftal --help\' for more information')
            sys.exit()

    if sys.argv[1] == '--help':
        print('usage: blwftal [OPTION]\n  or:  blwftal [OPTION] --compact\n\nmandatory argument options:')
        print('  --square\n  --saw\n  --invsaw\n  --triangle\n  --all')
        print('\noptional argument:\n  --compact')
        sys.exit()
    elif sys.argv[1] == '--square':
        if compact:
            file = open('square_table_compact.h', 'w')
            file.write(waveform_table.get_table('square_compact'))
            file.close()
        else:
            file = open('square_table.h', 'w')
            file.write(waveform_table.get_table('square'))
            file.close()
        print("done!")
    elif sys.argv[1] == '--saw':
        if compact:
            file = open('saw_table_compact.h', 'w')
            file.write(waveform_table.get_table('saw_compact'))
            file.close()
        else:
            file = open('saw_table.h', 'w')
            file.write(waveform_table.get_table('saw'))
            file.close()
        print("done!")
    elif sys.argv[1] == '--invsaw':
        if compact:
            file = open('inverted_saw_table_compact.h', 'w')
            file.write(waveform_table.get_table('inverted_saw_compact'))
            file.close()
        else:
            file = open('inverted_saw_table.h', 'w')
            file.write(waveform_table.get_table('inverted_saw'))
            file.close()
        print("done!")
    elif sys.argv[1] == '--triangle':
        if compact:
            file = open('triangle_table_compact.h', 'w')
            file.write(waveform_table.get_table('triangle_compact'))
            file.close()
        else:
            file = open('triangle_table.h', 'w')
            file.write(waveform_table.get_table('triangle'))
            file.close()
        print("done!")
    else:
        print(f'blwftal: unknown operand \'{sys.argv[1]}\'\ntry \'blwftal --help\' for more information')
        sys.exit()