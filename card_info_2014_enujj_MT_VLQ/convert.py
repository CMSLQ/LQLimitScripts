import sys
import subprocess as sp

original_masses = [ 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200]
new_masses      = [ 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800 ]
new_values      = []


VLQ_types = [
    "LQ_AM",
    "LQ_YM",
    "LQ_MC",
    "LQ_MM"
]


def getDictNames( file_name ):    
    retval = []
    data = sp.Popen ( "cat " + file_name + " | grep '{}'", shell=True, stdout=sp.PIPE ).communicate()[0]    
    entries = data.split("\n")
    for entry in entries: 
        name = entry.split("=")[0].strip() 
        if name == "": continue
        retval.append ( name ) 
    return retval

def getDict ( module_name, dict_name ) : 
    exec "from " + module_name + " import " + dict_name
    my_dict = eval ( dict_name ) 
    return my_dict

def getNewValues ( original_values ) :
    
    if len ( original_values ) > len ( original_masses ):
        new_last_index = len ( original_masses ) 
        truncated_values = original_values[:new_last_index]
    else:
        truncated_values = list(original_values)
    
    new_values = []
    for i_original_mass, original_mass in enumerate ( original_masses ) :
        if original_mass not in new_masses: continue
        value = original_values[i_original_mass]
        new_values.append ( value ) 
    n_additional_masses = len ( new_masses ) - len ( new_values ) 
    last_value = new_values[-1]
    for i in range (0, n_additional_masses): new_values.append ( last_value ) 
    return new_values

file_name   = sys.argv[1]
module_name = file_name.split(".py")[0]
dict_names  = getDictNames ( file_name ) 

new_file_name = "new_" + file_name

new_file = open ( new_file_name, "w" )

for dict_name in dict_names:
    my_dict = getDict ( module_name, dict_name ) 
    my_keys = my_dict.keys()
    new_dict = {}
    new_string = dict_name + " = {}\n"
    for key in my_keys:
        if key == "LQ" : continue
        old_values = my_dict[key]
        new_values = getNewValues ( old_values ) 
        new_dict[key] = new_values
        new_string += dict_name + "[\"" + str(key) + "\"]\t=\t" + str(new_values) + "\n"
        
    if "gjet" in my_keys:
        for VLQ_type in VLQ_types:
            new_string += dict_name + "[\"" + VLQ_type + "\"]\t=\t[" 
            for i in range(0, len(new_dict["gjet"])): new_string += "0.0, "
            new_string = new_string[:-2] + "]\n"
    
    new_file.write ( new_string + "\n" )

new_file.close()
    
        
    
    

    

