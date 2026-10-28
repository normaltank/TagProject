# 教师实验与运行登记

本页维护已运行事实、解释范围和本地证据入口。执行前读[教师审核规则](TEACHER_REVIEW_PROTOCOL.md)及任务 Issue，运行方法见[操作指南](TEACHER_PATH_AND_TOOLS.md)。完整原文和逐项意见仅保留本地；新克隆不含 outputs 中的证据。

## 运行登记

| 编号 | 状态 | 证据与结论 |
| --- | --- | --- |
| R-AUDIT／VERIFY／INSPECT | 已完成输入审计、XML核验和定向观察 | [DATA_AUDIT](DATA_AUDIT.md)维护分母、字段和失败修正；不是分类效果 |
| R-COST／E-08 | 已运行预算算术，未运行模型 | [历史实验设计](history/EXPERIMENTS_PHASE1_20261023.md)保留假设、单位和计算口径 |
| T-DEV-01 | 原16例 Agent 开发材料已完成 | 下节；长文未穷尽，非独立答案 |
| T-DS-01 | 工具及两次有界连通已完成 | 下节；只证明连通和格式约束 |
| T-REVIEW-01 | 原16例教师模型开发审核已完成 | 下节；不增加独立测试分母 |
| T-PREP-02 | 20条源材料与初判已冻结，发送副本已审核 | 原冻结版本保留，最终发送版本见 T-PILOT-02 |
| T-PILOT-02 | 新20条流程诊断已完成 | 17次请求、3条本地分流；下节记录失败、复审及用量 |
| T-BERT-01 | 同批20条历史标签对照已完成 | 共同层级与细化价值分开；下节说明开发审核结果及不可比范围 |
| T-FIX-01 | 输出诊断与证据约束离线修复已验收 | [#11](https://github.com/normaltank/TagProject/issues/11)；下节记录复现、50项本地检查及该轮未运行模型的边界 |
| T-PILOT-03 | 另批10条新版提示运行及教师模型复审已形成交付 | [#12](https://github.com/normaltank/TagProject/issues/12)维护验收与审查状态；10次请求、8条通过校验、2条隔离，详情见下节 |
| T-MODEL、E-01至E-07 | 未运行，保留待续 | [原实验设计](history/EXPERIMENTS_PHASE1_20261023.md)；恢复条件见 PROJECT |

## T-DEV-01：旧16例

来源：teacher_20261022 工作表的 A:O，具体16个行号、原文和哈希见本地 [examples.json](../outputs/teacher_dev_20261023_v0_2/examples.json)及 [manifest](../outputs/teacher_dev_20261023_v0_2/manifest.json)。本轮工作包隔离 S 旧标签，部分材料曾在早期审计上下文暴露，不能称完全盲审。

分母16条：选取34个方向，9条有建议／7条不赋标；20次标签建议（含3次近似范围待审），另5个候选未赋标，40条逐字引文及25个词库位置。长文方向未穷尽。v0.2只补乱码分流短引，v0.1保留；两版均为 Agent 开发材料。

示例生成器只渲染和校验已配置的方向／映射，不能自动识别新简介。原 human_feedback 保持历史状态，未用新教师模型反馈覆盖。

## T-DS-01：工具与连通

本地 [离线／模拟HTTP校验](../outputs/deepseek_20261023_validation_v1/checks.json)32项通过；Git上传准备另验证29项纯合成检查，不依赖工作簿。电话脱敏与空单元格定位的初次失败及修正保留在原目录。

真实外部请求共2次，均单次 HTTP 200、无重试，返回 deepseek-flash，提示 teacher_ds_v1：

| 输入 | 输入／输出 token | HTTP耗时 | 结果与证据 |
| --- | --- | --- | --- |
| 合成30字符简介 | 11645／242 | 1.9611秒 | 1方向、1标签建议；[manifest](../outputs/deepseek_20261023_synthetic_live_v1/manifest.json) |
| 教师表 O10，93字符 | 11675／316 | 2.0658秒 | 3方向、2标签建议、3条引用；[manifest](../outputs/deepseek_20261023_teacher10_live_v1/manifest.json) |

两次费用均为 null，未核对实际账单；耗时不含全部 CLI／工作簿加载。原请求发送完整词库1535个来源引用。原模型结果及[语义提醒](../outputs/deepseek_20261023_validation_v1/review_notes.md)保留，引用与成员合法不证明语义正确。

[教师 dry-run](../outputs/deepseek_20261023_teacher_dry_v1/REVIEW.md)和[合成回放](../outputs/deepseek_20261023_synthetic_replay_v1/REVIEW.md)不增加真实请求数。没有独立质量或经济性结论。

## T-REVIEW-01：旧16例的教师模型反馈

本地 [v0.2审核稿](../outputs/teacher_model_review_20261023_v0_2/REVIEW.md)及 [checks](../outputs/teacher_model_review_20261023_v0_2/checks.json)已验收，v0.1单例校准保留。

审核原34方向、20建议及5候选：20建议中16项保留、4项范围待审（资源与环境化工3、城乡规划1），5候选未晋升，7例原不赋标维持。按新意见是8例有保留建议、1例仅范围待审、7例不赋标；与原9／7的“曾有建议”口径分开。

115项记录／只读核验通过，40条原引文和3条辅助上下文逐字一致，25个词库位置有效。初次记录ID的数字／文本表示差异经统一口径修正，失败诊断保留。辅助书目未外部核实，DS单例对照不计第17位或增加方向分母。

这些计数是模型开发审核，不是准确率、漏标率或独立金标；成本和审核耗时未测。

## T-PREP-02：新20条的先判材料

来源：同一教师表 A:O，不读 S；原19条选择和排除说明在 [v0.1材料包](../outputs/teacher_prejudge_20261023_v0_1/materials.json)，补充第20条在 [选择补充记录](../outputs/teacher_prejudge_20261023_v0_2/selection_addendum.json)。旧16例及已知重复被排除，公式候选因重复排除而缺层。

原“外文正文候选”经语义查看为中文正文＋英文书目；随后在任何 DS 对照前补充真正中英双语正文，原19条未替换。当前20条含17条文本、空／数字／日期各1；没有非英语外文正文覆盖，双语叙述不计独立证据。

指挥端初判已先于新 DS 结果保存：[完整初判](../outputs/teacher_prejudge_20261023_v0_2/first_judgement_N01_N20.frozen.json)、[释义快照](../outputs/teacher_prejudge_20261023_v0_2/working_scopes_N01_N20.frozen.json)及 [关联核验](../outputs/teacher_prejudge_20261023_v0_2/first_20_link_checks.json)。分母20条：41项方向描述、39条建议映射、8条待审／部分映射、5例不赋标；48段引用定位55处。方向可含子题和重叠，映射数不是不同标签总数；同一标签针对不同方向可有不同状态。新增44条工作释义并沿用1条，均非发布者确认的正式定义。

原始初判文件及哈希独立保留。等长 API 副本、17份文本和3条原类型本地路由记录在 [输入索引](../outputs/teacher_prejudge_20261023_v0_2/API_READY_INDEX.json)；[最终派生检查](../outputs/teacher_prejudge_20261023_v0_2/privacy_checks.final.json)通过已列结构及已知回归项。准备阶段当时仍待指挥端逐项核查遮盖边界；后续核查及新发送版本见 T-PILOT-02，不能把此前的程序检查当作完整隐私或语义验收。

此前作者缩写／编号误识别曾遮盖题名和课程词；失败及过渡副本保留。以上为准备阶段记录，后续发送审核、真实调用及复审见 T-PILOT-02；初判未因预测而改写。

## T-PILOT-02：新20条流程诊断

2026-10-26完成 [#3](https://github.com/normaltank/TagProject/issues/3)、[#4](https://github.com/normaltank/TagProject/issues/4) 与 [#5](https://github.com/normaltank/TagProject/issues/5) 的运行及诊断。17份发送副本逐项审核后补遮盖导师、作者等姓名，最终send_v3保留研究正文、题名与55处冻结引文。原冻结副本及过渡版本不改；[发送批准](../outputs/teacher_pilot_20261026_v1/commander/send_approval.json)记录边界与哈希。

17次API请求全部HTTP 200、每文1次、重试0；另3条空／数值／日期在本地分流、网络0。没有未运行案例。模型deepseek-flash、提示teacher_ds_v1、完整1535个词库引用均保持冻结条件。

| 层次与分母 | 结果 |
| --- | --- |
| 17条文本 | 12条通过结构／引文／词库校验（10条建议、2条abstain），5条隔离 |
| 5条隔离 | 重复标签1、词库路径不符2、声明支持不足2；不是空标签拒判 |
| 23项可用方向 | 教师模型保留20项描述、3项收窄；方向合并与子题关系不等于初判41项的逐项对应 |
| 30项标签候选 | 教师模型保留20、范围待审10；原自报supported的21项中3项降待审，原scope_review的9项中2项按较宽关系保留 |
| 实际用量 | 输入217,511／输出10,030 token；输入缓存命中8,704／未命中208,807 |
| HTTP耗时 | 累计64.3161秒，中位3.9524秒，范围1.3403—5.7341秒；不含准备、启动、读表及审核 |

费用、真人审核时间未知，未核对账单。两次本地启动失败均证明发生在API前，网络0：PowerShell参数绑定冲突、从Python启动Windows PowerShell时模块发现路径不兼容。修正的是本地调用入口，原分类代码、提示和词库未改；原失败记录保留。

主要发现：资料不足时可正确拒判；仍会把授课、未说明的方法、AI兴趣与论文题名联想扩大为研究陈述。标签范围需区分无机、杂化和有机材料；部分已有上位标签被漏掉，细名称缺失被过早描述为词库缺口。初判以外也出现有据建议，已逐项回到原文判断。

[完整诊断](../outputs/teacher_pilot_20261026_v1/commander/PILOT_REPORT.md)、[逐项意见](../outputs/teacher_pilot_20261026_v1/commander/DS_REVIEW.md)、[预测冻结](../outputs/teacher_pilot_20261026_v1/commander/predictions.frozen.json)与[用量记录](../outputs/teacher_pilot_20261026_v1/commander/run_statistics.json)均在本地。非法原响应按现有CLI设计不保存，故5条隔离只能核验错误码、哈希及usage，不能追认其中具体标签；已明确诊断限制。

这些是教师模型开发审核，非独立金标或准确率。教师模型与DS可见释义不同，样本选择和缺层限制仍在。优先改善输出契约、证据角色和范围映射，再用另批材料验证；本轮不重试拟合，不启动训练或全量赋标。全部预测及教师复审先冻结，再由 [#9](https://github.com/normaltank/TagProject/issues/9) 完成以下历史BERT对照。

## T-BERT-01：历史BERT标签与首次DS结果

预测及教师模型复审冻结后，读取同20条的S列旧标签；以来源行、教师ID和原件哈希核验关联。旧标签共34项，全部能唯一定位到现有词库L2。新预测的L3候选按原词库路径投影至L2，原候选、自报supported、原待审、教师模型保留和待审五组分别保存；原预测没有被复审结果覆盖。输入隔离、读取顺序和校验见本地[对照验证](../outputs/teacher_pilot_20261026_v1/commander/comparison_validation.json)。

| 案例判断（20条） | 数量 | 含义 |
| --- | --- | --- |
| 新结果更有依据 | 3 | 新增有据的共同层级覆盖，或路径更直接；仍保留该例的待审候选 |
| 旧结果更有依据 | 1 | 旧上位兴趣范围更稳妥，DS部分细化超出当前证据 |
| 两者均有依据 | 6 | 共同范围或不同研究侧面有据；不表示两套全部标签均通过 |
| 暂无法判断 | 10 | 5条DS输出隔离、2条正文不足而拒判、3条非文本；不能据此判历史模型错误 |

旧34项的当前简介审核：17项有依据、5项范围待审、1项当前未见足够依据、11项因输入不足无法核验。此处标签分母与DS的30个细候选不同，不比较两者保留比例。10条有可用标签的材料中，DS提供更细方向和引文，但细化本身不计胜出；共同层级集合相等也不代表细标签正确。

本地交付：[可读对照报告](../outputs/teacher_pilot_20261026_v1/commander/COMPARISON_REPORT.md)、[新旧对照表](../outputs/teacher_pilot_20261026_v1/commander/教师标签新旧对照.xlsx)、[逐项机器记录](../outputs/teacher_pilot_20261026_v1/commander/comparison_approved.json)及[描述性统计](../outputs/teacher_pilot_20261026_v1/commander/comparison_statistics.json)。原表、旧16例、已冻结材料均未改，比较阶段新增API请求0。

交付经两个独立子代理（gpt-6.1-sol／high）完成 Standards 与 Spec 审查，均无可行动发现；实际分工、此前提前关闭任务的纠正和审查范围见本地[流程验收记录](../outputs/teacher_pilot_20261026_v1/commander/WORKFLOW_REVIEW.md)。本批采用逐票 implement 加明确委派。

历史BERT的输入字段、模型配置及训练划分未知，结果只描述当前简介的支持程度；不是同输入模型排名、独立金标或全量准确率。本批不支持直接用DS全量替换BERT：17次请求中5次没有可用输出，剩余候选仍需范围审核。下一步优先处理输出失败可诊断性、输出契约和证据范围，再用另批材料验证；训练本地模型的必要性及费效比仍待这些基线与真实费用数据补齐。

## T-FIX-01：输出失败诊断与证据范围离线修复

2026-10-28按[#11](https://github.com/normaltank/TagProject/issues/11)处理T-PILOT-02暴露的问题。5条历史隔离仅能核验错误码、哈希和usage，原非法响应缺失保持未知；本轮使用纯合成响应复现对应类型，不冒称还原原5条响应，不改变历史分母及首次预测。

最小CLI回放4例先失败，重复与去触发控制确认症状。单变量探针证实：错误产生时缺少字段定位、支持检查只覆盖supported标签路径、审阅稿未呈现安全诊断。修复保留严格隔离和既有错误码，在results与REVIEW显示安全字段位置；v2将支持一致性检查补到方向自身，并在提示中区分兴趣、课程、作品线索、方法依据及范围待审。提示teacher_ds_v2、契约teacher_output_v2、工具0.2.0；旧契约仅显式离线回放，不修改冻结预测。

18项公共CLI回归及50项完整测试通过，含合法／拒判、重复标签、身份／路径、伪造引文、Unicode偏移／非法偏移、弱线索及无标签／待审标签分支。完整检查耗时7.566秒，10次连接均为127.0.0.1模拟服务，外部连接及真实分类API请求0。首次完整检查因清空SystemRoot触发8项Windows SSL环境错误；单独恢复该系统变量后通过，失败证据保留，没有修改分类逻辑规避该环境错误。

证据入口：[最小复现及假设](../outputs/teacher_output_fix_20261028_v1/executor/PHASE1_3_REPORT.md)、[单变量探针](../outputs/teacher_output_fix_20261028_v1/executor/phase4_probes/hypothesis_results.json)、[完整检查](../outputs/teacher_output_fix_20261028_v1/finisher/full_systemroot/summary.json)、[交付与验收](../outputs/teacher_output_fix_20261028_v1/commander/DELIVERY.md)。原执行证据中的H2/H3编号与报告排序相反，交付记录按具名原因对应。两次执行上下文初始化停滞及主Agent接管文档收尾见[恢复记录](../outputs/teacher_output_fix_20261028_v1/commander/RECOVERY.md)，最终独立审查和提交状态见#11。

本轮没有新模型输出；本地约束通过不证明角色声明、自然语言语义、包含关系或新提示实际效果正确。另批验证见下节T-PILOT-03，不能用本轮回归计作准确率或增加独立测试分母。新增论文仅登记为待审稿件来源，未混入教师回放输入。

## T-PILOT-03：新版提示的10条新简介诊断

2026-10-28按[#12](https://github.com/normaltank/TagProject/issues/12)使用teacher_ds_v2、teacher_output_v2、工具0.2.0和deepseek-flash。教师表A:O只读，不读S列；排除旧16例、旧20条及已知原文、规范化原文和主页重复。扫描100,525个物理数据行，100,000条正ID记录中98,863条未删除，92,833条可路由非空文本；20—6,500字符窗口候选76,711条，排重后可选74,443条。固定词法槽位依序选最早未用行，最终10条均有独立来源和哈希；这是诊断选择，不是随机或总体代表样本。规则、各槽位分母和排除证据见[选择冻结](../outputs/teacher_v2_validation_20261028_v1/executor/selection.frozen.json)。

指挥端先于任何本批预测保存[初判](../outputs/teacher_v2_validation_20261028_v1/commander/first_judgement.frozen.json)与[工作释义](../outputs/teacher_v2_validation_20261028_v1/commander/working_scopes.frozen.json)：29项方向、27条映射、25个词库来源引用及29项已定位引文。原文21—5,616字符，发送文本合计15,132字符、等长遮盖419字符；全部初判引文保留原偏移。材料、16次离线预览与最终10份dry_run_v2核查见[准备交付](../outputs/teacher_v2_validation_20261028_v1/preparer/PHASE_A_DELIVERY.md)；最初预览中的重复遮盖检查失败保留，未修改产品或研究原文。主Agent完整检查副本并冻结[发送批准](../outputs/teacher_v2_validation_20261028_v1/commander/send_approval.frozen.json)，API仅收到脱敏简介和完整1535个词库引用。

实际覆盖含短文、长文、跨学科、兴趣及研究活动线索；所谓授课／作品槽位原文另有明确研究陈述，不属于纯课程或孤立单篇作品样例。外文候选为同一简介的中英平行复述，没有独立英语或非英语外文、非文本异常覆盖。1条源单元格末尾已疑似不完整；副本未截断不能证明源简介完整。不补换样拟合结果。

| 层次与分母 | 结果 |
| --- | --- |
| 10条文本、10次真实请求 | 全部HTTP 200，每条一次、重试0、未知0；本地分流0、未运行0，预算余量0 |
| 输出可用性（10条） | 8条通过本地校验，原decision均suggest；2条整条隔离，abstain为0 |
| 2条隔离 | 均insufficient_declared_support；安全位置分别为directions[3].support、directions[2].support，REVIEW与results可追溯；原非法正文未保存，具体语义未知 |
| 可读预测24项方向 | 教师模型保留16、收窄6、另2项归背景；40项引文原偏移均匹配原文，16项证据角色在复审中细化 |
| 可读预测29项标签候选 | 原9项supported保留；原20项scope_review中3项按较宽包含关系保留、16项继续待审、1项改用更直接已有类；另补3项已有映射 |
| 复审建议记录 | 共15条保留映射、16条待审候选；11项gap逐项说明，正式赋标0。均按案例计数，不是不同概念数或准确率 |
| 实际用量（10次） | 输入125,061／输出6,789 token；输入缓存命中6,912／未命中118,149，合计131,850 token |
| HTTP耗时（10次） | 累计38.9819秒，中位4.21545秒，范围1.9480—5.6755秒；不含准备、初始化中断、全部CLI启动和语义复审 |

用量及逐条状态见[运行统计](../outputs/teacher_v2_validation_20261028_v1/run_v1/run_statistics.frozen.json)、[首次预测索引](../outputs/teacher_v2_validation_20261028_v1/run_v1/predictions.frozen.json)及[主Agent调用核验](../outputs/teacher_v2_validation_20261028_v1/commander/run_acceptance_checks.frozen.json)。费用为null，定价未配置且未核对账单；不以token数量冒充实际费用。未知请求及已用额度未补回，旧批次未重试。

逐项意见见[教师模型复审](../outputs/teacher_v2_validation_20261028_v1/commander/DS_REVIEW.md)、[机器记录](../outputs/teacher_v2_validation_20261028_v1/commander/semantic_review.frozen.json)及[定位核查](../outputs/teacher_v2_validation_20261028_v1/commander/semantic_review_checks.frozen.json)。主要问题仍包括：课程或成果数量进入方向列表，教学／项目／作品角色混用，宽领域扩成未写明的方法，省略题名被补出研究任务，以及已有上位类遗漏或误报词库缺口。明确包含关系可承接细方向，不要求研究复合标签的所有分支。16个待审候选继续待审，不把待审本身称错标。两例复审修订了原先保守的初判，接受更充分的区域项目依据及短主题清单语境；初判和首次预测均未改写。新增10条工作范围提案附在复审记录，未获本地发布者核实，正式词库不变。

执行分工及接管见#12和本地[恢复记录](../outputs/teacher_v2_validation_20261028_v1/commander/RECOVERY_03.md)。独立执行子代理完成选材、脱敏、预览、首条调用及续跑脚本；工具切换与初始化停滞后主Agent核实停止并接管剩余九条、统计和文档。指挥端按用户指定负责语义初判／复审；不冒称全程子代理实施。受保护检查原10580项中32项变化均来自旧目录node_modules的Junction，实际指向共享运行库，触发者未知；原失败报告保留，未恢复或覆盖库文件。[分类核查](../outputs/teacher_v2_validation_20261028_v1/run_v1/protection_classification.frozen.json)记录项目材料2052项无变化、本批140份预冻结材料及首条输出无变化；本次职责文档更新前另复核#11归档1204项一致，获准更新文档的历史版本由base提交保留。离线收尾只分类该差异及汇总用量，新增网络0，不能声称原10580项全部不变。

本轮只支持流程诊断：与T-PILOT-02相比样本、提示和契约不同，8/10与12/17是各批校验结果，不能据此推断准确率提高或修复的因果效果。当前审核为教师模型开发意见，非真人意见或独立金标；教师模型可见工作释义，DS只见词库名称／路径。历史BERT输入未知，本批未读取其标签，不作模型胜负结论。后续优先针对仍有隔离、不必要背景方向和已有标签映射问题设计修正与未暴露材料验证；本批不调提示重跑，不启动训练、全量赋标或待审稿件处理。

## 新运行的记录要求

运行前冻结输入／选择范围、词库、初判／审核规则、代码／提示／配置和调用上限。保存不可变版本或哈希；改动上述条件则另开版本并说明可比性。

每次写入新的输出目录，记录成功／拒判／失败／未运行、原始预测、证据、审核差异、实际 token／耗时／费用来源。缺失值记 null，假设算术与实测分开。结束后更新本页对应运行及任务 Issue 的完成证据；STATUS 只保留当前入口。
