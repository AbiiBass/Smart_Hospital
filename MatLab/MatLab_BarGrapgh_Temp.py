% Read Body Temperature for the last 10 hours from the ThingSpeak channel Health Monitoring Sysytem
% visualize Body Temperature variations using the MATLAB HISTOGRAM function. 
   
% The data is collected once every minute. 
% 2 contains Body Temperature data. 
% Channel ID to read data from 
readChannelID = 1642167; 
   
% Body Temperature Field ID 
BodyTemperatureFieldID = 2; 
   
% Channel Read API Key   
readAPIKey = 'T9M6OKLS4MZRLH8U'; 

% Get Body Temperature data from field 2 for the last 10 hours = 10 x 60 minutes  
%BTemp is short for Body Temperature
BTemp = thingSpeakRead(readChannelID,'Fields',BodyTemperatureFieldID,...
'NumMinutes',10*60, 'ReadKey',readAPIKey); 
   
histogram(BTemp); 
xlabel('Body Temperature'); 
ylabel('Number of Measurements\newline for Each Body Temperature'); 
title('Histogram of Body Temperature tVariation');
