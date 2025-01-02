

def wrraper(func):
    def design():
        print ("************")
        func()
        print ("************")
    
    return design







@wrraper
def star():
    print ("This is Five Starts")



star()