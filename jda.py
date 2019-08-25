import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfiglet

def poly(coeff, x):
    exp = len(coeff)
    fx = 0
    for i in range(len(coeff)):
        fx += coeff[i] * x ** (exp - 1)
        exp -= 1
    return fx



if __name__ == '__main__':
    ascii = pyfiglet.figlet_format('HackMTY x JDA')
    print(ascii)

    print('This program uses Machine Learning algorithms to estimate the sales forecast up to three months away.')
    print('\nEnter the name of the input .csv file. The first column must correspond to the location number and the second one to the product number.')
    input_file = input()
    print('\nEnter the name of the output .csv file. The first column must correspond to the location number and the second one to the product number.')
    output_file = input()

    location = input('\nEnter the location number: ')
    product = input('Enter the product number: ')

    dates = {}
    sa_quantity = []

    with open(input_file) as input_file:
        reader = csv.reader(input_file, delimiter = ',')
        counter = 1
        for row in reader:
            if row[0] == location and row[1] == product:
                dates.update({counter : row[2]})
                sa_quantity.append(float(row[3]))
                counter += 1
    input_file.close()

    temp = []
    for key in dates.keys():
        temp.append(key)



    for row in temp:
        x = np.append(temp, row)

    for row in sa_quantity:
        y = np.append(sa_quantity, row)

    change_degree = True

    while change_degree:
        degree = int(input('\nEnter the degree of the polynomial regression: '))
        coeff = np.polyfit(x, y, degree)
        print('\nThe coefficients for the polynomial are:')
        for c in coeff:
            print(c)

        days = int(input('\nEnter how many days from the last date registered you would like to predict the sales of: '))

        pred_x = []
        pred_y = []
        why = []

        for i in range(len(x), len(x) + days + 1):
            pred_x.append(i)
            pred_y.append(poly(coeff, i))

        for i in range(len(x)):
            why.append(poly(coeff, i))

        mse = np.mean((y - why)**2)
        print('\nThe MSE for this polynomial is: ', mse)

        dict = {'sa_quantity' : pred_y}
        temp_df = pd.DataFrame(dict)

        df = pd.read_csv(output_file)
        df.insert(3, 'sa_quantity', temp_df.sa_quantity)

        df.to_csv(output_file, index=False)

        answer = input('\nA new column has been inserted into the output file with the sales forecast.\nWould you like to plot the data? (Y/N) ')

        if answer == 'Y':
            for i in range(len(x) + days + 1):
                pred_x.append(i)
                pred_y.append(poly(coeff, i))

            pred_x = np.array(pred_x)
            pred_y = np.array(pred_y)

            plt.plot(x, y)
            plt.plot(pred_x, pred_y)
            plt.show()
            answer = input('\nWould you like to change the degree of the polynomial? (Y/N) ')
            if answer == 'Y':
                df = pd.read_csv(output_file)
                df.drop('sa_quantity', axis = 1, inplace = True)
                df.to_csv(output_file, index=False)
            else:
                change_degree = False
        else:
            answer = input('\nWould you like to change the degree of the polynomial? (Y/N) ')
            if answer == 'Y':
                df = pd.read_csv(output_file)
                df.drop('sa_quantity', axis = 1, inplace = True)
                df.to_csv(output_file, index=False)
            else:
                change_degree = False
