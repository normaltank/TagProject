# 当前状态

更新：2026-11-01（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

工作流规范化[#10](https://github.com/normaltank/TagProject/issues/10)、[教师输出失败诊断与证据范围修复 #11](https://github.com/normaltank/TagProject/issues/11)、[新版教师提示小样验证 #12](https://github.com/normaltank/TagProject/issues/12)及[接手核验与方法讨论归档 #13](https://github.com/normaltank/TagProject/issues/13)已验收关闭。[证据角色最小对照 #14](https://github.com/normaltank/TagProject/issues/14)与[#15本地三模型试跑](https://github.com/normaltank/TagProject/issues/15)已归档关闭，最终状态以对应Issue为准。

[#16扩大本地比较与弱监督分类头试验](https://github.com/normaltank/TagProject/issues/16)已验收关闭，产物作为新票依赖。当前[#17证据判别与任务适配](https://github.com/normaltank/TagProject/issues/17)的实验、主Agent AI先判／后审、统计、图及可复核队列已完成，正在交付待审；主Agent数值核对已完成，独立Standards／Spec审查、最终验收及同步归档关闭仍按[工作流](agents/workflow.md)推进。实测与成果入口见[证据判别实验](EXPERIMENTS.md#t-evidence-01证据判别与同nli任务适配)，最终状态以Issue为准。

教师小样 [#2](https://github.com/normaltank/TagProject/issues/2)及任务 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4)、[#5](https://github.com/normaltank/TagProject/issues/5)，以及 [#9：历史BERT标签对照](https://github.com/normaltank/TagProject/issues/9)已完成交付检查和独立双轴审查。此前提前关票已补验收留证；入口见 [EXPERIMENTS](EXPERIMENTS.md)，最终提交和任务状态在 GitHub 维护。

## 实验进度与下一步

旧16例、新20条、另批10条新版提示材料及#14纯合成材料分别保留；#14的明确短模板角色诊断及教学背景清理问题见[EXPERIMENTS的T-ROLE-01](EXPERIMENTS.md#t-role-01纯合成证据角色最小对照)。#15复用#12真实开发文本和#14合成文本，实际运行现成encoder NLI头、BGE encoder dense embedding及Qwen decoder embedding；共同L2与细L3覆盖、角色反例、耗时／显存、下载修复及限制见[T-LOCAL-01](EXPERIMENTS.md#t-local-01三个本地模型的共同开发材料试跑)。

#17当前可直接复核的成果是去gen重排候选队列，全部requires_review；现成NLI保留为独立证据对照，不是重排后再串NLI。BGE／Qwen候选与完整139覆盖继续保留，未证明四基线缺一不可。生成支路成本高且无保留收益，当前NLI LoRA增益区间跨0，暂不扩大；结论限本配置和AI开发样本。全部冻结点在held未维持90%支持目标，不用于全库自动赋标。后续先完成本票验收／双轴审查，扩大验证另设未暴露材料与答案。[旧方法讨论](RESEARCH_AND_DECISIONS.md#旧对话方法讨论2026-10-30归档)不是最终架构，不预设embedding后必须接DeepSeek。

#16轻量头只使用冻结表示与历史S弱监督；#17使用有来源的旧AI支持意见作小规模任务头／LoRA对照。尚未开展真人答案的独立效果验证或全量赋标，产品、提示和正式词库未改。历史BERT输入未知，#16另按已固定顺序审计其标签对当前简介的支持，不能据此称历史模型错误率。新增待审稿件来源及初检边界见[DATA_AUDIT](DATA_AUDIT.md)，稿件分类和师稿匹配支线保持暂停。选型官方依据见[研究记录](RESEARCH_AND_DECISIONS.md)，独立验证与扩大规模门槛仍未定。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
