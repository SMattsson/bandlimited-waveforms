import math

class WaveformTable:
    table_message = '/* This array was created by using the blwftal tool (Bandlimited Waveforms for Teensy Audio Library)\n   https://github.com/SMattsson/bandlimitied-waveforms */\n\n'
    def __init__(self):
        pass

    def generate_freq_list(self, num_of_notes):
        freq_list = []
        note = 0
        while note < 128:
            freq_list.append(pow(2.0, (note - 69.0) / 12.0) * 440.0)
            if num_of_notes == 128 / 2:
                note += 2
            else:
                note += 1
        return freq_list

    def multiply(self, table, factor):
        for note in range(len(table)):
            peak = max(table[note])
            for sample in range(len(table[0])):
                table[note][sample] *= factor / peak
        return table

    def convert_to_int_list(self, table):
        for note in range(len(table)):
            for sample in range(len(table[0])):
                table[note][sample] = int(table[note][sample])
        return table

    def generate_square_table(self, freq_list, num_of_samples, max_frequency):
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

    def get_square_table(self, num_of_notes, num_of_samples, max_frequency, max_amplitude, shrink):
        if shrink:
            table = self.generate_square_table(self.generate_freq_list(num_of_notes / 2), num_of_samples, max_frequency)
        else:
            table = self.generate_square_table(self.generate_freq_list(num_of_notes), num_of_samples, max_frequency)
        table = self.multiply(table, max_amplitude)
        table = self.convert_to_int_list(table)
        return table