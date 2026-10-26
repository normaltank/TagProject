# 当前状态

更新：2026-10-26（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

档案整理提交4881367已在main；2026-10-25核实仓库没有PR，用户确认无需另行合并。后续subagent配置已按用户要求写入[AGENTS](../AGENTS.md)，协作方式见[工作流](agents/workflow.md)。

当前规格：[教师新20条材料的先判后比诊断 #2](https://github.com/normaltank/TagProject/issues/2)。下一张可执行任务是 [#3：贯通首条教师简介与异常分流的先判后比](https://github.com/normaltank/TagProject/issues/3)；随后 [#4：其余16条](https://github.com/normaltank/TagProject/issues/4) 依赖 #3，[#5：诊断汇总](https://github.com/normaltank/TagProject/issues/5) 依赖 #4。规格与任务正文、依赖和完成证据在 GitHub 维护。

## 实验进度与下一步

旧16例开发审核已验收；新20条初判与工作释义已冻结。17份 API 文本及3条非文本本地路由材料已派生，最终遮盖边界仍待审核。该批 API 未调用；具体计数、版本与证据统一见 [EXPERIMENTS](EXPERIMENTS.md)。

按 #3 先核查派生副本，再贯通首条文本与异常分流。小样／API授权保持有效。2026-10-26完成进度核对与[近期技术调查 #7](https://github.com/normaltank/TagProject/issues/7)，本次未运行新调用；调查结论见[选型记录](RESEARCH_AND_DECISIONS.md)。新旧标签对照顺序已补入[审核规则](TEACHER_REVIEW_PROTOCOL.md)，实际对照尚未开展。未来独立验证与扩大规模门槛未定，技术调查及新旧比较均不增加 #3 的前置条件。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
