import pandas as pd
import numpy as np
import errors
from natsort import humansorted, ns_enum, ns



class process_dataframe():
    required_fields = ["Street", "Zip", "City", "Last Check-In Date", "Company"]
    fields_to_delete = []

    # method to initialise dataframe, read from csv and check against exceptions
    def initialise_dataframe(self):
        data = process_dataframe().read_dataframe()
        # call methods to check for exceptions
        process_dataframe().check_for_required_fields(data)
        process_dataframe().check_empty_rows(data)
        process_dataframe().check_empty_fields(data)
        # Give user the option to call the method to delete problem rows, if any.
        if len(self.fields_to_delete):
            data = process_df.delete_rows(data)
        return data

    # method to read data
    def read_dataframe(self):
        # read csv data into pandas dataframe
        dataframe = pd.read_csv('data.csv')
        return dataframe

    # Method to check all required fields are present
    def check_for_required_fields(self, dataframe):
        # Check that all required fields are filled out, if not list the rows that aren't
        rows_without_required_fields = []
        for field in self.required_fields:
            rows_without_required_fields = np.where(dataframe[field].isnull())[0]

        # if any rows have empty required fields, raise exception
        needs_fixing = False
        try:
            if len(rows_without_required_fields):
                raise errors.RequiredFieldEmptyError
        except errors.RequiredFieldEmptyError:
            print("[Exception] Rows did not have all required fields filled in!")
            needs_fixing = True

        # if the exception was raised append rows that don't have required fields to rows to delete
        if needs_fixing:
            for item in rows_without_required_fields:
                self.fields_to_delete.append(item)

    # Method to check that no fields in the dataframe are empty
    def check_empty_fields(self, dataframe):
        # Get list of rows with empty fields
        rows_with_empty_fields = np.where(dataframe.isnull())[0]
        rows_with_empty_fields = list(dict.fromkeys(rows_with_empty_fields))

        # if any rows have empty fields, raise exception
        needs_fixing = False
        try:
            if rows_with_empty_fields is not []:
                raise errors.LessInfoThanExpectedError
        except errors.LessInfoThanExpectedError:
            print("[Exception] Some rows had missing data")
            needs_fixing = True
        # if the exception was raised append rows that don't have required fields to rows to delete
        if needs_fixing:
            for item in rows_with_empty_fields:
                self.fields_to_delete.append(item)

    # Method checks whether a value is invalid (Nan, not a number is not equal to itself)
    def isNaN(self, val):
        return val == val

    # Method to check for empty rows
    def check_empty_rows(self, dataframe):
        empty_rows = []
        # put all empty rows into list
        for x in range(len(dataframe)):
            row = dataframe.iloc[x, :]
            a = row.values.tolist()
            invalid_values = 0
            for value in a:
                if not process_dataframe().isNaN(value):
                    invalid_values += 1
                if invalid_values >= 10:
                    empty_rows.append(x)
        # If there are empty rows raise exception and add these to the fields that are to be deleted
        needs_fixing = False
        try:
            if len(empty_rows):
                raise errors.NoDataOnRowError
        except errors.NoDataOnRowError:
            print("[Exception] Some rows were empty")
            needs_fixing = True
        if needs_fixing:
            for item in empty_rows:
                self.fields_to_delete.append(item)

    # Method to delete problem row
    def delete_rows(self, dataframe):
        self.fields_to_delete = list(dict.fromkeys(self.fields_to_delete))
        # let the user decide whether they want these rows removed
        correct_answer = False
        while not correct_answer:
            print("Some rows have raised exceptions do you want to delete them? y/n")
            answer = input("type y to delete them, n to keep the table as is: ")
            if answer.lower() == 'y':
                dataframe = dataframe.drop(dataframe.index[self.fields_to_delete])
                print("Rows without required fields were deleted.")
                correct_answer = True
            elif answer.lower() == 'n':
                print("Table will be kept as is.")
                correct_answer = True
            else:
                print("Please input a valid answer, either y or n")
        return dataframe

# Method to obtain list of names alphabetically
    def get_list_of_names_alphabetically(self, dataframe):
        # Slice dataframe so that it's only first and last names
        names =  dataframe.iloc[:,0]
        surnames = dataframe.iloc[:,1]
        names = names.values.tolist()
        surnames = surnames.values.tolist()
        full_names = []
        # join these in a new array
        for index in range(len(names)):
            full_names.append(str(names[index]) + " " + str(surnames[index]))
        # order and return array
        full_names = humansorted(full_names,alg=ns.REAL | ns.LOCALE | ns.IGNORECASE)
        return full_names

# Method to sort dataframe by date
    def sort_by_dob(self, dataframe):
        # sort dataframe by date
        dataframe["Last Check-In Date"] = pd.to_datetime(dataframe["Last Check-In Date"], dayfirst=True)
        dataframe.sort_values(by='Last Check-In Date', inplace=True)
        # return dataframe
        return dataframe

# Method to get customer with latest check-in date
    def get_customer_last_checkin_date(self, dataframe):
        # call method to sort dataframe by date
        dataframe = process_dataframe().sort_by_dob(dataframe)
        # return last item
        return dataframe.iloc[-1,:]


# Method to get customer with earliest check-in date
    def get_customer_first_checkin_date(self, dataframe):
        # call method to sort dataframe by date
        dataframe = process_dataframe().sort_by_dob(dataframe)
        # return first item
        return dataframe.iloc[0, :]

process_df = process_dataframe()

# read dataframe
dataframe = process_df.initialise_dataframe()

# Get list of clients in alphabetical order
print("-------List of customers ordered alphabetically: -------")
print(process_df.get_list_of_names_alphabetically(dataframe))

# Get first and latest clients to check-in
print("-------Latest customer to check-in: ------- ")
print(process_df.get_customer_last_checkin_date(dataframe))
print("-------First customer to check-in: -------")
print(process_df.get_customer_first_checkin_date(dataframe))
