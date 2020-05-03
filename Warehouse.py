"""
     Program: WarehousemanagementSystemError
     Functionality:
         - repeated menu
         - register items to the catalog
               id(auto generated)
               title category price stock
         - display catalog
         - display items with no stock(out of stock)
     saving / retrieving data to/from file
     update the stock of an item
       show list of items
       ask user id
       ask stock
       find item
     update/save
     -print the total value of the stock(sum(price * stock))
     -remove an item from the catalog
     -
     register sale
     - show list of all items
     - ask the use to choose an id
     - ask to provide quantity
     - update the stock
     have a log of the events
     - file name for the logs
     - list for the log entries
     - add_log_event function that receives a string
     save_log
     read_log
     update existing fn to register log entries
     display the log of events
"""

from menu import menu, clear, header
from item import Item
import pickle
import datetime

#  global vars
catalog = []
log = []
data_file = 'warehouse.data'
last_id = 0
logs_file = 'logs.data'


def save_catalog():
    global data_file
    # create file (overwrites), open to write binary
    writer = open(data_file, 'wb')
    pickle.dump(catalog, writer)
    writer.close()
    print('** Data Saved!!')


def save_log():
    global logs_file
    write = open(logs_file, 'wb')
    pickle.dump(log, write)
    write.close()
    print('** Log Saved!!')


def read_catalog():
    try:
        global data_file
        global last_id

        reader = open(data_file, 'rb')
        temp_list = pickle.load(reader)

        for item in temp_list:
            catalog.append(item)

        last = catalog[-1]
        last_id = last.id

        how_many = len(catalog)
        print('** loaded' + str(how_many) + 'items')
    except:
        print('** no data file found, database is empty')


def read_log():
    try:
        global logs_file
        reader = open(logs_file, 'rb')
        temp_list = pickle.load(reader)

        for entry in temp_list:
            log.append(entry)

        how_many = len(catalog)
        print('** loaded' + str(how_many) + 'logs')
    except:
        print('** no logs file found, database is empty')


# functions


def register_item():
    global last_id
    header('Register new item')
    title = input('New item title: ')
    cat = input('New item category: ')
    price = float(input('New item price: '))
    stock = int(input('New item stock: '))

    new_item = Item()  # <- how you create instances of a class (objects)
    last_id += 1  # no last_id ++
    new_item.id = last_id
    new_item.title = title
    new_item.category = cat
    new_item.price = price
    new_item.stock = stock

    catalog.append(new_item)
    add_log_event('New Item', 'Added: ' + str(last_id))

    print("Item created!")


def display_catalog():
    size = len(catalog)
    header('Current Catalog (' + str(size) + 'items)')

    print(
        '|' + 'ID'.rjust(2)
            + ' |' + ' Title'.ljust(27)
            + ' |' + ' Category'.ljust(15)
            + ' |' + ' Price'.ljust(10)
            + ' |' + ' Stock'.ljust(5) + '|')
    print('-'*70)

    for item in catalog:
        print(
            '|' + str(item.id).rjust(2)
            + ' |' + item.title.ljust(27)
            + ' |' + item.category.ljust(15)
            + ' |' + str(item.price).rjust(10)
            + ' |' + str(item.stock).rjust(5) + '|')
    print('-' * 70)


def display_oos():
    size = len(catalog)
    header('Out of stock(' + str(size) + 'items)')

    print(
        '|' + 'ID'.rjust(2)
            + ' |' + ' Title'.ljust(27)
            + ' |' + ' Category'.ljust(15)
            + ' |' + ' Price'.ljust(10)
            + ' |' + ' Stock'.ljust(5) + '|')
    print('-'*70)

    for item in catalog:

        if (item.stock == 0):
            print(
                '|' + str(item.id).rjust(2)
                + ' |' + item.title.ljust(27)
                + ' |' + item.category.ljust(15)
                + ' |' + str(item.price).rjust(10)
                + ' |' + str(item.stock).rjust(5) + '|')
        print('-' * 70)


def update_stock(opc):
    display_catalog()
    id = int(input('Please select an id from the list: '))
    # find the id = id
    found = False
    for item in catalog:
        if(item.id == id):
            found = True
            if(opc == 1):
                stock = int(input('New stock value: '))
                item.stock = stock
                print('Stock Updated!')
                add_log_event(
                    "SetStock", "Updated stock for item: " + str(item.id))
            else:
                sold = int(input('Number of items to sell: '))
                item.stock -= sold
                print('Sale registered')
                add_log_event("sale", "Sold " + str(sold) +
                              " items of item: " + str(item.id))

    if(not found):
        print('Error: Selected id does not exist, try again')


def calculate_stock_value():
    total = 0.0
    for item in catalog:
        total += (item.price * item.stock)

    print('Total stock value:' + str(total))


def remove_item():
    display_catalog()
    id = int(input('select the id of the item to remove: '))
    found = False
    for item in catalog:
        if(item.id == id):
            catalog.remove(item)
            found = True
            add_log_event("Remove", "Removed item: " + str(item.id))
            break
    if(found):
        print('Item removed from catalog')
    else:
        print('** Error: selected id is incorrect, try again!')


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime('%b/%d/%Y%T')


def add_log_event(event_type, event_description):
    entry = get_current_time() + '|  ' + event_type.ljust(10) + \
        ' | ' + event_description
    log.append(entry)
    save_log()


def print_log():
    header("Log of events")
    for entry in log:
        print(entry)


# instructions

# start menu

# first load all data
read_catalog()
read_log()
input('Press enter to continue')

opc = ''

while (opc != 'x'):
    clear()
    menu()
    print('\n')
    opc = input('Please select an option: ')

    if (opc == '1'):
        register_item()
        save_catalog()
    elif (opc == '2'):
        display_catalog()
    elif (opc == '3'):
        display_oos()
    elif(opc == '4'):
        update_stock(1)  # update stock
        save_catalog()
    elif(opc == '5'):
        calculate_stock_value()
    elif(opc == '6'):
        remove_item()
        save_catalog()
    elif(opc == '7'):
        update_stock(2)  # register sale
        save_catalog()
    elif(opc == '8'):
        print_log()

    input('Press Enter to continue...')
    clear()
