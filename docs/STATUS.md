# 当前状态

更新：2026-10-26（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

档案整理提交4881367已在main；2026-10-25核实仓库没有PR，用户确认无需另行合并。后续subagent配置已按用户要求写入[AGENTS](../AGENTS.md)，协作方式见[工作流](agents/workflow.md)。

本批已完成：[教师新20条材料的先判后比诊断 #2](https://github.com/normaltank/TagProject/issues/2)及任务 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4)、[#5](https://github.com/normaltank/TagProject/issues/5)，以及 [#9：历史BERT标签对照](https://github.com/normaltank/TagProject/issues/9)。交付物检查与独立 Standards／Spec 两路审查均通过。此前提前关闭任务的流程偏差已补做验收并留证；审查及交付入口见 [EXPERIMENTS](EXPERIMENTS.md)，最终提交和任务状态在 GitHub 维护。

## 实验进度与下一步

旧16例开发审核已验收；新20条已完成有界运行、教师模型复审与预测冻结。成功、隔离、拒判及实际用量统一见 [EXPERIMENTS](EXPERIMENTS.md)。

历史对照及本地报告／表格入口见 [EXPERIMENTS](EXPERIMENTS.md)。历史BERT输入未知，不作同输入模型排名；比较阶段无新增API请求。下一步优先形成输出失败诊断与证据范围修复任务，再另批验证，尚未启动修复、训练或全量赋标。2026-10-26[近期技术调查 #7](https://github.com/normaltank/TagProject/issues/7)已完成，选型依据见[研究记录](RESEARCH_AND_DECISIONS.md)。独立验证与扩大规模门槛仍未定。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
