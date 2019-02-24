使用手册之SUMO

sumo 是一个微观交通仿真器，是一个空间连续，时间上离散的交通流仿真工具。
  sumo 开发的目的是： 仿真一个设定的交通场景
  系统： 可在Linux和Windows 系统上运行；
  
  仿真所需要的基础文件（必选的）：
  1）一个路网文件，格式为*net.xml,该文件可通过工具： NETCONVERT或者NETGENERATE 实现。亦或者自己按照路网格式编写xml文件；
  2） 一个路径集文件： 格式为*rou.xml 或者 *flow.xml 或者 *trip.xml 。 可利用工具DUAROUTER, JTRROUTER, DFROUTER, or ACTIVITYGEN 生成，亦或者自己根据route/flow/trip文件的格式编写xml
  
  仿真所需要的文件（可选项）：
    1）附加文件（additional files）：附加定义的信号灯文件， 可变速信息文件， 检测器输出的信息文件 等。
  
  仿真的输出文件 ： 利用sumo-gui展示仿真可视化；仿真可输出一系列检测信息，评价指标文件。
  
  Usage Description
  
