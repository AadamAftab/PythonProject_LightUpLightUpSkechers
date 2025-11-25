import json
import os
import random
import getpass  # <--- ENABLED for masking password input
from datetime import datetime, date # <--- ADDED for date validation
import time

# --- Constants ---
STATIONS = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Kanpur", "Nagpur", "Patna", "Bhopal", "Chandigarh",
]

# --- File Paths for Persistence ---
USERS_FILE = "cli_users.json"
TRAINS_FILE = "cli_trains.json"
BOOKINGS_FILE = "cli_bookings.json"

class BookingSystem:
    """Main class to handle all booking logic."""
    
    def __init__(self):
        # Load data from files, or create them if they don't exist
        self.users = self._load_data(USERS_FILE, {})
        self.bookings = self._load_data(BOOKINGS_FILE, [])
        self.trains_db = self._load_data(TRAINS_FILE, None)
        
        if self.trains_db is None:
            print("No train database found. Generating a new one...")
            self.trains_db = self._create_train_database()
            self._save_data(TRAINS_FILE, self.trains_db)
            print(f"Train database saved to {TRAINS_FILE}.")
            
        self.current_user = None

    def _load_data(self, filepath, default):
        """Helper to load JSON data from a file."""
        if not os.path.exists(filepath):
            return default
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Error reading {filepath}. Starting with empty data.")
            return default

    def _save_data(self, filepath, data):
        """Helper to save data to a JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error: Could not save data to {filepath}. {e}")

    def _create_train_database(self):
        """Generates a large, persistent mock database of trains."""
        db = {}
        train_prefixes = ["Rajdhani", "Shatabdi", "Duronto", "Garib Rath", "Superfast"]
        
        for from_stn in STATIONS:
            for to_stn in STATIONS:
                if from_stn == to_stn:
                    continue
                
                # Use a string key for JSON compatibility
                route_key = f"{from_stn}::{to_stn}"
                route_trains = []
                
                for i in range(random.randint(2, 6)):
                    train_name_base = random.choice(train_prefixes)
                    train_id = f"{from_stn[:2].upper()}{to_stn[:2].upper()}{random.randint(100, 999)}"
                    
                    dep_hour = random.randint(0, 23)
                    dep_min = random.choice([0, 15, 30, 45])
                    departure = f"{dep_hour:02d}:{dep_min:02d}"
                    
                    travel_hours = random.randint(4, 28)
                    arr_hour = (dep_hour + travel_hours) % 24
                    arr_min = random.choice([0, 15, 30, 45])
                    arrival_day = ""
                    if (dep_hour + travel_hours) >= 24:
                        days = (dep_hour + travel_hours) // 24
                        arrival_day = f" (D+{days})"
                    
                    arrival = f"{arr_hour:02d}:{arr_min:02d}{arrival_day}"
                    price = random.randint(300, 5000) // 10 * 10
                    seats = random.randint(10, 200)

                    route_trains.append({
                        "id": train_id,
                        "name": f"{train_name_base} {random.choice(['Express', 'Special'])}",
                        "departure": departure,
                        "arrival": arrival,
                        "price": price,
                        "seats": seats
                    })
                
                db[route_key] = route_trains
        return db

    # --- User Management ---
    
    def register(self):
        """Registers a new user."""
        print("\n--- Register New User ---")
        username = input("Enter new username: ").strip()
        
        if not username:
            print("Username cannot be empty.")
            return
            
        if username in self.users:
            print("Username already exists. Please try another.")
            return
            
        # --- REFINED: Use getpass ---
        password = getpass.getpass("Enter new password: ").strip()
        password_confirm = getpass.getpass("Confirm password: ").strip()
        # --- END REFINEMENT ---
        
        if not password:
            print("Password cannot be empty.")
            return
            
        if password != password_confirm:
            print("Passwords do not match. Registration failed.")
            return
            
        # In a real app, hash this password!
        self.users[username] = {"password": password}
        self._save_data(USERS_FILE, self.users)
        print(f"User '{username}' registered successfully!")

    def login(self):
        """Logs in an existing user."""
        print("\n--- User Login ---")
        username = input("Username: ").strip()
        
        # --- REFINED: Use getpass ---
        password = getpass.getpass("Password: ").strip()
        # --- END REFINEMENT ---
        
        user = self.users.get(username)
        
        if user and user["password"] == password:
            self.current_user = {"username": username}
            print(f"\nWelcome, {username}!")
            # self.user_menu() # Removed, main_menu loop handles this
        else:
            print("Invalid username or password.")
            
    def logout(self):
        """Logs out the current user."""
        print(f"\nLogging out {self.current_user['username']}...")
        self.current_user = None
        time.sleep(1)
        print("You have been logged out.")

    # --- Main Menus ---

    def main_menu(self):
        """Displays the main menu for all users."""
        print("\n" + "="*40)
        print("   Welcome to the BCC Train Booking CLI")
        print("="*40)
        
        while True:
            # If a user is logged in, show the user menu
            if self.current_user:
                self.user_menu()
                # When user_menu breaks (logout), self.current_user is None,
                # so the loop continues and shows the main menu.
            
            print("\n--- Main Menu ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                print("\nThank you for using BCC Train Services!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def user_menu(self):
        """Displays the menu for logged-in users."""
        # This loop continues as long as a user is logged in
        while self.current_user:
            print(f"\n--- {self.current_user['username']}'s Dashboard ---")
            print("1. Search & Book Train")
            print("2. View My Bookings")
            # --- REFINED: Added new option ---
            print("3. Cancel a Booking")
            print("4. Logout")
            # --- END REFINEMENT ---
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                self.search_and_book_trains()
            elif choice == '2':
                self.view_my_bookings()
            # --- REFINED: Added new choice ---
            elif choice == '3':
                self.cancel_booking()
            elif choice == '4':
                self.logout()
                # break: Exits the user_menu loop, returning to main_menu
                break 
            # --- END REFINEMENT ---
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    # --- Booking Functions ---

    def _get_station_choice(self, prompt):
        """Helper to get a valid station name from the user."""
        print(f"\n{prompt}")
        # Show stations for user to pick
        for i, station in enumerate(STATIONS, 1):
            print(f"  {i}. {station}", end="\n" if i % 5 == 0 else "\t")
        
        # --- REFINED: Added cancel option ---
        print("\n\n(Enter '0' or 'c' to cancel)")
        # --- END REFINEMENT ---
        
        while True:
            try:
                choice = input(f"Enter number (1-{len(STATIONS)}): ").strip()
                
                # --- REFINED: Handle cancel ---
                if choice.lower() in ['0', 'c']:
                    return None
                # --- END REFINEMENT ---
                
                if not choice.isdigit() or not (1 <= int(choice) <= len(STATIONS)):
                    print("Invalid number. Please try again.")
                else:
                    return STATIONS[int(choice) - 1]
            except (ValueError, IndexError):
                print("Invalid input. Please enter a number from the list.")

    # --- REFINED: New helper method for date validation ---
    def _get_validated_date(self):
        """Helper to get a valid, future date from the user."""
        while True:
            date_str = input("\nEnter Date (YYYY-MM-DD) (or 'c' to cancel): ").strip()
            if date_str.lower() == 'c':
                return None
            
            try:
                # Attempt to parse the date
                chosen_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
                
            if chosen_date < date.today():
                print("Date cannot be in the past. Please enter a valid date.")
                continue
                
            # If all checks pass, return the valid date string
            return date_str
    # --- END REFINEMENT ---

    def search_and_book_trains(self):
        """Guides user through searching and then booking a train."""
        print("\n--- Search for Trains ---")
        
        from_stn = self._get_station_choice("Select 'From' Station:")
        # --- REFINED: Check for cancel ---
        if not from_stn:
            print("Search cancelled.")
            return
        # --- END REFINEMENT ---
            
        to_stn = self._get_station_choice("Select 'To' Station:")
        # --- REFINED: Check for cancel ---
        if not to_stn:
            print("Search cancelled.")
            return
        # --- END REFINEMENT ---
        
        if from_stn == to_stn:
            print("From and To stations cannot be the same.")
            return

        # --- REFINED: Use new date validation method ---
        date_str = self._get_validated_date()
        if not date_str:
            print("Search cancelled.")
            return
        # --- END REFINEMENT ---
            
        route_key = f"{from_stn}::{to_stn}"
        # We get a *reference* to the list in trains_db, so
        # seat updates will be reflected in real-time.
        results = self.trains_db.get(route_key, [])
        
        if not results:
            print(f"\nSorry, no trains found for {from_stn} to {to_stn}.")
            return

        print(f"\n--- Results for {from_stn} to {to_stn} on {date_str} ---")
        print("="*70)
        print("  # | Train ID | Train Name           | Departs | Arrives   | Price (₹) | Seats")
        print("-"*70)
        
        for i, train in enumerate(results, 1):
            print(f" {i:>2} | {train['id']:<8} | {train['name']:<20} | {train['departure']:<7} | {train['arrival']:<9} | {train['price']:>9.2f} | {train['seats']}")
        
        print("="*70)
        
        # --- Booking Step ---
        while True:
            choice = input("\nEnter the number (#) of the train to book (or '0' to cancel): ").strip()
            
            if choice == '0':
                print("Booking cancelled.")
                return
                
            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(results):
                    selected_train = results[choice_index]
                    
                    # --- Ask for number of tickets ---
                    try:
                        num_tickets_str = input(f"Enter number of tickets (Available: {selected_train['seats']}): ").strip()
                        num_tickets = int(num_tickets_str)
                        
                        # Check against the *current* seat count
                        if not (1 <= num_tickets <= selected_train['seats']):
                            print(f"Invalid number. Must be between 1 and {selected_train['seats']}.")
                            # We 'continue' to ask for the *train number* again,
                            # in case the user wants to pick a different train.
                            continue 
                            
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue 
                    
                    # --- END ADDED SECTION ---

                    self.confirm_and_create_booking(selected_train, from_stn, to_stn, date_str, num_tickets)
                    return
                else:
                    print("Invalid train number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def confirm_and_create_booking(self, train, from_stn, to_stn, date_str, num_tickets):
        """Handles the final confirmation and saving of a booking."""
        
        total_price = train['price'] * num_tickets
        
        print("\n--- Confirm Your Booking ---")
        print(f"  Train:    {train['name']} ({train['id']})")
        print(f"  Route:    {from_stn} to {to_stn}")
        print(f"  Date:     {date_str}")
        print(f"  Time:     {train['departure']} - {train['arrival']}")
        print(f"  Tickets:  {num_tickets}")
        print(f"  Total Price: ₹{total_price:.2f} ({num_tickets} x ₹{train['price']:.2f})")
        
        confirm = input("\nConfirm booking? (y/n): ").strip().lower()
        
        if confirm == 'y':
            booking_id = f"BCC{int(time.time())}{random.randint(100, 999)}"
            
            booking_record = {
                "booking_id": booking_id,
                "username": self.current_user['username'],
                "booking_time": datetime.now().isoformat(),
                # Store a *copy* of train details at time of booking
                "train_details": train.copy(), 
                "route": {"from": from_stn, "to": to_stn},
                "travel_date": date_str,
                "num_tickets": num_tickets,
                "total_price": total_price
            }
            
            self.bookings.append(booking_record)
            self._save_data(BOOKINGS_FILE, self.bookings)
            
            # --- Update seat count in the main database ---
            # This is safe because 'train' is a reference to an
            # item inside self.trains_db
            try:
                train['seats'] -= num_tickets
                self._save_data(TRAINS_FILE, self.trains_db)
            except Exception as e:
                print(f"\nWarning: Could not update seat count. {e}")
            # --- END SECTION ---
            
            print("\nBooking Confirmed!")
            print(f"Your Booking ID is: {booking_id}")
            print("Thank you for booking with BCC!")
        else:
            print("Booking cancelled.")

    def view_my_bookings(self):
        """Displays all bookings for the currently logged-in user."""
        print("\n--- My Bookings ---")
        
        user_bookings = [b for b in self.bookings if b['username'] == self.current_user['username']]
        
        if not user_bookings:
            print("You have no bookings.")
            return
            
        # Sort by travel date, then booking time
        user_bookings.sort(key=lambda b: (b['travel_date'], b['booking_time']))
            
        for i, booking in enumerate(user_bookings, 1):
            print("\n" + "="*50)
            print(f"  Booking #{i} | ID: {booking['booking_id']}")
            print(f"  Booked On:   {booking['booking_time']}")
            print(f"  Travel Date: {booking['travel_date']}")
            print(f"  Route:       {booking['route']['from']} -> {booking['route']['to']}")
            print(f"  Train:       {booking['train_details']['name']} ({booking['train_details']['id']})")
            print(f"  Departure:   {booking['train_details']['departure']}")
            print(f"  Tickets:     {booking['num_tickets']}")
            print(f"  Total Price: ₹{booking['total_price']:.2f}")
            print("="*50)

    # --- REFINED: New method to cancel bookings ---
    def cancel_booking(self):
        """Allows a user to cancel a booking and restores seats."""
        print("\n--- Cancel a Booking ---")
        
        user_bookings = [b for b in self.bookings if b['username'] == self.current_user['username']]
        
        if not user_bookings:
            print("You have no bookings to cancel.")
            return
        
        print("Your current bookings:")
        for i, booking in enumerate(user_bookings, 1):
            print(f"\n  --- Booking #{i} ---")
            print(f"  ID: {booking['booking_id']}")
            print(f"  Date: {booking['travel_date']}")
            print(f"  Route: {booking['route']['from']} -> {booking['route']['to']}")
            print(f"  Train: {booking['train_details']['name']}")
            print(f"  Tickets: {booking['num_tickets']}")

        print("\n" + "="*50)
        
        while True:
            choice_str = input(f"Enter the number (#) of the booking to cancel (1-{len(user_bookings)}) (or '0' to go back): ").strip()
            
            if choice_str == '0':
                print("Cancellation aborted.")
                return
                
            try:
                choice_index = int(choice_str) - 1
                if 0 <= choice_index < len(user_bookings):
                    # Found the booking to cancel
                    booking_to_cancel = user_bookings[choice_index]
                    
                    # Confirm
                    confirm = input(f"Are you sure you want to cancel booking {booking_to_cancel['booking_id']}? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        # 1. Add seats back to trains_db
                        num_tickets = booking_to_cancel['num_tickets']
                        train_id = booking_to_cancel['train_details']['id']
                        route_key = f"{booking_to_cancel['route']['from']}::{booking_to_cancel['route']['to']}"
                        
                        try:
                            # Find the train in the master DB
                            for train in self.trains_db[route_key]:
                                if train['id'] == train_id:
                                    train['seats'] += num_tickets
                                    break
                            self._save_data(TRAINS_FILE, self.trains_db)
                        except Exception as e:
                            print(f"Error: Could not restore seat count. Please contact support. {e}")
                            # Don't proceed if we can't restore seats
                            return

                        # 2. Remove booking from self.bookings (the master list)
                        self.bookings.remove(booking_to_cancel)
                        self._save_data(BOOKINGS_FILE, self.bookings)
                        
                        print(f"\nBooking {booking_to_cancel['booking_id']} has been successfully cancelled.")
                        print(f"{num_tickets} seats have been restored.")
                        return
                    
                    else:
                        print("Cancellation aborted.")
                        return
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    # --- END REFINEMENT ---


# =============================================================================
# --- Main Execution ---
# =============================================================================

if __name__ == "__main__":
    system = BookingSystem()
    system.main_menu()