"""This script is used to mark this directory
as a Python package.

Function definitions and variable assignments 
will be executed first when the package is imported.
"""

# Import module to print colored text.
from colorama import init as colorama_init
from colorama import Fore
from colorama import Back
from colorama import Style

# Import module to clear terminal text.
from os import system, name
from time import sleep

# Import module to produce ASCII art.
import pyfiglet

# Import module to print table.
import tabulate
import pandas as pd

# Import module for currency formatting.
import locale


# Call colorama initialization function, so we can print colored text.
colorama_init()

# Set Indonesia locale as formatting.
locale.setlocale(locale.LC_ALL, "id_ID")


class ClearScreen:
    """A class to clear the terminal screen."""

    def clear(self):
        """Clears the terminal screen.

        This method uses the appropriate clear command 
        for the current operating system.
        """

        # Determine the operating system:
        # for Windows
        if name == "nt":
            _ = system("cls")

        # for Mac and Linux(here, os.name is "posix")
        else:
            _ = system("clear")


# Define global variable for clear screen.
clear_screen = ClearScreen()


class WelcomeMessage:
    """A class to show welcome message."""

    def show(self):
        """Shows the welcome message.

        After showing it, then it clears the screen.
        """

        # Set app name for banner.
        APP_NAME = "Omega Cashier"

        # Use pyfiglet to create ASCII art for app banner.
        message = pyfiglet.figlet_format(APP_NAME, font="ogre")
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")


# Define global variable for printing welcome message.
welcome_message = WelcomeMessage()


class Cart:
    """A class to handle all cashier operations.

    Constant:
    MIN_DISCOUNT_THRESHOLD: the minimum requirement of total order for 5% discount.
    MID_DISCOUNT_THRESHOLD: the minimum requirement of total order for 8% discount.
    MAX_DISCOUNT_THRESHOLD: the minimum requirement of total order for 10% discount.

    MIN_DISCOUNT: 5% discount.
    MID_DISCOUNT: 8% discount.
    MAX_DISCOUNT: 10% discount.

    """

    MIN_DISCOUNT_THRESHOLD = 200000
    MIN_DISCOUNT = 0.05

    MID_DISCOUNT_THRESHOLD = 300000
    MID_DISCOUNT = 0.08

    MAX_DISCOUNT_THRESHOLD = 500000
    MAX_DISCOUNT = 0.1

    SUCCESS_MESSAGE = "Your cart has been successfully updated."

    COLUMN_NAMES = ["Item", "Quantity", "Price per Item", "Total"]
    EMPTY_CART_MESSAGE = "There are no items in your cart. Please add items to begin shopping."
    CURRENT_CART_MESSAGE = "Here is what you have in your current cart."
    

    def __init__(self):
        """An initial class function that includes an empty pandas dataframe, 
        which will later be populated with items and their attributes.

        """

        # Set item name as index
        self.df = pd.DataFrame(columns=self.COLUMN_NAMES)


    def is_true(self):
        """A boolean function is executed to determine whether the cart is empty or not, 
        and it is utilized by other functions.

        If the cart is not empty, indicating that the add_item function has been invoked, 
        another function can be executed as intended.

        Otherwise, an error message will be generated.

        """

        if len(self.df) != 0:
            return True
        else:
            return False
        

    def display_cart(self):
        """A function for storing and displaying the cart.

        """

        print_cart = self.df.to_markdown(tablefmt="fancy_grid", index=False)
        return print(print_cart)
    

    def add_item(self, item_name, item_quantity, item_price):
        """A function to manage the addition of items to the cart.

        This function accepts item_name, item_quantity, 
        and item_price, then adds them to the dataframe.
        
        The total_item is calculated by multiplying item_quantity and item_price.

        """

        self.item_name = item_name
        self.item_quantity = item_quantity
        self.item_price = item_price

        # Verifying user input to determine whether it is a positive integer or not.
        if (isinstance(item_quantity, int)
            and item_quantity > 0) and (isinstance(item_price, int) and item_price > 0) and (isinstance(item_name, str)):
            print("\n")
            total_item = item_quantity * item_price
            new_item = pd.DataFrame({
                "Item": [item_name],
                "Quantity": [item_quantity],
                "Price per Item": [item_price],
                "Total": [total_item]
            })
            self.df = pd.concat([self.df, new_item], ignore_index=True)

            self.display_cart()
            print("\n")

        else:
            clear_screen.clear()


    def update_item_name(self, item_name, new_item):
        """A function for managing the modification of the item_name entered by the user in the cart.

        Input:
        item_name [String] - The original name of the item entered into the cart by the user.
        new_item [String] - The new name for the item.

        Process:
        If the item_name is found in the cart, it will be replaced with the new_item.
        Subsequently, the cart will be updated.
        In case the item_name is not present in the cart, an error message will be displayed.

        """

        if self.is_true():
            if item_name in self.df["Item"].values:
                clear_screen.clear()
                welcome_message.show()

                self.df["Item"] = self.df["Item"].replace(to_replace=item_name, value=new_item)
                self.display_cart()
                
                print(f"{Back.GREEN}{Fore.BLACK}{self.SUCCESS_MESSAGE}{Style.RESET_ALL}")
                print(f"{item_name} has been renamed to {new_item}.")
                print("\n")
            else:
                print("\n")
                print(f"{Back.YELLOW}{Fore.BLACK}We didn't find {item_name} in the cart. Aborted.{Style.RESET_ALL}")
        else:
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")


    def update_item_quantity(self, item_name, new_quantity):
        """A function for managing the update of the item_quantity entered by the user in the cart.

        Input:
        item_name [String] - The name of the item entered into the cart by the user.
        new_quantity [Integer] - The new quantity for the item.

        Process:
        If the item_name is found in the cart, the item's quantity will be changed to the new_quantity.
        Subsequently, the cart will be updated.
        If the item_name is not present in the cart, an error message will be displayed.
        """

        # Verify whether the cart's empty by invoking the is_true function.
        if self.is_true():
            # Verify if the item_name exists in the cart and if the new_quantity is a positive integer.
            if (item_name in self.df["Item"].values) and (isinstance(new_quantity, int) and new_quantity > 0):
                clear_screen.clear()
                welcome_message.show()

                print(f"{Back.GREEN}{Fore.BLACK}{self.SUCCESS_MESSAGE}{Style.RESET_ALL}")
                
                # Populate the new item quantity and the total price.
                self.df.loc[self.df["Item"] == item_name, "Quantity"] = new_quantity
                self.df.loc[self.df["Item"] == item_name, "Total"] = new_quantity * self.df["Price per Item"]
                
                # Display updated cart.
                self.display_cart()
                print(f"{item_name}'s quantity has been updated to {new_quantity}.")

            # If not, an error message will be displayed.
            else:
                print("\n")
                print(f"{Back.YELLOW}{Fore.BLACK}Invalid input. Aborted.{Style.RESET_ALL}")
                print(f"Please try again.")

        # If not, it will display a message which indicates the cart is empty.        
        else:
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")

    
    def update_item_price(self, item_name, new_price):
        """A function for managing the update of the item_price entered by the user in the cart.

        Input:
        item_name [String] - The name of the item entered into the cart by the user.
        new_price [Integer] - The new price for the item.

        Process:
        If the item_name is found in the cart, the item's price will be changed to the new_price.
        Subsequently, the cart will be updated.
        In case the item_name is not present in the cart, an error message will be displayed.

        """

        # Verify whether the cart's empty by invoking the is_true function.
        if self.is_true():
            # Verify if the item_name exists in the cart and if the new_price is a positive integer.
            if item_name in self.df["Item"].values and (isinstance(new_price, int) and new_price > 0):
                clear_screen.clear()
                welcome_message.show()
                
                print(f"{Back.GREEN}{Fore.BLACK}{self.SUCCESS_MESSAGE}{Style.RESET_ALL}")
                self.df.loc[self.df["Item"] == item_name, "Price per Item"] = new_price
                self.df.loc[self.df["Item"] == item_name, "Total"] = new_price * self.df["Quantity"]

                self.display_cart()
                new_price = locale.currency(new_price, grouping=True)
                print(f"{item_name}'s price has been updated to {new_price} per item.")

            # If not, an error message will be displayed.
            else:  
                print("\n")
                print(f"{Back.YELLOW}{Fore.BLACK}Invalid input. Aborted.{Style.RESET_ALL}")
                print(f"Please try again.")

        else:
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")


    def remove_item(self, item_name):
        """A function for removing an item from the cart.

        Input:
        item_name [String] - The name of the item to be removed.

        Process:
        If the item_name exists in the cart, it will be promptly removed.
        In the event that the item_name is not found in the cart, an error message will be printed.

        """
    
        # Check if the cart is not empty.
        if self.is_true():
            # Check if the item_name exists in the cart.
            if item_name in self.df["Item"].values:
                # Clear the screen and display welcome message.
                clear_screen.clear()
                welcome_message.show()
                
                # Remove the item from the cart's dataframe.
                self.df = self.df[self.df["Item"] != item_name]
                
                # Display success message and current cart contents.
                print(f"{Back.GREEN}{Fore.BLACK}{self.SUCCESS_MESSAGE}{Style.RESET_ALL}")
                print(self.CURRENT_CART_MESSAGE)
                self.display_cart()
                
                # Confirm that the item was successfully deleted.
                print(f"{item_name} was successfully deleted.")
                print("\n")
                
            else:
                # Display an error message if item_name is not found in the cart.
                print("\n")
                print(f"{Back.YELLOW}{Fore.BLACK}We didn't find {item_name} in the cart. Please try again.{Style.RESET_ALL}")

        else:
            # Display a message if the cart is empty.
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")


    def reset_item(self):
        """A function for emptying the cart.

        Process:
        It checks if the cart is empty or not.
        If it's empty, all user-entered values will be removed.

        Otherwise, it will display an error message.
        """
        # Check if the cart is not empty.
        if self.is_true():
            # Remove all items from the cart's dataframe.
            self.df.drop(self.df.index, inplace=True)
            print("\n")

            # Display a success message.
            print(f"{Back.GREEN}{Fore.BLACK}{self.SUCCESS_MESSAGE}{Style.RESET_ALL}")
            print("All items have been successfully removed from the cart.")

        # Display an error message if the cart is empty
        else:
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")

    
    def check_order(self):
        """A function to check the user's current order.

        Process:
        - Checks if the cart is not empty.
        - Displays the current cart contents.
        - Calculates and displays the grand total of the order.
        - Informs the user that their order is ready for checkout.

        If the cart is empty, it displays an error message.
        """
        
        # Check if the cart is not empty
        if self.is_true():
            # Display the current cart contents.
            print(f"{self.CURRENT_CART_MESSAGE}")
            print("\n")
            self.display_cart()
            print("\n")

            # Calculate and display the grand total with currency formatting.
            grand_total = self.df["Total"].sum()
            pretty_grand_total = locale.currency(grand_total, grouping=True)
            print(f"Grand total: {Back.GREEN}{Fore.BLACK}{pretty_grand_total}{Style.RESET_ALL}")
            print("Your order is ready to checkout. Please go to the checkout page for discount eligibility.")

        else:
            # Display an error message if the cart is empty.
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")


    def checkout(self):
        """Handle cart checkout and calculate the total.

        Process:
        - If the cart is not empty:
            - It prints the current cart and calculates the grand_total by summing the Total column.
            - If grand_total is greater than MAX_DISCOUNT_THRESHOLD (500,000), the user receives a 10% discount.
            - If grand_total is greater than MID_DISCOUNT_THRESHOLD (300,000), the user receives an 8% discount.
            - If grand_total is greater than MIN_DISCOUNT_THRESHOLD (200,000), the user receives a 5% discount.
            - If grand_total is lower or equal to MIN_DISCOUNT_THRESHOLD (200,000), no discount is applied.
            - The grand_total is adjusted by its discount, and the value is displayed.
        - Otherwise, an error message is displayed.
        """
        
        # Check if the cart is not empty
        if self.is_true():
            # Calculate the grand total by summing the Total column
            grand_total = self.df["Total"].sum()
            pretty_grand_total = locale.currency(grand_total, grouping=True)
            
            # Display the current cart
            self.display_cart()
            print("\n")

            # Check if grand_total is greater than MAX_DISCOUNT_THRESHOLD (500,000)
            if grand_total > self.MAX_DISCOUNT_THRESHOLD:
                # Apply a 10% discount
                grand_total = grand_total - (grand_total * self.MAX_DISCOUNT)
                pretty_grand_total = locale.currency(grand_total, grouping=True)
                print(f"You receive a 10% discount! Total order: {Back.GREEN}{Fore.BLACK}{pretty_grand_total}{Style.RESET_ALL}")
                print("Thank you for your order.")

                # Reset the order by removing all items from the cart's dataframe
                self.df.drop(self.df.index, inplace=True)

            # Check if grand_total is greater than MID_DISCOUNT_THRESHOLD (300,000)
            elif grand_total > self.MID_DISCOUNT_THRESHOLD:
                # Apply an 8% discount
                grand_total = grand_total - (grand_total * self.MID_DISCOUNT)
                pretty_grand_total = locale.currency(grand_total, grouping=True)
                print(f"You receive an 8% discount! Total order: {Back.GREEN}{Fore.BLACK}{pretty_grand_total}{Style.RESET_ALL}")
                print("Thank you for your order.")

                # Reset the order
                self.df.drop(self.df.index, inplace=True)

            # Check if grand_total is greater than MIN_DISCOUNT_THRESHOLD (200,000)
            elif grand_total > self.MIN_DISCOUNT_THRESHOLD:
                # Apply a 5% discount
                grand_total = grand_total - (grand_total * self.MIN_DISCOUNT)
                pretty_grand_total = locale.currency(grand_total, grouping=True)
                print(f"You receive a 5% discount! Total order: {Back.GREEN}{Fore.BLACK}{pretty_grand_total}{Style.RESET_ALL}")
                print("Thank you for your order.")

                # Reset the order
                self.df.drop(self.df.index, inplace=True)

            else:
                # No discount applied, display the total order
                print(f"Total order: {Back.GREEN}{Fore.BLACK}{pretty_grand_total}{Style.RESET_ALL}")
                print("Thank you for your order.")

                # Reset the order
                self.df.drop(self.df.index, inplace=True)
        else:
            # Display an error message if the cart is empty
            print("\n")
            print(f"{Back.YELLOW}{Fore.BLACK}{self.EMPTY_CART_MESSAGE}{Style.RESET_ALL}")