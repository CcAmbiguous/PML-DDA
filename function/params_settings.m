function par = params_settings(ttt)
%%%       alpha     beta    gamma   ratio  
params = [1e-0,    1e-0,    1e-2,    0.8;      %% 1.mirflickr;
          1e-1,    1e-4,    1e-2,    0.8;      %% 2.music_emotion;
          1e-1,    1e-4,    1e-3,    0.6;      %% 3.music_style;
          1e-1,    1e-3,    1e-2,    0.4;      %% 4.YeastBP;
          1e-0,    1e-1,    1e-1,    0.8;      %% 5.emotions-3;
          1e-0,    1e-1 ,   1e-1,    0.8;      %% 6.emotions-4 and 5;
          1e-1,    1e-1,    1e-1,    0.8;      %% 7.birds;
          1e-1,    1e-1,    1e-1,    1.0;      %% 8.flags;
          1e-1,    1e-2,    1e-2,    0.8;      %% 9.image;
          1e-2,    1e-4,    1e-2,    0.8;      %% 10.scene;
          1e-1,    1e-4,    1e-1,    0.6;      %% 11.health;
          1e-2,    1e-2,    1e-1,    0.6;      %% 12.recreation;
          1e-2,    1e-4,    1e-2,    0.8;      %% 13.science;
          1e-2,    1e-2,    1e-2,    0.6;      %% 14.eduction;
          1e-0,    1e-1,    1e-0,    0.8;      %% 15.arts;
          1e-0,    1e-2,    1e-2,    0.8;      %% 16.yeast;
          1e-1,    1e-2,    1e-2,    0.6;      %% 17.reference;
          1e-0,    1e-1,    1e-1,    0.6;      %% 18.foodtruck;
          1e-2,    1e-2,    1e-1,    0.8;      %% 19.corel5k;
          1e-0,    1e-2,    1e-2,    0.8;      %% 20.enron;
          1e-2,    1e-2,    1e-1,    0.8;      %% 21.medical;
          1e-1,    1e-3,    1e-1,    0.4;      %% 22.YeastCC;
          1e-1,    1e-3,    1e-2,    0.4;      %% 23.YeastMF;
          ];
par = params(ttt,:);
end