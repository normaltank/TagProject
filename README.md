# 教师简介的研究方向与标签识别

当前唯一活跃任务：从教师简历／简介中识别有证据支持的研究方向，映射现有词库，给出标签、原文证据和待核查项。顺序为可用文本及异常分流→方向／证据识别→现有词库映射及缺口→小样人工复核→决定是否扩大自动化。

第一阶段审计、研究和16条Agent开发示例已保留。本次按用户新增授权实现DeepSeek API分类工具，完成合成简介和教师第10行各一次真实调用，结果均待人工语义审核；不修改原表、不产生正式新概念ID。工作进度和入口以 [STATUS](docs/STATUS.md) 为准。真实稿件缺失不阻塞教师主线。

待审稿件识别、师稿匹配、跨对象联合评测、完整词库重构和平台建设均保留待续，恢复条件见 [PROJECT](docs/PROJECT.md)。未来共同概念兼容性是接口约束，不是本轮实施这些支线的要求。

流程已定、最终模型未定：已实施Python／openpyxl只读工具，以及DeepSeek的方向提取、现有标签映射和原文／词库校验。默认离线预览，显式live一次一条，32项离线／模拟HTTP测试通过。此前固定先编码A规则基线的顺序已由本次DeepSeek优先要求覆盖；规则／传统、监督BERT类和语义检索重排保留为后续对照候选，没有路线质量或经济性胜出结论。

BERT／RoBERTa／XLM-R类的监督多标签分类（冻结表示＋轻量分类头或任务微调）也明确保留为竞争候选，本地推理不等于必须训练。全部候选、工具分工及同质量门槛下的总费效比比较见[研究与决策](docs/RESEARCH_AND_DECISIONS.md)，当前没有训练经济性结论。

## 文档入口

- **当前路径／工具及操作**：[教师任务清单与DeepSeek说明](docs/TEACHER_PATH_AND_TOOLS.md)、[教师第10行真实结果](outputs/deepseek_20261023_teacher10_live_v1/REVIEW.md)、[32项测试](outputs/deepseek_20261023_validation_v1/checks.json)、[语义待审提醒](outputs/deepseek_20261023_validation_v1/review_notes.md)。

- **本轮可审阅结果**：[16条教师示例审阅稿](outputs/teacher_dev_20261023_v0_2/REVIEW.md)、[结构化结果](outputs/teacher_dev_20261023_v0_2/examples.json)、[真人反馈模板](outputs/teacher_dev_20261023_v0_2/human_feedback.json)。9条有标签建议、7条暂不赋标；均为Agent开发示例，非独立金标，详见状态与审阅稿。

- [PROJECT](docs/PROJECT.md)：需求基线、边界和输出约定。
- [DATA_AUDIT](docs/DATA_AUDIT.md)：输入版本、分母、问题定位与语义抽查。
- [RESEARCH_AND_DECISIONS](docs/RESEARCH_AND_DECISIONS.md)：官方资料、整体方案、选择与重新考虑条件。
- [EXPERIMENTS](docs/EXPERIMENTS.md)：独立人工基准、2×2 对照、指标、成本假设和运行记录。
- [STATUS](docs/STATUS.md)：当前教师主线、实际结果、待续支线和下一步。
- [AGENTS](AGENTS.md)：后续 Agent 的稳定工作约定。

## 目录

`Sheets/` 保存两份原始工作簿；`tagging/` 保存DeepSeek分类及本地校验；`scripts/` 保存只读工具与启动入口；`config/` 保存无密钥示例；`tests/` 保存合成及模拟HTTP测试；`outputs/` 保存独立版本结果；`logs/research/` 保存官方查阅记录。根目录三个planning文件只记录执行进度并指向职责文档。

当前输入为教师样本 `teacher_20261022.xlsx` 与词库 `review_tagscollection_20261022.xlsx`。本地没有独立人工答案或可审查的历史 BERT 实现；教师示例仍可基于现有原文推进。样本数据不能代表业务全量。

## Git上传范围与本地依赖

仓库准备只包含源码、整理后的项目文档、无密钥配置、依赖说明及纯合成测试。`Sheets/`、`outputs/`、`logs/`、环境文件／密钥、虚拟环境和缓存均忽略，仍保留在原本地路径；原XLSX和16条示例不改写。公开文档已移除真实记录内部ID、原始简介摘录及个人机器路径；修改前文档副本保留在本地被忽略的`outputs/git_upload_prepare_20261023_v1/private_before_upload/`。

新克隆不带原工作簿、16例、审计输出、真实API结果、研究下载或密钥。因此文档指向`outputs/`／`logs/`的历史结果链接仅在保有这些本地文件的工作区可用。将获授权的原文件放回`Sheets/`，或使用命令参数指定文件路径，才能运行工作簿检查和CLI；即使输入纯合成简介，当前CLI仍需词库工作簿，不会凭空附带本项目词库。

运行环境建议Python 3.10以上，本机已验证Python 3.12.14。只读XLSX依赖在`requirements.txt`中固定为openpyxl 3.1.5；HTTP、JSON与测试框架使用标准库：

```powershell
python -m pip install -r requirements.txt

# 仅合成与本地模拟HTTP，不需要教师／词库文件或真实API密钥
python -m unittest discover -s tests -v -k ValidatorTests -k InputAndEnvelopeTests -k HttpTests

# 完整32项：需要两份本地工作簿，包括CLI的默认词库读取
python -m unittest discover -s tests -v
```

真实API调用还需要环境密钥；DPAPI加密文件属于当前Windows用户，本仓库不上传且其他电脑／用户不能假定可解密。PowerShell入口支持`-PythonPath`和`-SecretFile`显式选择本地运行路径。

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

真实首轮输出：`outputs/audit_20261023_v1_1_0_run1/`；通过的独立校验为 `outputs/audit_20261023_checks_v1/verification_v2.json`。旧的 `verification.json` 是修正读取表示前的失败诊断，保留用于追溯。

教师示例使用 `prepare_teacher_examples.py` 读取本轮不含旧标签的材料，`build_teacher_examples.py` 对Agent配置的方向与映射生成审阅稿并核验原文／词库定位；配置、结果和脚本版本见示例目录的manifest。此工具不能接收一篇新简介就自动推断标签。当前正式审阅版本为v0_2；v0_1保留，v0_2仅补一条乱码质量短引，方向和标签映射不变。
