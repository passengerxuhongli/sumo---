# sumo---
完整了软件文档中文译本；自己在学习sumo过程中的心得；典型的小案例；
语言：python3.6
软件：sumo version0.32

生成区域路网的笔记：
程序生成example.rou.xml文件后，需要对check routes 并fix route  
python "C:\Program Files (x86)\DLR\Sumo\tools\route\routecheck.py" -n example.net.xml vehicletype.add.xml --fix example.rou.xml
转换完事之后，加载之后可能会报错如下：
====================
done.
Loading net-file from 'C:\Users\。。。\Desktop\SUMO\data\writeRoute\example.net.xml'... done (84ms).
Warning: Unused states in tlLogic '90002', program '0' in phase 0 after tl-index 18
Loading route-files from 'C:\Users\lixuhong\Desktop\SUMO\data\writeRoute\wujin.rou.xml.fixed'... 
Error: invalid byte '?' at position 1 of a 1-byte sequence
 In file 'C:\Users\。。。\Desktop\SUMO\data\writeRoute\example.rou.xml.fixed'
 At line/column 2/1.

Loading of route-files failed.
Quitting (on error).
=================
这时，删除第一行，手动复制一份，即可正常加载


##生成瓶颈路段
编写瓶颈flow文件example.flow.xml
命令行生成瓶颈路段路径
duarouter -f example.flow.xml -n wujin1.net.xml --output-file=bottleneckRoutes.rou.xml


信号控制方案加载
 运行自造的tls_create.py函数

利用Webster优化现有相位绿灯时长(好像路网底图编号有点问题，函数和命令没问题)
python "C:\Program Files (x86)\DLR\Sumo\tools\tlsCycleAdaptation.py" -n example.net.xml -r example.rou.xml -o examplenewTLS.add.xml




信号控制方案动态修改


xml文件转化为CSV
  python "C:\Program Files (x86)\DLR\Sumo\tools\xml\xml2csv.py" your.xml


生成检测器的工具

python "C:\Program Files (x86)\DLR\Sumo\tools\output\generateTLSE3Detectors.py"  -n example.net.xml -l 250 -d .1 -f 60

python "C:\Program Files (x86)\DLR\Sumo\tools\output\generateTLSE2Detectors.py"  -n example.net.xml -l 250 -d .1 -f 60


python "C:\Program Files (x86)\DLR\Sumo\tools\output\generateTLSE1Detectors.py"  -n example.net.xml  -d .1 -f 60


时间上求各个监测器数据的均值，设置这种均值的addtional文件(但是这样设置检测器，逻辑上好像不对，可以之间按照edgedata的格式设置，不需要借助检测器）
python "C:\Program Files (x86)\DLR\Sumo\tools\output\generateMeanDataDefinitions.py"  -d e2.add.xml -t e2 -f 300 -p measure -o e2_edgedata.add.xml




###非常重要
   生成路网评价指标，前提是输出tripinfos.xml和vehroutes.xml
python "C:\Program Files (x86)\DLR\Sumo\tools\output\generateITetrisNetworkMetrics.py" -n example.net.xml -p "C:\Users\。。。\Desktop\SUMO\data\writeRoute" -t type1 -i 60
python generateITetrisNetworkMetrics.py -n wujin1.net.xml -p "C:\Users\。。。\Desktop\SUMO\data\writeRoute" -t type1 -i 60
   生成路网交叉口评价指标，前提是输出e2output.xml文件
python "C:\Program Files (x86)\DLR\Sumo\tools\output\generateITetrisIntersectionMetrics.py" -n example.net.xml -p "C:\Users\。。。\Desktop\SUMO\data\writeRoute"
python generateITetrisIntersectionMetrics.py -n example.net.xml -p "C:\Users\。。。\Desktop\SUMO\data\writeRoute"



对比两个方案运行结果的差异
仿真运行耗时评估
python "C:\Program Files (x86)\DLR\Sumo\tools\output\timingStats.py" -c example.sumocfg -r 20 
按照路径，一车道为单位分析路网
python "C:\Program Files (x86)\DLR\Sumo\tools\output\vehLanes.py"  rawdump1.xml analysisresults.xml
行程时间，损失时间等变化
python "C:\Program Files (x86)\DLR\Sumo\tools\output\tripinfoDiff.py" tripinfos1.xml tripinfos2.xml result.xml

路网(报错：dump文件无关键字，可能是找的netstate dump 文件不对，或者是程序本身有问题，需修改节点标签）
python "C:\Program Files (x86)\DLR\Sumo\tools\output\netdumpdiff.py" -1 rawdump1.xml -2 rawdump2.xml -o Mynetdumpdiff.xml 
python "C:\Program Files (x86)\DLR\Sumo\tools\output\netdumpmean.py" -1 rawdump1.xml -2 rawdump2.xml -o Mynetdumpdiff.xml 
路径行程时间变化（--vehroute-output.exit-times命令获得的vehroutes.xml）
python "C:\Program Files (x86)\DLR\Sumo\tools\output\vehrouteDiff.py"  vehroutes1.xml vehroutes2.xml routeresult.xml


指标可视化展示界面
C:\Program Files (x86)\DLR\Sumo\tools\visualization>python plot_net_speeds.py -n example.net.xml
C:\Program Files (x86)\DLR\Sumo\tools\visualization>python plot_summary.py -i summary.xml
C:\Program Files (x86)\DLR\Sumo\tools\visualization>python plot_tripinfo_distributions.py -i tripinfos.xml,tripinfos1.xml,tripinfos2.xml -o tripinfo_distribution_duration.png -v -m duration --minV 0 --maxV 3600 --bins 10 --xticks 0,3601,360,14 --xlabel "duration [s]" --ylabel "number [#]" --title "duration distribution" --yticks 14 --xlabelsize 14 --ylabelsize 14 --titlesize 16 -l tripsinfo,tripinfo1,tripsinfo2 --adjust .14,.1 --xlim 0,3600
#貌似程序有点问题
C:\Program Files (x86)\DLR\Sumo\tools\visualization>python plot_net_dump.py -v -n example.net.xml -i aggregated_60.xml -m measures traveltime entered --xlabel [m] --ylabel [m] --default-width 1 --xlim 7000,14000 --ylim 9000,16000 --default-width .5 --default-color #606060 --min-color-value -1000 --max-color-value 1000 --max-width-value 1000 --min-width-value -1000 --max-width 3 --min-width .5 --colormap #0:#0000c0,.25:#404080,.5:#808080,.75:#804040,1:#c00000



