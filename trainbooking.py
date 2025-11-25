#Importing necessary tools to build project
import json #Data storage helper (for reading and writing JSON files)
import os #to access file system functions (like checking if a file exists)
import random #to generate random numbers for train data (like price, seats)
import getpass #to hide password input on the command line
from datetime import datetime, date #to work with dates and times (e.g., check for future dates)
import time #to pause the program or generate time-based IDs

#station data
STATIONS = [ # A list of city names used as train stations
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Kanpur", "Nagpur", "Patna", "Bhopal", "Chandigarh",
]

#json data files
USERS_FILE = "cli_users.json" # The file name for storing user accounts
TRAINS_FILE = "cli_trains.json" # The file n   ame for storing the train schedule and seats
BOOKINGS_FILE = "cli_bookings.json" # The file name for storing confirmed bookings

class BookingSystem: # This is the main blueprint (class) for the entire application
    
    #slabbed discount rates according to age
    DISCOUNT_RATES = { # A dictionary holding our fixed discount percentages
        "CHILD": 0.50,       # 50% discount
        "INFANT": 1.00,      # 100% discount (meaning free ticket)
        "SENIOR_CITIZEN": 0.30, # 30% discount
        "OFF_PEAK_SEASON": 0.10, # 10% extra discount during slow months
    }

    #class attributes for project, loading json data files data using class function load data
    def __init__(self): # This function runs first when the app starts
        self.users = self.load_data(USERS_FILE, {}) # Load users; if file missing, use empty dictionary {}
        self.bookings = self.load_data(BOOKINGS_FILE, []) # Load bookings; if file missing, use empty list []
        self.trains_db = self.load_data(TRAINS_FILE, None) # Load trains; if file missing, use None
        
        if self.trains_db is None: # Checking if the train data failed to load (it returned None)
            print("No train database found. Generating a new one...") # Tell the user what's happening
            self.trains_db = self._create_train_database() # calling function to create a new mock database
            self._save_data(TRAINS_FILE, self.trains_db) # saving the new database to the file
            print(f"Train database saved to {TRAINS_FILE}.") # Confirmation message
            
        self.current_user = None # setting the default state: no user is logged in

    def load_data(self, filepath, default): # Function to safely load data from a JSON file
        if not os.path.exists(filepath):# checking if the file exists using the os module
            return default # If the file isn't there, return the default value (e.g., {} or [])
        try: # Start trying to read the file
            with open(filepath, 'r') as f: # Open the file in read mode ('r') as 'f'
                return json.load(f) # Convert the JSON text in the file into a Python object (like a dictionary)
        except json.JSONDecodeError: # If the file is broken/corrupted (not valid JSON)
            print(f"Warning: Error reading {filepath}. Starting with empty data.") # Tell the user about the error
            return default # Return the safe default value instead of crashing

    def _save_data(self, filepath, data): # Function to save a Python object back to a JSON file
        try: # Start trying to write the file
            with open(filepath, 'w') as f: # Open the file in write mode ('w')—this overwrites any old data
                json.dump(data, f, indent=4) # Convert the Python 'data' object to JSON text and write it to file 'f'. Indent=4 makes it readable.
        except IOError as e: # Catch errors if the system prevents saving (e.g., permissions)
            print(f"Error: Could not save data to {filepath}. {e}") # Print an error message

    def _create_train_database(self): # Function to make up a large list of train routes
        db = {} # empty dictionary to hold all the routes and their trains
        train_prefixes = ["Rajdhani", "Shatabdi", "Duronto", "Garib Rath", "Superfast"] # Names to pick from
        
        for from_stn in STATIONS: # Loop through every station as a starting point
            for to_stn in STATIONS: # Loop through every station as an ending point
                if from_stn == to_stn: # Skip if the start and end stations are the same
                    continue 
                
                route_key = f"{from_stn}::{to_stn}" # Create a key like "Mumbai::Delhi"
                route_trains = [] # Start an empty list to hold trains for this route
                
                for i in range(random.randint(2, 6)): # Create a random number of trains (2 to 6) for this route
                    train_name_base = random.choice(train_prefixes) # Pick a random base name
                    train_id = f"{from_stn[:2].upper()}{to_stn[:2].upper()}{random.randint(100, 999)}" # Create a unique train ID
                    
                    dep_hour = random.randint(0, 23) # Pick a random hour (0 to 23)
                    dep_min = random.choice([0, 15, 30, 45]) # Pick a random minute
                    departure = f"{dep_hour:02d}:{dep_min:02d}" # Format the time (e.g., 08:15)
                    
                    travel_hours = random.randint(4, 28) # Pick a random travel duration
                    arr_hour = (dep_hour + travel_hours) % 24 # Calculate the arrival hour, wrapping around 24
                    arr_min = random.choice([0, 15, 30, 45]) # Pick a random arrival minute
                    arrival_day = "" # Initialize the arrival day marker
                    if (dep_hour + travel_hours) >= 24: # Check if the journey takes more than 24 hours
                        days = (dep_hour + travel_hours) // 24 # Calculate the number of days taken
                        arrival_day = f" (D+{days})" # Add a marker like (D+1)
                    
                    arrival = f"{arr_hour:02d}:{arr_min:02d}{arrival_day}" # Format the final arrival time
                    price = random.randint(300, 5000) // 10 * 10 # Create a random price rounded to the nearest 10
                    seats = random.randint(10, 200) # Give the train a random number of seats

                    route_trains.append({ # Add the train's details as a dictionary to the list
                        "id": train_id,
                        "name": f"{train_name_base} {random.choice(['Express', 'Special'])}",
                        "departure": departure,
                        "arrival": arrival,
                        "price": price,
                        "seats": seats
                    })
                
                db[route_key] = route_trains # Store the list of trains under the route key
        return db # Return the completed database

    def register(self): # Function to create a new user account
        print("\n--- Register New User ---")
        username = input("Enter new username: ").strip() # Get the desired username
        if not username: # Check if the username is empty
            print("Username cannot be empty.")
            return
        if username in self.users: # Check if the username already exists in the loaded data
            print("Username already exists. Please try another.")
            return
        password = getpass.getpass("Enter new password: ").strip() # Get password (hidden input)
        password_confirm = getpass.getpass("Confirm password: ").strip() # Get password confirmation
        if not password: # Check if the password is empty
            print("Password cannot be empty.")
            return
        if password != password_confirm: # Check if the passwords match
            print("Passwords do not match. Registration failed.")
            return
        self.users[username] = {"password": password} # Store the new user's password in the users dictionary
        self._save_data(USERS_FILE, self.users) # Save the updated user list to the file
        print(f"User '{username}' registered successfully!") # Success message

    def login(self): # Function to log in an existing user
        print("\n--- User Login ---")
        username = input("Username: ").strip() # Get the username
        password = getpass.getpass("Password: ").strip() # Get the password (hidden input)
        user = self.users.get(username) # Try to find the user in the dictionary
        if user and user["password"] == password: # Check if the user exists AND the password matches
            self.current_user = {"username": username} # Set the session state to the logged-in user
            print(f"\nWelcome, {username}!") # Welcome message
        else:
            print("Invalid username or password.") # Failure message
            
    def logout(self): # Function to log out the current user
        print(f"\nLogging out {self.current_user['username']}...")
        self.current_user = None # Clear the session state (no one is logged in now)
        time.sleep(1) # Pause for 1 second for effect
        print("You have been logged out.")

    def main_menu(self): # The main menu loop of the application
        print("\n" + "="*40)
        print("    Welcome to the BCC Train Booking CLI")
        print("="*40)
        while True: # Keep looping until the user chooses to exit
            if self.current_user: # Check if someone is logged in
                self.user_menu() # Show the user dashboard
                
            print("\n--- Main Menu ---") # Show the main options for anonymous users
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ").strip() # Get user choice
            
            if choice == '1': # If choice is 1
                self.register() # Call the register function
            elif choice == '2': # If choice is 2
                self.login() # Call the login function
            elif choice == '3': # If choice is 3
                print("\nThank you for using BCC Train Services!")
                break # Exit the infinite loop (ending the application)
            else:
                print("Invalid choice. Please enter 1, 2, or 3.") # Handle bad input

    def user_menu(self): # The dashboard shown to logged-in users
        while self.current_user: # Keep looping as long as a user is logged in
            print(f"\n--- {self.current_user['username']}'s Dashboard ---")
            print("1. Search & Book Train")
            print("2. View My Bookings")
            print("3. Cancel a Booking")
            print("4. Logout")
            
            choice = input("Enter your choice (1-4): ").strip() # Get user choice
            
            if choice == '1': # If choice is 1
                self.search_and_book_trains() # Start the booking process
            elif choice == '2': # If choice is 2
                self.view_my_bookings() # View existing bookings
            elif choice == '3': # If choice is 3
                self.cancel_booking() # Start the cancellation process
            elif choice == '4': # If choice is 4
                self.logout() # Log out the user
                break # Exit this user_menu loop
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.") # Handle bad input

    def _get_station_choice(self, prompt): # Helper function to get a valid station choice from a list
        print(f"\n{prompt}") # Print the question (e.g., "Select 'From' Station:")
        for i, station in enumerate(STATIONS, 1): # Loop through the station list, starting count at 1
            print(f"  {i}. {station}", end="\n" if i % 5 == 0 else "\t") # Print the number and name, 5 per line
        print("\n\n(Enter '0' or 'c' to cancel)")
        while True: # Keep looping until valid input is given
            try:
                choice = input(f"Enter number (1-{len(STATIONS)}): ").strip() # Get the number input
                if choice.lower() in ['0', 'c']: # Check if user wants to cancel
                    return None # Return nothing (cancel the operation)
                if not choice.isdigit() or not (1 <= int(choice) <= len(STATIONS)): # Check if it's a number and in the correct range
                    print("Invalid number. Please try again.") # Print error
                else:
                    return STATIONS[int(choice) - 1] # Return the station name (using index choice - 1)
            except (ValueError, IndexError): # Catch errors if input is not a number
                print("Invalid input. Please enter a number from the list.")

    def _get_validated_date(self): # Helper function to get a valid date in the future
        while True: # Keep looping until a valid date is entered
            date_str = input("\nEnter Date (YYYY-MM-DD) (or 'c' to cancel): ").strip() # Get date input
            if date_str.lower() == 'c': # Check if user wants to cancel
                return None # Cancel the operation
            try:
                chosen_date = datetime.strptime(date_str, "%Y-%m-%d").date() # Try to convert the string to a date object in YYYY-MM-DD format
            except ValueError: # Catch error if the format is wrong
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue # Go back to the start of the loop
            if chosen_date < date.today(): # Check if the date is in the past
                print("Date cannot be in the past. Please enter a valid date.")
                continue # Go back to the start of the loop
            return date_str # Return the valid date string

    def _calculate_discounted_price(self, base_price, travel_date_str, num_adults, num_infants, num_children, num_seniors): # Function to calculate the final ticket price
        price_adults = base_price * num_adults # Price for adults (full price)
        
        infant_discount_rate = self.DISCOUNT_RATES["INFANT"] # Get the 100% infant discount rate
        price_infants = base_price * num_infants * (1 - infant_discount_rate) # Calculate infant price (should be 0)
        infant_savings = base_price * num_infants * infant_discount_rate # Calculate infant savings
        
        child_discount_rate = self.DISCOUNT_RATES["CHILD"] # Get the 50% child discount rate
        price_children = base_price * num_children * (1 - child_discount_rate) # Calculate child price (50% of base)
        child_savings = base_price * num_children * child_discount_rate # Calculate child savings
        
        senior_discount_rate = self.DISCOUNT_RATES["SENIOR_CITIZEN"] # Get the 30% senior discount rate
        price_seniors = base_price * num_seniors * (1 - senior_discount_rate) # Calculate senior price (70% of base)
        senior_savings = base_price * num_seniors * senior_discount_rate # Calculate senior savings
        
        subtotal = price_adults + price_infants + price_children + price_seniors # Calculate total price after category discounts
        total_category_discount = infant_savings + child_savings + senior_savings # Sum up all category savings
        
        season_savings = 0.0 # Initialize season savings to zero
        try:
            travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d").date() # Convert date string back to date object
            if travel_date.month in [1, 2]: # Check if the month is January (1) or February (2)
                season_discount_rate = self.DISCOUNT_RATES["OFF_PEAK_SEASON"] # Get the 10% season discount rate
                season_savings = subtotal * season_discount_rate # Calculate the season discount on the subtotal
        except ValueError:
            pass # Ignore if the date was somehow still bad
        
        final_total_price = subtotal - season_savings # Calculate final price by subtracting season savings
        total_discount = total_category_discount + season_savings # Calculate total final discount
        
        return { # Return a dictionary containing the detailed pricing breakdown
            "final_price": final_total_price, # The final amount due
            "base_price_per_ticket": base_price,
            "adults_tickets": num_adults, # Count of adults
            "infant_tickets": num_infants, # Count of infants
            "children_tickets": num_children, # Count of children
            "seniors_tickets": num_seniors, # Count of seniors
            "subtotal": subtotal, # Total before seasonal discount
            "total_discount": total_discount, # Total discount amount
            "breakdown": { # More detail on where savings came from
                "infant_savings": infant_savings,
                "child_savings": child_savings,
                "senior_savings": senior_savings,
                "season_savings": season_savings,
            }
        }
    
    def search_and_book_trains(self): # Function to handle searching and initial booking steps
        print("\n--- Search for Trains ---")
        
        from_stn = self._get_station_choice("Select 'From' Station:") # Get starting station
        if not from_stn: return # Exit if user canceled
        to_stn = self._get_station_choice("Select 'To' Station:") # Get destination station
        if not to_stn: return # Exit if user canceled
        
        if from_stn == to_stn: # Check for same station error
            print("From and To stations cannot be the same.")
            return

        date_str = self._get_validated_date() # Get validated date
        if not date_str: return # Exit if user canceled
            
        route_key = f"{from_stn}::{to_stn}" # Create the route key
        results = self.trains_db.get(route_key, []) # Get list of trains for this route (or empty list)
        
        if not results: # If the results list is empty
            print(f"\nSorry, no trains found for {from_stn} to {to_stn}.")
            return

        print(f"\n--- Results for {from_stn} to {to_stn} on {date_str} (Base Price) ---")
        print("="*70) # Print separator
        print("  # | Train ID | Train Name           | Departs | Arrives   | Price (₹) | Seats") # Print header
        print("-"*70)
        
        for i, train in enumerate(results, 1): # Loop through the found trains and display them
            print(f" {i:>2} | {train['id']:<8} | {train['name']:<20} | {train['departure']:<7} | {train['arrival']:<9} | {train['price']:>9.2f} | {train['seats']}")#>n <m are used for indentations
        
        print("="*70)
        
        while True: # Loop for the user to select a train
            choice = input("\nEnter the number (#) of the train to book (or '0' to cancel): ").strip() # Get train number
            
            if choice == '0': # Check if user wants to cancel
                print("Booking cancelled.")
                return
                
            try:
                choice_index = int(choice) - 1 # Convert choice to list index
                if 0 <= choice_index < len(results): # Check if the index is valid
                    selected_train = results[choice_index] # Get the chosen train's details
                    
                    try:
                        print(f"\n--- Ticket Selection (Available: {selected_train['seats']}) ---")
                        # Get number of tickets for each category from user
                        num_adults = int(input("Number of Adult tickets (Full Price): ").strip() or 0)
                        num_infants = int(input("Number of Infant tickets (0-5 yrs, FREE): ").strip() or 0)
                        num_children = int(input("Number of Child tickets (5-12 yrs, 50% Off): ").strip() or 0)
                        num_seniors = int(input("Number of Senior Citizen tickets (30% Off): ").strip() or 0)
                        
                        num_tickets = num_adults + num_infants + num_children + num_seniors # Calculate total tickets
                        
                        if num_tickets == 0: # Check if no tickets were selected
                            print("You must book at least one ticket.")
                            continue # Restart the loop for train selection

                        if not (1 <= num_tickets <= selected_train['seats']): # Check if total tickets exceed available seats
                            print(f"Total tickets ({num_tickets}) exceeds available seats ({selected_train['seats']}).")
                            continue # Restart the loop for train selection
                            
                    except ValueError: # Catch error if input was not a number
                        print("Invalid input. Please enter a valid number for each category.")
                        continue # Restart the loop for train selection
                    
                    pricing_details = self._calculate_discounted_price( # Calculate final price details
                        selected_train['price'], date_str, 
                        num_adults, num_infants, num_children, num_seniors
                    )

                    self.confirm_and_create_booking( # Move to the confirmation step
                        selected_train, from_stn, to_stn, date_str, 
                        num_tickets, pricing_details
                    )
                    return # Exit the function after moving to confirmation
                else:
                    print("Invalid train number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def confirm_and_create_booking(self, train, from_stn, to_stn, date_str, num_tickets, pricing_details): # Final confirmation and booking creation
        final_total_price = pricing_details['final_price'] # Get the final price
        
        print("\n--- Confirm Your Booking ---") # Display booking details for confirmation
        print(f"  Train:    {train['name']} ({train['id']})")
        print(f"  Route:    {from_stn} to {to_stn}")
        print(f"  Date:     {date_str}")
        print(f"  Time:     {train['departure']} - {train['arrival']}")
        
        print("\n--- Price Breakdown ---") # Display price and ticket breakdown
        print(f"  Base Price (per ticket): ₹{pricing_details['base_price_per_ticket']:.2f}")
        print(f"  Adult Tickets (Normal):  {pricing_details['adults_tickets']}")
        print(f"  Infant Tickets (0-5, Free): {pricing_details['infant_tickets']}")
        print(f"  Child Tickets (5-12, 50% Off): {pricing_details['children_tickets']}")
        print(f"  Senior Tickets (Old, 30% Off): {pricing_details['seniors_tickets']}")
        print(f"  Total Tickets:           {num_tickets}")
        
        category_savings = (pricing_details['breakdown']['infant_savings'] + # Calculate total savings from categories
                            pricing_details['breakdown']['child_savings'] + 
                            pricing_details['breakdown']['senior_savings'])
        print(f"  Discount (Category Fares): - ₹{category_savings:.2f}") # Display category savings
        
        if pricing_details['breakdown']['season_savings'] > 0: # Check if seasonal discount was applied
             print(f"  Discount (Off-Season):   - ₹{pricing_details['breakdown']['season_savings']:.2f} (10% General)") # Display seasonal savings
        
        print(f"  TOTAL SAVINGS:           ₹{pricing_details['total_discount']:.2f}") # Display total savings
        print(f"  TOTAL PAYABLE:           ₹{final_total_price:.2f}") # Display final amount
        
        confirm = input("\nConfirm booking? (y/n): ").strip().lower() # Get final confirmation
        
        if confirm == 'y': # If confirmed
            booking_id = f"BCC{int(time.time())}{random.randint(100, 999)}" # Create a unique booking ID
            
            booking_record = { # Create the full booking record dictionary
                "booking_id": booking_id,
                "username": self.current_user['username'],
                "booking_time": datetime.now().isoformat(),
                "train_details": train.copy(), 
                "route": {"from": from_stn, "to": to_stn},
                "travel_date": date_str,
                "num_tickets": num_tickets,
                "pricing": pricing_details, # Store the full pricing breakdown
                "total_price": final_total_price # Store the final price
            }
            
            self.bookings.append(booking_record) # Add the new record to the master list
            self._save_data(BOOKINGS_FILE, self.bookings) # Save the updated bookings file
            
            try: # Try to update the seat count in the master train list
                train['seats'] -= num_tickets # Reduce available seats on the chosen train
                self._save_data(TRAINS_FILE, self.trains_db) # Save the updated train database
            except Exception as e: # Catch any error during seat update
                print(f"\nWarning: Could not update seat count. {e}")
            
            print("\nBooking Confirmed!")
            print(f"Your Booking ID is: {booking_id}")
            print("Thank you for booking with BCC!")
        else:
            print("Booking cancelled.") # If user chose 'n'

    def view_my_bookings(self): # Function to display all the user's bookings
        print("\n--- My Bookings ---")
        
        user_bookings = [b for b in self.bookings if b['username'] == self.current_user['username']] # Filter the master list to get only the current user's bookings
        
        if not user_bookings: # Check if the user has any bookings
            print("You have no bookings.")
            return
            
        user_bookings.sort(key=lambda b: (b['travel_date'], b['booking_time'])) # Sort bookings by travel date then time
            
        for i, booking in enumerate(user_bookings, 1): # Loop through and display each booking
            is_discounted = 'pricing' in booking # Check if the booking has the detailed pricing data
            
            print("\n" + "="*50)
            print(f"  Booking #{i} | ID: {booking['booking_id']}")
            print(f"  Booked On:   {booking['booking_time']}")
            print(f"  Travel Date: {booking['travel_date']}")
            print(f"  Route:       {booking['route']['from']} -> {booking['route']['to']}")
            print(f"  Train:       {booking['train_details']['name']} ({booking['train_details']['id']})")
            print(f"  Departure:   {booking['train_details']['departure']}")
            
            if is_discounted: # If the detailed pricing data is available
                p = booking['pricing']
                print(f"  Tickets:     {booking['num_tickets']} (A:{p['adults_tickets']} | I:{p['infant_tickets']} | C:{p['children_tickets']} | S:{p['seniors_tickets']})") # Show ticket breakdown
                print(f"  Total Price: ₹{booking['total_price']:.2f}")
                
                total_savings = p['total_discount']
                if total_savings > 0.01: # Check if there was any significant saving
                    print(f"  SAVINGS:     ₹{total_savings:.2f}")
            else: # Fallback if for some reason the pricing data is missing
                print(f"  Tickets:     {booking['num_tickets']}")
                print(f"  Total Price: ₹{booking['total_price']:.2f}")
                
            print("="*50)

    def cancel_booking(self): # Function for handling partial or full cancellation
        print("\n--- Cancel or Modify a Booking ---")
        
        user_bookings = [b for b in self.bookings if b['username'] == self.current_user['username']] # Get user's bookings
        
        if not user_bookings: # If no bookings found
            print("You have no bookings to cancel.")
            return
        
        print("Your current bookings:") # List the user's bookings
        for i, booking in enumerate(user_bookings, 1):
            p = booking['pricing']
            print(f"\n  --- Booking #{i} | ID: {booking['booking_id']} ---")
            print(f"  Tickets Remaining: {booking['num_tickets']}")
            print(f"    Adults: {p.get('adults_tickets', 0)} | Infants: {p.get('infant_tickets', 0)} | Children: {p.get('children_tickets', 0)} | Seniors: {p.get('seniors_tickets', 0)}") # Show breakdown of remaining tickets
        
        print("\n" + "="*80)
        
        while True: # Loop to select the booking to modify
            choice_str = input(f"Enter the number (#) of the booking to modify (1-{len(user_bookings)}) (or '0' to go back): ").strip() # Get choice
            
            if choice_str == '0': # If user cancels
                print("Modification aborted.")
                return
                
            try:
                choice_index = int(choice_str) - 1 # Convert choice to index
                if 0 <= choice_index < len(user_bookings): # Check if valid choice
                    booking_to_modify = user_bookings[choice_index] # Get the selected booking
                    p = booking_to_modify['pricing'] # Get the pricing details
                    current_tickets = booking_to_modify['num_tickets'] # Get total current tickets
                    
                    if current_tickets == 0:
                        print("This booking has 0 tickets remaining.")
                        continue

                    cancellations = {} # Dictionary to store how many of each category the user cancels
                    categories = [ # List of all categories to loop through
                        ('Adult', 'adults_tickets'),
                        ('Infant (FREE)', 'infant_tickets'),
                        ('Child (50% Off)', 'children_tickets'),
                        ('Senior (30% Off)', 'seniors_tickets'),
                    ]
                    
                    total_cancelled_seats = 0 # Counter for total seats cancelled
                    total_refund_gross = 0.0 # Counter for the refund before fee
                    
                    print(f"\n--- Enter number of tickets to cancel (Current Total: {current_tickets}) ---")
                    
                    for display_name, key in categories: # Loop through each ticket category
                        remaining = p.get(key, 0) # Get how many of this category are left
                        if remaining > 0: # If there are any left to cancel
                            while True: # Loop to get valid cancellation count for this category
                                try:
                                    cancel_count = int(input(f"Cancel {display_name} (Remaining: {remaining}): ").strip() or 0) # Get cancellation count
                                    if 0 <= cancel_count <= remaining: # Check if count is valid (0 to remaining)
                                        cancellations[key] = cancel_count # Store the count
                                        total_cancelled_seats += cancel_count # Add to total seats cancelled
                                        
                                        base_price = p['base_price_per_ticket'] # Get the base price of the ticket
                                        
                                        # Calculate the price originally paid for one ticket in this category
                                        if key == 'adults_tickets':
                                             ticket_paid_price = base_price * 1.0 
                                        elif key == 'infant_tickets':
                                            ticket_paid_price = 0.0
                                        elif key == 'children_tickets':
                                            ticket_paid_price = base_price * (1.0 - self.DISCOUNT_RATES['CHILD'])
                                        elif key == 'seniors_tickets':
                                            ticket_paid_price = base_price * (1.0 - self.DISCOUNT_RATES['SENIOR_CITIZEN'])
                                        
                                        total_refund_gross += cancel_count * ticket_paid_price # Add the calculated refund amount to the total gross refund
                                        break # Exit inner while loop
                                    else:
                                        print(f"Invalid input. Must be between 0 and {remaining}.")
                                except ValueError:
                                    print("Invalid input. Please enter a number.")
                        else:
                            cancellations[key] = 0 # Store 0 if none were available to cancel

                    
                    if total_cancelled_seats == 0: # Check if the user didn't cancel anything after all the prompts
                        print("No seats selected for cancellation. Modification aborted.")
                        return
                    
                    # Confirm the cancellation
                    if total_cancelled_seats == current_tickets: # Check if it's a full cancellation
                        confirm_prompt = f"Are you sure you want to cancel ALL {total_cancelled_seats} tickets? (y/n): "
                    else: # It's a partial cancellation
                        confirm_prompt = f"Are you sure you want to cancel {total_cancelled_seats} tickets? (y/n): "

                    confirm = input(confirm_prompt).strip().lower()
                    
                    if confirm != 'y': # If user aborts
                        print("Cancellation aborted.")
                        return

                    cancellation_fee_rate = 0.10 # Set the mock cancellation fee rate
                    cancellation_fee = total_refund_gross * cancellation_fee_rate # Calculate the fee
                    net_refund = total_refund_gross - cancellation_fee # Calculate the final refund amount
                    
                    new_tickets = current_tickets - total_cancelled_seats # Calculate remaining tickets
                    new_total_price = booking_to_modify['total_price'] - net_refund # Calculate the new total price of the remaining booking
                    
                    if new_tickets == 0: # If all tickets were cancelled (full cancellation)
                        self.bookings.remove(booking_to_modify) # Remove the entire booking record
                        status_msg = "fully cancelled"
                    else: # If it's a partial cancellation
                        for key, count in cancellations.items(): # Loop through the cancelled categories
                            p[key] -= count # Decrease the count of that category in the pricing dictionary
                        
                        booking_to_modify['num_tickets'] = new_tickets # Update total ticket count
                        booking_to_modify['total_price'] = new_total_price # Update total price
                        status_msg = f"partially cancelled ({total_cancelled_seats} seats removed)"
                        
                    train_id = booking_to_modify['train_details']['id'] # Get train ID
                    route_key = f"{booking_to_modify['route']['from']}::{booking_to_modify['route']['to']}" # Get route key
                    
                    try: # Try to restore seats
                        for train in self.trains_db[route_key]: # Find the correct train in the database
                            if train['id'] == train_id:
                                train['seats'] += total_cancelled_seats # Add the cancelled seats back
                                break
                        self._save_data(TRAINS_FILE, self.trains_db) # Save the updated train database
                    except Exception as e:
                        print(f"Error: Could not restore seat count. Please contact support. {e}")
                        pass # Continue even if seat restore fails
                    
                    self._save_data(BOOKINGS_FILE, self.bookings) # Save the updated booking list
                    
                    # Print success and financial details
                    print(f"\nBooking {booking_to_modify['booking_id']} has been {status_msg}.")
                    print(f"Refund processed for {total_cancelled_seats} seats.")
                    print(f"Total Gross Refund: ₹{total_refund_gross:.2f}")
                    print(f"Cancellation Fee ({cancellation_fee_rate*100:.0f}%): ₹{cancellation_fee:.2f}")
                    print(f"NET REFUND: ₹{net_refund:.2f}")
                    return
                else:
                    print("Invalid number. Please try again.") # Invalid booking selection
            except ValueError:
                print("Invalid input. Please enter a number.") # Non-numeric input for selection

if __name__ == "__main__": # Code starts execution here
    system = BookingSystem() # Create the main BookingSystem object (runs __init__)
    system.main_menu() # Start the main application menu