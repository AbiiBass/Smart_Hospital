% Read Pulse rate for the last 10 hours from the ThingSpeak channel Health Monitoring Sysytem
% visualize Pulse rate variations using the MATLAB HISTOGRAM function. 
   
% The data is collected once every minute. 
% 1 contains Pulse rate data.
% Channel ID to read data from 
readChannelID = 1642167; 
   
% Pulse rate Field ID 
PulserateFieldID = 1; 
   
% Channel Read API Key   
readAPIKey = 'T9M6OKLS4MZRLH8U'; 

% Get Pulse rate data from field 1 for the last 10 hours = 10 x 60 minutes
% PR is short for Pulse Rate
PR = thingSpeakRead(readChannelID,'Fields',PulserateFieldID,...
'NumMinutes',10*60, 'ReadKey',readAPIKey); 
   
histogram(PR); 
xlabel('Pulse Rate'); 
ylabel('Number of Measurements\newline for Each beat'); 
title('Histogram of Heart Beat Variation');
