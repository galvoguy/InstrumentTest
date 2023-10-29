#Automated Vitrek V74 test to be performed on all 3 permutations of motor phases. 
# Example: ADD,IR,1000.0,60.0,0.0,100e6,
# Configures test to : IR mode, 1000V, 60 sec dwell, 0 delay, 100M ohm min IR limit, No max IT limit, DUT is isolated.
# Missing end fields translate to delfauts (No max IR, Isolated DUT, and Dut is resistive)

import pyvisa as visa
import os
import time

rm=visa.ResourceManager()
resource_list_detailed = rm.list_resources_info() #Lists detailed info if needed to select correct device
print(resource_list_detailed)
resource_list = rm.list_resources() #Lists simple format
resource_name = "No resource selected" #Init variable
print(resource_list)

#Select the correct resource (instrument port)
for x in resource_list:
    if "A" in x:          #Set this string to be unique to the Vitrek V74 USB Id. 
        resource_name = x #String to use. Example "ASRL3::INSTR"
print('Resource Name: ', resource_name)

my_tester = rm.open_resource(resource_name)

#Initialize
my_tester.write('*RST') # Clear the buffers of the V74
print (my_tester.query('*ERR?')) # Check if the reset and comms work.

my_tester.read_termination = '/r' # Sets PC to use Carriage Return character 
my_tester.write_termination = '/r' #Sets PC to use Carriage Return character 
header_string = my_tester.query('*IDN?') 
print(header_string) #should be something like "VITREK, V74, 00000000, v1.15"

# Create the test sequence
my_tester.write('NOSEQ') # Clear and set active sequence to #0
my_tester.write('ADD', 'IR', '1000.0', '60.0', '0.0','100e6',) #Add command to sequence, IR mode, 1000 Volts, 60 sec dwell, 0 delay, 100M ohm min IR limit, No max IT limit, DUT is isolated, DUT is resistive.
print (my_tester.query('*ERR?')) # Check if the command was received.
#Use the above 2 lines as a template for more commands in the #0 sequence.  

#Run the sequence
my_tester.write('RUN') #The V74 will run the entire sequence asyncronously...

while my_tester.write('STEP?') != 0:
    #do nothing and wait
    print("Waiting for test to complete")

#Gather the test results
result = my_tester.write('STEPRSLT?')
print(result)

# TODO parse the result into JSON fields into the database. 

# TODO: embed into GUI that prompts the user to change leads onto 3 combinations of phases and hit run again. 

