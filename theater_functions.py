

def get_row_data():
    """
    Returns rows
    :return: int number of rows in theater
    """
    while True:
        rows = input("Please enter the number of rows in your theater: ")
        try:
            rows = int(rows)
            if rows > 0:
                break
            print("Invalid input")
        except ValueError:
            print("Invalid input")
    return rows


def get_col_data():
    """
    Returns columns
    :return: int number of columns in theater
    """
    while True:
        columns = input("Please enter the number of seats in each row: ")
        try:
            columns = int(columns)
            if columns > 0:
                break
            print("Invalid input")
        except ValueError:
            print("Invalid input")
    return columns


def get_price_data(rows):
    """
    Returns prices
    :param rows: int number of rows in theater
    :return: int list of seat prices by row
    """
    prices = list()
    for i in range(1, rows + 1):
        while True:
            price = input("Please enter the seat price for row {}: ".format(i))
            try:
                price = float(price)
                if price < 0:
                    print("Invalid input")
                    continue
                break
            except ValueError:
                print("Invalid input")
        prices.append(price)
    return prices


def initialize_pull():
    """
    Returns rows, columns, and prices
    :return: tuple of data gathered
    """
    with open("theater.txt", "r") as file:
        rows = int(file.readline())
        columns = int(file.readline())
        prices = list()
        for price in file.readlines():
            prices.append(int(price))
    return (rows, columns, prices)


def initialize_push():
    """
    Returns rows, columns, prices
    :return: tuple of data gathered
    """
    with open("theater.txt", "w") as file:
        rows = get_row_data()
        columns = get_col_data()
        prices = get_price_data(rows)
        file.write(str(rows))
        file.write("\n")
        file.write(str(columns))
        file.write("\n")
        for price in prices:
            file.write(str(price))
            file.write("\n")
    return (rows, columns, prices)


def initialize(overwrite = False):
    """
    Returns rows, columns, prices, seating
    :param overwrite: bool whether or not to automatically reset the program
    :return: tuple of data gathered and a configured empty seating chart
    """
    if overwrite:
        with open("theater.txt", "w") as file:
            rows, columns, prices = initialize_push()
    else:
        try:
            with open("theater.txt", "r") as file:
                rows, columns, prices = initialize_pull()
        except FileNotFoundError:
            with open("theater.txt", "w") as file:
                rows, columns, prices = initialize_push()
    # Initialize the Table
    seating = list()
    for i in range(1, rows + 1):
        row = list()
        for j in range(1, columns + 1):
            row.append("#")
        seating.append(row)
    return (rows, columns, prices, seating)


def save_data(rows, columns, prices):
    """
    :param rows: int number of rows
    :param columns: int number of seats per row
    :param prices: int list of prices by row
    :return:
    """
    with open("theater.txt", "w") as f:
        f.write(str(rows))
        f.write("\n")
        f.write(str(columns))
        f.write("\n")
        for price in prices:
            f.write(str(price))
            f.write("\n")


def display_menu():
    """
    Returns choice
    :return: int choice made by the user
    """
    print("\nWelcome to TheOpera, the Ticket Assistance Program\n"
          "You may select: \n"
          "\t(1) Display a seating chart\n"
          "\t(2) Sell tickets\n"
          "\t(3) Display statistics about ticket sales and remaining seats\n"
          "\t(4) Reset the program\n"
          "\t(5) Exit the program\n")
    while True:
        choice = input("What would you like to do? ")
        try:
            choice = int(choice)
            if 0 < choice <= 5:
                break
            print("Invalid input")
        except ValueError:
            print("Invalid input")
    return choice


def display_chart(rows, columns, seating):
    """
    :param rows: int number of rows
    :param columns: int number of seats per row
    :param seating: string array of seating chart
    :return:
    """
    print("\t\t0        ", end='')
    for i in range (1, (columns // 10) + 1):
        print(i%10, end='')
        print("         ", end='')
    print("\n\t\t", end='')
    for i in range(1, columns + 1):
        print(i%10, end='')
    print("\n", end='')
    for i in range(1, rows + 1):
        print("Row\t{}\t".format(i), end='')
        for j in range(1, columns + 1):
            print(seating[i-1][j-1], end='')
        print("\n", end='')


def seats_free(seating, row_choice, column_choice, seat_range):
    """
    Returns available
    :param seating: string array of seating chart
    :param row_choice: int specific row
    :param column_choice: int specific seat
    :param seat_range: int number of seats
    :return: bool whether or not the given seat is available
    """
    available = True
    for i in range(column_choice - 1, (column_choice - 1) + seat_range):
        if seating[row_choice - 1][i] == '*':
            available = False
    return available


def purchase_seats(seating, prices, row_choice, column_choice, seat_range):
    """
    Returns prices[row_choice - 1] * seat_range
    :param seating: string array of seating chart
    :param prices: int list of prices by row
    :param row_choice: int specific row
    :param column_choice: int specific seat
    :param seat_range: int number of seats
    :return: float total money earned from purchase
    """
    for i in range(column_choice - 1, (column_choice - 1) + seat_range):
        seating[row_choice - 1][i] = '*'
    return prices[row_choice - 1] * seat_range


def sell_tickets(rows, columns, prices, seating):
    """
    Returns revenue
    :param rows: int number of rows
    :param columns: int number of seats per row
    :param prices: int list of prices by row
    :param seating: string array of seating chart
    :return: float total money earned from purchase
    """
    # Determine the purchase type
    while True:
        purchase_type = input("Would you like to buy a (S)ingle seat or a (R)ange? ")
        if purchase_type == 'S' or purchase_type == 'R':
            break
        else:
            print("Invalid input")

    # Determine the number of tickets being purchased
    if purchase_type == 'S':
        seat_range = 1
    else:
        while True:
            seat_range = input("How many seats would you like to purchase? ")
            try:
                seat_range = int(seat_range)
                if 0 < seat_range <= columns:
                    break
                else:
                    print("Invalid input")
            except ValueError:
                print("Invalid input")

    # Determine which seats are being purchased
    display_chart(rows, columns, seating)
    if purchase_type == 'S':
        print("Please enter the row, and the seat number of the seat being purchased.")
    else:
        print("Please enter the row, and the seat number of the first seat in the range being purchased.")
    while True:
        row_choice = input("Row number: ")
        column_choice = input("Seat number: ")
        try:
            row_choice = int(row_choice)
            column_choice = int(column_choice)
            row_choice_valid = 0 < row_choice <= rows
            column_choice_valid = 0 < column_choice <= (columns - seat_range + 1)
            available_seats = seats_free(seating, row_choice, column_choice, seat_range)
            if row_choice_valid and column_choice_valid and available_seats:
                break
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")

    # Purchase the seats and display final bill
    revenue = purchase_seats(seating, prices, row_choice, column_choice, seat_range)
    print("You owe ${}".format(revenue))
    return revenue


def display_stats(rows, columns, seating, revenue):
    """
    :param rows: int number of rows
    :param columns: int number of columns
    :param seating: string array of seating chart
    :param revenue: total money earned
    :return:
    """
    print("Total ticket sales: ${}".format(revenue))
    sold = 0
    for i in range(0, rows):
        for j in range(0, columns):
            if seating[i][j] == '*':
                sold += 1
    print("Total tickets sold: {}".format(sold))
    available = (rows*columns) - sold
    print("Total seats still available: {}".format(available))