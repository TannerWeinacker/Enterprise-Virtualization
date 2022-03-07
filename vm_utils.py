from mmap import MADV_NOHUGEPAGE
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnect
import cli
import pchelper
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
    print("[4] VM Actions")
    print("[0] Exit Program")

def action_menu():
    print("[1] Power On ")
    print("[2] Power Off")
    print("[3] Create Snapshot")
    print("[4] Change VM Specs")
    print("[5] Delete a VM")
    print("[6] Create a VM")
    print("[0] Menu")

def vmactions(content):
    action_menu()
    option = int(input("Please select an option: "))
    while option != 0:
        if option == 1:
            poweron(content)
        if option == 2:
            poweroff(content)
        if option == 3:
            create_snapshot(content)
        if option == 4:
            change_specs(content)
        if option == 5:
            createnew(content)
        if option == 6:
            destroy(content)
        if option == 0:
            menu()
        else:
            print("Invalid option")
    
        action_menu()
        option = int(input("Please select an option: "))

def destroy(content):
    filter = input("Please Enter a VM Name: ")
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for managed_object_ref in container.view:
        if managed_object_ref.name == filter:
            obj.update({managed_object_ref: managed_object_ref.name})
        elif filter == "":
            print("VM does not exist")
    getAllVms = obj
    for vm in getAllVms:
        vm.Destroy()

def createnew(content):
    destination_host = pchelper.get_obj(content, [vim.HostSystem]) 
    datacenter_name = "SYS350"
    source_pool = destination_host.parent.resourcePool
    datastore_name = "datastore2-super11"
    config = create_config(datastore_name=datastore_name, name="test")

    for child in content.rootFolder.childEntity:
        if child.name == datacenter_name:
            vm_folder = child.vmfolder
        else:
            print("Invalid")

    vm_folder.CreateVM(config, pool=source_pool, host=destination_host)
    
def create_config(datastore_name, name):
    datastore_name = "datastore2-super11"
    guest="otherGuest"
    annotation="Sample"
    config = vim.vm.configSpec()
    config.annotation = annotation
    config.memoryMB = int(input("Enter in your desired memory: "))
    config.guestID = guest
    config.name = name
    config.numCPUs = int(input("Enter in your desired CPUs: "))
    files = vim.vm.FileInfo()
    files.vmPathName = "["+datastore_name+"]"
    return config

def obj(content, getAllVms):
    filter = input("Please Enter a VM Name: ")
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for managed_object_ref in container.view:
        if managed_object_ref.name == filter:
            obj.update({managed_object_ref: managed_object_ref.name})
        elif filter == "":
            print("VM Not found")
            change_specs(content)
    getAllVms = obj

def change_specs(content, getAllVms):
    change = input("Please enter what you want to change: ")
    print("Make sure the VM is powered off!")
    if change == "CPU":
        obj(content)
        vm_cpus = int(input("Enter a new amount of CPUs: "))
        for vm in getAllVms:
            vim.vm.ConfigSpec(numCPUs = vm_cpus)
    elif change == "Name" :
        obj(content)
        vm_name = input("Enter a new name: ")
        for vm in getAllVms:
            vim.vm.ConfigSpec(name = vm_name)
    elif change == "Memory":
        obj(content)
        vm_mem = int(input("Enter a new amount of memory: "))
        for vm in getAllVms:
            vim.vm.ConfigSpec(memoryMB = vm_mem)
    else:
        print("Option not valid! \n Please try CPU, Name, or Memory")

def create_snapshot(content):
    filter = input("Please Enter a VM Name: ")
    print("Make sure the VM is powered off!")
    snap_des = input("Enter a description for the snapshot: ")
    snap_name = input("Enter a name for the snapshot: ")
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for managed_object_ref in container.view:
        if managed_object_ref.name == filter:
            obj.update({managed_object_ref: managed_object_ref.name})
        elif filter == "":
            print("VM Not found")
    getAllVms = obj
    for vm in getAllVms:
        vm.CreateSnapshot_Task(name = snap_name, description = snap_des, memory = True, quiesce=False)


def poweron(content):
    filter = input("Please Enter a VM Name: ")
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for managed_object_ref in container.view:
        if managed_object_ref.name == filter:
            obj.update({managed_object_ref: managed_object_ref.name})
        #elif filter == "":
         #   print("VM does not exist")
          #  createvm = input("Would you like to create one?(Y/N)")
           # createvm
           # if createvm == "Y" or "y":
            #    createvm()
        elif filter == "":
            print("VM Not found")
            poweron(content)
    getAllVms = obj
    for vm in getAllVms:
        vm.PowerOn()
        print("VM has been powered on!")

def poweroff(content):
    filter = input("Please Enter a VM Name: ")
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    for managed_object_ref in container.view:
        if managed_object_ref.name == filter:
            obj.update({managed_object_ref: managed_object_ref.name})
        elif filter == "":
            print("VM Not found")
            poweroff(content)
    getAllVms = obj
    for vm in getAllVms:
        vm.PowerOff()
        print("VM has been powered off!")


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
        elif option == 4:
            vmactions(content)
        else:
            print("Invalid option")
        
        menu()
        option = int(input("Please select an option: "))
        

    print("Thanks for running this program")

main()
