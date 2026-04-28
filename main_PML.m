function [result] = main_PML(dataname,avg_cls,ttt)
% Initialization
% Fixed seed
rng(42)
addpath(genpath('datasets')); % Add path
addpath(genpath('function'));
addpath(genpath('metrics'));

% Import data set
[pLabels,data,target] = addnoise(dataname,avg_cls);
%%
% 1.Mirflickr(3.35)      % 2.Music_emotion(5.29)  % 3.Music_style(6.04)   
% 4.YeastBP(5.93)        % 5.YeastCC(1,39)        % 6.YeastMF(1.04)
% 7.emotions(3,4,5)      % 8.birds(3,4,5)         % 9.medical(5,7,9)    
% 10.image(2,3,4)        % 11.yeast(7,9,11)       % 12.corel5k(7,9,11) 

%%params settings
par = params_settings(ttt);
opt.alpha = par(1);                  
opt.beta = par(2);                   
opt.gamma = par(3); 
opt.ratio  = par(4);
opt.max_iter = 40;



%%
N= size(data,1);
indices = crossvalind('Kfold', 1:N ,10);  % Dividing the data set

for round = 1:10
   ht = round*10;
    fprintf('%.1f%%\n',ht)
    test_idxs = (indices == round);                       
    train_idxs = ~test_idxs;                       
    train_data = data(train_idxs,:); 
    train_target = pLabels(train_idxs,:); 
    true_target = target(train_idxs,:);
    test_data = data(test_idxs,:);                                          
    test_target = target(test_idxs,:);
                    
                      
    % pre-processing                                       
    [train_data, settings]=mapminmax(train_data');                                        
    test_data=mapminmax('apply',test_data',settings);                                          
    train_data(isnan(train_data))=0;                                           
    test_data(isnan(test_data))=0;                                           
    train_data=train_data';                                           
    test_data=test_data';                                             
    X = train_data';
    Xt = test_data';
    Y = train_target;
    Yt = test_target;
    
    % High dimensional kernel mapping
    tf = strcmp(dataname,'birds');
    if tf~=1
        [K,Kt] = Kernel_mapping(X,Xt);                       
        X = K;
        Xt = Kt;
    end
           
    % training
    fprintf('Running PML-DDA on %s ...\n', dataname);
    tStart = tic;
    [P, U] = DDA_PML(X,Y,opt);
    X_train = (U'*X)';
    X_test = (U'*Xt)';
    Y_train = P';
    Y_test = Yt;
    Y_noise = Y;

    elapsedTime = toc(tStart);
    fprintf('%s | PML-DDA | Time: %.4f s\n', dataname, elapsedTime);
    filename = sprintf('deep_classifier/data/%s%d_cv%d.mat',dataname, avg_cls, round);

    % 保存 Y 到 mat 文件
    save(filename, 'X_train','X_test','Y_train','Y_test','Y_noise');
    fprintf('已保存');
    result = [];
  
end
end
                                            