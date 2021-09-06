%-------------------------------------------------------------------------%

Image = imread('T:\masters\program\MESHING_AND_ANALYSIS_NEW\test\t115_ctrl_1_t001_mask.png');
I     = flipdim(Image,1); %#ok<DFLIPDIM>
[B,L,N] = bwboundaries(I);

%B = bwboundaries(Ifill);
for k = 1
    b = B{k};
    plot(b(:,2),b(:,1),'g','linewidth',2);
end

% for k=1:length(B),
%    b1 = B{k};
%    b2 = B{k};
%    if(k > N)
%      plot(b2(:,2), b2(:,1), 'g','LineWidth',2);
%    else
%      plot(b1(:,2), b1(:,1), 'r','LineWidth',2);
%    end
% end

c1  = downsample(b(:,2),1);
c2  = downsample(b(:,1),1);

% c3 = downsample(b2(:,2),1);
% c4 = downsample(b2(:,1),1);

[NyI, NxI]   = size(I);
cl_1         = 100;
cl_2         = 5;

% domain extent
xmin         = 1;
xmax         = NxI;
ymin         = 1;
ymax         = NyI;

%------- writing to GMsh ------------------------------------------------

fileID = fopen('T:\masters\program\MESHING_AND_ANALYSIS_NEW\test\scratch_mesh_01.txt','w');

%--- mesh size and boundary information
fprintf(fileID,'\n');
C  = sprintf('// mesh size description');
fprintf(fileID,'%s\n',C);
fprintf(fileID,'\n');
C  = sprintf('cl_1   =  %d;',cl_1 );
fprintf(fileID,'%s\n',C);
C  = sprintf('cl_2   =  %d;',cl_2 );
fprintf(fileID,'%s\n',C);

    
fprintf(fileID,'\n');
C  = sprintf('// boundary points that forms Rhizotron');
fprintf(fileID,'%s\n',C);
C  = sprintf('Point(1) = {%d, %d, 0, cl_1};',xmin,ymin);
fprintf(fileID,'%s\n',C);
C  = sprintf('Point(2) = {%d, %d, 0, cl_1};',xmax,ymin);
fprintf(fileID,'%s\n',C);
C  = sprintf('Point(3) = {%d, %d, 0, cl_1};',xmax,ymax);
fprintf(fileID,'%s\n',C);
C  = sprintf('Point(4) = {%d, %d, 0, cl_1};',xmin,ymax);
fprintf(fileID,'%s\n',C);
fprintf(fileID,'\n');
fprintf(fileID,'\n');
    
C  = sprintf('// lines that connect boundary');
fprintf(fileID,'%s\n',C);
    
C  = sprintf('Line(1) = {1, 2};');
fprintf(fileID,'%s\n',C);
C  = sprintf('Line(2) = {3, 2};');
fprintf(fileID,'%s\n',C);
C  = sprintf('Line(3) = {4, 3};');
fprintf(fileID,'%s\n',C);
C  = sprintf('Line(4) = {1, 4};');
fprintf(fileID,'%s\n',C);
C  = sprintf('Line Loop(4) = {1, -2, -3, -4};');
fprintf(fileID,'%s\n',C);
fprintf(fileID,'\n');
    
C  = sprintf('// Mesh Parameters');
fprintf(fileID,'%s\n',C);
C  = sprintf('Mesh.CharacteristicLengthExtendFromBoundary = 0;');
fprintf(fileID,'%s\n',C);
C  = sprintf('Mesh.CharacteristicLengthMax = 25;');
fprintf(fileID,'%s\n',C);
fprintf(fileID,'\n');
    
C  = sprintf('// Define Segment coordinates');
fprintf(fileID,'%s\n',C);
count = numel(c1);
x  = c1; y = c2; z = zeros(count,1);
% X = typecast(x, 'uint8'); Y = typecast(y, 'uint8'); Z = typecast(z, 'uint8');
xs = sprintf('X =');
ys = sprintf('Y =');
a = strjoin(arrayfun(@(x) num2str(x),x,'UniformOutput',false),',');
b = strjoin(arrayfun(@(y) num2str(y),y,'UniformOutput',false),',');
A = strcat(xs,'{',a,'};');
B = strcat(ys,'{',b,'};');
fprintf(fileID,'\n');
fprintf(fileID,'%s\n',A);
fprintf(fileID,'%s\n',B);
fprintf(fileID,'\n');
fprintf(fileID,'\n');
C  = sprintf('// Define spline surface');
fprintf(fileID,'%s\n',C);
fprintf(fileID,'\n');
C  = sprintf('LN = 90;');
fprintf(fileID,'%s\n',C);
C  = sprintf('nR = #X[ ];');
fprintf(fileID,'%s\n',C);
C  = sprintf('p0  =  newp;');
fprintf(fileID,'%s\n',C);
C  = sprintf('p   =  p0;');
fprintf(fileID,'%s\n',C);
C  = sprintf('For i In {0:nR-1}');
fprintf(fileID,'%s\n',C);
C  = sprintf('Point(newp)  =    {X[i], Y[i], 0, cl_2};');
fprintf(fileID,'%s\n',C);
C  = sprintf('EndFor');
fprintf(fileID,'%s\n',C);
C  = sprintf('p2  =  newp-1;');
fprintf(fileID,'%s\n',C);
C  = sprintf('BSpline(90)   =  {p:p2,p};');
fprintf(fileID,'%s\n',C);
C  = sprintf('Line Loop(91) = {90};');
fprintf(fileID,'%s\n',C);
C  = sprintf('Plane Surface(92) = {91};');
fprintf(fileID,'%s\n',C); 
C  = sprintf('Plane Surface(93) = {4,91};');
fprintf(fileID,'%s\n',C);
fclose(fileID);

% open the geo file
uiopen('T:\masters\program\MESHING_AND_ANALYSIS_NEW\test\scratch_mesh_01.txt',1);
x2 = vertcat(x,x);
y2 = vertcat(y,y);
%z1 = zeros(count,1);
z2 = ones(count,1)*10;
z3 = ones(count,1)*20;
z4 = ones(count,1)*30;
z_cat = vertcat(z,z4);
% X = x(:) ; 
% Y = y(:) ; 
% Z = z(:) ; 
% p = [X, Y, Z] ;
p = [x, y, z];
p_3d = [x2,y2,z_cat];
% P = typecast(p, 'uint8');
% writematrix(p,'test.txt', 'Delimeter', 'tab');
% type 'test.txt';
fid = fopen('scratch_mesh_01_matlab_b.xyz', 'wt');
fprintf(fid, [repmat('%.f\t', 1, size(p,2)-1) '%f\n'],p.');
fclose(fid);
fid = fopen('scratch_mesh_01_matlab_b_3d_0_30.xyz', 'wt');
fprintf(fid, [repmat('%.f\t', 1, size(p_3d,2)-1) '%f\n'],p_3d.');
fclose(fid);
uiopen('T:\masters\program\MESHING_AND_ANALYSIS_NEW\meshing\scratch_mesh_01_matlab_b_3d_0_30.xyz')
%-------------------------------------------------------------------------
