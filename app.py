from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)


with open("static/departments.json", "r") as f:
    departments = json.load(f)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data       = request.json
    state      = data.get("state")
    user_input = data.get("input", "").strip()
    dept_key   = data.get("dept_key")

    if state == "GREETING":
        name = user_input
        return jsonify({
            "state": "MAIN_MENU",
            "dept_key": None,
            "message": f"Welcome <strong>{name}</strong> to CIDCO Unified Helpdesk! How may I assist you today?",
            "options": build_main_menu()
        })

    
    if state == "MAIN_MENU":
        if user_input == "0":
            return jsonify({
                "state": "DONE",
                "dept_key": None,
                "message": "Thank you for contacting CIDCO Helpdesk. Have a good day! 🙏",
                "options": []
            })
        if user_input in departments:
            dept_name = departments[user_input]["name"]
            return jsonify({
                "state": "SUB_MENU",
                "dept_key": user_input,
                "message": f"You selected <strong>{dept_name}</strong> Department. Please choose an option:",
                "options": build_sub_menu(user_input)
            })
        return jsonify({
            "state": "MAIN_MENU",
            "dept_key": None,
            "message": "Invalid selection. Please choose a valid department.",
            "options": build_main_menu()
        })

    
    if state == "SUB_MENU":
        if user_input == "9":
            return jsonify({
                "state": "MAIN_MENU",
                "dept_key": None,
                "message": "Please select a department:",
                "options": build_main_menu()
            })
        if dept_key and user_input in departments[dept_key]["options"]:
            response = departments[dept_key]["options"][user_input]["response"]
            return jsonify({
                "state": "SUB_MENU",
                "dept_key": dept_key,
                "message": response,
                "options": build_sub_menu(dept_key)
            })
        return jsonify({
            "state": "SUB_MENU",
            "dept_key": dept_key,
            "message": "Invalid option. Please try again.",
            "options": build_sub_menu(dept_key)
        })

    return jsonify({"error": "Unknown state"}), 400



def build_main_menu():
    options = [{"key": k, "label": v["name"]} for k, v in departments.items()]
    options.append({"key": "0", "label": "Exit"})
    return options

def build_sub_menu(dept_key):
    opts = departments[dept_key]["options"]
    options = [{"key": k, "label": v["title"]} for k, v in opts.items()]
    options.append({"key": "9", "label": "Back to Main Menu"})
    return options


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    
    
    
    
    





# import json
# import time

# from flask import Flask, render_template, jsonify
# import json

# app = Flask(__name__)

# # Load departments once at startup
# with open("static/departments.json", "r") as f:
#     departments = json.load(f)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/departments")
# def get_departments():
#     return jsonify(departments)

# if __name__ == "__main__":
#     app.run(debug=True)

# def greet():
#     print("Namaste 🙏")
#     name = input("May I know your name? ")
#     print(f"\nWelcome {name} to CIDCO Unified Helpdesk.")
#     print("How may I assist you today?\n")

# def show_main_menu():
#     print("\nPlease select a department:")
#     for number, dept in departments.items():
#         print(f"{number}. {dept['name']}")
#     print("0. Exit")


# def show_sub_menu(dept_number):
#     dept = departments[str(dept_number)]

#     print(f"\nYou selected {dept['name']} Department.")
#     print("Please choose an option:")

#     for number, option in dept["options"].items():
#         print(f"{number}. {option['title']}")

#     print("9. Back to Main Menu")



# def start_chat():
#     greet()

#     while True:
#         show_main_menu()

#         choice = input("Enter your choice: ")

#         if choice == "0":
#             print("Bot: Thank you for contacting CIDCO Helpdesk. Have a good day! 🙏")
#             break

#         if choice in departments:

#             while True:
#                 show_sub_menu(choice)

#                 sub_choice = input("Enter your option: ")

#                 if sub_choice == "9":
#                     break

#                 elif sub_choice in departments[choice]["options"]:
#                     time.sleep(1)
#                     response = departments[choice]["options"][sub_choice]["response"]
#                     print("Bot:", response)

#                 else:
#                     print("Bot: Invalid option. Please try again.")

#         else:
#             print("Bot: Invalid department selection.")



# if __name__ == "__main__":
#     start_chat()

