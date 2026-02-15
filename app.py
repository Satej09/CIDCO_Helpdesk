import json
import time

with open("data/departments.json", "r") as file:
    departments = json.load(file)

def greet():
    print("Namaste 🙏")
    name = input("May I know your name? ")
    print(f"\nWelcome {name} to CIDCO Unified Helpdesk.")
    print("How may I assist you today?\n")

def show_main_menu():
    print("\nPlease select a department:")
    for number, dept in departments.items():
        print(f"{number}. {dept['name']}")
    print("0. Exit")


def show_sub_menu(dept_number):
    dept = departments[str(dept_number)]

    print(f"\nYou selected {dept['name']} Department.")
    print("Please choose an option:")

    for number, option in dept["options"].items():
        print(f"{number}. {option['title']}")

    print("9. Back to Main Menu")



def start_chat():
    greet()

    while True:
        show_main_menu()

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Bot: Thank you for contacting CIDCO Helpdesk. Have a good day! 🙏")
            break

        if choice in departments:

            while True:
                show_sub_menu(choice)

                sub_choice = input("Enter your option: ")

                if sub_choice == "9":
                    break

                elif sub_choice in departments[choice]["options"]:
                    time.sleep(1)
                    response = departments[choice]["options"][sub_choice]["response"]
                    print("Bot:", response)

                else:
                    print("Bot: Invalid option. Please try again.")

        else:
            print("Bot: Invalid department selection.")



if __name__ == "__main__":
    start_chat()
