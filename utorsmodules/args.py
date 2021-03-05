import sys

def checkArgs():
    global config
    config = {
        "period": None,
        "transcriptions": False,
        "transcribers": False,
        "checkClaim": False,
        "userToCheck": "",
        "coverage": False,
        "verbose": False,
        "refreshable": False,
        "graph": False,
        "graphType": "",
    }
    
    args = sys.argv
    args.pop(0)
    for arg in args:
        getPeriod(arg)
        if arg in ["--transcriptions", "--transcribers", "--coverage", "--verbose", "--refreshable"]:
            config[arg.split('--')[1]] = True
        elif arg == "--claims":
            config["checkClaim"] = checkClaim(args)
        elif arg.split("=")[0] == "--graph":
            config["graph"] = graph(args)
        else:
            if config["period"] is None: print(f" Error: unrecognised argument. Argument is: {arg}")
    
    if config["coverage"] and not config["transcriptions"]:
        print(" Cannot calculate coverage without measuring transcriptions; setting transcriptions to True.")
        config["transcriptions"] = True
    
    if program(): return config
    else: print(" No functions set to True; exiting."); sys.exit(0)
    

def program():
    if config["period"] is None: print(" Missing required period argument; exiting."); sys.exit(0)
    for i in config:
        if config[i] and i in ["transcriptions", "transcribers", "checkClaim", "coverage"]: return True
    return False

def checkClaim(argv):
    for arg in argv:
        try:
            if arg.split['='][0] == "--user":
                config["userToCheck"] = arg.split['='][1]
                return True
        except IndexError: pass
    print(" Error: -claims was passed but no user was given to check. Will be set to false for this instance.")
    return False

def getPeriod(arg):
    if arg.split('=')[0] in ["--period", "-p"]:
        try: config["period"] = int(arg.split("=")[1]); return True
        except ValueError: print(" Error: --period was passed but no period was specified; exiting."); sys.exit(0)

def graph(argv):
    for arg in argv:
        try:
            if arg.split('=')[1] in ["pie", "barH", "barV"]:
                config["graphType"] = arg.split('=')[1]
                return True
        except IndexError: pass
    print(" Error: --graph was passed but no graph type was specified. Will be set to false for this instance.")
    return False
