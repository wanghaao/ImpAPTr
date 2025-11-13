# ImpAPTr

中文版 | [English](./README.md)

ImpAPTr（基于剪枝树的影响分析工具）是一个用于通过分析服务调用数据中的多维属性来识别在线服务异常线索的工具。

## 关于本项目

这是以下论文的工件仓库：

**Wang, Hao, Rong, Guoping, Xu, Yangchen, and You, Yong.** "ImpAPTr: a tool for identifying the clues to online service anomalies." *Proceedings of the 35th IEEE/ACM International Conference on Automated Software Engineering (ASE '20)*, 2021, pp. 1307-1311. DOI: [10.1145/3324884.3415301](https://doi.org/10.1145/3324884.3415301)

### 扩展工作

该工作已被扩展并发表为：

**Rong, Guoping, Wang, Hao, Gu, Shenghui, Xu, Yangchen, Sun, Jialin, Shao, Dong, and Zhang, He.** "Locating Anomaly Clues for Atypical Anomalous Services: An Industrial Exploration." *IEEE Transactions on Dependable and Secure Computing*, vol. 20, no. 4, 2023, pp. 2746-2761. DOI: [10.1109/TDSC.2022.3181143](https://doi.org/10.1109/TDSC.2022.3181143)

扩展版本（ImpAPTr+）通过引入时间维度并移除固定阈值限制，解决了非典型异常问题。

## 功能特点

- **多维分析**：跨多个维度属性（如城市、ISP、平台、网络等）分析服务调用
- **根因识别**：识别导致服务异常的属性组合
- **实际验证**：在美团（全球最大的在线服务提供商之一）的生产数据上进行评估
- **高准确性**：在异常检测准确性方面优于该领域的先前工具

## 安装

### 前置要求

- Python 3.x
- 所需包：numpy

### 安装步骤

1. 克隆此仓库：
```bash
git clone https://github.com/wanghaoUp/ImpAPTr.git
cd ImpAPTr
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 数据集

该工具使用来自美团的真实服务调用数据。数据集包含每个服务调用的多维属性。

### 数据集1 
数据集1包含三天（2020年3月10日、19日、22日）的服务调用，并包括下面示例中使用的真实异常。

**链接**：https://www.jianguoyun.com/p/De4m7c8QtbXZCBiktbID

### 数据集2
此数据集包含来自1月的31个文件，每个文件包含一天的所有服务调用。

**链接**：https://www.jianguoyun.com/p/DTPfNicQtbXZCBiTtbID

### 数据格式

**注意**：所有数据集均已脱敏以保护隐私。

数据文件中的每一行遵循以下格式：
```
A4,B0,C1,D1,E30,F9,G6055,2,200
```

其中：
- **前7个值**：不同维度的属性值
  - A: 网络类型
  - B: 连接类型
  - C: 平台
  - D: 运营商
  - E: 城市
  - F: 来源
  - G: （附加维度）
- **第8个值**：服务调用次数
- **最后一个值**：HTTP状态码（200 = 成功，其他表示失败）

每行的第一个数字表示时间间隔（每个间隔5分钟）。

## 使用方法

### 运行工具

1. **识别异常间隔**：当您观察到SRSC（服务调用成功率）的DSR（成功率下降）时，记录发生的日期和时间间隔。

![成功率示例 - 2020年3月10日](ImpAPTr_module/success_rate_3.10.png)

2. **执行分析**：使用以下命令运行工具：

```bash
python ImpAPTr_test.py [day] [interval]
```

**参数**：
- `day`：发生DSR的日期（月份中的日期）
- `interval`：发生DSR的时间间隔（以5分钟为增量）

3. **查看结果**：工具输出候选线索，可以帮助运维人员识别根本原因并维护服务稳定性。

## 示例

我们提供两个来自2020年3月的真实异常示例：

### 示例1：急剧下降
**时间**：2020年3月10日 08:00-08:05（间隔480）

```bash
python ImpAPTr_test.py 10 480
```

### 示例2：轻微下降
**时间**：2020年3月19日 11:20-11:25（间隔680）

```bash
python ImpAPTr_test.py 19 680
```

## 项目结构

```
ImpAPTr/
├── ImpAPTr_module/
│   ├── dataset/              # 数据文件（需单独下载）
│   ├── ImpAPTr.py            # 主要算法实现
│   ├── ImpAPTr_test.py       # 测试脚本和入口点
│   └── success_rate_3.10.png # 示例可视化
├── README.md                 # 英文说明
├── README_zh.md              # 本文件
├── requirements.txt          # Python依赖
└── .gitignore                # Git忽略文件
```

## 引用

如果您在研究中使用此工具，请引用：

```bibtex
@inproceedings{10.1145/3324884.3415301,
  author = {Wang, Hao and Rong, Guoping and Xu, Yangchen and You, Yong},
  title = {ImpAPTr: a tool for identifying the clues to online service anomalies},
  year = {2021},
  isbn = {9781450367684},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3324884.3415301},
  doi = {10.1145/3324884.3415301},
  booktitle = {Proceedings of the 35th IEEE/ACM International Conference on Automated Software Engineering},
  pages = {1307–1311},
  numpages = {5},
  keywords = {clues identification, multi-dimensional attributes, success rate},
  location = {Virtual Event, Australia},
  series = {ASE '20}
}
```

对于扩展工作（ImpAPTr+）：

```bibtex
@ARTICLE{9793673,
  author={Rong, Guoping and Wang, Hao and Gu, Shenghui and Xu, Yangchen and Sun, Jialin and Shao, Dong and Zhang, He},
  journal={IEEE Transactions on Dependable and Secure Computing}, 
  title={Locating Anomaly Clues for Atypical Anomalous Services: An Industrial Exploration}, 
  year={2023},
  volume={20},
  number={4},
  pages={2746-2761},
  doi={10.1109/TDSC.2022.3181143}
}
```

## 许可证

请参阅许可证文件或联系作者了解使用条款。

## 联系方式

如有问题或疑问，请在GitHub上提交issue或联系作者。

