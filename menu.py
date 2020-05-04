import os


def menu():
    print('\n\n')
    print('-' * 70)
    print('   Warehouse Control')
    print('-' * 70)

    print(' [1] Register Items')
    print(' [2] Display Catalog')
    print(' [3] Display Out of Stock')
    print(' [4] Update item stock')
    print(' [5] Calculate stock value')
    print(' [6] Remove item')
    print(' [7] Register sale')
    print(' [8] Display Log')
    print('\n')

    print(' [x] Exit')


def header(title):
    clear()
    print('-' * 70)
    print(' ' + title)
    print('-'*70)


def clear():
    return os.system('cls')
