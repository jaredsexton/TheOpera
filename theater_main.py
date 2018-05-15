

import theater_functions

# Initialize all variables
rows, columns, prices, seating = theater_functions.initialize()
revenue = 0

while True:
    decision = theater_functions.display_menu()
    if decision == 1:  # Display a seating chart
        theater_functions.display_chart(rows, columns, seating)
    elif decision == 2:  # Sell Tickets
        revenue += theater_functions.sell_tickets(rows, columns, prices, seating)
    elif decision == 3:  # Display statistics about ticket sales and remaining seats
        theater_functions.display_stats(rows, columns, seating, revenue)
    elif decision == 4:  # Reset the program
        rows, columns, prices, seating = theater_functions.initialize(True)
    elif decision == 5:  # Exit the program
        theater_functions.save_data(rows, columns, prices)
        break
    else:
        print("Invalid input")




































