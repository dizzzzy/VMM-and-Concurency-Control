import pickle
from Page import Page

with open("memconfig.txt") as a:
    max_pages = a.read()

command_list = []
with open("commands.txt") as a:
    c_list = a.readlines()[0:]
    for ind, com in enumerate(c_list):
        sub_commands = com.split(" ")
        command_list.append(sub_commands)


class VMM:
    def __init__(self):
        self.max_memory = int(max_pages)
        self.main_memory = []  #list of Pages
        for i in range(self.max_memory):
            page = Page()
            self.main_memory.append(page)
        self.disk_memory = "vm.txt"
        self.command_list = command_list

    def store(self, variable_id, value):
        boolean, index = any_i(page.var_id == '' for page in self.main_memory)
        if boolean:
            self.main_memory[index].var_id = variable_id
            self.main_memory[index].var_value = value
            self.main_memory[index].update_was_used()
        else:
            with open(self.disk_memory, 'a') as the_file:
                the_file.write(str(variable_id) + " " + value)
        # self.main_memory.append(zip(variable_id, value))
        # with open(self.disk_memory, 'w') as f:
        #     pickle.dump(self.main_memory, f)

    def release(self, variable_id):
        boolean, index = any_i(page.var_id == variable_id for page in self.main_memory) # found in main memory?
        if boolean:   # true
            temp = self.main_memory.pop(index)
            return ["Main memory", temp]
        else:   # false
            disk = open(self.disk_memory, "r+")
            d = disk.readlines()
            disk.seek(0)
            found = False
            for i in d:
                variable = i.split(" ")
                if variable[0] != variable_id:
                    disk.write(i)
                else:
                    found = True
                    released_var = variable
            disk.truncate()
            disk.close()
            if found:
                return released_var
        if not found:
            return -1

    def lookup(self, variable_id):
        boolean, index = any_i(page.var_id == variable_id for page in self.main_memory)  # found in main memory?
        if boolean:  #  yes
            self.main_memory[index].update_was_used()
            return ["Main memory", self.main_memory[index].var_id, self.main_memory[index].var_value]
        else:  #  no
            disk = open(self.disk_memory, "r+")
            d = disk.readlines()
            disk.seek(0)
            found = False
            for i in d:
                variable = i.split(" ")
                if variable[0] != variable_id:
                    disk.write(i)
                elif not found:   #  Makes sure that 2 swaps are not performed
                    found = True      # found variable
                    boolean, ind = any_i(page.var_id == '' for page in self.main_memory)   # any empty pages?
                    if boolean:   #  yeaaaa -->
                        self.main_memory[ind].var_id = variable[0]
                        self.main_memory[ind].var_value = variable[1]
                    else:       #  nooo --> Need to perform a swap with the oldest var in memory
                        oldest_age = ''
                        for page in self.main_memory:
                            if oldest_age == '':
                                oldest_age = page.aging_counter
                                oldest_page = page
                            elif page.aging_counter < oldest_age:
                                oldest_age = page.aging_counter
                                oldest_page = page
                        old_var_id, old_var_value = oldest_page.var_id, oldest_page.var_value     # found oldest variable in main mem
                        oldest_page.var_id = variable[0]
                        oldest_page.var_value = variable[1]
                        oldest_page.update_was_used()
                        temp_string = str(old_var_id) + " " + str(old_var_value)
                        disk.write(temp_string)
            disk.truncate()
            disk.close()
        if not found:
            return -1

    def update_age_counters(self):
        for page in self.main_memory:
            page.update_age_counter()


def any_i(iterable):
    for i, element in enumerate(iterable):
        if element:
            return [True, i]
    return [False, '']


