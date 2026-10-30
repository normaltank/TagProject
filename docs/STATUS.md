# 当前状态

更新：2026-10-30（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

工作流规范化[#10](https://github.com/normaltank/TagProject/issues/10)、[教师输出失败诊断与证据范围修复 #11](https://github.com/normaltank/TagProject/issues/11)、[新版教师提示小样验证 #12](https://github.com/normaltank/TagProject/issues/12)及[接手核验与方法讨论归档 #13](https://github.com/normaltank/TagProject/issues/13)已验收关闭。本轮[证据角色最小对照 #14](https://github.com/normaltank/TagProject/issues/14)的10条纯合成有界运行、主Agent先判与逐项复审已分别冻结并形成执行交付；验收、独立审查、归档及最终状态以#14为准，后续门槛按[工作流](agents/workflow.md)。

教师小样 [#2](https://github.com/normaltank/TagProject/issues/2)及任务 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4)、[#5](https://github.com/normaltank/TagProject/issues/5)，以及 [#9：历史BERT标签对照](https://github.com/normaltank/TagProject/issues/9)已完成交付检查和独立双轴审查。此前提前关票已补验收留证；入口见 [EXPERIMENTS](EXPERIMENTS.md)，最终提交和任务状态在 GitHub 维护。

## 实验进度与下一步

旧16例、新20条及另批10条新版提示材料分别保留。本轮另用10条纯合成／5对检查研究与授课、合作者、兴趣、代表作和导航的角色区别，真实教师分母0；初判、发送批准、首次预测和语义复审分别冻结。实际用量、候选与研究判断的不同任务、发现及限制统一见[EXPERIMENTS的T-ROLE-01](EXPERIMENTS.md#t-role-01纯合成证据角色最小对照)。

本轮明确短模板中的目标支持状态符合先判期待，但教学弱背景仍进入方向列表，同名L3结果也未检验上位映射；不能据此解决旧真实小样中的隔离、方法外推和范围问题。下一步优先设计未暴露的真实混合语境材料，检查角色归属及方向列表清理，再按工作流明确评价和资源边界。[方法比较建议](RESEARCH_AND_DECISIONS.md#旧对话方法讨论2026-10-30归档)中的三路线保留独立竞争，四步探索顺序仍是旧Agent建议，尚非用户确认的最终架构。本轮#14实用10次HTTP、未知0、余量0；#13新增调用上限0仅为其归档任务的历史边界，#12旧预算也不恢复。

尚未开展新模型对照、独立效果验证、训练或全量赋标；本轮未改产品、提示或正式词库。历史BERT输入未知，当前不同样本的诊断不作模型排名。新增待审稿件服务“共用领域标签匹配审稿人”，来源及初检边界见[DATA_AUDIT](DATA_AUDIT.md)，稿件分类和师稿匹配支线保持暂停。2026-10-26[近期技术调查 #7](https://github.com/normaltank/TagProject/issues/7)已完成，选型依据见[研究记录](RESEARCH_AND_DECISIONS.md)。独立验证与扩大规模门槛仍未定。

## 阅读入口

- [PROJECT](PROJECT.md)：当前范围与暂停支线恢复条件。
- [Matt 工作流与写作规范](agents/workflow.md)：阶段、职责与完成条件。
- [审核规则](TEACHER_REVIEW_PROTOCOL.md)：先判后比及分歧记录。
- [历史档案](history/README.md)：原需求、旧 planning 与未运行设计。

原始 XLSX、旧16例、已冻结初判及预测版本保持原位置。新克隆缺少本地数据、outputs 与密钥，见 [README](../README.md)。
