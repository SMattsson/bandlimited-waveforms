from waveformTable import WaveformTable
import sys

MAX_FREQUENCY = 22050 #Highest playable frequency for a system with 44.1kHz sample rate (Nyquist theorem)
MAX_AMPLITUDE = 32767
NUM_OF_SAMPLES = 256
NUM_OF_NOTES = 128

if __name__ == "__main__":
    shrink = False
    waveform_table = WaveformTable()
    if len(sys.argv) < 2:
        print('blwftal: missing operand\ntry \'blwftal --help\' for more information')
        sys.exit()
    
    if len(sys.argv) >= 3:
        if sys.argv[2] == '--shrink':
            shrink = True
        else:
            print(f'blwftal: unknown operand \'{sys.argv[2]}\'\ntry \'blwftal --help\' for more information')
            sys.exit()

    if sys.argv[1] == '--help':
        print('usage: blwftal [OPTION]\n  or:  blwftal [OPTION] --shrink\n\nmandatory argument options:')
        print('  --square\n  --saw\n  --invsaw\n  --triangle\n  --all')
        print('\noptional argument:\n  --shrink')
        sys.exit()
    elif sys.argv[1] == '--square':
        table = waveform_table.get_square_table(NUM_OF_NOTES, NUM_OF_SAMPLES, MAX_FREQUENCY, MAX_AMPLITUDE, shrink)
        file = open('square_table.h', 'w')
        file.write(waveform_table.table_message)
        if shrink:
            file.write(f'const int16_t squareTable[{int(NUM_OF_NOTES / 2)}][{NUM_OF_SAMPLES}] = ')
        else:
            file.write(f'const int16_t squareTable[{int(NUM_OF_NOTES)}][{NUM_OF_SAMPLES}] = ')
        file.write(str(table).replace('[', '{').replace(']', '}'))
        file.write(';')
        file.close()
        print("done!")
    elif sys.argv[1] == '--saw':
        pass
    elif sys.argv[1] == '--invsaw':
        pass
    elif sys.argv[1] == '--triangle':
        pass
    else:
        print(f'blwftal: unknown operand \'{sys.argv[1]}\'\ntry \'blwftal --help\' for more information')
        sys.exit()