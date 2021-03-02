#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes, functions, binary data and error handling.
# Change Log: (Who, When, What)
# CScott, 2021-Feb-23, Created File
# CScott, 2021-Feb-24, Revised DataProcessor functions
# CScott, 2021-Feb-28, Incorporated feedback and edits from Assignment06 comments
# CScott, 2021-Mar-01, Revised for Assignment07
#------------------------------------------#
import pickle
# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dictionaries to hold data
dicRow = {}  # dictionary of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
CD_info = [None, None, None] # CD ID, title and artist

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data within the current inventory"""

    @staticmethod
    def add_CD(CD_info, table):
        """Adds CD to current inventory

        Args:
            CD_info (list): list of strgings containing CD ID, title and artist
            table (list): list of dictionaries
        Returns:
            None
        """
        intID = int(CD_info[0]) # Extracts intID from list CD_info
        strTitle = str(CD_info[1]) # Extracts strTitle from list CD_info
        strArtist = str(CD_info[2]) # Extracts strArtist from list CD_info
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist} # Creates dictionary containing all CD info
        table.append(dicRow)
        
    @staticmethod
    def delete_CD(intIDDel, table):
        """Deletes a specific CD from current inventory based on ID

        Args:
            intIDDel (integer): ID of the CD to be deleted from current inventory
            table (list): list of dictionaries
        Returns:
            blnCDRemoved (boolean): Boolean to track whether the specific CD ID was deleted
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            print (intRowNr)
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from serialized file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            table.clear()  # this clears existing data and allows to load data from file
            with open(file_name, 'rb') as objFile:
                pickled_data = pickle.load(objFile)
                for line in pickled_data:
                    table.append(line)
        except FileNotFoundError as e:
            with open(file_name, 'wb') as objFile:
                print('ERROR:'+ e.__doc__ +' An empty file called ' + file_name + ' was created within the working directory')
        except EOFError as e:
            print('The data file is empty! Current inventory is blank')
                

    @staticmethod
    def write_file(file_name, table):
        """Function to manage exporting data from list of dictionaries to a serialized file

        Writes the data to file identified by file_name from a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file that the data is written to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as file:
            pickle.dump(table, file)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """
        Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        print() # Add extra space for layout

    @staticmethod
    def ID_title_artist_add():
        """Gets user input for specific CD to add

        Args:
            None.

        Returns:
            CD_info (list): list containing CD ID, title and artist

        """
        while True:
            try:
                intID = int(input('Enter ID: ').strip())
                break
            except ValueError as e:
                print('ERROR: ID that was entered is not of type: integer')
                print(e.__doc__)
                
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        print() # Add extra space for layout
        CD_info = [intID, strTitle, strArtist]
        return CD_info
    
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. Start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        CD_info=IO.ID_title_artist_add()
        # 3.3.2 Add item to the table
        DataProcessor.add_CD(CD_info, lstTbl)
        # 3.3.3 Display current inventory after adding CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            removed = DataProcessor.delete_CD(intIDDel,lstTbl)
            if removed:
                print('The CD was removed')
            else:
                print('Could not find this CD!')
        except ValueError:
            print ('Please enter an integer if you would like to delete an entry \n')
            # 3.5.3 display current inventory after deleting CD
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')