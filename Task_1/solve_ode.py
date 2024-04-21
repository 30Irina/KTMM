import numpy as np
from scipy.integrate import odeint
import csv
from read_param import read_param
from scipy.optimize import fsolve


class HeatEquationSolver:
    def __init__(self, params: read_param):
        self.k_ij = np.zeros((5, 5))
        self.Q_iE = np.zeros(5)
        self.A = 0.1
        self.Q_iR = self.calculate_Q_iR
        self.c_i = params.c_i
        self.initial_temp = params.start_temp
        self.time_grid = params.time_grid
        for i in range(5):
            self.Q_iE[i] = -params.eps_i[i] * params.s_i[i] * 5.67 / (100 ** 4)
            for j in range(5):
                self.k_ij[i][j] = params.lambda_ij[i][j] * params.s_ij[i][j]
        # print(self.k_ij)

    def calculate_Q_stat(self, temp):
        Q_total = np.zeros(5)
        for i in range(5):
            Q_sum = 0
            for j in range(5):
                Q_sum += self.k_ij[i][j] * (temp[j] - temp[i])
            Q_total[i] = (Q_sum + self.Q_iE[i] * (temp[i] ** 4)) / self.c_i[i]
        return Q_total

    def calculate_Q(self, temp, t):
        Q_total = np.zeros(5)
        for i in range(5):
            Q_sum = 0
            for j in range(5):
                Q_sum += self.k_ij[i][j] * (temp[j] - temp[i])
            Q_total[i] = (Q_sum + self.Q_iE[i] * (temp[i] ** 4) + self.Q_iR(t, self.A)[i]) / self.c_i[i]
        return Q_total

    def solve_equation_stat(self, params: read_param):
        temp = np.ones(5)
        solution_stat = fsolve(self.calculate_Q_stat, temp)
        return solution_stat

    def solve_equation(self, params: read_param):
        #solution = odeint(self.calculate_Q, self.initial_temp, self.time_grid)
        solution = odeint(self.calculate_Q, params.start_temp, params.time_grid)
        return solution

    def calculate_Q_iR(self, t, A):
        return [A * (20 + 3 * np.sin(t / 4)) if i == 4 else 0 for i in range(5)]


'''
params = read_param('parameters.csv', 'temperature.csv')
heat_solver = HeatEquationSolver(params)
solution = heat_solver.solve_equation()
with open('solution.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'T1', 'T2', 'T3', 'T4', 'T5'])
    for time, row in zip(params.time_grid, solution):
        writer.writerow([time] + row.tolist())
'''
