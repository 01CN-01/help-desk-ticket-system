from help_desk_system import HelpDeskSystem
from error_handling import int_checker
help_desk_system = HelpDeskSystem()

def login_register_menu():
    # Loop account_menu
    while True:
        print("==============================")
        print("    Login / Register Menu")
        print("==============================")
        print("1) Login")
        print("2) Register")
        print("3) Exit Program")
        print("==============================")
        menu_option = int_checker("Enter A Option: ")
        if menu_option == 1:
            login_user = help_desk_system.login()
            if login_user: # Login Returns TRUE 
                help_desk_system.account_menu()
        elif menu_option == 2:
            register_user = help_desk_system.register()
            if register_user: # Register Returns True
                login_user = help_desk_system.login()
                if login_user:
                    help_desk_system.account_menu()
        elif menu_option == 3:
            print("Program Ended.")
            break
        
login_register_menu()
    