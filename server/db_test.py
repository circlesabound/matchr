import DB

def create_if_not_exists_john_howard(db):
    ud = {}
    ud["first_name"] = "John"
    ud["last_name"] = "Howard"
    ud["gender"] = 'm'
    ud["image"] = None
    ud["description"] = "I used to be PM"
    ud["email"] = "j.howard@gov.au"
    ud["password"] = "maddj"
    code = '''
#include <stdio.h>
int main() {
    printf("Hello World");
    return 0;
}
'''
    try:
        user_id = db.add_new_user_code(ud, code)
        print("Created new user John Howard with id {}".format(user_id))
    except ValueError:
        user_id = db.get_id_from_email(ud["email"])
        print("User John Howard already exists with id {}".format(user_id))
    finally:
        print(user_id)
        print(db.get_user_details(user_id))
    return

db = DB.DB('matchr.db')
db.connect()
create_if_not_exists_john_howard(db)
db.close()
