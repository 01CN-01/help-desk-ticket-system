import sqlite3
import bcrypt
from error_handling import int_checker, input_checker, email_format_checker, password_checker, is_password_secure

# Login
#     - Email + Password
#     - Check against database
#     - Go to main menu

# # Register
#     - First name
#     - Last name
#     - Email
#     - Password
#     - Confirm password
#     - Save user to database

# # ----- Main Menu (after login) -----
#     1) Create ticket
#         - Problem title
#         - Description
#         - Created time
#         - Automatically assigned to logged-in user

#     2) Edit ticket
#         - Only if user owns the ticket
#         - (staff/admin can edit any ticket)

#     3) View tickets
#         - Own tickets (user)
#         - All tickets (staff)

#     4) Exit program
#----------------------------------------------------------
# users.db
    # id (Primary Key)
    # firstname
    # lastname
    # email
    # password
    # role (user, staff)
# tickets.db
    # id (Primary Key)
    # created_by (id) (Auto)
    # subject (Must)
    # description (Must)
    # created_at (Auto)


class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class HelpDeskSystem:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor() # Runs SQL 
# Creates Table if it doesnt exist       
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users
                (studentid INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT,
                lastname TEXT,
                email TEXT,
                password TEXT,
                role TEXT)
            """)
# Creates user table        
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets
                (ticketid INTEGER PRIMARY KEY AUTOINCREMENT,
                created_by INTEGER,
                subject TEXT,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)
            """)
        self.user = None # User Data
    def login(self):
            print("========== LOGIN ==========")
            email = email_format_checker("Enter Email: ")
            password = password_checker("Enter Password: ")
# Validation of Email / Password            
            # Fetch user by email only
            self.cursor.execute(
                """
                SELECT 
                    studentid, firstname, lastname, email, password, role 
                FROM 
                    users 
                WHERE 
                    email = ?
                """,
                (email,)
            )
            self.user = self.cursor.fetchone()

            if self.user:
                db_hashed_pw = self.user[4]  # Comparing Hash password
                if bcrypt.checkpw(password.encode('utf-8'), db_hashed_pw.encode('utf-8')):
                    print("------- Successfully Logged In -------")
                    return True
                else:
                    print("------- Invalid Password -------")
                    return None
            else:
                print("------- Email Not Found -------")
                return None

    
    def register(self):
        print("========== REGISTER ==========")
        first_name = input_checker("Enter First Name: ")
        last_name = input_checker("Enter Last Name: ")
        email = email_format_checker("Enter your email: ")
        while True:
            password = password_checker("Enter Password: ")
            
            if is_password_secure(password): # Checks if Password is secure
                
                confirm_password = password_checker("Confirm Password: ")
                if confirm_password != password: # Confirmation of Password
                    print("Password Does Not Match")
                else:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    user_class_info = User(first_name, last_name, email, hashed_password)
                # Writing DATA   
                    self.cursor.execute(
                        """
                        INSERT INTO 
                            users (firstname, lastname, email, password, role)
                        VALUES
                            (?, ?, ?, ?, ?)
                        """,
                        (user_class_info.first_name,
                         user_class_info.last_name,
                         user_class_info.email,
                         user_class_info.password,
                         "User")
                        )
                    
                    self.conn.commit() # Commits to DB
                    
                    print("Sucessfully Made An Account")
                return True
            else:
                print("Password must be at least 8 characters long and contain:\n"
            "- 1 uppercase letter\n"
            "- 1 lowercase letter\n"
            "- 1 number\n"
            "- 1 special character\n"
            "- Longer than 8 characters")
        
    def account_menu(self):
        firstname = self.user[1]
        lastname = self.user[2]
        print("------------- Account Menu -------------")
        print(f"======= {firstname} {lastname} ======= ")
        print("1) Create Ticket")
        print("2) View Ticket")
        print("3) Edit Ticket") # Staff/Admin can edit any ticket
        print("4) Delete Ticket")
        print("5) Menu")
        print("=======================================")
        
        while True:
            account_menu_option = int_checker("Select An Option: ")
            if account_menu_option == 1:
                subject = input_checker("Subject: ")
                description = input_checker("Description of Problem: ")
            # Putting Data In    
                self.cursor.execute(
                    """
                    INSERT INTO 
                        tickets (created_by, subject, description)
                    VALUES
                        (?, ?, ?)
                    """,
                    (self.user[0],
                    subject,
                    description)
                    )
                
                self.conn.commit() # Confirms it
            elif account_menu_option == 2:
                if self.user[5] == "User": # User only able to view their own
                    self.cursor.execute(
                        """
                        SELECT 
                            *
                        FROM 
                            tickets
                        WHERE
                            created_by = ?
                        """,
                        (self.user[0],)
                    )
                    ticket_create_by_user = self.cursor.fetchall()
                    found = False
                    for ticket in ticket_create_by_user:
                            found = True
                            print(f"TicketID: {ticket[0]}")
                            print(f"Subject: {ticket[2]}")
                            print(f"Description: {ticket[3]}")
                            print(f"Created At: {ticket[4]}")
                            print("-" * 30)
                    
                    if not found:
                        print("No Tickets Found.")
                else: # If users is Staff / Admin they can access everyones
                    self.cursor.execute(
                        """
                        SELECT 
                            *
                        FROM 
                            tickets
                        """,
                    )
                    ticket_create_by_user = self.cursor.fetchall()
                    found = False
                    for ticket in ticket_create_by_user:
                            found = True
                            print(f"TicketID: {ticket[0]}")
                            print(f"Made by UserID: {ticket[1]}")
                            print(f"Subject: {ticket[2]}")
                            print(f"Description: {ticket[3]}")
                            print(f"Created At: {ticket[4]}")
                            print("-" * 30)
                    
                    if not found:
                        print("No Tickets Found.")
            elif account_menu_option == 3:
                if self.user[5] == "User": # If its User
                    self.cursor.execute(
                        """
                        SELECT
                            *
                        FROM
                            tickets
                        WHERE
                            created_by = ?
                        """,
                        (self.user[0],)
                    )
                    
                    ticket_create_by_user = self.cursor.fetchall()
                    found = False
                    for ticket in ticket_create_by_user:
                            found = True
                            print(f"TicketID: {ticket[0]}")
                            print(f"Subject: {ticket[2]}")
                            print(f"Description: {ticket[3]}")
                            print(f"Created At: {ticket[4]}")
                            print("-" * 30)
                    
                    if not found:
                        print("No Tickets Found.")
                    else:
                        ticketid_edit = int_checker("What ticket would you like to edit? (Enter using ticketID): ")
                        select = input_checker("What do you want too change? (Subject or Description): ").lower()
                        if select == "subject":
                            select_change = input_checker("Subject: ")
                            self.cursor.execute(
                                """
                                UPDATE
                                    tickets 
                                SET 
                                    subject = ?
                                WHERE
                                    ticketid = ? AND created_by = ?
                                """,
                                (select_change, 
                                 ticketid_edit,
                                 self.user[0],)
                            )
                            if self.cursor.rowcount == 1:
                                print("Successfully Changed.")
                                self.conn.commit()
                            else:
                                print("Not Found or Doesnt Belong To You.")
                        elif select == "description":
                            select_change = input_checker("Description: ")
                            self.cursor.execute(
                                """
                                UPDATE
                                    tickets 
                                SET 
                                    description = ?
                                WHERE
                                    ticketid = ? AND created_by = ?
                                """,
                                (select_change, 
                                 ticketid_edit,
                                 self.user[0],)
                            )
                            if self.cursor.rowcount == 1:
                                print("Successfully Changed.")
                                self.conn.commit()
                            else:
                                print("Not Found or Doesnt Belong To You.")
                        else:
                            print("Invalid Option.")
                else: #Staff / Admin
                    self.cursor.execute(
                        """
                        SELECT
                            *
                        FROM
                            tickets
                        """
                    )
                    
                    ticket_create_by_user = self.cursor.fetchall()
                    found = False
                    for ticket in ticket_create_by_user:
                            found = True
                            print(f"TicketID: {ticket[0]}")
                            print(f"StudentID: {ticket[1]}")
                            print(f"Subject: {ticket[2]}")
                            print(f"Description: {ticket[3]}")
                            print(f"Created At: {ticket[4]}")
                            print("-" * 30)
                    
                    if not found:
                        print("No Tickets Found.")
                    else:
                        ticketid_edit = int_checker("What ticket would you like to edit? (Enter using ticketID): ")
                        select = input_checker("What do you want too change? (Subject or Description): ").lower()
                        # Subject Selection
                        if select == "subject":
                            select_change = input_checker("Subject: ")
                            self.cursor.execute(
                                """
                                UPDATE
                                    tickets 
                                SET 
                                    subject = ?
                                WHERE
                                    ticketid = ?
                                """,
                                (select_change, 
                                 ticketid_edit)
                            )
                            if self.cursor.rowcount == 1:
                                print("Successfully Changed.")
                                self.conn.commit()
                            else:
                                print("Not Found or Doesnt Belong To You.") 
                        # Description Selection   
                        elif select == "description":
                            select_change = input_checker("Description: ")
                            self.cursor.execute(
                                """
                                UPDATE
                                    tickets 
                                SET 
                                    description = ?
                                WHERE
                                    ticketid = ?
                                """,
                                (select_change, 
                                 ticketid_edit,)
                            )
                            if self.cursor.rowcount == 1:
                                print("Successfully Changed.")
                                self.conn.commit()
                            else:
                                print("Not Found or Doesnt Belong To You.")
                        else:
                            print("Invalid Option.")
            elif account_menu_option == 4:
                if self.user[5] == "User":
                    self.cursor.execute(
                        """
                        SELECT
                            *
                        FROM
                            tickets
                        WHERE
                            created_by = ?
                        """,
                        (self.user[0],)
                    )
                    ticket_create_by_user = self.cursor.fetchall()
                    found = False
                    for ticket in ticket_create_by_user:
                            found = True
                            print(f"TicketID: {ticket[0]}")
                            print(f"Subject: {ticket[2]}")
                            print(f"Description: {ticket[3]}")
                            print(f"Created At: {ticket[4]}")
                            print("-" * 30)
                    
                    if not found:
                        print("No Tickets Found.") 
                    else:
                        delete_selection = int_checker("What ticket do u want too delete? (Select by ID): ")
                        self.cursor.execute(
                            """
                            DELETE
                            FROM
                                tickets
                            WHERE
                                ticketid = ? AND
                                created_by = ?
                            """,
                            (delete_selection,
                             self.user[0],)
                        )
                        self.conn.commit()
                        rowcount = self.cursor.rowcount
                        if rowcount == 1:
                            print("Successfully Delete Ticket.")
                        else:
                            print("Ticket Doesnt Exist.")
                else:
                    self.cursor.execute(
                        """
                        SELECT
                            *
                        FROM
                            tickets
                        """
                    )
                    ticket_create_by_user = self.cursor.fetchall()
                    found = False
                    for ticket in ticket_create_by_user:
                            found = True
                            print(f"TicketID: {ticket[0]}")
                            print(f"StudentID: {ticket[1]}")
                            print(f"Subject: {ticket[2]}")
                            print(f"Description: {ticket[3]}")
                            print(f"Created At: {ticket[4]}")
                            print("-" * 30)
                    
                    if not found:
                        print("No Tickets Found.") 
                    else:
                        delete_selection = int_checker("What ticket do u want too delete? (Select by ID): ")
                        self.cursor.execute(
                            """
                            DELETE
                            FROM
                                tickets
                            WHERE
                                ticketid = ?
                            """,
                            (delete_selection,)
                        )
                        self.conn.commit()
                        rowcount = self.cursor.rowcount
                        if rowcount == 1:
                            print("Successfully Delete Ticket.")
                        else:
                            print("Ticket Doesnt Exist.")                  
                                      
            elif account_menu_option == 5:
                return
            else:
                print("Invalid Option")
        
        
        