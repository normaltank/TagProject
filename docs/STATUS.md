# 当前状态

更新：2026-11-05（Asia/Singapore）。唯一活跃主线：教师简介→研究方向→现有标签＋证据。

## 当前阶段

[#30教师监督与双初始化微调入口](https://github.com/normaltank/TagProject/issues/30)已生成可追溯masked监督，并经root显式放行完成旧论文/同HFL通用encoder各8次真实更新、mask与fresh-model保存重载验证；实际细类稀疏覆盖决定采用路径条件支持判别新头。当前到执行交付待审，下一步由root独立核验、同head双轴及归档；[实际包与限制](../outputs/teacher_adaptation_pilot_20261105_v1/executor/RESULTS.md)。仅训练工程可行性，不是独立效果擂台或正式赋标，最终关闭以#30为准。

[#29前人方法理解、批判与教师适配建议](https://github.com/normaltank/TagProject/issues/29)已形成[研究报告与阅读账](../outputs/predecessor_method_review_20261105_v1/executor/REVIEW.md)：前人论文微调／批处理有实物，教师证据／充分度／三态及retrain有设计，人工完成量和教师运行绑定仍缺。下一笔建议对称比较旧论文初始化与相同通用底座的教师微调，以及当前简洁候选方案；精确对照尚未实测，现有默认仅为阶段性参赛者。只读研究无新训练／推理或正式赋标，#28未知费用不释放；主Agent核验、同head双轴、同步归档及关闭以#29为准。

[#28旧教师清洗追溯与完整赋标补测](https://github.com/normaltank/TagProject/issues/28)的首结果／未知账本、root逐项cal审核与取舍锁、全分层未尝试统计及106待审成果已形成，本轮实验已按预算预留守卫停止。教师清洗未建立可重现运行绑定；校准未跑满、其余组未运行，依预冻incomplete/U规则保留目标2级后续开发C1优先＋RR补充，旧A粗层默认不改，无完整系统优越结论。实际分母、费用估算／未知预留和证据入口见[实验记录](EXPERIMENTS.md#t-complete-01完整赋标有限试跑)；下一步有限验证的输入／完整输出／独立答案边界见[研究入口](RESEARCH_AND_DECISIONS.md#28完整语义判别补测的冻结边界2026-11-05)。不再推理或重试，正式赋标0；最终验收、同head双轴、同步与关闭以#28及其凭据为准。

[#27选型边界与遗漏核验](https://github.com/normaltank/TagProject/issues/27)已验收、双轴审查及归档关闭。共同1级擂台、有限短名单和完整输出补测依据见[选型入口](RESEARCH_AND_DECISIONS.md#27最终候选边界与下一笔投入2026-11-05)；当前接续任务为#28，旧STATUS中的“待审交付”快照已同步。

[#26目标2级细标签开发对照](https://github.com/normaltank/TagProject/issues/26)已验收、双轴审查及归档关闭。cal锁Qwen为后续细候选优先；重排诊断／语言数值更好，尚不能最终定型。原预测及宽池校正分别保留，候选全pending、正式赋标0，旧A粗层默认不改；[结果与证据](EXPERIMENTS.md#t-fine-01目标2级细标签开发对照)。

[#25证据决定标注粒度](https://github.com/normaltank/TagProject/issues/25)已形成独立离线profile及root冻结13例合同验证：用户已澄清模糊为简介与标签的标注关系；允许有据2级及明确0／1级宽保留，宽类不下推、未决不升级。操作与限制见[新入口](TEACHER_PATH_AND_TOOLS.md#证据粒度离线profile25)，实际运行见[实验记录](EXPERIMENTS.md#t-granularity-01证据决定粒度离线合同试运行)。主Agent核验、同版本独立双轴审查、归档及最终状态以#25记录为准；本票不跑新模型、不读新教师行、不证明真实准确率或恢复稿件生产匹配。

[#24 Benchmark有效性审计](https://github.com/normaltank/TagProject/issues/24)已形成审计与新评价设计，核心修正是用户目标2级secondary而#16–23主赛只比较139个用户1级中类；A仅在该历史窄口径领先，尚未选出目标2级最优方案。层级定义及旧引用对应见[PROJECT](PROJECT.md#当前用户要求)，问题证据与新评价设计见[研究入口](RESEARCH_AND_DECISIONS.md#24benchmark有效性与目标层级修正2026-11-04)。核验、独立双轴审查、归档及关闭阶段以#24记录为准；模糊标注关系已由#25澄清，后续仍需目标2级的独立答案／新评价。未开展新模型／真人标注，不借旧held调参或扩大赋标。

[#23旧BERT实跑擂台](https://github.com/normaltank/TagProject/issues/23)已形成论文1000真实forward复现、同#21教师120三配置对照及固定统计：当前保留A旧四top1并集→Qwen逐窗为待审默认；论文高margin的85%—88%可复现，但不是教师真人准确率。独立审查、验收、归档和关闭阶段统一以该票记录为准；结果及运行入口见[实验记录](EXPERIMENTS.md#t-bert-duel-01旧论文bert实跑复现与教师迁移擂台)。下一步优先补可信本人角色／范围纠错监督与教师人工模型来源链，独立新答案验证另定；不依本轮held调参、扩大训练或正式赋标。

[#22前人BERT成果与指标审计](https://github.com/normaltank/TagProject/issues/22)已形成只读实物审计、离线指标重算及拟议公平教师擂台；本票未训练、评分新模型或恢复稿件支线，后续实际复现与教师迁移由#23分票执行。审查、验收、归档与关闭阶段统一以#22记录为准；报告与操作入口见[实验记录](EXPERIMENTS.md#t-predecessor-audit-01前人bert实物与指标只读审计)。

[#21准确性优先的GLiNER2.5与GLiClass多语补测](https://github.com/normaltank/TagProject/issues/21)已验收关闭。当前待审默认仍为四top1并集→Qwen逐窗，阈值未改，暂不扩大训练或正式自动赋标。冻结七配置结果、候选队列与限制见[实验记录](EXPERIMENTS.md#t-priority-01准确性优先的多语原生分类与整篇对照)，默认／替代及部署方向见[选型记录](RESEARCH_AND_DECISIONS.md#21当前方案与后训练决定2026-11-03)。

[#20多语输入与既有评测覆盖盘点](https://github.com/normaltank/TagProject/issues/20)已完成本地教师/稿件快照脚本统计及完整代表的root AI核查，确认英语内容与字段间双语实际存在；文字脚本、正文/书目角色和全表语种比例分开解释。当前无配置数据库连接，结论限已有导出。数据事实及旧评价语言覆盖限制见[DATA_AUDIT](DATA_AUDIT.md#2026-11-01多语输入与既有评价覆盖盘点)，修正仅中文选型前提及跨语中文词库待测约束见[研究记录](RESEARCH_AND_DECISIONS.md#20多语输入对后续比较的约束)。本票不新增模型实验，审查、最终验收、归档同步和关闭阶段统一以#20为准；后续比较须覆盖实际语言与证据角色，仍优先积累可信监督。

[#19中文BERT、mmBERT与专用encoder重排补测](https://github.com/normaltank/TagProject/issues/19)的实验及主Agent核验已完成：五路完整预测、全部100组先判/匿名后审及配对统计可复核。cal推荐mmBERT保留不变；held未显示其超过旧BGE头的明确联合支持收益，全部候选仍待审、正式赋标0。独立审查、最终验收、归档同步和关闭阶段与证据统一以#19为准；下一项研究优先积累可信角色/纠错监督。结论与限制见[实验记录](EXPERIMENTS.md)，本地证据在`outputs/bert_encoder_tools_20261101_v1/executor/`。

Matt Setup、[档案整理 #1](https://github.com/normaltank/TagProject/issues/1)、小样规格与任务拆分已落地。用户已确认现有 CLI→输出校验→审核报告的验收入口，以及三张任务的粒度和依赖。

工作流规范化[#10](https://github.com/normaltank/TagProject/issues/10)、[教师输出失败诊断与证据范围修复 #11](https://github.com/normaltank/TagProject/issues/11)、[新版教师提示小样验证 #12](https://github.com/normaltank/TagProject/issues/12)及[接手核验与方法讨论归档 #13](https://github.com/normaltank/TagProject/issues/13)已验收关闭。[证据角色最小对照 #14](https://github.com/normaltank/TagProject/issues/14)与[#15本地三模型试跑](https://github.com/normaltank/TagProject/issues/15)已归档关闭，最终状态以对应Issue为准。

[#16扩大本地比较与弱监督分类头试验](https://github.com/normaltank/TagProject/issues/16)及[#17证据判别与任务适配](https://github.com/normaltank/TagProject/issues/17)均已验收关闭，产物作为新票依赖。[#18完整本地流程比较](https://github.com/normaltank/TagProject/issues/18)已完成最终12配置、200先判/匿名后审、cal锁点及1000待审候选成果，主Agent独立数值/统计/队列/图核验通过。独立审查、最终验收、归档同步及关闭的阶段与证据统一以#18为准。成果入口见[完整流程实验](EXPERIMENTS.md#t-pipeline-01完整本地流程比较与1000组待审试运行)，可按用途复用候选队列和广覆盖短名单。

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
