# 当前状态

更新：2026-10-30（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

工作流规范化[#10](https://github.com/normaltank/TagProject/issues/10)、[教师输出失败诊断与证据范围修复 #11](https://github.com/normaltank/TagProject/issues/11)及[新版教师提示小样验证 #12](https://github.com/normaltank/TagProject/issues/12)已验收关闭。#12的有界运行、指挥教师模型逐项复审、工具中断接管和独立双轴审查均已留证。当前任务为[接手核验与方法讨论归档 #13](https://github.com/normaltank/TagProject/issues/13)；本次接手核验与讨论归档见 #13，验收、审查及最终状态以 Issue 为准，后续门槛按[工作流](agents/workflow.md)。

教师小样 [#2](https://github.com/normaltank/TagProject/issues/2)及任务 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4)、[#5](https://github.com/normaltank/TagProject/issues/5)，以及 [#9：历史BERT标签对照](https://github.com/normaltank/TagProject/issues/9)已完成交付检查和独立双轴审查。此前提前关票已补验收留证；入口见 [EXPERIMENTS](EXPERIMENTS.md)，最终提交和任务状态在 GitHub 维护。

## 实验进度与下一步

旧16例、新20条及另批10条新版提示材料分别保留。新版首次预测、初判和复审已分开冻结；输出可用性、语义修订、覆盖缺口及实际用量统一见 [EXPERIMENTS](EXPERIMENTS.md)。

新版小样仍发现输出隔离、背景混入方向、未说明的方法扩展，以及已有上位标签遗漏／过度保守映射。下一步将[方法比较建议](RESEARCH_AND_DECISIONS.md#旧对话方法讨论2026-10-30归档)整理成可审实验规格，按工作流确认材料、评价及资源缺口，再安排后续任务；三路线独立竞争和四步探索顺序目前均为旧 Agent 建议，尚未成为用户确认的新规格或最终架构。本票新增分类请求上限为0，不恢复或重置旧批次预算；#12已用10次、未知0、余量0。

尚未开展下一轮修正、新模型对照、独立效果验证、训练或全量赋标。历史BERT输入未知，当前不同样本的诊断不作模型排名。新增待审稿件服务“共用领域标签匹配审稿人”，来源及初检边界见[DATA_AUDIT](DATA_AUDIT.md)，稿件分类和师稿匹配支线保持暂停。2026-10-26[近期技术调查 #7](https://github.com/normaltank/TagProject/issues/7)已完成，选型依据见[研究记录](RESEARCH_AND_DECISIONS.md)。独立验证与扩大规模门槛仍未定。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
