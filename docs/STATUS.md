# 当前状态

更新：2026-10-28（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

工作流规范化[#10](https://github.com/normaltank/TagProject/issues/10)已验收。当前任务：[教师输出失败诊断与证据范围修复 #11](https://github.com/normaltank/TagProject/issues/11)，已形成离线修复与待审交付；逐项验收、独立审查及最终交付状态统一见 #11。执行恢复与接管已留证，后续门槛按[工作流](agents/workflow.md)。

教师小样 [#2](https://github.com/normaltank/TagProject/issues/2)及任务 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4)、[#5](https://github.com/normaltank/TagProject/issues/5)，以及 [#9：历史BERT标签对照](https://github.com/normaltank/TagProject/issues/9)已完成交付检查和独立双轴审查。此前提前关票已补验收留证；入口见 [EXPERIMENTS](EXPERIMENTS.md)，最终提交和任务状态在 GitHub 维护。

## 实验进度与下一步

旧16例开发审核已验收；新20条已完成有界运行、教师模型复审与预测冻结。成功、隔离、拒判及实际用量统一见 [EXPERIMENTS](EXPERIMENTS.md)。

历史对照与本轮离线修复证据见[EXPERIMENTS](EXPERIMENTS.md)。历史BERT输入未知，不作同输入模型排名；新版提示的实际效果待另批有界验证，尚未启动训练或全量赋标。新增待审稿件已按“共用领域标签匹配审稿人”的用途登记，来源及初检边界见[DATA_AUDIT](DATA_AUDIT.md)。2026-10-26[近期技术调查 #7](https://github.com/normaltank/TagProject/issues/7)已完成，选型依据见[研究记录](RESEARCH_AND_DECISIONS.md)。独立验证与扩大规模门槛仍未定。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
