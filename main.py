import datetime


def read_vehicles():
    vehicles = []
    with open("vehicles.txt", "r") as f:
        for line in f:
            reg, model, rate, *properties = line.strip().split(",")
            vehicles.append(
                {
                    "reg": reg,
                    "model": model,
                    "rate": float(rate),
                    "properties": properties,
                }
            )
    return vehicles


def read_customers():
    customers = []
    with open("customers.txt", "r") as f:
        for line in f:
            dob, fname, lname, email = line.strip().split(",")
            customers.append(
                {"dob": dob, "fname": fname, "lname": lname, "email": email}
            )
    return customers


def read_rented():
    rented = []
    with open("rentedVehicles.txt", "r") as f:
        for line in f:
            reg, customer_dob, start_time = line.strip().split(",")
            rented.append(
                {"reg": reg, "customer_dob": customer_dob, "start_time": start_time}
            )
    return rented


def read_transactions():
    transactions = []
    with open("transActions.txt", "r") as f:
        for line in f:
            reg, dob, start, end, days, price = line.strip().split(",")
            transactions.append(
                {
                    "reg": reg,
                    "dob": dob,
                    "start": start,
                    "end": end,
                    "days": int(days),
                    "price": float(price),
                }
            )
    return transactions


def list_available_cars():
    vehicles = read_vehicles()
    rented = read_rented()
    rented_regs = [r["reg"] for r in rented]

    available = [v for v in vehicles if v["reg"] not in rented_regs]

    if not available:
        print("\nNo cars are currently available.")
        return

    print("\nAvailable cars:")
    for car in available:
        print(
            f"*Reg. nr. {car['reg']}, Model: {car['model']}, Price per day: {car['rate']} "
        )
        print(f"Properties: {', '.join(car['properties'])}")


def add_customer():
    print("\nEnter customer details:")
    while True:
        dob = input("Date of birth (DD/MM/YYYY): ")
        try:
            datetime.datetime.strptime(dob, "%d/%m/%Y")
            break
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY")

    fname = input("First name: ")
    lname = input("Last name: ")
    email = input("Email: ")

    with open("customers.txt", "a") as f:
        f.write(f"{dob},{fname},{lname},{email}\n")

    return dob


def rent_car():
    vehicles = read_vehicles()
    rented = read_rented()
    rented_regs = [r["reg"] for r in rented]
    available = [v for v in vehicles if v["reg"] not in rented_regs]

    if not available:
        print("\nSorry, no cars are currently available.")
        return

    while True:
        reg = input("\nEnter registration number of car to rent: ")
        if any(r["reg"] == reg for r in rented):
            print("This car is already rented.")
            continue
        if any(car["reg"] == reg for car in available):
            break
        print("Invalid registration number. Please try again.")

    dob = add_customer()

    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with open("rentedVehicles.txt", "a") as f:
        f.write(f"{reg},{dob},{now}\n")

    print("\nCar rented successfully!")


def return_car():
    reg = input("\nEnter registration number of car to return: ")

    # Find rental record
    rented = read_rented()
    rental = None
    for r in rented:
        if r["reg"] == reg:
            rental = r
            break

    if not rental:
        print("No rental found for this registration number.")
        return

    # Calculate rental duration and cost
    vehicles = read_vehicles()
    car = next(v for v in vehicles if v["reg"] == reg)

    start_time = datetime.datetime.strptime(rental["start_time"], "%d/%m/%Y %H:%M")
    end_time = datetime.datetime.now()

    # Calculate days (counting partial days as full days)
    days = (end_time - start_time).days + 1
    cost = days * car["rate"]

    # Record transaction
    with open("transActions.txt", "a") as f:
        f.write(
            f"{reg},{rental['customer_dob']},{rental['start_time']},"
            f"{end_time.strftime('%d/%m/%Y %H:%M')},{days},{cost:.2f}\n"
        )

    # Remove from rented vehicles
    with open("rentedVehicles.txt", "r") as f:
        lines = f.readlines()
    with open("rentedVehicles.txt", "w") as f:
        for line in lines:
            if not line.startswith(reg):
                f.write(line)

    print(f"\nCar returned successfully!")
    print(f"Rental duration: {days} days")
    print(f"Total cost: ${cost:.2f}")


def count_money():
    transactions = read_transactions()
    if not transactions:
        print("\nNo completed rentals yet.")
        return

    total = sum(t["price"] for t in transactions)
    print(f"\nTotal earnings: ${total:.2f}")
    print(f"Number of completed rentals: {len(transactions)}")


def main():
    while True:
        print("\n=== Car Rental System ===")
        print("1. List available cars")
        print("2. Rent a car")
        print("3. Return a car")
        print("4. Count money")
        print("0. Exit")

        choice = input("\nWhat is your selection? ")

        if choice == "1":
            list_available_cars()
        elif choice == "2":
            rent_car()
        elif choice == "3":
            return_car()
        elif choice == "4":
            count_money()
        elif choice == "0":
            print("\nThank you for using the Car Rental System!")
            break
        else:
            print("\nYou may select one of the following:")


if __name__ == "__main__":
    main()
