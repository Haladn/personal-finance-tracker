import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

from data_entry import get_amount, get_category,get_date,get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ['date','amount','category','description']
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            # export pandas dataframe to a csv FileExistsError
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry={
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }

        # "a" means append, so it append new entry to the end of the csv file
        with open(cls.CSV_FILE,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print('Entry added successfully')   

    @classmethod
    def  get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)

        # conver all date in csv to datetime object then we can filter them by different transactons
        # df["date"] => select the date column in  the csv file
        df['date'] = pd.to_datetime(df['date'],format=cls.FORMAT)

        start_date = datetime.strptime(start_date,cls.FORMAT) # convert to a date time object
        end_date = datetime.strptime(end_date,cls.FORMAT)   # convert to a date time object

        # mask is sth that we can apply to different rows inside dataframe to see if we should select that row or not
        mask = (df['date'] >= start_date) & (df['date'] <= end_date) # select all dates between start and end datetime
        filtered_df = df.loc[mask] # locate alle different rows within the mask range

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x:x.strftime(cls.FORMAT)}))

            total_income = filtered_df[filtered_df['category'] == "Income"]['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == "Expense"]['amount'].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}") #round it to 2 decimal point as well
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df
def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction (dd-mm-yyyy) or enter for today's date: ",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def plot_transaction(df):
    df.set_index("date",inplace=True)
    
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0) # D => daily frequency
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0) # D => daily frequency

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df['amount'], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label = "Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary whithin a date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date,end_date)

            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transaction(df)
        
        elif choice == "3":
            print('Exiting...')
            break
        else:
            print("Invalid choice. Enter 1,2 or 3.")



if __name__ == "__main__":
    main()