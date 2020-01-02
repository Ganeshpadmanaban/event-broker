import pickle
import os
import signal


class EventManager:

    def __init__(self, filename, user):
        self.filename = filename
        self.user = user
        self.folder = "./log_" + self.filename.split(".")[0] + "/"

        self.customers, self.processes = self.load_event_data()

    def load_event_data(self):
        """
        # loads customer & process data
        :return: dicts
        """

        # checks if any process is running or customer is present
        # else creates an empty dict
        try:
            with open(self.folder + 'processes.p', 'rb') as fp:
                processes = pickle.load(fp)
        except Exception:
            processes = {}

        try:
            with open(self.folder + 'customers.p', 'rb') as fp:
                customers = pickle.load(fp)
        except Exception:
            customers = {}

        return customers, processes

    def save_event_data(self):
        """
        # saves customer & processes dict
        :return: None
        """
        # creates a new dir with filename to save event data for future use
        os.makedirs(os.path.dirname(self.folder), exist_ok=True)
        with open(self.folder + 'processes.p', 'wb') as fp:
            pickle.dump(self.processes, fp, protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.folder + 'customers.p', 'wb') as fp:
            pickle.dump(self.customers, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def update_event_data(self):
        """
        # updates customer & processes dict when new cust is added
        :return: None
        """

        print("Adding customer to the event: ", self.user)
        try:
            self.customers[self.filename].append(self.user)
        except Exception:
            self.customers[self.filename] = [self.user]

    def check_customer_exist(self):
        """
        # checks if any process_id has 0 customers
        :return: (lst)
        """

        key_id = []

        for key, lst in self.customers.items():
            if len(lst) < 1:
                key_id.append(key)

        return key_id

    def clean_process(self, key_id):
        """
        # terminates all child processes in the dict
        :param key_id: file_id(lst)
        :return:
        """

        for key in key_id:
            os.kill(self.processes[key], signal.SIGTERM)
            print("killing the process_id: ", self.processes[key])

    def clean_dir(self):
        """
        # cleans the directory
        :return: None
        """
        # delete customer and process data / log file is not removed
        print("Cleaning files..")
        os.remove(self.folder + "processes.p")
        os.remove(self.folder + "customers.p")
