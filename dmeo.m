%% The result is recorded in the result folder
clear
% clc
close all
% dataname = 'emotions';
% num_noise = 1;% The amount of noise added

% ttt = 2;  %Select your noise method


% 1.mirflickr(3.35)      % 2.music_emotion(5.29)  % 3.music_style(6.04)   % 4.YeastBP(18.84)
% 5.emotions(3)          % 6.emotions(4,5)        % 7.birds(3,4,5)        % 8.flags(4,5,6)        
% 9.image(2,3,4)         % 10.scene(3,4,5)        % 11.health(5,7,9)      % 12.recreation(7,9,11)
% 13.science(5,7,9)      % 14.education(5,7,9)    % 15.arts(5,7,9,11)     % 16.yeast(5,7,9,11)
% 17.reference(5,7,9,11) % 18.foodtruck(5,7,9)    % 19.corel5k(5,7,9,11)  % 20.enron(3,5,7,9) 
% 21.medical(3,5,7,9)    % 22.YeastBP(1.29)       % 23.YeastBP(1.04)


%% 1 2 3 4
% [~] = main_PML('Mirflickr',3.35,1);
% [~] = main_PML('Music_emotion',5.29,2);
% [~] = main_PML('Music_style',6.04,3);
% [~] = main_PML('YeastBP',5.93,4);
%% 22 23
% [~] = main_PML('YeastCC',1.29,22);
% [~] = main_PML('YeastMF',1.04,23);
%% 5 6
[~] = main_PML('emotions',3,5);
% [~] = main_PML('emotions',4,6);
% [~] = main_PML('emotions',5,6);
%% 7
% [~] = main_PML('birds',3,7);
% [~] = main_PML('birds',4,7);
% [~] = main_PML('birds',5,7);
%% 8
% [~] = main_PML('flags',4,8);
% [~] = main_PML('flags',5,8);
% [~] = main_PML('flags',6,8);
% %% 9
% [~] = main_PML('image',2,9);
% [~] = main_PML('image',3,9);
% [~] = main_PML('image',4,9);
% %% 10 
% [~] = main_PML('scene',3,10);
% [~] = main_PML('scene',4,10);
% [~] = main_PML('scene',5,10);
%% 11 
% [~] = main_PML('health',5,11);
% [~] = main_PML('health',7,11);
% [~] = main_PML('health',9,11);
%% 12
% [~] = main_PML('recreation',7,12);
% [~] = main_PML('recreation',9,12);
% [~] = main_PML('recreation',11,12);
% %% 13
% [~] = main_PML('science',5,13);
% [~] = main_PML('science',7,13);
% [~] = main_PML('science',9,13);
% %% 14
% [~] = main_PML('education',5,14);
% [~] = main_PML('education',7,14);
% [~] = main_PML('education',9,14);
% %% 15
% [~] = main_PML('arts',5,15);
% [~] = main_PML('arts',7,15);
% [~] = main_PML('arts',9,15);
% [~] = main_PML('arts',11,15);
% %% 16
% [~] = main_PML('yeast',5,16);
% [~] = main_PML('yeast',7,16);
% [~] = main_PML('yeast',9,16);
% [~] = main_PML('yeast',11,16);
% %% 17
% [~] = main_PML('reference',5,17);
% [~] = main_PML('reference',7,17);
% [~] = main_PML('reference',9,17);
% [~] = main_PML('reference',11,17);
% %% 18
% [~] = main_PML('foodtruck',5,18);
% [~] = main_PML('foodtruck',7,18);
% [~] = main_PML('foodtruck',9,18);
%% 19 
% [~] = main_PML('corel5k',5,19);
% [~] = main_PML('corel5k',7,19);
% [~] = main_PML('corel5k',9,19);
% [~] = main_PML('corel5k',11,19);
% %% 20 
% [~] = main_PML('enron',3,20);
% [~] = main_PML('enron',5,20);
% [~] = main_PML('enron',7,20);
% [~] = main_PML('enron',9,20);
% %% 21
% [~] = main_PML('medical',3,21);
% [~] = main_PML('medical',5,21);
% [~] = main_PML('medical',7,21);
% [~] = main_PML('medical',9,21);