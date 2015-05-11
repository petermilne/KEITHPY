% Plots linearity of DACs
% Using the python script the X channels from the Keithley are in colums 1 -> X with the DAC setting in column X+2
% Scott Robson - 15:12:49 Thu 15 Jan 2015
function dac_linearity_test(filename)

nchan = 32;
pdffile = "./linearity_results/test.pdf";

% Open the file and read in the data
myfile = fopen(filename, "r");
data = csvread(myfile);
fclose(myfile);

% Kill top row of headings
data = data(2:end,:);

% This is the requested voltage
dac_volts = data(:,[nchan+1]);
avg_code = mean(dac_volts);

% Get coefficients for line of best fit between dac_volts and reported voltages from KMUX
for i = 1:nchan
	ch_data = data(:,[i]);
	regress = polyfit(ch_data,dac_volts,1);
	printf("CH%02d M = %10f C = %10f  \n", i, regress(1), regress(2));
	ch_fit =  ch_data*regress(1) + regress(2); % Create a straight line using these coefficients (y=mx+c).
	ch_error{i} = ch_fit - dac_volts; % Subtract dac voltages from the points on this line to give error
end

% loc_in_str = strfind(filename,"cpsc");
% boardname	= substr(filename, loc_in_str(length(loc_in_str)), 8);
% boardname = strrep(boardname, '_', '\_');
% boardname = toupper(boardname);

boardname = "XXX";

% Create plot command
plot_command = "plot("; legend_command = "";
for i = 1:nchan; j = sprintf("%i",i); plot_command = strcat(plot_command,"dac_volts,ch_error{",j,"},"); end
plot_command(numel(plot_command)) = []; plot_command = strcat(plot_command,");");

eval(plot_command)
legend('Channel 1','Channel 2','Channel 3','Channel 4','Channel 5','Channel 6','Channel 7','Channel 8', ...
       'Channel 9','Channel 10','Channel 11','Channel 12','Channel 13','Channel 14','Channel 15','Channel 16', ...
	  'Channel 17','Channel 18','Channel 19','Channel 20','Channel 21','Channel 22','Channel 23','Channel 24', ...
	  'Channel 25','Channel 26','Channel 27','Channel 28','Channel 29','Channel 30','Channel 31','Channel 32','outside'
);
set(gcf, "papersize",[8.3,11.7]);
set(gcf(),"paperposition",[0,0,8.3,11.7]); # Bottom,Left,Top,Right
set(gcf(),"paperorientation","landscape");
titletext1 = sprintf('Board %s Linearity Test\n',  boardname);
titletext2 = sprintf('Board Test Data, Not To Be Used Without Permission, Copyright D-TACQ Solutions %s\n',strftime("%Y",localtime(time())));
thetitle = strcat(titletext1,titletext2);

%pdffile = strcat(boardname, '_Linearity_Test','.pdf');
grid("on");
axis ([-10,10]);
xlabel ('Volts', 'FontName','LiberationMono-Regular.ttf','FontSize',10);
ylabel ('Volts') #, 'FontName','LiberationMono-Regular.ttf','FontSize',10);
title(thetitle, 'FontName','LiberationMono-Regular.ttf','FontSize',10);
text(0, -0.1,ctime(time()), 'FontName','LiberationMono-Regular.ttf','FontSize',8, 'units', 'normalized' );

outfilecommand = sprintf("print -dpdf -landscape  \"%s\"",pdffile);
eval(outfilecommand);

endfunction
