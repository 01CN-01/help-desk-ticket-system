from getpass import getpass

def int_checker(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Enter a Number.")

def input_checker(prompt):
    while True:
        answer = input(prompt)
        if answer != "":
            return answer
        else:
            print("Cannot Leave Blank.")

def password_checker(prompt):
    while True:
        password = getpass(prompt) # Hides Password
        if password != "":
            if len(password.strip()) > 0:
                return password
        else:
            print("Cannot Leave Blank.")


def is_password_secure(password): # Only Checks
    SPECIAL_CHARS = ["@", "*", "!", "#", "$"]
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for c in password:
        if c.isupper():
            has_upper = True
        if c.islower():
            has_lower = True
        if c.isdigit():
            has_digit = True
        if c in SPECIAL_CHARS:
            has_special = True

    if len(password) < 8:
        return False
    if not has_upper:
        return False
    if not has_lower:
        return False
    if not has_digit:
        return False
    if not has_special:
        return False
 
    return True

def email_format_checker(prompt):
    while True:
        answer = input(prompt)
        if "@" in answer:
            parts = answer.split("@")
            if len(parts) != 2:
                print("Invalid Format.")
            else:
                if parts[0] == "" or parts[1] == "":
                    print("Invalid Format.")
                else:
                    return answer
        else:
            print("Must include @")

            