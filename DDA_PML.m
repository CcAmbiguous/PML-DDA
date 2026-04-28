function [P,U] = DDA_PML(train_data,train_target,opt)

warning('off');
rng(42)

alpha = opt.alpha;
beta = opt.beta;
gamma = opt.gamma;
ratio = opt.ratio;
max_iter = opt.max_iter;

model = [];

[d,n]=size(train_data);
[~,q]=size(train_target);

%% Training
X = train_data;
Y = train_target';
k = ceil(ratio*d);
U = randn(d,k);
V = rand(k,n);
Q = eye(q);
P = Y;
Z = row_softmax(eye(n));
S= row_softmax(P');
F = softmax(P)';
O = randn(k,q); 

%%
psi = softmax(P);
dis = pdist2(V', O', 'squaredeuclidean');
total_loss = norm(X-U*V*Z,'fro')^2+norm(X-X*Z,'fro')^2+norm(Y-Q*P,'fro')^2+alpha*norm(P-P*Z,'fro')^2+beta * sum(sum(F .* dis))+ gamma *norm(psi'-F,'fro')^2;
loss(1) = total_loss;

miniLossMargin = 1e-3;
%%Update
for ii = 1:max_iter

    Dn = diag(sum(F,2));
    %% update Q
    [S1,~,S2] = svd(Y*(P'),"econ");
    Q = S1*S2';
    clear S1 S2
   
    %% update U
    [S1,~,S2] = svd(X*Z'*V',"econ");
    U = S1*S2';
    clear S1 S2

    %% update V
    Va = U'*X*Z' + beta*O*F';
    Vb = V*Z*(Z)' + beta*V*Dn;
    V = V.*Va./(Vb+eps);
    clear Va Vb 

    %% update O
    % O = V*F*pinv(Dq);
    F_squared = F.^2;
    Oa = V * F_squared;
    Ob = sum(F_squared, 1);
    O = Oa ./ Ob;
    %% update Z
    Za = V'*U'*X + X'*X + alpha*P'*P;
    Zb = V'*V*Z + X'*X*Z + alpha*P'*P*Z;
    Z_new = Z .* (Za ./ Zb + eps);
    for kk = 1:1:n
        Z(:,kk) = EProjSimplex_new(Z_new(:,kk));
    end
    
    %% update F
    dis = pdist2(V', O', 'squaredeuclidean');
    ones_matrix = ones(n, q);
    A = beta*dis + gamma * ones_matrix;
    Ft = (gamma * S)  ./  A;
    for i = 1:n
        F(i,:) = EProjSimplex_new(Ft(i,:));
    end 
    S= row_softmax(P');
    %% update P
    theta = max(P-Y,0);
    p11 = gamma*(S'.*F');
    p22 = gamma*(S' .* S' .* ones(size(S')));
    Pa = Q'*Y + alpha*P*Z + alpha*P*Z'+ p11;
    Pb = P + alpha*P + alpha*P*Z*Z' + p22 + eps;
    Pc = theta.*Y;
    P = P.*Pa./Pb-Pc./Pb;

    %% loss
    loss_1 = norm(X-U*V*Z,'fro')^2;
    loss_2 = norm(X-X*Z,'fro')^2;
    loss_3 = norm(Y-Q*P,'fro')^2;
    loss_4 = alpha*norm(P-P*Z,'fro')^2;
    loss_5 = beta * sum(sum(F .* dis));
    loss_6 = gamma *norm(psi'-F,'fro')^2;
    total_loss = loss_1+loss_2+loss_3+loss_4+loss_5+loss_6;
    loss(ii+1) = total_loss;
    if ii>2
        temp_loss = (loss(ii-1) - loss(ii))/loss(ii-1); 
        if temp_loss<miniLossMargin
            break;%如果收敛就跳出循环
        end
    end
    time = toc;

end
model.loss=loss;
model.time=time;
end

function B = row_softmax(A)
    B = exp(A - max(A, [], 2)) ./ sum(exp(A - max(A, [], 2)), 2);
end
