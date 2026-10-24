catalogue = {
    "P001": {"name": "Notebook", "price": 45, "category": "Stationery", "quantity": 50},
    "P002": {"name": "Pen", "price": 10, "category": "Stationery", "quantity": 100},
    "P003": {"name": "Water Bottle", "price": 250, "category": "Accessories", "quantity": 30},
    "P004": {"name": "Backpack", "price": 899, "category": "Bags", "quantity": 15},
    "P005": {"name": "Wireless Mouse", "price": 650, "category": "Electronics", "quantity": 25},
    "P006": {"name": "Desk Lamp", "price": 450, "category": "Home & Office", "quantity": 20},
    "P007": {"name": "Sticky Notes", "price": 30, "category": "Stationery", "quantity": 80},
    "P008": {"name": "USB Flash Drive", "price": 350, "category": "Electronics", "quantity": 40},
}

cart = {}

def view_catalogue():
    print("\n--- Store Catalogue ---")
    for item_id, details in catalogue.items():
        print(f"{item_id}: {details['name']} - ₹{details['price']} ({details['category']})")
    print("-" * 25)

def add_to_cart():
    # Loop to allow adding multiple items continuously
    while True:
        item_id = input("\nEnter Product ID: ").strip().upper()

        if item_id not in catalogue: 
            print("Error: Product ID does not exist in the catalogue!")
        else:
            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Error: Quantity must be greater than 0.")
                else:
                    if item_id in cart: 
                        cart[item_id]["quantity"] += quantity
                    else:
                        cart[item_id] = {
                            "name": catalogue[item_id]["name"],
                            "price": catalogue[item_id]["price"],
                            "quantity": quantity
                        }
                    print(f"Added {quantity} x {catalogue[item_id]['name']} to cart.")
            except ValueError:
                print("Error: Please enter a valid number for quantity.")

        # Ask if they want to add more items right here
        more = input("Do you want to add more items? (Y/N): ").strip().upper()
        if more != "Y":
            break

def remove_from_cart():
    if not cart:
        print("Your cart is empty!")
        return
        
    item_id = input("Enter the ID you want to remove from cart: ").strip().upper()

    if item_id not in cart:
        print("Error: Item not found in your cart.")
        return

    del cart[item_id] 
    print("Item removed from cart.")

def view_cart():
    print("\n======= YOUR CART =======")
    if not cart:
        print("Your cart is empty.")
    else:
        for items, details in cart.items():
            print(f"{details['name']} x{details['quantity']} - ₹{details['price'] * details['quantity']}")
    print("=========================")

def check_out():
    if not cart:
        print("\nYour cart is empty! Add items before checking out.")
        return

    print("\n======= YOUR BILL =======")

    subtotal = 0
    for items in cart:
        name = cart[items]["name"]
        quantity = cart[items]["quantity"]
        total = cart[items]["price"] * quantity
        subtotal += total  
        print(f"{name:<10} x{quantity:<3} ₹ {total:>6.2f}")

    print("-------------------------")

    discount_amount = subtotal * 0.18

    print(f"{'Subtotal':<17} ₹ {subtotal:>6.2f}")
    print(f"{'Discount':<17} ₹ {discount_amount:>6.2f}")

    print("-" * 28)
    print(f"{'Total':<17} ₹ {(subtotal - discount_amount):>6.2f}")
    print("=" * 28)
    cart.clear() # Clear cart after successful checkout


# Main Menu Display
print(" " * 16, "1. View Items")
print(" " * 16, "2. Add Item to Cart")
print(" " * 16, "3. Remove Item from Cart")
print(" " * 16, "4. View Cart")
print(" " * 16, "5. Checkout")
print(" " * 16, "6. Exit\n")

character = "Y"

while character == "Y":
    try:
        choice = int(input("Enter the Number which You want to choose? "))
    except ValueError:
        print("Invalid input! Please enter a number between 1 and 6.")
        continue

    if choice == 1:
        view_catalogue()
    elif choice == 2:
        add_to_cart()
    elif choice == 3:
        remove_from_cart()
    elif choice == 4:
        view_cart()
    elif choice == 5:
        check_out()
    elif choice == 6:
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice! Please select a number from 1 to 6.")

    character = input("\nDo you want to continue to main menu? (Y/N): ").strip().upper()
    print(" " * 16, "1. View Items")
    print(" " * 16, "2. Add Item to Cart")
    print(" " * 16, "3. Remove Item from Cart")
    print(" " * 16, "4. View Cart")
    print(" " * 16, "5. Checkout")
    print(" " * 16, "6. Exit\n")