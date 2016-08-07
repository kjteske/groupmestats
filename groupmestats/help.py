import pkg_resources

def gstat_help():
    entry_map = pkg_resources.get_entry_map("groupmestats")
    console_scripts = entry_map["console_scripts"]
    print("Available commands:")
    for name in console_scripts.keys():
        if name != 'gstat_help':
            print("    - " + name)
    print("Run `<command> --help` for details on each command")
    # print("Available commands:gstat_fetch_data
