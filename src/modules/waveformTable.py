import math
from config import const

class WaveformTable:
    _table_message = '/* This array was created by using the blwftal tool (Bandlimited Waveforms for Teensy Audio Library)\n   https://github.com/SMattsson/bandlimitied-waveforms */\n\n'
    def __init__(self):
        pass

    def _generate_freq_list(self, num_of_notes):
        freq_list = []
        note = 0
        while note < 128:
            freq_list.append(pow(2.0, (note - 69.0) / 12.0) * 440.0)
            if num_of_notes == 128 / 2:
                note += 2
            else:
                note += 1
        return freq_list

    def _multiply(self, table, factor):
        for note in range(len(table)):
            peak = max(table[note])
            for sample in range(len(table[0])):
                table[note][sample] *= factor / peak
        return table

    def _convert_to_int_list(self, table):
        for note in range(len(table)):
            for sample in range(len(table[0])):
                table[note][sample] = int(table[note][sample])
        return table

    def _generate_square_table(self, freq_list, num_of_samples, max_frequency):
        square_table = []
        note = 0
        while note < len(freq_list):
            tmp = [0 for x in range(num_of_samples)]
            square_table.append(tmp)
            note += 1
        note = 0
        while note < len(freq_list):
            freq = freq_list[note]
            number_of_overtones = int(max_frequency / freq)
            multiplier = 1
            while multiplier <= number_of_overtones:
                for sample in range (num_of_samples):
                    square_table[note][sample] += math.sin(multiplier * sample / (num_of_samples / 2) * math.pi) / multiplier
                multiplier += 2
            note += 1 
        return square_table

    def _generate_saw_table(self, freq_list, num_of_samples, max_frequency):
        saw_table = []
        note = 0
        while note < len(freq_list):
            tmp = [0 for x in range(num_of_samples)]
            saw_table.append(tmp)
            note += 1
        note = 0
        while note < len(freq_list):
            freq = freq_list[note]
            number_of_overtones = int(max_frequency / freq)
            multiplier = 1
            while multiplier <= number_of_overtones:
                for sample in range (num_of_samples):
                    saw_table[note][sample] += math.sin(-1 * multiplier * sample / (num_of_samples / 2) * math.pi) / multiplier
                multiplier += 1
            note += 1 
        return saw_table

    def _generate_inverted_saw_table(self, freq_list, num_of_samples, max_frequency):
        inverted_saw_table = []
        note = 0
        while note < len(freq_list):
            tmp = [0 for x in range(num_of_samples)]
            inverted_saw_table.append(tmp)
            note += 1
        note = 0
        while note < len(freq_list):
            freq = freq_list[note]
            number_of_overtones = int(max_frequency / freq)
            multiplier = 1
            while multiplier <= number_of_overtones:
                for sample in range (num_of_samples):
                    inverted_saw_table[note][sample] += math.sin(multiplier * sample / (num_of_samples / 2) * math.pi) / multiplier
                multiplier += 1
            note += 1 
        return inverted_saw_table

    def _generate_triangle_table(self, freq_list, num_of_samples, max_frequency):
        triangle_table = []
        note = 0
        while note < len(freq_list):
            tmp = [0 for x in range(num_of_samples)]
            triangle_table.append(tmp)
            note += 1
        note = 0
        while note < len(freq_list):
            freq = freq_list[note]
            number_of_overtones = int(max_frequency / freq)
            multiplier = 0
            while multiplier <= number_of_overtones:
                for sample in range (num_of_samples):
                    triangle_table[note][sample] += 1 / pow((2*(multiplier + 1)-1), 2) * math.sin((2*(multiplier + 1) - 1) * sample / (num_of_samples / 2) * math.pi + multiplier * math.pi)
                multiplier += 1
            note += 1 
        return triangle_table

    def get_table(self, waveform):
        if waveform == 'square':
            table = self._generate_square_table(self._generate_freq_list(const.NUM_OF_NOTES), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'square_compact':
            table = self._generate_square_table(self._generate_freq_list(const.NUM_OF_NOTES_DIV_2), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'saw':
            table = self._generate_saw_table(self._generate_freq_list(const.NUM_OF_NOTES), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'saw_compact':
            table = self._generate_saw_table(self._generate_freq_list(const.NUM_OF_NOTES_DIV_2), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'inverted_saw':
            table = self._generate_inverted_saw_table(self._generate_freq_list(const.NUM_OF_NOTES), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'inverted_saw_compact':
            table = self._generate_inverted_saw_table(self._generate_freq_list(const.NUM_OF_NOTES_DIV_2), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'triangle':
            table = self._generate_triangle_table(self._generate_freq_list(const.NUM_OF_NOTES), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
        elif waveform == 'triangle_compact':
            table = self._generate_triangle_table(self._generate_freq_list(const.NUM_OF_NOTES_DIV_2), const.NUM_OF_SAMPLES, const.MAX_FREQUENCY)
            
        table = self._multiply(table, const.MAX_AMPLITUDE)
        table = self._convert_to_int_list(table)
        output = self._table_message

        if waveform == 'square':
            output += 'const int16_t squareTable'
            output += f'[{const.NUM_OF_NOTES}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'square_compact':
            output += 'const int16_t squareTableCompact'
            output += f'[{const.NUM_OF_NOTES_DIV_2}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'saw':
            output += 'const int16_t sawTable'
            output += f'[{const.NUM_OF_NOTES}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'saw_compact':
            output += 'const int16_t sawTableCompact'
            output += f'[{const.NUM_OF_NOTES_DIV_2}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'inverted_saw':
            output += 'const int16_t invertedSawTable'
            output += f'[{const.NUM_OF_NOTES}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'inverted_saw_compact':
            output += 'const int16_t invertedSawTableCompact'
            output += f'[{const.NUM_OF_NOTES_DIV_2}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'triangle':
            output += 'const int16_t triangleTable'
            output += f'[{const.NUM_OF_NOTES}][{const.NUM_OF_SAMPLES}] = '
        elif waveform == 'triangle_compact':
            output += 'const int16_t triangleTableCompact'
            output += f'[{const.NUM_OF_NOTES_DIV_2}][{const.NUM_OF_SAMPLES}] = '
        tmp = str(table).replace('[', '{').replace(']', '}')
        return output + tmp + ';'