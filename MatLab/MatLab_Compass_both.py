%Read Body Temperature and Pulse Rate from the ThingSpeak channel health monitoring system 
%velocity using the MATLAB COMPASS plot function. 
   
% Channel 1642167 contains data from the MathWorks Weather Station, located 
% in Natick, Massachusetts. The data is collected once every minute. Field 
% 1 contains  Pulse Rate data and field 2 contains Body Temperature data. 
   
% Channel ID to read data from 
readChannelID = 1642167; 
%  Pulse Rate Field ID 
PulseRateID = 1; 
% Body Temperature Field ID 
TemperatureID = 2; 
   
% Channel Read API Key   
readAPIKey = 'T9M6OKLS4MZRLH8U'; 
   
% Fetch  Pulse Rate for the last 60 points
PulseRate = thingSpeakRead(readChannelID,'Fields',PulseRateID,'NumPoints',60,...
'ReadKey',readAPIKey); 
   
% Fetch Body Temperature for the last 60 points 
Temperature = thingSpeakRead(readChannelID,'Fields',TemperatureID,...
'NumPoints',60,'ReadKey',readAPIKey); 
   
% Convert to radians 
rad = PulseRate*2*pi/360; 
   
% Add 90 counter clockwise rotation to align the compass with true North 
rad = rad+pi/2; 
   
% Calculate the x component 
u = cos(rad) .* Temperature;   
   
% Calculate the y component 
v = sin(rad) .* PulseRate;   
   
% Generate a compass plot 
compass(u,v);
