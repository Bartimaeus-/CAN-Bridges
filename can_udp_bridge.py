from gooey import Gooey
from gooey import GooeyParser

import os

import socket
import json
import can
import cantools

db = cantools.database.Database()
baudDict = {'125 kbps':125000,'250 kbps':250000,'500 kbps':500000,'1000 kbps':1000000}

#set up UDP socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

# Script execution goes here
def runCommand(args):
    inputFiles = args.DBC_files
    port = args.port
    ip = args.IPaddress
    
    busType = args.CAN_Device
    
    timestampName = args.JSONtimestamp
    
    bus = can.interface.Bus(bustype=busType, bitrate = baudDict[args.baud])
    # bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=baudDict[args.baud])
    print('UDP Config | IP Address: ',ip, '    Port: ',port)
    
    for inputFile in inputFiles:
        db.add_dbc_file(inputFile)
        db.refresh()

    
    while True:
        message = bus.recv()
        
        print('Message Received. ID: ', message.arbitration_id)
        
        message_matched = False
        
        try:
            signals = db.decode_message(message.arbitration_id, message.data)
            
            msg = db.get_message_by_frame_id(message.arbitration_id)
            message_matched = True
        except: #To-Do: better handling. db.decode_message raises an exception if the message isn't in any of the messages. See if there's a better way to test this insstead of a try/except
            message_matched = False
        
        if(message_matched):            
            msg_name = msg.name
            
            data = {
                timestampName: message.timestamp,
                msg_name: signals
                }
            
            sock.sendto( json.dumps(data).encode(), (ip, port) )
    
    
    
def getCANbauds():
    return ['125 kbps','250 kbps','500 kbps','1000 kbps']
    
def getCANdeviceTypes():
    return ['virtual','pcan','ixxat']

# Put initialization for the Gooey here (this includes arguments)
def initGooey(parser):

    defaultIP = '127.0.0.1'
    defaultPort = 9870
    defaultTimestamp = 'timestamp'
    
    defaultBaud = '250 kbps'
    
    defaultDBC = ''
    
    
    #stored arguments example: https://pbpython.com/pandas-gui.html
    stored_args = {}
    # get the script name without the extension & use it to build up
    # the json filename
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    # Read in the prior arguments as a dictionary
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)
        
        defaultPort = stored_args.get('port')
        defaultIP = stored_args.get('IPaddress')
        defaultTimestamp = stored_args.get('JSONtimestamp')
        defaultBaud = stored_args.get('baud')
        defaultDBC = stored_args.get('DBC_files')
        
        #have to handle default file paths differently if there's more than one
        if len(defaultDBC) > 1:
            result = ''
            for file in defaultDBC:
                result += file + ';'
            defaultDBC = result[:-1]
        else:
            defaultDBC = defaultDBC[0]
    
    # https://github.com/chriskiehl/Gooey/blob/master/docs/Gooey-Options.md
    
    
    dbcGroup = parser.add_argument_group('DBC Files',gooey_options={'show_border':True,'columns':2})
    
        
    dbcGroup.add_argument('DBC_files',help='DBC files to use for CAN message parsing. Multiple DBC files can be selected, but they cannot have shared messages',widget='MultiFileChooser',nargs='+', gooey_options={'wildcard':"Database files: (*.dbc) |*.dbc"}, default = defaultDBC)
    # parser.add_argument('--outputFileName', action='store', help="Name of output file. If not provided the input file name will be used with a 'output_' prefix",default='')
        
    canGroup = parser.add_argument_group('CAN Bus Configuration',gooey_options={'show_border':True,'columns':2})
    canGroup.add_argument('CAN_Device',action='store', help='Program must be restarted to update list', choices=getCANdeviceTypes()) #widget='FilterableDropdown',
    canGroup.add_argument('baud',action='store',help='The baud rate of the CAN bus.',choices=getCANbauds(), default = defaultBaud)  #widget='FilterableDropdown'
    
    udpGroup = parser.add_argument_group('UDP Configuration', description = 'Configure PlotJuggler as follows:\n-UDP Server (use same IP and port as entered here)\n-Message protocol: JSON\n-Use field as timestamp: enabled, set to match JSONtimestamp',gooey_options={'show_border':True,'columns':2})
    udpGroup.add_argument('IPaddress', action='store', help="IP address to use. Leave at 127.0.0.1 if streaming to local machine",default=defaultIP)
    udpGroup.add_argument('port', type=int, action='store', help="Port to use for UDP stream. Plotjuggler default port set as default",default=defaultPort)
    udpGroup.add_argument('JSONtimestamp', action='store', help="JSON timestamp field name (should match PlotJuggler configuration)",default=defaultTimestamp)
    
    
    
# This function should not need to be changed (it is used for adding the tool to another GUI as a subparser)
def initSubparser(gooeyParser, parserKey = 'can_udp_bridge'):  
    
    myParser = gooeyParser.add_parser(parserKey,help='CAN bus to UDP bridge. Intended for use with PlotJuggler')
    initGooey(myParser)
    return parserKey, runCommand



# For most cases this will not need to be modified. Put your script execution in runCommand
if __name__ == "__main__":
     

    @Gooey(clear_before_run = True, show_success_modal = False, default_size=(596, 750), dump_build_config = True)
    def main():
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        args_file = "{}-args.json".format(script_name)
        
        parser = GooeyParser(description='CAN bus to UDP bridge. Intended for use with PlotJuggler')
        
        initGooey(parser)
        
        args = parser.parse_args()
        
        # Store the values of the arguments so we have them next time we run
        with open(args_file, 'w') as data_file:
        # Using vars(args) returns the data as a dictionary
            json.dump(vars(args), data_file)
            
            print('settings saved to: ', args_file)

        runCommand(args)
    
    main()
