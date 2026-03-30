# Physical Function Meta-Analysis | 身体功能指标 Meta 分析

<div align="center">

**Systematic Review & Meta-Analysis | 系统评价与 Meta 分析**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Research](https://img.shields.io/badge/Research-Meta--Analysis%20%26%20Sports%20Medicine-green.svg)]()

**Author | 作者**: YichuanAlex (Zixi Jiang)  
**Email | 邮箱**: jiangzixi1527435659@gmail.com  
**Last Updated | 最后更新**: 2026-03-24

</div>

---

## Overview | 项目概述

**English:**  
This project conducts a comprehensive meta-analysis of physical function outcomes including grip strength, 30-second chair stand test (30CST), Five Times Sit-to-Stand Test (FTSST), muscle mass, Modified Falls Efficacy Scale (MFES), gait speed, and Timed Up and Go Test (TUG). The analysis follows PRISMA guidelines and employs fixed-effects models with publication bias assessment.

**中文:**  
本项目对身体功能指标进行全面的 Meta 分析，包括握力、30 秒椅子站立测试（30CST）、五次坐立测试（FTSST）、肌肉量、改良跌倒效能量表（MFES）、步速和计时起立行走测试（TUG）。分析遵循 PRISMA 指南，采用固定效应模型并进行发表偏倚评估。

---

## Methodology | 研究方法

**English:**
- **Effect Measure**: Standardized Mean Difference (SMD) using Hedges' g
- **Model**: Fixed-effects meta-analysis
- **Publication Bias**: Funnel plots, Rosenthal's Fail-Safe N
- **Sensitivity Analysis**: Trim-and-fill method
- **Visualization**: Forest plots, funnel plots, subgroup analysis

**中文:**
- **效应量**: 使用 Hedges' g 的标准化均数差（SMD）
- **模型**: 固定效应 Meta 分析
- **发表偏倚**: 漏斗图、Rosenthal 的 Fail-Safe N
- **敏感性分析**: 剪补法
- **可视化**: 森林图、漏斗图、亚组分析

---

## Project Structure | 项目结构

```
体术分析/
│
├── meta_analysis.py                       # Main analysis script | 主分析脚本
├── meta_analysis_academic.py              # Academic version | 学术版本
├── CMA- analysis.xlsx                     # Source data | 源数据
│
├── subtables/                             # Subgroup tables | 亚组表
│   ├── 30CST.xlsx                         # Chair stand test | 椅子站立测试
│   ├── FTSST.xlsx                         # Sit-to-stand test | 坐立测试
│   ├── grip_strength.xlsx                 # Grip strength | 握力
│   └── ... (other outcomes)
│
├── forest_plot/                           # Forest plots | 森林图
│   ├── 30CST_forest.png
│   ├── FTSST_forest.png
│   └── ... (all outcomes)
│
├── funnel_plot/                           # Funnel plots | 漏斗图
│   ├── 30CST_funnel.png
│   └── ... (all outcomes)
│
├── trim_fill/                             # Trim-and-fill analysis | 剪补分析
│   ├── 30CST_trimfill.png
│   └── ... (all outcomes)
│
└── fail_safe_n/                           # Fail-safe N analysis | 失安全数分析
    ├── 30CST_failsafe.xlsx
    └── ... (all outcomes)
```

---

## Key Features | 功能特性

**English:**
- Automated data extraction from Excel
- Standardized effect size calculation
- Comprehensive publication bias assessment
- Academic-quality visualization
- Batch processing for multiple outcomes

**中文:**
- 从 Excel 自动提取数据
- 标准化效应量计算
- 全面的发表偏倚评估
- 学术级可视化
- 多结局批量处理

---

## Installation and Usage | 安装与使用

**English:**
```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn statsmodels

# Run meta-analysis
python meta_analysis.py
```

**中文:**
```bash
# 安装依赖
pip install pandas numpy matplotlib seaborn statsmodels

# 运行 Meta 分析
python meta_analysis.py
```

---

## License | 许可证

**English:**
MIT License

**中文:**
MIT 许可证

---

## Contact | 联系方式

**English:**
- **Author**: Zixi Jiang
- **Email**: jiangzixi1527435659@gmail.com
- **GitHub**: https://github.com/YichuanAlex

**中文:**
- **作者**: 江子曦
- **邮箱**: jiangzixi1527435659@gmail.com
- **GitHub**: https://github.com/YichuanAlex

---

## Keywords | 关键词

**English:**  
Meta-Analysis, Physical Function, Sports Medicine, Systematic Review, Effect Size, Publication Bias

**中文:**  
Meta 分析、身体功能、运动医学、系统评价、效应量、发表偏倚

---

<div align="center">

**Thank you for your interest in this research!**  
**感谢您对本研究的关注!**

</div>
