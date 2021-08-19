import datetime
def log(str, show_time=True, vis=True):
    if str == "":
        print()
        return
    if vis:
        print(f"[{datetime.datetime.now()}] [*] {str}")
    
    
