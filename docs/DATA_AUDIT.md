# 数据审计（公开仓库整理版）

审计日期：2026-10-23（Asia/Singapore）。本页保留汇总口径和复核结论，不包含真实教师内部ID、姓名／联系方式或原始简介摘录。修改前完整文档在本地忽略目录`outputs/git_upload_prepare_20261023_v1/private_before_upload/docs/DATA_AUDIT.md`；原始XLSX、逐行审计和16例均未改写或上传。

## 输入与可复核性

教师审计基线的两份本地文件为`Sheets/teacher_20261022.xlsx`（108968834字节）和`Sheets/review_tagscollection_20261022.xlsx`（30080字节）。原件SHA-256：

- 教师：`fbdac1e9f1464ac32b4d2e9ea87831c3fe3023a0c48f73b731cf17d0b00b376d`。
- 词库：`8e130842d70a8418b538caa10097f7595817ac45fde01dcc58d67726b58eb08f`。

主审计`audit_inputs.py` v1.1.0使用Python 3.12.14、openpyxl 3.1.5，只读、data_only=False，不计算或保存工作簿。原本地输出`outputs/audit_20261023_v1_1_0_run1/`含manifest、脚本快照、summary和定位CSV；独立标准库XML核验在`outputs/audit_20261023_checks_v1/verification_v2.json`为23/23。原verification.json为22/23的失败诊断，保留未覆盖。新克隆不带这些本地证据文件。

初次差异来自日期／公式读取表示，统一解码口径后通过，不是放宽容差。deleted=0简介解码字符数115058149，词法XML口径115057748，差401；由28项日期和3项公式的表示差异解释。原件哈希不变。审计及 XML 脚本复跑方法见本页末节。

## 教师口径与缺失

原sheet为`teacher_20261022`，声明100526行×21列（含表头）。严格非None／非空字符串为100399个非空数据行，逐单元格strip后100398；一条仅空白行造成差异，不能据此改变教师分母。

主分析保留ASCII正整数且唯一的记录ID：100000条／100000唯一，重复0。该语法条件不证明字段结构完整或简介有效；398个trim后非记录候选及127个空行留在原表，未自动拼接或删除。

- 全100000条：简介缺失5948、旧标签缺失19；99981个非空字符串数组，177991次旧赋值、139个唯一字符串，JSON解析错误0。
- deleted=0共98863条：简介缺失5909、标签缺失19，175923次旧赋值。
- deleted=1共1137条：简介缺失39、标签缺失0，2068次旧赋值。

字段deleted的业务含义待字典确认，98863不等于可用教师数。全部5948条空简介都有旧标签，但不能据此认定旧标签正确或补写方向。交接的缺失数来自包含非记录行的另一分母，不能混用。

## 数据质量与解释边界

- 19条简介恰为32767字符，均在deleted=0，伴随尾列缺失和相邻残片，支持导出／结构损坏假设，原因未确认。另有8000字符堆积432条，仅为疑似来源限制线索，不证明截断。
- 精确重复非空简介869组／5222行，重复主页475组／1539行；可能是采集、模板或同页线索，不能自动合并教师。
- HTML样式152条、Unicode替换符58条、短于100字符28103条，均为诊断信号，不是最终无效判定。
- 简介类型：字符串94006、None5948、整数18、日期28；非空字符串化94052不能称有效研究简介数。46个非字符串与另3个公式候选需分流；原始公式和缓存仅在本地记录，不执行。
- 有效记录主页缺失1340、title缺失7296、collect_date缺失12342、collector缺失19133、is_interdisciplinary缺失916。记录时间不等于研究事实时间。

教师列为A=id、B=name、C=email、D=send_count、E=last_send_at、F=department_id、G=collect_date、H=collector、I=title、J=last_export_date、K=created、L=deleted、M=modified、N=homepage、O=intro、P=external_userid、Q=aminer_synced、R=enrichment_status、S=tags、T=wecom_added、U=is_interdisciplinary。方向识别主要用O，S仅作有来源的历史线索；联系方式和系统状态不作为专长证据。

## 词库与历史标签

词库sheet为`review_tagscollection_20261022`，140行×7列含表头，139个来源ID唯一、deleted均0。A=id、B=created、C=modified、D=deleted、E=primary_tag、F=secondary_tag、G=family_tag，按来源G→E→F的JSON数组解释层级。

共有35个一级名称、139个二级、1396个三级出现位置／1384个三级字符串。12组三级名称各出现两次，是否同义、异义或多归属待定义，不按同名自动合并。19个二级无三级，说明来源粒度不齐，不能凭空补齐。来源ID只标整行，数组下标标出现位置，均未升级为正式概念ID；没有完整范围定义或多语言别名。

来源补充（2026-10-26）：用户确认交付教师表的旧tag由BERT方案生成；用户暂不清楚当时只用简介还是还用了其他资料。这是用户提供的来源说明，本轮未重跑或复现旧模型。具体模型／版本、输入字段与时间快照、训练样本及划分、阈值／后处理、是否有人修订和历史耗时／成本均未核实；未发现可审查的历史BERT代码／训练记录。

旧标签主要落于较粗层级，可作为已有BERT方案的历史赋标结果对照，不能未经核验充当细粒度金标、独立测试答案或唯一成功指标。原表5948条空简介均有旧标签，不足以证明BERT无依据赋标：历史输入或导出时点可能不同，原因仍未知。当前可先审核历史标签对现有简介的支持程度；在输入未核实时，不能把这种审核称为同输入条件下的BERT与DeepSeek性能比较。独立人工答案仍缺失；2026-10-28新增的待审稿件来源另列如下。

## 新增待审稿件：结构初检

用户2026-10-28确认`Sheets/ex_paper_snapshot_20261027.xlsx`为待审稿件并授权使用，目的为后续稿件打标与师稿领域匹配。文件895579字节，SHA-256为`30f16ea8a5a29ffcbc31bb1495388150cf0b527a226fa7cd55c11e24b386ba99`，保持只读且不纳入Git。

2026-10-28只读初检一个sheet `ex_paper_snapshot_20261027`，声明1001行×23列；字段含`id`、`paper_id`、`title`、`abstract`、`keywords`、现有标签及文件链接／流程状态。2026-10-31按[#16](https://github.com/normaltank/TagProject/issues/16)仅核id／paper_id／title／abstract／keywords，实际1000条所选字段非空数据行，id、paper_id、title缺失0，abstract缺22、keywords缺41；id与paper_id重复0，非空title／abstract／keywords各1组2行，title+abstract+keywords完全相同1组。证据见本地[稿件结构汇总](../outputs/scale_benchmark_20261031_v1/executor/paper_summary.frozen.json)。这是当前稿件表1000记录的结构汇总，不代表其他目录／项目外全部论文存量，也未做有效稿件质量审核；未读取标签值、分类、访问链接或核对正文文件。

这些稿件无需归属到某位教师才能做领域匹配。本次教师输出修复未将稿件、稿件旧标签或摘要混入冻结简介输入；稿件分类与匹配的输入版本、隐私和验收另记任务。

## 2026-10-31：扩大教师实验的输入池

[#16](https://github.com/normaltank/TagProject/issues/16)只读重用原教师表A:O及既有审计口径：仍为100000条唯一正ID记录，原类型／缺失分母未变。按顺序互斥排除来源分流6090条、deleted非0/未知或20–11999码点边界之外14843条、前两类之后的旧暴露组35条，得79032行／77095组可选池。该条件只表示可进入本实验，不证明是有效研究简介；[池汇总](../outputs/scale_benchmark_20261031_v1/executor/pool_summary.frozen.json)保留逐种原因、长度边界与分母。

全100000行按原文精确hash、NFKC／casefold／去空白的原文及模型输入hash、同规范化非空主页作连通分组，共94081组，1437个多行组含7356行。旧16+20+#12的10条共46来源行，关联46组／48行；本轮全部划分与它们组互斥。未建立近重复平台，语义改写、主页别名及真实同人异页仍可能漏连；组不是已经确认的真实人物身份。

选样不看S，以seed20261031固定组和代表行；评价材料先独占Latin-heavy、角色混合词法层，再按长度分短／中／长。Latin脚本比例不是实际语言，角色标记也不是本人研究判定。完整输入与120条主Agent AI初判、弱训练／验证、吞吐的划分及实测统一见[扩大实验](EXPERIMENTS.md#t-scale-01扩大真实材料与冻结表示弱监督头)，不把13120个模型输入说成13120条质量核验。

姓名／邮箱等独立列只作溯源和等长遮盖，不作为独立特征。正文仍发现英文姓名转写、分隔空格邮箱及机构／履历线索残留，也有遮盖触及邻近研究词；因此称“既有方法等长遮盖副本”，仅本地处理，不能宣称彻底匿名或未经新内容核查直接送远程API。观察记录与冻结输入均保留，未为此改写原件或重跑。

S在120先判冻结后仅为固定训练／弱验证读取；评价S在全部首预测和校准工作点冻结后才另读作当前文本支持审计，吞吐S未读。未赋标签当0只是弱训练假设，不是真负例；旧S来源条件仍按上节保留未知。本轮原三份XLSX与实际旧冻结源的必要前后hash一致，证据见[阶段B保护](../outputs/scale_benchmark_20261031_v1/executor/stage_b_protected.after.json)。

## 2026-11-01：证据判别的新材料与旧AI监督

[#17](https://github.com/normaltank/TagProject/issues/17)复用#16全100000记录的连通组索引；原文／canonical输入／非空主页口径不变。排除#16全部13120输入组及此前46暴露组，合13166组关联13650源行，再按来源分流、deleted和20–2999码点资源边界筛选，剩57342行／55805组。该边界是本地完整生成的资源范围，不证明简介有效；互斥排除顺序与#16不同，不能直接相减其瀑布计数。近重复、主页别名及真实同人异页仍未穷尽。

新100以seed20261101固定组和代表行，命名J001–J100以区别旧E编号；五个既有脚本／词法proxy各20，cal20每层4、held80每层16。完整等长遮盖输入共84070码点／559个200码点窗口、40重叠，实际长度20–2977，未截断。原表仅A:O供准备，**新S不读取或用于选样、训练、校准及评价**；完整原文、遮盖与Unicode区间的私有映射在本地。分组、来源、排除与输入hash见[阶段A](../outputs/evidence_judge_20261101_v1/executor/STAGE_A.md)及[准备核对](../outputs/evidence_judge_20261101_v1/executor/preparation_checks.frozen.json)。

支持判别监督仅从#16七份不可变主Agent AI审核派生539个唯一case-L2：225支持、231当前无据、83不确定。旧120组按五层各18/6固定90训练／30验证，新cal／held与二者组交集均0。训练178S/160N/61U、验证47S/71N/22U，仅338／118个S/N pair进入损失；不确定及未审pair不作负例。N只指当前固定输入无据，不是现实领域负标签，也不是真人金标。该监督受旧候选池、同一AI意见来源及范围边界影响。

训练只有68/139类有正例、94类有任一S/N监督，71类无正例；这表示覆盖不足，不表示这些类无效。旧验证33类有正例、64类有任一监督，14个验证pair的标签未见训练监督、8个正pair标签没有训练正例。NLI共享三类任务头，不能将这些计数当139个独立可靠分类器的覆盖。逐类计数见本地[监督覆盖](../outputs/evidence_judge_20261101_v1/executor/supervision_longtail.frozen.json)。原三XLSX及实际复用旧源的显式32项前后hash一致，不遍历旧runtime／大权重；核对见[最终保护](../outputs/evidence_judge_20261101_v1/executor/protected_final.after.json)。新材料质量与工具结果在[EXPERIMENTS](EXPERIMENTS.md)登记，不能从输入分母推断模型效果。

## 语义观察与本轮范围

定向材料只用于开发问题诊断：研究正文、导航、课程、行政岗位、文章页、旧项目、论文偶现主题、乱码和非文本需分别判断角色；引用存在不等于稳定专长，未提及不等于没有该方向。语种和文字脚本分开，外文不限英语，尚未做全表语种普查。

16条Agent开发示例、本地引文及逐行定位保留在`outputs/teacher_dev_20261023_v0_2/`，不纳入Git，不充当独立真人金标或模型效果。公开文档不复刻这些简介内容；详细方法及本次DeepSeek能力见[路径／工具说明](TEACHER_PATH_AND_TOOLS.md)，最新授权与状态见[STATUS](STATUS.md)。

## 已验证的历史审计复跑方法（PowerShell）

以下命令在项目根目录执行，使用本机 bundled Python；每次更换全新输出目录。脚本拒绝覆盖已有非空审计目录或已有校验结果，不保存工作簿。

```powershell
$tagPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$tagRunName = '20261023_run2'
$tagAuditOut = "outputs/audit_$tagRunName"
$tagChecksOut = "outputs/checks_$tagRunName"
& $tagPython 'scripts/audit_inputs.py' --teachers 'Sheets/teacher_20261022.xlsx' --vocabulary 'Sheets/review_tagscollection_20261022.xlsx' --out $tagAuditOut
& $tagPython 'scripts/verify_audit.py' --run $tagAuditOut --out "$tagChecksOut/verification.json"
& $tagPython 'scripts/inspect_samples.py' --run $tagAuditOut --out "$tagChecksOut/directed_inspection.json"
```

每次复跑前将 `$tagRunName` 改为新的日期／版本标识。主审计依赖 openpyxl（实际版本见 manifest）；独立校验只用 Python 标准库直接读取 XLSX 内的 XML。校验器针对此版本的一个工作表和日期格式 14，换输入结构后先检查适用性。复跑前后核验原件 SHA-256，验收基准见 DATA_AUDIT。
