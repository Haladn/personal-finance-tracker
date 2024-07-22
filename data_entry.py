from datetime import datetime

date_format = "%d-%m-%Y"

CATEGORIES = {"I":"Income","E":"Expense"}
def get_date(prompt,allow_default = False):
    date_str = input(prompt)
    if allow_default and not date_str:
        # strftime = string format time => change time to string format to be more readable
        return datetime.today().strftime(date_format)
    
    try:
        # strptime => convert string to datetime object in the given format
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)  # format the datetime object to string then return it
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt,allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()




def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expence): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category



def get_description():
    return input("Enter a description (optional): ")