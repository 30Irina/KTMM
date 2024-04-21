import numpy as np
import csv


class read_param:
    def __init__(self, filename: str, filename_temp=''):
        self.eps_i, self.c_i, self.lambda_ij, self.s_i, self.s_ij, self.time_calc = self.read_prms(filename)
        N_t = int(self.time_calc[0])*10+1
        self.time_grid = np.linspace(0, self.time_calc[0], N_t)
        self.start_temp = self.read_start_temp(filename_temp)


    def read_prms(self, filename: str):
        with open(filename, 'r', newline='') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',')
            params = [list(map(float, row)) for row in file_reader]
        eps_i = params[0]
        c_i = params[1]
        lambda_ij = np.array(params[2:7])
        s_i = params[7]
        s_ij = np.array(params[8:13])
        time_calc = params[13]

        return eps_i, c_i, lambda_ij, s_i, s_ij, time_calc


    def read_start_temp(self, filename=''):
        if filename != '':
            with open(filename, 'r', newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=',')
                start_temp = next(file_reader)
                start_temp = list(map(float, start_temp))
        else:
            start_temp = []
        return start_temp

#params = read_param('parameters.csv', 'temperature.csv')
'''
print(params.eps_i)
print(params.c_i)
print(params.lambda_ij)
print(params.s_i)
print(params.s_ij)
print(params.time_calc)
print(params.start_temp)
print(params.time_grid)
'''

