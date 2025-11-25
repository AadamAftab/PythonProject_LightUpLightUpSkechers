# PythonProject_LightUpLightUpSkechers
PythonProject 2025 - Team LightUp Skechers
Train Booking CLI System (Python Beginner Project)

This project is a Command Line Interface (CLI) application built using basic Python to simulate a simplified railway ticket reservation system. It uses core programming concepts like Object-Oriented Programming (OOP), Data Persistence (saving data to files), and Input/Output (I/O) to build a practical application.

The goal was to mimic real-world features like passenger categorization and partial ticket cancellation found in systems like IRCTC.

Use cases:
1. Object-Oriented Programming:
   Everything runs inside the BookingSystem class. This organizes all the logic (login, searching, booking) into one neat blueprint.

2. Data Persistence
   We use Python's built-in json library to save users, trains, and bookings to local files (.json). This means your data is still there when you close and reopen the program!

3. Functions & Helpers
   Small, reusable functions are used for repetitive tasks, like _get_station_choice or _save_data.

4. Input/Output (I/O)
   The entire program runs by taking user input (like station choices) and printing results to the console.

Features:
User Accounts: Simple Registration and Login with secure password masking (getpass).

Mock Database Generation: If you delete the data files, the program instantly creates a new set of train routes with random prices and seats so you can start testing immediately.

Smart Pricing: Tickets are priced based on Indian Railways-inspired passenger categories, including Adult, Child (50% Off), Senior Citizen (30% Off), and Infant (Free).

Real-time Seat Tracking: Seats are reserved when booked and returned when canceled, updating the cli_trains.json file automatically.

Advanced: Partial Cancellation: You don't have to cancel the whole ticket! You can specify exactly how many Adult or Child tickets you want to cancel from a single booking. The system calculates the specific refund based on the ticket type's price.

How to run project:
Prerequisites
You only need Python 3.x installed. The project uses only standard built-in libraries.
Steps to Launch
Download the Code: Get the trainbooking.py file onto your computer.

Open your Terminal/Command Prompt and navigate to the folder where you saved the file.
Run Script using command - python trainbooking.py

First-Time Setup: If this is your first run, the program will generate three JSON data files (cli_users.json, cli_trains.json, cli_bookings.json) in the same folder.

Guide through:
Main Menu:
1. Register
2. Login
3. Exit

User Dashboard:
1. Search and book train
2. view my bookings
3. cancel a booking
4. logout

Project Files:
trainbooking.py - complete application code
cli_users.json - user accounts and password
cli_trains.json - the inventory of all train routes and available seats. Seats are updated her when you book or cancel!
cli_bookings.json - records of all confirmed tickets

Ideas for improvements:
1. GUI interface- replace basic CLI with graphical user interface (Tkinter or PyQt)
2. Error Handling- Add more robust checks for invalid file operations or corrupted data.
3. PNR system - implement a true unique PNR generation and check system.
4. Class Refinement - Split BookingSystem into smaller focused classes - UserHandler, TrainDB, PricingEngine.
