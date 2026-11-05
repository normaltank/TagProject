# 当前状态

更新：2026-11-05（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

用户在[#32](https://github.com/normaltank/TagProject/issues/32)将论文／教师当前目标统一为用户1级primary_tag，1级是层级而非单标签数量；二级路线暂缓，后续明确收益／方法或技术更新再定。此要求替代#31教师优先2级的现行目标，旧实验和词库保持原样。无据不强标，方向／证据／未知继续保留，规则见[PROJECT](PROJECT.md#当前用户要求)及[审核规则](TEACHER_REVIEW_PROTOCOL.md)。

#32已完成有界人工来源差异核查及新20全文的root AI开发审核；未取得可绑定人工结果，历史人工修订和完成量未知。新20直接一级masked监督、排旧与覆盖账已形成，见[RESULTS](../outputs/teacher_review_batch_20261105_v1/executor/RESULTS.md)，实际登记见[实验记录](EXPERIMENTS.md#t-primary-review-01新20一级ai开发审核)。没有项目模型推理／训练／API或正式赋标；root验收、同head独立双轴、同步归档及最终关闭状态以#32与凭据为准，不以数据包形成代替完成门槛。

## 下一步与可复用资产

下一步在139共同目标下重新冻结有限公平对照与组隔离用途，旧论文原139头继续教师微调可保留为候选，不预定架构或胜出；新20仅development_pool，不能既训练又作独立测试。当前目标及旧成绩可复用边界见[研究记录](RESEARCH_AND_DECISIONS.md#32统一1级目标与下一步2026-11-05)。#30已验证双初始化训练／重载工程可行性，旧160真实＋13合成／split不改，不以细类每类仅1正例作为当前一级任务前置。

#16–23旧139一级对照重新与目标粒度相关，仍是冻结AI开发意见及特定配置证据，不是独立真人准确率／完整系统最优结论。旧A候选／证据默认及替代边界见[#21选择记录](RESEARCH_AND_DECISIONS.md#21当前方案与后训练决定2026-11-03)；#24–31按原目标留作历史研究，实际运行统一见[EXPERIMENTS](EXPERIMENTS.md)，不列为几十项新待办。

#28有限API试跑已按预算停止，发送／计费未知预留不释放；不重试或借旧额度扩大。稿件分类／生产匹配、全量正式赋标、服务器部署及二级路线均未恢复，恢复条件见[PROJECT](PROJECT.md#待续支线)。

## 阅读入口

- [PROJECT](PROJECT.md)：当前要求、业务边界与暂停支线。
- [DATA_AUDIT](DATA_AUDIT.md)：来源、分母、字段和未知项。
- [Matt工作流](agents/workflow.md)：分工、审查与关票门槛。
- [操作指南](TEACHER_PATH_AND_TOOLS.md)：本地入口与使用限制。
- [历史索引](history/README.md)：旧需求、实验与计划，冻结材料保持只读。

新克隆缺少本地Sheets、outputs和密钥，见[README](../README.md)。
