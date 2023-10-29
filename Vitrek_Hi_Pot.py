# Vitrek Hi-Pot Automation

import pyvisa as visa
import os
import time

rm=visa.ResourceManager()
resource_list_detailed = rm.list_resources_info() #Lists detailed info if needed to select correct device
print(resource_list_detailed)
resource_list = rm.list_resources() #Lists simple format
resource_name = "Temp"
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
my_tester.write('ADD', 'DCW', '1750.0', '5', '30.0',' ','0.005') #Add command to sequence, DC mode, 1750 Volts, 5 second ramp, 30 second dwell, no min leakage I, 5mA max leakage I, DUT is isolated because field 7 is blank. 
print (my_tester.query('*ERR?')) # Check if the command wqsa received.
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
























