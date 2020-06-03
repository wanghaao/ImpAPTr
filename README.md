# ImpAPTr
A Tool For Identifying The Clues To Online Service Anomalies

## Dataset
There is a dataset of all service calls of March of MT. The first level directory represents the day of march and the second represents the different interval(5 minutes for an interval) of each day.

Dataset: https://pan.baidu.com/s/1BgxoQ9l1PHCWHr1ZfM7pFQ  Extraction code: 'h1am'

**Attention**
- The dataset has been desensitized.
- ''A4,B0,C1,D1,E30,F9,G6055,2,200'' is a line of a file, and the first 7 values are the different dimensional values and the 8th value presents the number of service calls, further, the last is the status code of these service calls (200, the code for a successful service call, otherwise, failed).

## Running 
The python file 'ImpAPTr.py' is the main body of our tool and you should run the file 'ImpAPTr_test.py'.
1. When you notice the DSR(Declining Success Rate) of SRSC(Success Rate of Service Calls), you should get the interval on where the DSR occurs.
![The success rate of 10 March, 2020](https://github.com/wanghaoUp/ImpAPTr/blob/master/ImpAPTr_module/success_rate_3.10.png)
2. Please run the file 'ImpAPTr_test.py' by the following command,
> _python ImpAPTr\_test.py \[day] \[interval]_

The parameter 'day' and 'interval' are the time of DSR's occuring.

3. After the running of the tool, there are some candidate clues which can benefit operators to find out the real 'root cause' and maintain the stability of service.

## The project directory
- /ImpAPTr_module/dataset/..
- /ImpAPTr_module/ImpAPTr.py
- /ImpAPTr_module/ImpAPTr_test.py

## Example
We propose two anomaly examples for the service on March. The first is an example of sharp DSR, and another is slight drop.
- 2020.3.10 08:00~08:05     --python ImpAPTr\_test.py  10  480
- 2020.3.19 11:20~11:25     --python ImpAPTr\_test.py  19  680
