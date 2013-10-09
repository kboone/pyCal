from pycal import Bspace

a = Bspace()
a.printSites()

a.sites[2].printPages()
a.sites[2].printAssignments()
#a.sites[2].downloadAssignments()
a.sites[2].download()


#import pdb
#pdb.set_trace()
