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
| T-ROLE-01 | 10条纯合成角色对照运行及教师模型复审已形成交付 | [#14](https://github.com/normaltank/TagProject/issues/14)维护验收与审查状态；5对、10次请求、真实教师0，词法候选与研究标签判断分开，详情见下节 |
| T-LOCAL-01 | 三个本地模型完成共同20条开发材料推理及主Agent核验 | [#15](https://github.com/normaltank/TagProject/issues/15)维护验收与审查状态；encoder NLI、encoder dense embedding、decoder embedding，详情见下节 |
| T-SCALE-01 | 13120输入、轻量头、120例AI初判与后审已实际完成 | [#16](https://github.com/normaltank/TagProject/issues/16)维护最终验收／审查／关闭状态；八路线及1000候选成果，见下节 |
| 旧T-MODEL、E-01至E-07 | 原设计未运行，保留待续 | [原实验设计](history/EXPERIMENTS_PHASE1_20261023.md)；不与本轮T-LOCAL-01混用，恢复条件见 PROJECT |

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

## T-ROLE-01：纯合成证据角色最小对照

2026-10-30按[#14](https://github.com/normaltank/TagProject/issues/14)诊断“领域词不变、角色／归属改变时，当前输出能否区分本人研究与弱线索”。用户本轮继续实验／试运行的授权、单列预算和阶段放行在该任务留证，不恢复旧批次额度。分母为10条纯合成、5对、真实教师0；材料由指定短中文模板组成，未新增真实教师资料、读取原教师行或S列，也不计入此前教师小样分母。

授课、合作者归属、兴趣、孤立代表论文题名、学院导航各1对，使用现有“分离工程”和“历史文献学”控制词；每对各词出现次数相同，但措辞、位置、句长和标点并非完全受控。实际词库核验、原文／UTF-8发送文件、逐词次数、变动点及限制分别见[材料冻结](../outputs/teacher_role_contrast_20261030_v1/executor/materials.frozen.json)、[配对设计](../outputs/teacher_role_contrast_20261030_v1/executor/paired_design.frozen.json)与[目标身份](../outputs/teacher_role_contrast_20261030_v1/executor/target_identity.frozen.json)。两标签只是控制词，不是全库排他答案。

独立执行者先冻结词库、代码／提示／契约／配置、精确词法候选和10份直接Python离线预览；主Agent在本批预测前独立保存[初判](../outputs/teacher_role_contrast_20261030_v1/commander/first_judgement.frozen.json)与[工作释义](../outputs/teacher_role_contrast_20261030_v1/commander/working_scopes.frozen.json)，核对完整发送副本后冻结[发送批准](../outputs/teacher_role_contrast_20261030_v1/commander/send_approval.frozen.json)。发送用户消息仅intro和完整1535个合法词库引用，无期待、配对条件或本地case ID。teacher_ds_v2／teacher_output_v2／工具0.2.0及deepseek-flash不变；每次max_tokens=2048、timeout=60秒、max_retries=0，其余产品默认配置不变。准备证据及哈希见[Phase A交付](../outputs/teacher_role_contrast_20261030_v1/executor/PHASE_A_DELIVERY.md)和[预览索引](../outputs/teacher_role_contrast_20261030_v1/executor/dry_run_index.frozen.json)。

唯一串行dispatch按R01→R10运行，dispatch／case／launch均先留独占持久化记录，再进入既有凭证入口；不自动续调或重发。10次请求全部HTTP 200、每条一次、重试0、未知0、未运行0、预算余量0。10条均通过结构／引文／词库校验，原decision为8条suggest、1条needs_review、1条abstain，隔离0。原始payload、逐条actual attempts和usage保留在[首次预测索引](../outputs/teacher_role_contrast_20261030_v1/run_v1/predictions.frozen.json)及[Phase B完整结果入口](../outputs/teacher_role_contrast_20261030_v1/run_v1/PHASE_B_DELIVERY.md)，校验通过不等于语义正确。

主Agent完整复审11项方向、11条逐字引文、9条标签候选和0项gap：保留8项支持研究方向，1项兴趣弱线索继续待审，2项教学归为背景；保留8条支持标签建议和1条待审候选，正式赋标0。教学两项原本已为weak／teaching且没有研究标签，问题是仍列在directions，不记作2个错标。R05／R07的explicit_direction与初判偏好的research_activity均可表达直接研究自述，接受这2项强角色子类差异，初判保持不变。逐项意见及原文回切核验见[教师模型复审](../outputs/teacher_role_contrast_20261030_v1/commander/DS_REVIEW.md)、[机器记录](../outputs/teacher_role_contrast_20261030_v1/commander/semantic_review.frozen.json)和[复审核查](../outputs/teacher_role_contrast_20261030_v1/commander/semantic_review_checks.frozen.json)。

五对的目标支持状态在本组合中符合先判期待：研究／授课、本人／合作者及研究／导航交换时，支持标签跟随本人研究；兴趣保留weak与scope_review，孤立论文题名abstain。8条支持建议均为现有同名L3，L2回退0，因此没有检验歧义范围或已有上位类映射能力；教学背景仍进方向列表的发现，说明方向清理与标签映射要分别核查。这些是教师模型开发判断，不是独立真人答案。

[精确词法基线](../outputs/teacher_role_contrast_20261030_v1/executor/lexical_candidates.frozen.json)逐条遍历全部1535个合法引用，按末级名称精确子串匹配，保留同名多位置、全部命中与Unicode区间，不做Top-K或自动supported。共16次候选命中，其中8次对应初判的研究陈述、8次来自弱线索或背景；后8次不是分类器假阳性统计。它完成的是候选任务，不与DS最终研究判断作同任务胜负，也未测试encoder或embedding，不能据此排除这些路线。

实测输入118,871／输出1,779 token，合计120,650；输入缓存命中7,680／未命中111,191。HTTP attempts累计18.2817秒；分类elapsed累计18.4725秒，含局部准备与校验开销，两者均不含全部启动、材料准备和审核投入。费用为null，未配置单价、未核对账单；逐例用量和发送一致性见[运行统计](../outputs/teacher_role_contrast_20261030_v1/run_v1/run_statistics.frozen.json)、[操作核验](../outputs/teacher_role_contrast_20261030_v1/run_v1/phase_b_operation_checks.frozen.json)及上述复审核查，不能以token或分类计时冒充全流程成本。

现有PS默认内置Python实际3.12.14，系统默认python为3.12.10；准备helper在首条离线预览后因旧版本断言中断，初版代码／预览和[中断记录](../outputs/teacher_role_contrast_20261030_v1/executor/phase_a_preparation_interruption.frozen.json)保留，续准备仍用同一3.12.14完成另九份，未发生API重试。未安装、下载模型或训练。原始XLSX、旧16例及旧冻结研究载荷只读，保护核验排除本批目录、运行库缓存和获准更新的EXPERIMENTS／STATUS；本批初判／发送／首次预测／复审保持冻结，两份职责文档旧版由base提交保留。检查范围见[准备保护记录](../outputs/teacher_role_contrast_20261030_v1/executor/protection_checks.frozen.json)和上述操作核验，不能把历史清单连同获准更新文档宣称为全部字节不变。

本轮仅支持明确短中文模板中的角色诊断，没有真实混合语境、长简介、多语、长尾概念或独立质量验证覆盖，不能外推真实教师准确率、统计显著性、全量表现或最终架构。deepseek-flash仅为本次请求／返回标识，托管后端权重revision未核实；本轮不是与旧批同输入／同权重的改进实验。下一步优先设计未暴露真实混合语境材料，继续检查角色归属和方向列表背景清理；三路线仍保留独立竞争，不根据本轮合成表现选型。产品／提示／契约／词库未改，本轮不补调拟合结果；新任务仍须明确输入版本、评价和资源边界。

## T-LOCAL-01：三个本地模型的共同开发材料试跑

2026-10-31按[#15](https://github.com/normaltank/TagProject/issues/15)实际运行mDeBERTa-NLI、BGE-M3 dense和Qwen3-Embedding-0.6B，非历史BERT复现或教师监督头训练。模型任务、固定官方revision及方法依据见[研究记录](RESEARCH_AND_DECISIONS.md#2026-10-31本地试跑的方法依据)。本轮3/3模型完成全部输入，无推理失败、OOM或重跑调参；正式赋标0、训练0、新付费推理API调用0。

共同20条为#14的10条纯合成及#12已批准、实际发送过的10条脱敏真实开发文本；真实文本共15132 Unicode码点，含原隔离的V02/V09，不重新读取原教师行或S列。逐条请求／批准／首次预测索引和hash核对后冻结[数据及引用](../outputs/model_pilot_20261031_v1/executor/dataset.frozen.json)，不是新增20条独立材料。200码点窗口、40重叠产生107公共片段，保留原发送文本[start,end)并全覆盖；含假设／指令的实际最大输入长度NLI160、BGE134、Qwen190 tokens，均不超过512，无静默截断。协议及首次推理前冻结hash见[配置](../outputs/model_pilot_20261031_v1/executor/config.frozen.json)、[长度检查](../outputs/model_pilot_20261031_v1/executor/token_lengths.frozen.json)和[输入绑定](../outputs/model_pilot_20261031_v1/executor/inference_inputs.frozen.json)。

两种embedding对全部1535合法引用精确评分，无Top-K预筛或DeepSeek接续；NLI独立评分全部139 L2，另加两个合成L3目标。三者共同139 L2直接排名，各标签取公共片段max并保留winner偏移。真实参考来自#12既有教师模型复审：15条保留映射投影、按case+L2去重为11对／8案例；其中细粒度参考另为11个case+L3对／5案例。16条待审不当负例，V02/V09无保留参考，仅不计覆盖分母，仍完整推理。合成参考为既有初判及复审保留的8个本人研究目标，兴趣待审与代表作拒判分开。所有参考均是已暴露开发材料上的AI意见，不是独立金标。

共同139 L2的known-positive reference coverage@1／5／10如下，数字是命中数，分别除以各组固定分母；不是准确率或precision，未判断候选不计假阳性：

- mDeBERTa-NLI：真实2／3／4（分母11对、8案例）；合成0／1／3（分母8对、8案例）。
- BGE-M3：真实4／6／7（分母11对、8案例）；合成0／5／5（分母8对、8案例）。
- Qwen3-Embedding：真实5／8／10（分母11对、8案例）；合成0／3／8（分母8对、8案例）。

完整1535排名中的已保留L3参考覆盖@1／5／10：BGE真实3／4／5、Qwen真实2／6／8，分母均11条L3／5案例；BGE合成5／8／8、Qwen合成8／8／8，分母均8条L3／8案例。NLI只测两个诊断L3，不参加全细粒度覆盖比较。合成L2 top1均为0，不代表同名细标签未被找回；共同L2与完整排名的L3分母、任务不能混用。逐案例分数、排名与分母见[机器汇总](../outputs/model_pilot_20261031_v1/executor/summary.json)。

主Agent重读10条合成并核对原始数组：R02“主讲分离工程课程。研究方向：历史文献学。”中，NLI授课目标X entailment=0.9963、研究目标Y=0.0029，临时0.5规则会错授X并漏Y；这是该模板与现成NLI头的反例，不是监督encoder路线的一般结论。BGE/Qwen均把R06兴趣X及R08孤立论文题名X排完整1535的第1名；本轮embedding无正式赋标阈值，不能把这些高排名计作已经赋出的无据标签。Qwen在部分研究／背景交换中能把本人研究目标置顶，但未解决全部角色判别。真实V05/V07/V08的winner抽查显示优势并非逐条一致，教育／访问经历段也可能胜出；召回已保留标签不自动验证winner角色或完整证据。逐目标数值及主Agent意见见[角色目标](../outputs/model_pilot_20261031_v1/executor/role_targets.csv)与[结果核验](../outputs/model_pilot_20261031_v1/commander/RESULT_REVIEW.md)。

实际环境Python3.12.10、PyTorch2.11.0+cu128、Transformers4.57.6，RTX4060 Laptop GPU（8188MiB），FP32、batch8、逐模型加载释放。评分墙钟NLI131.656秒、BGE14.156秒、Qwen25.265秒，合计171.077秒；该计时含分词、评分与聚合，不是纯GPU内核时间，也不含下载安装、材料准备及审核。加载加评分合计178.296秒，低于90分钟推理预算。forward序列数分别15087／1642／1642，任务工作量不同。PyTorch峰值allocated分别1.199／2.173／2.310GiB，reserved为1.309／2.230／2.365GiB，非整台GPU总占用。环境、执行脚本SHA及原始分数见[环境记录](../outputs/model_pilot_20261031_v1/executor/environment.frozen.json)、[NLI运行](../outputs/model_pilot_20261031_v1/runs/nli/run.json)、[BGE运行](../outputs/model_pilot_20261031_v1/runs/bge/run.json)与[Qwen运行](../outputs/model_pilot_20261031_v1/runs/qwen/run.json)；各运行同目录保留首次成功scores.npz／scores.csv和脚本副本。

公开依赖及权重仅在新runtime安装／下载，BGE官方bin的安全权重加载例外在#15留证，其余取safetensors，权重SHA均匹配官方固定revision。首次PyTorch下载超时，第二次停顿后保留前缀续传并按官方SHA核对；Qwen首次传输少尾段，补齐后SHA通过；一个重复BGE下载被停止，其未完成前缀计入投入。最终必要模型文件3.799GiB；没有网络流量计量器，按首次失败完整wheel上界、已知文件、重复前缀及小依赖／metadata余量估算累计下载上界9.263GiB，低于10GiB，不能称精确实测流量。日志、估算口径和失败详情见[投入与检查](../outputs/model_pilot_20261031_v1/executor/resources_and_checks.json)及[执行记录](../outputs/model_pilot_20261031_v1/executor/RESULTS.md)。没有安装全局库或修改驱动，未重发DeepSeek；总准备、审核人时和能耗未计量，不能用评分墙钟冒充全流程成本。

主Agent独立重算输入与参考、max／winner、三类概率和、归一化向量点积及全部覆盖算术，通过[输入核验](../outputs/model_pilot_20261031_v1/commander/input_checks.json)和[结果核验](../outputs/model_pilot_20261031_v1/commander/results_checks.json)。执行者对三份原始XLSX及实际读取的旧冻结源文件做前后hash，31项一致，runtime未纳入保护扫描；入口为[保护前](../outputs/model_pilot_20261031_v1/executor/protected.before.json)及[保护后](../outputs/model_pilot_20261031_v1/executor/protected.after.json)。产品、提示、正式词库及旧预测不变，脚本、原始分数与逐条文本仅留本地新版本目录。

本批开发参考中Qwen候选覆盖值得继续验证，BGE保留为较低评分耗时的比较；现成NLI模板暂不适合直接赋标。训练任务、模板／池化不同，旧DeepSeek后端revision／任务条件及历史BERT输入未知，不作架构因果胜负。max chunk有长文偏差及跨段归属限制，未审全部候选的证据角色。下一步先用未暴露真实混合语境材料核候选覆盖、可接受赋标及复核投入，盘点可信监督样本，再决定encoder分类头训练可行性；不预设embedding后必须接DeepSeek，不据本轮扩大赋标或认定监督分类无效。任务验收、独立双轴审查、归档及最终状态以#15为准。

## T-SCALE-01：扩大真实材料与冻结表示弱监督头

2026-10-31按[#16](https://github.com/normaltank/TagProject/issues/16)实际使用13120条教师输入：120新评价（20校准／100保留）、10000弱训练、2000弱验证、1000吞吐；不是13120条质量核验。教师源与可选池口径、当前稿件表的结构汇总见[DATA_AUDIT](DATA_AUDIT.md#2026-10-31扩大教师实验的输入池)；该表不代表其他目录或项目外论文存量，未做有效稿件质量审核。本轮稿件未分类或进入教师训练。五个评价层各24例，校准各4、保留各20；Latin-heavy及角色混合为脚本／词法proxy，未据此认定实际语言或本人研究。各集合和旧暴露材料按重复／主页连通组互斥，近重复及真实同人异页未穷尽。

全部简介仅用O字段的既有方法等长遮盖副本，身份／系统独立列不作特征；正文仍有转写姓名、特殊邮箱和履历线索残留，也有遮盖触及研究词的观察，限制身份无关泛化。固定输入未为此重跑，未送远程API。共同200码点窗口、40重叠产生108083片段，共16590801码点；120评价为735片段，无截断。词库139 L2／1535引用、模型revision／池化／指令沿用#15，方法补充见[研究记录](RESEARCH_AND_DECISIONS.md#同日扩大实验的方法补充)。输入与协议见本地[阶段A](../outputs/scale_benchmark_20261031_v1/executor/STAGE_A.md)。

### 先判、监督与训练

主Agent在新标签评分和评价旧S之前冻结120例方向、引文与映射；这是AI开发参考，不是真人／独立金标。校准20有17例确认L2、29个case-L2对，L3为14例／33对；保留100有83例确认L2、192对，L3为66例／149对，另11拒判、6待审。未列出的标签不是负例，初判在后审中保持不变。[冻结初判](../outputs/scale_benchmark_20261031_v1/commander/prejudge.frozen.json)。

先判冻结后仅解码训练／弱验证S。固定10000／2000行全部有效，分别17966／3626个正case-L2对，训练覆盖139类、弱验证136类；17训练类只有1–9例。缺失／不可解析／未知标签行原定保留输入但mask掉梯度或弱val loss，本批未命中。未赋标签当0只是弱训练假设，未核查所有负赋值，不等于不存在研究方向。

两个头使用归一化chunk向量的均值再L2归一化、Linear(1024,139)、unweighted BCEWithLogits、AdamW(lr=.001,weight_decay=.01)、batch256、seed20261031，主干始终冻结。v1固定20epoch与首次分数保留；在仅弱val曲线仍下降、尚未读保留质量时，对两者对称追加预先冻结的v2：max500、无改善50轮停，仅弱val最低BCE选代表。两v2均选epoch382、在432停，首20曲线与相应v1完全一致，校准前绑定，未以保留100选版本。

- BGE v1／v2弱val BCE .06009233／.02973500；Qwen .05409424／.02625060。训练类先验常数的弱val BCE .06211153仅为优化诊断。
- v2固定sigmoid .5的弱标签拟合micro／macro F1：BGE .4997／.3248，Qwen .5810／.4544；这些不是研究质量，.5也不是最终试探工作点。
- v1 CPU墙钟5.672／4.563秒，v2 48.015／44.563秒；额外v2合92.578秒<600秒。完整曲线、参数、实际监督分母与[代表选择](../outputs/scale_benchmark_20261031_v1/executor/head_representatives.frozen.json)保持可回溯。

### 八路线与覆盖

词法为char2–4gram TF-IDF，fit仅用10000训练全文+1535引用、最多200000特征；NLI独立判139 L2。BGE／Qwen分别比较直接L2、同来源路径L2+L3的max投影、冻结表示轻量头，共八路线。检索仍maxchunk，层级投影保留child和winner，不表示细标签已成立；头的全篇均值表示没有自主证据定位。这些整条路线同时改变聚合及任务目标，不作主干架构因果排名。

下列L2命中为保留100中192个已知case-L2对的@1／5／10；macro@10是在83个有参考case上平均。末尾S／N／U为每路线100个top1的主Agent后审支持／当前无据／不确定，另一分母，不是真实precision或准确率。

- TF-IDF树：57／130／149，macro@10 78.71%；S/N/U 63／29／8。
- NLI直接：34／77／97，macro@10 52.91%；39／52／9。
- BGE直接：44／88／118，macro@10 64.46%；51／43／6。
- BGE树：49／112／134，macro@10 71.89%；55／38／7。
- Qwen直接：48／126／154，macro@10 83.73%；54／28／18。
- Qwen树：60／146／171，macro@10 91.27%；63／25／12。
- BGE头：63／138／166，macro@10 88.45%；68／17／15。
- Qwen头：64／147／169，macro@10 90.56%；68／14／18。

完整1535排名内的L3参考覆盖另用149对／66例：词法18／46／60，BGE8／26／39，Qwen21／54／79。头与NLI未输出完整L3排名。校准、保留及每层的micro／macro @1/5/10、无参考和资料不足分母均在[覆盖结果](../outputs/scale_benchmark_20261031_v1/executor/reference_coverage.frozen.json)，不把初判缺漏当模型错标。

### 匿名后审、固定工作点与信号审计

校准20的top1并集75项先去系统／分数／名次／提名数后审，27支持／39无据／9不确定。只用这些意见及各路线校准top1唯一分数选保留最多、至少5例且支持占保留≥90%的点，不确定不计支持。唯一可行点为BGE代表头score≥.8660585880279541，校准留6且6支持；其余七条无可用点。[工作点](../outputs/scale_benchmark_20261031_v1/executor/working_points.frozen.json)于12:10:22Z冻结后，才计算保留质量和读取评价S。

固定BGE点在保留100留28、拒72，28中23支持／2无据／3不确定，支持占保留82.14%，未维持90%设计目标。2000次五层各20组、共享配对索引、seed20261031的percentile区间：保留比例95%CI [19%,37%]，条件支持[66.67%,95.65%]；无保留路线条件比例为null，空保留重抽样也按未定义处理。分层组bootstrap只描述本平衡开发批次及AI意见的不确定性，不外推总体真实精度。

两个头对对应直接L2的top1支持占比增加17／14个百分点，配对95%CI分别[7,28]／[6,23]点；两头差0点CI[-5,5]，Qwen树减Qwen头差-5点CI[-13,2]。Qwen树@10比Qwen头多2/192，micro差CI[-.0383,.0594]，不能按微小点差认定唯一赢家。完整分层、拒判、配对结果见[最终统计](../outputs/scale_benchmark_20261031_v1/executor/final_statistics.frozen.json)及[比较图PNG](../outputs/scale_benchmark_20261031_v1/executor/comparison.png)／[SVG](../outputs/scale_benchmark_20261031_v1/executor/comparison.svg)。

保留100的八路top1和全部旧S并集452项，后审为193支持／189当前无据／70不确定；其中145复用同case已冻结确认positive，另外307逐项按全文／路径审核。校准S补充12项为5／3／4（2复用、10逐项），先前75项不改。已审的相同case-L2复用原结论，不因未列出就判负。

评价旧S仅在全部首次预测和工作点冻结后读取，120行216个case-L2对全部进入去来源审计：142支持／36当前无据／38不确定；校准32为22／5／5，保留184为120／31／33。历史BERT的输入与时间快照未知，这是当前遮盖文本对弱监督目标的支持程度，不是历史BERT错误率或同输入模型比较；也未审核全部未赋标签的负假设。评价反馈没有回流训练、epoch、阈值，吞吐S未读。

代表性边界包括：E026的机构／导航主题、E081的学部任职仍被高分头提名，当前无本人研究依据；E049的教学平台与方法研究边界、E083／E104的概念包含继续不确定。初判外也有有效补充，如E033的连续认知发展研究支持心理学、E050的城乡空间研究支持地理学上位映射，E085的海岸动力泥沙支持已有水利／海洋路径。它们是主Agent逐项开发意见，未改初判、词库或工作点，原文及理由只留本地。

### 成本、成果与当前选择

BGE／Qwen各实际编码13120输入及1535引用、109618序列；编码墙钟2184.594／4747.796秒，load2.562／1.954秒。两者保存(108083,1024)chunk、(1535,1024)label、(13120,1024)case向量和offset。NLI实际102165对，推理946.047秒、load1秒；工作量与两embedding不同。三模型FP32／batch8逐个GPU加载，最大tokens分别NLI225、BGE206、Qwen272，均≤512无截断。GPU加载加执行墙钟共7883.953秒=2.189987小时<4小时，非纯kernel或全流程人时；峰值allocated NLI1.269／BGE2.198／Qwen2.350GiB。TF-IDF fit与评分保存合31.829秒；轻量头的廉价增量仍以已有表示编码成本为前提。

复用#15权重，新模型下载及付费推理API均0，模型运行失败0。小依赖归档43.646MiB，加10MiB metadata余量按53.646MiB核预算，非实测网络流量；产物约1.34GiB<8GiB。三原XLSX及实际读取旧源9项hash保持，未遍历venv或重hash4GB权重；输入、首预测、代表头、先判、工作点及全部后审SHA绑定。统计导出另有两次辅助中断，诊断保留本地，修复未重跑模型或改分数；主Agent已独立核原分数、窗口、全部点估计及冻结索引下的配对区间。

实际成果为[1000输入／7000未审候选JSONL](../outputs/scale_benchmark_20261031_v1/executor/throughput1000_candidates.jsonl)、[BGE头checkpoint](../outputs/scale_benchmark_20261031_v1/models/bge_linear_head_v2.pt)、[Qwen头checkpoint](../outputs/scale_benchmark_20261031_v1/models/qwen_linear_head_v2.pt)和[短复跑入口](../outputs/scale_benchmark_20261031_v1/executor/RUN_LOCAL.ps1)。JSONL保留原生待核窗口及头无自主定位限制，全部未正式赋标；285例仅在固定BGE点上数学通过，未作语义审核。入口默认dry-run，使用全新版本、现有权重与冻结材料，不重读S、不覆盖旧输出；本轮只验证dry-run，未重复跑模型。

**当前建议按用途分别选用候选工具并复核原文。** L2候选兼顾编码成本时选BGE轻量头：本批top1支持与Qwen头相同，表示编码成本更低；优先top10覆盖和细方向时选Qwen层级检索，词法保留为便宜基线。本轮未验证两者串联或合并的额外收益。现成NLI配置不作为默认自动赋标。两个头的本批收益值得保留，但固定点未达到保留批90%支持目标，头也没有原生证据定位，不将其投为全库自动通过门槛。

**当前不扩大主干微调／LoRA。** 先利用已发现的角色与包含边界整理监督，区分本人研究、教学／任职、题名／兴趣及范围待审，处理长尾和未标作0的假设，再按新的分组评价验证训练收益。旧S有74/216项未获当前文本确认，继续增加同来源标签不能自动解决目标错配。这里不否定后续主干训练，也不要求当前用户逐条真人复核；正式独立精度仍需另设答案与验证。当前AI参考、平衡分层、小规模校准、脚本proxy、残留身份、近重复和跨段归属限制，使结论适用于本轮工具取舍，不能宣称全库或架构冠军。

本地[完整成果报告](../outputs/scale_benchmark_20261031_v1/executor/RESULTS.md)集中可复用入口与解释；最终提交、逐AC验收、双轴审查和关闭状态以#16为准。

## 新运行的记录要求

运行前冻结输入／选择范围、词库、初判／审核规则、代码／提示／配置和调用上限。保存不可变版本或哈希；改动上述条件则另开版本并说明可比性。

每次写入新的输出目录，记录成功／拒判／失败／未运行、原始预测、证据、审核差异、实际 token／耗时／费用来源。缺失值记 null，假设算术与实测分开。结束后更新本页对应运行及任务 Issue 的完成证据；STATUS 只保留当前入口。
