% Read Pulse Rate and Body Temperature data from the ThingSpeak channel Health Monitoring System 
% visualize the data on the same plot with different Y-Axes using the 
% YYAXIS and PLOT functions 

%Field 1 contains the Pulse Rate data and field 2 contains Body Temperature data. 
% Channel ID to read data from 
readChannelID = 1642167; 
% Pulse Rate Field ID 
PulseRateID = 1; 
% Body Temperature Field ID 
TempID = 2; 

% Channel Read API Key      
readAPIKey = 'T9M6OKLS4MZRLH8U'; 

% Read Data 
[data, timeStamps] = thingSpeakRead(readChannelID, 'Fields',[PulseRateID TempID], ...
                                                           'NumPoints', 170, ...
                                                           'ReadKey', readAPIKey);

% Extract the Pulse Rate data from the first column
PulseRateData = data(:, 1);
% Extract the windspeed data from the second column
TempData = data(:, 2);

% Visualize Data
yyaxis left
plot(timeStamps, PulseRateData);
ylabel('Pulse Rate');

yyaxis right
plot(timeStamps, TempData);
ylabel('Pulse Rate');
