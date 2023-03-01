# Logs-List-Script
Getting Log types and descriptions and converting to csv

All folders in target folder will be searched for the log types. Clone all repositories that need to be targeted there#

# STEPS TO RUN

        python3 app.py

Results will be generated in Log_details.csv. File locations are be provided for the logs as well incase details of the logs are not provided.

# BUGS
Bug: Unable to get description of some logs due to "\n" used in the middle of the log declaration which makes the script consider it as a new line (FIXED)

Bug: Unable to get all log descriptions due to no set standard.
Examples: 
        FourKitesCommon::Logger.debug(self,
                                 'sent a load  a status a change a to po pipeline #{message["trackingId", []]}')
        FourKitesCommon::Logger.error(self, "Error converting, time_stamp", error: e.message, backtrace: e.backtrace[0..5].("\n"))
        
        cannot get message based on positions on "" or ''
        after , and before ) has issues because some attributes after log message
        cannot check , not in between "" because attributes after can have "" as well

Bug: Empty description for Logs with only variable in log description OR \n before description
