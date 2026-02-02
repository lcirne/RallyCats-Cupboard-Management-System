
import pandas as pd
import sqlite3
from datetime import datetime

'''
Database Management file
'''

class Database:
    # Read in example date
    def __init__(self):
        self.cn = sqlite3.connect('RallyCats.db')
        self.cur = self.cn.cursor()
        self.inventory_df = pd.DataFrame(pd.read_csv("dummy_data.csv"))
        self.users_df = pd.DataFrame(pd.read_csv("user_data.csv"))

    def load_db(self):
        if self.cur.fetchall():
            print("Database loaded")
        else:
            self.inventory_df.to_sql('Inventory', self.cn, if_exists='replace', index=False)
            self.users_df.to_sql('Users', self.cn, if_exists='replace', index=False)
        #print(self.inventory_df)

    def print_db(self):
        rows = self.cn.execute("SELECT * FROM Inventory").fetchall()
        for row in rows:
            print(row)

    def close_db(self):
        self.cn.close()
        self.cur.close()

    # Add item

    def addItem(self, n, br, amt, cat, don, veget, kosh, vega, hall, exp, req):
        query = """INSERT INTO Inventory (name, brand, quantity, category, 
                       donor, vegetarian, kosher, vegan, hallal, expiration, requested) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        try:
            year = exp[0:4]
            month = exp[5:7]
            day = exp[8:11]
            target_date = datetime(int(year), int(month), int(day))
            current_date = datetime.now()
            expiration = (target_date - current_date).days + 1
            print(expiration)
            expiration = (target_date - current_date).days + 1
        except ValueError:
            print('Expiration date conversion failed')
        self.cur.execute(query, (n, br, amt, cat, don, veget, kosh, vega, hall, expiration, req))
        self.cn.commit()

# Remove item
    def removeItem(self, n):
        query = ("""DELETE FROM Inventory WHERE name = ?""")
        self.cur.execute(query, (n,))
        self.cn.commit()

    # Change quantity
    def changeQuantity(self, n, amt):
        query = """UPDATE Inventory SET quantity = ? WHERE name = ?"""
        self.cur.execute(query, (amt, n))
        self.cn.commit()


    # Check for expirations
    def checkExpirations(self):
        self.cur.execute("""SELECT * FROM Inventory WHERE expiration <= 30""")
        expires_soon = self.cur.fetchall()
        output = []
        for item in expires_soon:
            output.append([item[0], item[9]])
        self.cn.commit()
        return output



    # Check for low quantity
    #returns a list of [name, quantity]
    def lowQuanity(self):
        self.cur.execute("""SELECT * FROM Inventory WHERE quantity <= 5""")
        low = self.cur.fetchall()
        output = []
        for i in low:
            output.append([i[0], i[2]])
        self.cn.commit()
        return output




def Testing():
    db = Database()
    db.load_db()

    # Add a test item
    db.addItem("Test Item", "Test Brand", 10, "non-perishable",
               1, 1, 1, 1, 1, "2025-03-11", 0)

    # Change quantity of test item
    db.changeQuantity("Test Item", 25)

    #print(db.lowQuanity())

    # Remove test item
    db.removeItem("Apples")

    # Check for expirations less than 30
    print(db.checkExpirations())

    # Print all rows
    #db.print_db()

    print("\n--- Tests Completed Successfully ---")


if __name__ == '__main__':
    Testing()