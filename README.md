# Pyacet
Python Automated Custom EDA Toolkit

<!--배지-->
![Repository Size][repository-size-shield]

<!--목차-->
# Table of Contents
- [[1] About the Project](#1-about-the-project)
  - [Features](#features)
  - [Technologies](#technologies)
- [[2] Getting Started](#2-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [[3] Usage](#3-usage)
- [[4] Contact](#4-contact)



# [1] About the Project
<!-- 프로젝트 소개 추가 -->

## Features
<!-- 주요기능 설명 추가 -->

## Technologies
- [python](https://www.python.org/) 3.8.5
- [fpdf2](http://www.fpdf.org/) 2.7.9
- [matplotlib](https://matplotlib.org/) 3.7.5
- [numpy](https://numpy.org/) 1.24.4
- [pandas](https://pandas.pydata.org/) 2.0.3
- [scikit-learn](https://scikit-learn.org/) 1.3.2
- [seaborn](https://seaborn.pydata.org/) 0.13.2



# [2] Getting Started

## Prerequisites
- python(3.8>=)

## Installation
1. Repository Clone
```bash
git clone https://github.com/Linfo-KR/pyacet.git
```
2. PIP Packages Install
```bash
pip install git+https://github.com/Linfo-KR/pyacet.git
```



# [3] Usage
```python
import pyacet

data = pyacet.utils.generate_testset()
pyacet.ReportGenerator(data, output_path, 'Dataset Name').generate_report()
pyacet.Visualization(data, output_path).visualize()
```
<!-- 출력물 예시 추가 -->



# [4] Contact
- 📧 linfo4931@gmail.com



<!-- # [7] License
MIT 라이센스
라이센스에 대한 정보는 [`LICENSE`][license-url]에 있습니다. -->



<!--Url for Badges-->
[license-shield]: https://img.shields.io/github/license/dev-ujin/readme-template?labelColor=D8D8D8&color=04B4AE
[repository-size-shield]: https://img.shields.io/github/repo-size/dev-ujin/readme-template?labelColor=D8D8D8&color=BE81F7
[issue-closed-shield]: https://img.shields.io/github/issues-closed/dev-ujin/readme-template?labelColor=D8D8D8&color=FE9A2E

<!--Url for Buttons-->
[readme-eng-shield]: https://img.shields.io/badge/-readme%20in%20english-2E2E2E?style=for-the-badge
[view-demo-shield]: https://img.shields.io/badge/-%F0%9F%98%8E%20view%20demo-F3F781?style=for-the-badge
[view-demo-url]: https://dev-ujin.github.io
[report-bug-shield]: https://img.shields.io/badge/-%F0%9F%90%9E%20report%20bug-F5A9A9?style=for-the-badge
[report-bug-url]: https://github.com/dev-ujin/readme-template/issues
[request-feature-shield]: https://img.shields.io/badge/-%E2%9C%A8%20request%20feature-A9D0F5?style=for-the-badge
[request-feature-url]: https://github.com/dev-ujin/readme-template/issues

<!--URLS-->
[license-url]: LICENSE.md
[contribution-url]: CONTRIBUTION.md
[readme-eng-url]: ../README.md



