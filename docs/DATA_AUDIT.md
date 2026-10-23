# 数据审计（公开仓库整理版）

审计日期：2026-10-23（Asia/Singapore）。本页保留汇总口径和复核结论，不包含真实教师内部ID、姓名／联系方式或原始简介摘录。修改前完整文档在本地忽略目录`outputs/git_upload_prepare_20261023_v1/private_before_upload/docs/DATA_AUDIT.md`；原始XLSX、逐行审计和16例均未改写或上传。

## 输入与可复核性

两份本地文件为`Sheets/teacher_20261022.xlsx`（108968834字节）和`Sheets/review_tagscollection_20261022.xlsx`（30080字节）。原件SHA-256：

- 教师：`fbdac1e9f1464ac32b4d2e9ea87831c3fe3023a0c48f73b731cf17d0b00b376d`。
- 词库：`8e130842d70a8418b538caa10097f7595817ac45fde01dcc58d67726b58eb08f`。

主审计`audit_inputs.py` v1.1.0使用Python 3.12.14、openpyxl 3.1.5，只读、data_only=False，不计算或保存工作簿。原本地输出`outputs/audit_20261023_v1_1_0_run1/`含manifest、脚本快照、summary和定位CSV；独立标准库XML核验在`outputs/audit_20261023_checks_v1/verification_v2.json`为23/23。原verification.json为22/23的失败诊断，保留未覆盖。新克隆不带这些本地证据文件。

初次差异来自日期／公式读取表示，统一解码口径后通过，不是放宽容差。deleted=0简介解码字符数115058149，词法XML口径115057748，差401；由28项日期和3项公式的表示差异解释。原件哈希不变。审计及XML脚本复跑方法见[README](../README.md)。

## 教师口径与缺失

原sheet为`teacher_20261022`，声明100526行×21列（含表头）。严格非None／非空字符串为100399个非空数据行，逐单元格strip后100398；一条仅空白行造成差异，不能据此改变教师分母。

主分析保留ASCII正整数且唯一的记录ID：100000条／100000唯一，重复0。该语法条件不证明字段结构完整或简介有效；398个trim后非记录候选及127个空行留在原表，未自动拼接或删除。

- 全100000条：简介缺失5948、旧标签缺失19；99981个非空字符串数组，177991次旧赋值、139个唯一字符串，JSON解析错误0。
- deleted=0共98863条：简介缺失5909、标签缺失19，175923次旧赋值。
- deleted=1共1137条：简介缺失39、标签缺失0，2068次旧赋值。

字段deleted的业务含义待字典确认，98863不等于可用教师数。全部5948条空简介都有旧标签，但不能据此认定旧标签正确或补写方向。交接的缺失数来自包含非记录行的另一分母，不能混用。

## 数据质量与解释边界

- 19条简介恰为32767字符，均在deleted=0，伴随尾列缺失和相邻残片，支持导出／结构损坏假设，原因未确认。另有8000字符堆积432条，仅为疑似来源限制线索，不证明截断。
- 精确重复非空简介869组／5222行，重复主页475组／1539行；可能是采集、模板或同页线索，不能自动合并教师。
- HTML样式152条、Unicode替换符58条、短于100字符28103条，均为诊断信号，不是最终无效判定。
- 简介类型：字符串94006、None5948、整数18、日期28；非空字符串化94052不能称有效研究简介数。46个非字符串与另3个公式候选需分流；原始公式和缓存仅在本地记录，不执行。
- 有效记录主页缺失1340、title缺失7296、collect_date缺失12342、collector缺失19133、is_interdisciplinary缺失916。记录时间不等于研究事实时间。

教师列为A=id、B=name、C=email、D=send_count、E=last_send_at、F=department_id、G=collect_date、H=collector、I=title、J=last_export_date、K=created、L=deleted、M=modified、N=homepage、O=intro、P=external_userid、Q=aminer_synced、R=enrichment_status、S=tags、T=wecom_added、U=is_interdisciplinary。方向识别主要用O，S仅作有来源的历史线索；联系方式和系统状态不作为专长证据。

## 词库与历史标签

词库sheet为`review_tagscollection_20261022`，140行×7列含表头，139个来源ID唯一、deleted均0。A=id、B=created、C=modified、D=deleted、E=primary_tag、F=secondary_tag、G=family_tag，按来源G→E→F的JSON数组解释层级。

共有35个一级名称、139个二级、1396个三级出现位置／1384个三级字符串。12组三级名称各出现两次，是否同义、异义或多归属待定义，不按同名自动合并。19个二级无三级，说明来源粒度不齐，不能凭空补齐。来源ID只标整行，数组下标标出现位置，均未升级为正式概念ID；没有完整范围定义或多语言别名。

旧标签主要落于较粗层级，不能未经核验充当细粒度金标、独立测试答案或唯一成功指标。未发现可审查的历史BERT代码／训练结果；独立人工答案及真实稿件仍缺失。

## 语义观察与本轮范围

定向材料只用于开发问题诊断：研究正文、导航、课程、行政岗位、文章页、旧项目、论文偶现主题、乱码和非文本需分别判断角色；引用存在不等于稳定专长，未提及不等于没有该方向。语种和文字脚本分开，外文不限英语，尚未做全表语种普查。

16条Agent开发示例、本地引文及逐行定位保留在`outputs/teacher_dev_20261023_v0_2/`，不纳入Git，不充当独立真人金标或模型效果。公开文档不复刻这些简介内容；详细方法及本次DeepSeek能力见[路径／工具说明](TEACHER_PATH_AND_TOOLS.md)，最新授权与状态见[STATUS](STATUS.md)。
