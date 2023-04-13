class Transaction:
    def __init__(self) -> None:
        self.__address = None
        self.__client = {
            'first_client_name': None, 
            'second_client_name': None,
            'third_client_name': None,
            'fourth_client_name': None
        }
        self.__inspection_days = {}
        self.__closing_date = None
        self.__rentback = None
        self.__directory = None # Initialize here

    def __set_directory(self):
        if isinstance(self.__address, str):
            dir = self.__address.strip()
            self.__directory = dir[:8]
        else:
            self.__directory = None

    # get and set for address
    def get_address(self):
        return self.__address
    
    def set_address(self, address):
        self.__address = address
        if isinstance(self.__address, str):
            dir = self.__address.strip().replace(' ', '')[:12] # Remove spaces from address and take the first 8 characters
            self.__directory = dir
        else:
            self.__directory = None


    #gets the client in the position of the dictionary, 
    def get_client(self, position):
        return self.__client[position] 
    
    def set_client(self, client, name):
        self.__client[client] = name

    # get and set for inspection days 
    def get_insp(self):
        return self.inspection_days
    
    def set_insp(self, start, length):
        self.__inspection_days[start] = start
        self.__inspection_days[length] = length

    #get and set for the expected closing day
    def get_closing(self):
        return self.__closing_date
    
    def set_closing(self, date):
        self.__closing_date = date

    #get and set for the rent back final day
    def get_rentback(self):
        return self.__rentback
    
    def set_rentback(self, date):
        self.__rentback = date

    def get_directory(self):
        return self.__directory
    
    # add a folder named Data to the end of the directory string
    def get_data_folder(self):
        if self.__directory is not None:
            return f"{self.__directory}/data"


billz = Transaction()
billz.set_address('14825 SE 119th Clackamas OR')
print(billz.get_data_folder())
