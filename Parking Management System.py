import mysql.connector as c
import matplotlib.pyplot as plt
# Set the total parking space values
total_bicycles = 50  # Change this to the total number of available bicycle parking spaces
total_bikes = 100  # Change this to the total number of available bike parking spaces
total_cars = 150  # Change this to the total number of available car parking spaces

entries = []

# Create a MySQL database and a connection
con = c.connect(
    host="localhost",
    user="root",
    passwd="sakshi2002",
    database="parking"
)
cursor = con.cursor()

# Create the parking_entries table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS parking_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(15),
    vehicle_type CHAR(1),
    vehicle_name VARCHAR(255),
    owner_name VARCHAR(255),
    date DATE,
    time_entry TIME
)
''')
con.commit()

def main():
    try:
        while True:
            print("+---------------------------------------------+")
            print("|                   *1.Vehicle Entry                  |")
            print("|                  *2.Remove Entry                  |")
            print("|              *3.View Parked Vehicle             |")
            print("|          *4.View Left Parking Space           |")
            print("|                 *5.Amount Details                 |")
            print("|                       *6.Bill                             |")
            print("|                *7.Close Programme               |")
            print("+---------------------------------------------+")
            ch = int(input("\t..::Select option::.."))
            if ch == 1:
                park_vehicle()
            elif ch == 2:
                remove_vehicle()
            elif ch == 3:
                view_parked_vehicles()
            elif ch == 4:
                view_left_parking_space()
            elif ch == 5:
                view_parking_rate()
            elif ch == 6:
                generate_bill()
            elif ch == 7:
                print("..............................................................Thank you for using our service...........................................................................")
                print("                                     *(: Bye Bye :)*")
                break

    except Exception as e:
        print(e)

def park_vehicle():
    vehicle_no = input("\tEnter vehicle number (XXXX-XX-XXXX) - ").upper()
    vehicle_type = input("\tEnter vehicle type (Bicycle=A/Bike=B/Car=C): ").upper()
    vehicle_name = input("\tEnter vehicle name - ")
    owner_name = input("\tEnter owner name - ")
    date = input("\tEnter Date (YYYY-MM-DD) - ")
    time_entry = input("\tEnter Time (HH:MM:SS) - ")

    # Insert the entry into the database
    query = "INSERT INTO parking_entries (vehicle_number, vehicle_type, vehicle_name, owner_name, date, time_entry) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (vehicle_no, vehicle_type, vehicle_name, owner_name, date, time_entry)
    cursor.execute(query, values)
    con.commit()
    print("\n............................................................Record detail saved..................................................................")

def remove_vehicle():
    vehicle_no = input("\tEnter vehicle number to remove (XXXX-XX-XXXX) - ").upper()

    # Remove the entry from the database
    query = "DELETE FROM parking_entries WHERE vehicle_number = %s"
    cursor.execute(query, (vehicle_no,))
    con.commit()
    print("\n............................................................Removed Successfully..................................................................")

def view_parked_vehicles():
    cursor.execute('SELECT * FROM parking_entries')
    entries = cursor.fetchall()

    print("----------------------------------------------------------------------------------------------------------------------")
    print("\t\t\t\tParked Vehicle")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("ID\tVehicle No.\tVehicle Type\tVehicle Name\tOwner Name\tDate\tTime")
    print("----------------------------------------------------------------------------------------------------------------------")

    for entry in entries:
        print("\t".join(map(str, entry)))
    
    print("----------------------------------------------------------------------------------------------------------------------")

def view_left_parking_space():
    total_bicycles = 50  # Change this to the total number of available bicycle parking spaces
    total_bikes = 100  # Change this to the total number of available bike parking spaces
    total_cars = 150  # Change this to the total number of available car parking spaces

    available_bicycles = total_bicycles - len([entry for entry in entries if entry[2] == 'B'])
    available_bikes = total_bikes - len([entry for entry in entries if entry[2] == 'B'])
    available_cars = total_cars - len([entry for entry in entries if entry[2] == 'C'])

    # Create a bar chart to visualize available parking spaces
    categories = ['Bicycles', 'Bikes', 'Cars']
    spaces_left = [available_bicycles, available_bikes, available_cars]

    plt.bar(categories, spaces_left, color=['blue', 'green', 'red'])
    plt.xlabel('Vehicle Type')
    plt.ylabel('Spaces Left')
    plt.title('Available Parking Spaces')
    plt.show()

def view_parking_rate():
    print("----------------------------------------------------------------------------------------------------------------------")
    print("\t\t\t\tParking Rate")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("*1.Bicycle      Rs20 / Hour")
    print("*2.Bike         Rs40 / Hour")
    print("*3.Car          Rs60 / Hour")
    print("----------------------------------------------------------------------------------------------------------------------")

def generate_bill():
    vehicle_no = input("\tEnter vehicle number for billing (XXXX-XX-XXXX) - ").upper()

    # Retrieve the entry details from the database
    query = "SELECT * FROM parking_entries WHERE vehicle_number = %s"
    cursor.execute(query, (vehicle_no,))
    entry = cursor.fetchone()

    if entry:
        _, vehicle_number, vehicle_type, _, _, time_entry, _ = entry
        print("\tVehicle Check-in Time -", time_entry)
        print("\tVehicle Type -", vehicle_type)
        
        inp = True
        while inp:
            hours_parked = input("\tEnter No. of Hours Vehicle Parked - ")
            try:
                hours_parked = int(hours_parked)
                if hours_parked < 0:
                    print("Invalid input. Please enter a non-negative number of hours.")
                else:
                    inp = False
            except ValueError:
                print("Invalid input. Please enter a valid number of hours.")
        
        parking_rate = {"B": 20, "B": 40, "C": 60}
        rate_per_hour = parking_rate.get(vehicle_type, 0)
        total_charge = hours_parked * rate_per_hour
        additional_charge = (18 / 100) * total_charge
        
        print("\tParking Charge -", total_charge)
        print("\tAdd. charge 18 % -", additional_charge)
        print("\tTotal Charge - Rs", total_charge + additional_charge)
        
        # Remove the entry after billing
        query = "DELETE FROM parking_entries WHERE vehicle_number = %s"
        cursor.execute(query, (vehicle_number,))
        con.commit()
        
    else:
        print("\tNo such entry found.")

    print("\n..............................................................Thank you for using our service...........................................................................")

if __name__ == '__main__':
    main()
