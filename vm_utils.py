from mmap import MADV_NOHUGEPAGE
from pyVmomi import vim
from pyVim.connect import SmartConnect
import ssl
import getpass
vcenter_server = 'vcenter.tanner.local'

def login():   
    vcenter_user = input("Please enter a username: ")
    passw = getpass.getpass()
    s=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    si = SmartConnect(host=vcenter_server, user=vcenter_user, pwd=passw, sslContext=s)
    return si
    
# Getting the objects for the VMs and applying a filter
def vmName(content, vimtype, filter):
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for managed_object_ref in container.view:
        if managed_object_ref.name == filter:
            obj.update({managed_object_ref: managed_object_ref.name})
        elif filter == "":
            obj.update({managed_object_ref: managed_object_ref.name})
    return obj

def menu():
    print("[1] list VMs ")
    print("[2] Pyvmomi Session")
    print("[3] VM Hostname and Usernames")
    print("[0] Exit Program")

def main():
    si = login()
    content = si.RetrieveContent()
    menu()
    option = int(input("Please select an option: "))

    while option != 0:
        if option == 1:
            filter = input("Please enter a filter name: ")
            getAllVms = vmName(si.content, [vim.VirtualMachine], filter)
            for vm in getAllVms:
                print("name: ", vm.name)
                print("Memory: ",vm.config.hardware.memoryMB // 1024, "GB")
                print("CPU: ",vm.config.hardware.numCPU)
                print("State: ",vm.guest.guestState)
                print("IP: ",vm.guest.ipAddress)
                print("Full Name: ",vm.config.guestFullName)
        elif option == 2:
            session = si.content, [vim.HostSystem]
            for session in si.content.sessionManager.sessionList:
                print(
                    "username = {0.userName}"
                    "\n ip={0.ipAddress}".format(session)  
                )
            aboutInfo = si.content.about
            print(aboutInfo.name)
            print("option 2")
        elif option == 3:
            file1 = open("vcenter.txt", "r")
            print("Hostname")
            print(file1.readline(9))
            print("Username")
            print(file1.readline(18))
        else:
            print("Invalid option")
        
        menu()
        option = int(input("Please select an option: "))
        

    print("Thanks for running this program")

main()
