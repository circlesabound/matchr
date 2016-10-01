import sqlite3
import hashlib
import os.path

class db(object):

    def __init__(self, db_path):
        if not os.path.isfile(db_path):
            raise FileNotFoundError
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """
        Establishes a connection to the database.

        :raises RuntimeError: if a database connection has already been established
        """
        if self.conn is not None:
            raise RuntimeError
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """
        Closes the connection to the database.

        :raises RuntimeError: if there is no currently open database connection
        """
        if self.conn is None:
            raise RuntimeError
        self.conn.close()
        self.conn = None

    def check_credentials(self, email, password):
        """
        Validates a given email address and password against user records in the database.

        :param email: <str> an email address
        :param password: <str> a plain-text password
        :returns: [ None, <int> ] the user id of the matching user if one exists, otherwise None
        """
        c = self.conn.cursor()
        hashed = hashlib.sha256(password.encode('utf-8'))
        c.execute('''SELECT id
                FROM users
                WHERE email=? AND password=?''',
                (email,
                hashed.hexdigest()))
        result = c.fetchone()
        if result is not None:
            return int(result["id"])
        else:
            return None

    def get_next_match(self, user_id):
        """
        Finds the next matched user for the specified user.

        :param user_id: <int> a user id
        :returns: [ None, <int> ] the user id of the next matched user if one exists, otherwise None
        :raises ValueError: if the specified user does not exist in the database
        """
        #TODO
        return None

    def add_new_user(self, user_dict):
        """
        Adds a new user to the database and constructs all required relationship records.

        :param user_dict: a dictionary with the following key-value mappings:
                first_name      =>  <str>
                last_name       =>  <str>
                gender          =>  [ None, 'm', 'f' ]
                image           =>  [ None, <str> ]
                description     =>  <str>
                email           =>  <str>
                password        =>  <str>
                brace_placement =>  <int> #TODO
                space_or_tab    =>  <int> #TODO
                indent_amount   =>  <int> #TODO
                var_convention  =>  <int> #TODO
                comment_style   =>  <int> #TODO
                max_line_length =>  <int> #TODO
        :returns: <int> the user id of the newly created user
        :raises ValueError: if the specified email address already belongs to an existing user
        :raises KeyError: if there are missing fields in the user dict parameter
        """
        c = self.conn.cursor()
        #TODO
        return user_id

    def get_user_details(self, user_id):
        """
        Returns the full user details for the specified user.

        :param user_id: <int> a user id
        :returns: a dictionary with the following key-value mappings:
                first_name      =>  <str>
                last_name       =>  <str>
                gender          =>  [ None, 'm', 'f' ]
                image           =>  [ None, <str> ]
                description     =>  <str>
                email           =>  <str>
                password        =>  <str>
                brace_placement =>  <int> #TODO
                space_or_tab    =>  <int> #TODO
                indent_amount   =>  <int> #TODO
                var_convention  =>  <int> #TODO
                comment_style   =>  <int> #TODO
                max_line_length =>  <int> #TODO
        :raises ValueError: if the specified user does not exist in the database
        """
        c = self.conn.cursor()
        c.execute('''SELECT *
                FROM users
                WHERE id=?''',
                user_id)
        result = c.fetchone()
        if result is None:
            raise ValueError
        user_dict = {}
        #TODO
        return user_dict

    def get_compatibility_score(self, user_id_1, user_id_2):
        """
        Returns the compatibility score between the two specified users.

        :param user_id_1: <int> a user id
        :param user_id_2: <int> a user id
        :returns: <int> a compatibility score #TODO
        :raises ValueError: if either specified user does not exist in the database
        :raises RuntimError: if a relationship record between the two specified users cannot be found
        """
        #TODO
        return compatibility_score

    def set_relationship_status(self, user_id_1, action, user_id_2):
        """
        Changes the status of the relationship between the two specified users.

        :param user_id_1: <int> the user id of the user that triggered the action
        :param action: [ "reset", "accepts", "rejects" ] the action performed by user 1 in regard to their relationship to user 2
        :param user_id_2: <int> the user id of the user receiving the action
        :raises ValueError: if either specified user does not exist in the database
        :raises RuntimeError: if a relationship record between the two specified users cannot be found
        """
        #TODO
        return

