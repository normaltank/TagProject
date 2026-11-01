# 当前状态

更新：2026-11-01（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

工作流规范化[#10](https://github.com/normaltank/TagProject/issues/10)、[教师输出失败诊断与证据范围修复 #11](https://github.com/normaltank/TagProject/issues/11)、[新版教师提示小样验证 #12](https://github.com/normaltank/TagProject/issues/12)及[接手核验与方法讨论归档 #13](https://github.com/normaltank/TagProject/issues/13)已验收关闭。[证据角色最小对照 #14](https://github.com/normaltank/TagProject/issues/14)与[#15本地三模型试跑](https://github.com/normaltank/TagProject/issues/15)已归档关闭，最终状态以对应Issue为准。

[#16扩大本地比较与弱监督分类头试验](https://github.com/normaltank/TagProject/issues/16)及[#17证据判别与任务适配](https://github.com/normaltank/TagProject/issues/17)均已验收关闭，产物作为新票依赖。[#18完整本地流程比较](https://github.com/normaltank/TagProject/issues/18)已完成最终12配置、200先判/匿名后审、cal锁点及1000待审队列，正在收束待审交付。主Agent独立数值/统计/队列/图核验通过，后续仍须同base/head全新Standards/Spec审查、最终验收与归档同步关闭。成果入口见[完整流程实验](EXPERIMENTS.md#t-pipeline-01完整本地流程比较与1000组待审试运行)。

教师小样 [#2](https://github.com/normaltank/TagProject/issues/2)及任务 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4)、[#5](https://github.com/normaltank/TagProject/issues/5)，以及 [#9：历史BERT标签对照](https://github.com/normaltank/TagProject/issues/9)已完成交付检查和独立双轴审查。此前提前关票已补验收留证；入口见 [EXPERIMENTS](EXPERIMENTS.md)，最终提交和任务状态在 GitHub 维护。

## 实验进度与下一步

旧16例、新20条、另批10条新版提示材料及#14纯合成材料分别保留；#14的明确短模板角色诊断及教学背景清理问题见[EXPERIMENTS的T-ROLE-01](EXPERIMENTS.md#t-role-01纯合成证据角色最小对照)。#15复用#12真实开发文本和#14合成文本，实际运行现成encoder NLI头、BGE encoder dense embedding及Qwen decoder embedding；共同L2与细L3覆盖、角色反例、耗时／显存、下载修复及限制见[T-LOCAL-01](EXPERIMENTS.md#t-local-01三个本地模型的共同开发材料试跑)。

#18按cal保留旧四top1并集重排，已交1000组/2133候选，全部待审、正式赋标0；广覆盖多标签候选保留BGE5/union重排价值，不能仅据top1联合差区间跨0判无用。全139和当前原NLI不作本配置优先流程，暂不扩大后训练；具体收益、代价与AI意见限制见实验记录。本轮11可扩展候选在cal意见前固定，未依held改推荐/阈值。[旧方法讨论](RESEARCH_AND_DECISIONS.md#旧对话方法讨论2026-10-30归档)不是最终架构，不预设embedding后必须接DeepSeek。

#16轻量头只使用冻结表示与历史S弱监督；#17使用有来源的旧AI支持意见作小规模任务头／LoRA对照。尚未开展真人答案的独立效果验证或全量赋标，产品、提示和正式词库未改。历史BERT输入未知，#16另按已固定顺序审计其标签对当前简介的支持，不能据此称历史模型错误率。新增待审稿件来源及初检边界见[DATA_AUDIT](DATA_AUDIT.md)，稿件分类和师稿匹配支线保持暂停。选型官方依据见[研究记录](RESEARCH_AND_DECISIONS.md)，独立验证与扩大规模门槛仍未定。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
