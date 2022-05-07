import pandas as pd
import numpy as np
import errors



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
            data = a.delete_rows(data)
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
            a = np.where(dataframe[field].isnull())[0]
            for item in a:
                rows_without_required_fields.append(item)

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
# Slice dataframe so that it's only first and last names
# join these in a new array
# order and return array

# Method to sort dataframe by date
# sort dataframe by date
# return dataframe

# Method to get customer with latest check-in date
# call method to sort dataframe by date
# return last item

# Method to get customer with earliest check-in date
# call method to sort dataframe by date
# return last item

a = process_dataframe()

# read dataframe
dataframe = a.initialise_dataframe()

print(dataframe)
