"""
Modules for doing bulk of work
"""
import toml


# Code block function to retrieve posts, sort, flag those that are newer



# code block to open up and read the config files


def open_read_config (mainconfigfile_name):
    main_config = readMainConfig(mainconfigfile_name)
    statefile_name = main_config['GENERAL']['statefile']
    state_config = readStateConfig(statefile_name)
    configs = {
        'main_config':main_config,
        'state_config':state_config,
        }
    
    return (configs)

# class update_state_info:
    '''
    Update the state info with last read times, etc
    (stateoutfile_name,stateData2write):
    '''
    # def      
#    i = writeStateConfig(stateoutfile_name,stateData2write)

#    return i


# Smaller functions to read and write config info


def readMainConfig (mainconfigfile_name):

    with open(mainconfigfile_name, 'r') as mainconfigfile:
        toml_in = toml.load(mainconfigfile)

    mainconfigfile.close()
    return toml_in

def readStateConfig (stateconfigfile_name):

    with open (stateconfigfile_name, 'r') as stateconfigfile:
        statetoml_in = toml.load(stateconfigfile)

    stateconfigfile.close()
    return statetoml_in


def writeStateConfig (stateoutfile_name, stateData2write):
    with open(stateoutfile_name, 'w') as stateoutfile:
        toml.dump(stateData2write, stateoutfile)
    i=stateoutfile.close()
    return (i)
    



