import sys
import io
import os
import difflib
import datetime
from multiprocessing import Process

from event_manager import EventManager


class EventFileDiff(EventManager):

    def create_subprocess(self):
        """
        # creates subprocess for each setting
        :return: process_id
        """

        print("Starting file tracking process..\n")

        # child process runs intermittently irrespective of the main program
        spawn_process = Process(target=self.processing)
        spawn_process.start()
        return spawn_process.pid

    # noinspection PyMethodMayBeStatic
    def write_file(self, output_log, modded_time):
        """
        # writes the output with ext .out
        :param output_log: data (lst)
        :param modded_time: time (str)
        :return: None
        """

        orig_stdout = sys.stdout
        os.makedirs(os.path.dirname(self.folder), exist_ok=True)
        f = open(self.folder + "_log_" + self.filename, 'a')
        sys.stdout = f

        print("Modified time: ", modded_time)
        print("=" * 60)
        for val in output_log:
            print(val, end="\n")
        print("=" * 60)
        print("\n")

        sys.stdout = orig_stdout
        f.close()

    def check_diff(self, original_file, modded_timestamp):
        """
        # compares two files and gives diff
        :param original_file: data (lst)
        :param modded_timestamp: time (str)
        :return: None
        """

        """Show diff of files changed (between index and working copy)."""

        modified_file = io.open(self.filename, mode="r", encoding="utf-8").read()

        index_lines = original_file.splitlines()
        working_lines = modified_file.splitlines()

        diff_lines = difflib.unified_diff(index_lines, working_lines, "original_file", "modified_file", lineterm='')

        self.write_file(output_log=diff_lines, modded_time=modded_timestamp)

    def modification_date(self):
        """
        # returns the time when file was last modified
        :return: (str)
        """
        t = os.path.getmtime(self.filename)
        return str(datetime.datetime.fromtimestamp(t))

    def get_status(self):
        # prints stuff
        print("="*50)
        print("Tracking file: ", self.filename)
        print("Customers: ", self.customers[self.filename])
        print("process_id: ", self.processes[self.filename])
        print("\n")

    def processing(self):
        """
        # continiously tracks the file (exit is only if all users leave - check main())
        :return: None
        """

        # take the recent change to the file
        last_modified = self.modification_date()
        file_data = io.open(self.filename, mode="r", encoding="utf-8").read()

        while True:
            # check for new modification
            modified = self.modification_date()

            if last_modified != modified:
                last_modified = modified

                # find diff btw files
                self.check_diff(file_data, modified)

                # update the old file in memory
                file_data = io.open(self.filename, mode="r", encoding="utf-8").read()

    def main(self, cmd):
        """
        # add/remove/kill user and processes
        :param cmd: input arg (str)
        :return: None
        """

        # adding new customers to the event
        if cmd == "ADD":

            if self.filename not in self.processes.keys():
                self.update_event_data()
                self.processes[self.filename] = self.create_subprocess()

            else:
                self.customers[self.filename].append(self.user)

            self.get_status()
            self.save_event_data()

        # removing customers from the event
        # if customer name doesnt exist in the dict, show error -> to do
        elif cmd == "REMOVE":
            print("Removing customer..")
            self.customers[self.filename].remove(self.user)
            self.get_status()
            self.save_event_data()

            key_id = self.check_customer_exist()

            if len(key_id) > 0:
                print("\nNo customer exists in the event, hence killing all processes")
                self.clean_process(key_id=key_id)
                self.clean_dir()

        # kill all subprocesses and clean the directory
        else:
            print("Killing all processes")
            for key, pid in self.processes.items():
                print("killing the process_id: ", self.processes[key])
                os.system('pkill -TERM -P {pid}'.format(pid=pid))

            try:
                self.clean_dir()
            except Exception:
                pass


if __name__ == "__main__":

    fname = sys.argv[1]
    usr = sys.argv[2]

    efd = EventFileDiff(filename=fname, user=usr)

    efd.main(cmd=sys.argv[3])
    os._exit(0)
