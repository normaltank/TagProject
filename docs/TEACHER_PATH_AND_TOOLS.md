# 教师简介打标签：路径、工具与DeepSeek使用

更新：2026-10-23（Asia/Singapore）。只做教师简介→研究方向→现有标签＋原文证据。稿件、师稿匹配、全量赋标、长训练、完整词库重构和平台建设继续保留待续。

## 执行路径

1. 输入新简介或显式指定教师行，隔离历史标签。
2. 本地分流空值、数字、日期、公式和明显乱码；脱敏简介中的已知姓名、邮箱、常见电话与密钥样式文本，保持字符位置。
3. DeepSeek读取脱敏简介及完整紧凑词库，提取方向和证据，再映射已有L2／L3。允许不赋标、范围待审及缺口，不新建正式概念。
4. 本地校验JSON结构、逐字引文及位置、词库成员和路径；失败整条隔离，不当部分成功标签。
5. 人工复核方向、证据角色、持续专长与概念范围，再决定是否扩大自动化。当前工具不写正式赋标或原工作簿。

实际使用标签的最小定义、包含／排除范围、必要别名和跨语同义仍需维护；不等待完整词库改革。课程、导航、任职或单篇论文不能自动成为研究专长，未提及也不代表教师没有该方向。

## 方法路径与优先级

- **C：LLM提取与映射，现在可用。** 按用户新增要求优先实现DeepSeek API，已完成有界真实连通验证。适合产出方向、证据与候选映射供审核；本地LLM仍保留接口思路，未下载。尚无独立质量或经济性胜出结论。
- **A：规则／关键词与传统分类，后续对照候选。** 可比较关键词、必要时BM25／TF-IDF及轻量分类；监督分类需要训练答案。本次未实现A，不再把先做A作为DeepSeek的前置；词面命中仍需语义审核。
- **B：标签定义的语义检索＋重排，有条件加入。** 使用Sentence Transformers等组件处理词面差异／跨语并减少候选上下文；定义、模型revision、阈值和实际收益需小样验证，本次未安装或运行。
- **S：BERT／RoBERTa／XLM-R监督多标签，保留竞争路线。** 比较冻结编码器＋轻量分类头、任务微调。基础权重不会自带本词库受训分类头；本地推理不等于必须训练，微调不等于从零预训练。待可信教师答案、独立划分与预算齐备后开展有界可行性试验，本次未训练。
- **弱监督、主动学习、Teacher–Student，保留。** 需控制旧标签／伪标签噪声、Teacher偏差和测试泄漏，不直接把同一Teacher当独立裁判。

最终比较使用相同误标／漏标、证据可靠性、有用覆盖与复核要求，计入标注、实验／训练、推理／API、人工纠错和更新维护的总成本。两次连通调用不能决定最终路线或训练经济性，详见[研究与决策](RESEARCH_AND_DECISIONS.md)。

## 工具清单

- **Python＋openpyxl：当前必需、已使用。** 原表只读、显式选行、类型分流和独立输出；HTTP与校验用Python标准库。本机Python 3.12.14、openpyxl 3.1.5。
- **DeepSeek：当前已接入。** [核心模块](../tagging/deepseek.py)、[Python入口](../scripts/deepseek_classify.py)、[Windows加密密钥入口](../scripts/deepseek_classify.ps1)、[无密钥配置示例](../config/deepseek.example.json)。
- **本地JSON／审阅稿与人工审核：当前必需。Label Studio：可选后续界面。** 当前无需先部署平台；界面控件、字符偏移和导出需另验证，标注工具本身不等于金标。
- **Sentence Transformers：B路线组件。Transformers／BERT类模型：S路线工具。** 按后续试验条件引入，当前未下载或训练，不把组件当已适配的分类器。
- **Annif：可选多配置标引框架。** 可组织后端及自有词库，不是额外一个固定模型；当前CLI无需部署。
- **SKOS：概念、别名与关系的交换标准；VocBench：可选协同编辑平台。** 保留兼容，当前用来源行／路径／出现位置追溯；平台暂缓，但最小定义与别名审核继续。
- **BERTopic：可选候选主题发现。** 暂缓，主题／短语只进入人工提案，不自动成为正式标签。
- **pySHACL：采用RDF并制定约束后再用。** 当前暂缓，已实现轻量JSON成员／路径校验；两者均不能判断概念语义是否正确。

可选工具的官方来源与边界保留在[研究文档](RESEARCH_AND_DECISIONS.md)，以上不是本轮安装清单。

## DeepSeek配置与命令

默认endpoint为`https://api.deepseek.com/chat/completions`、模型`deepseek-flash`；显式禁用thinking，启用`json_object`，temperature=0、stream=false。官方JSON模式仍可能空内容，长度不足会截断；本地另做拒绝校验。来源：[接口首页](https://api-docs.deepseek.com/)、[Chat Completion](https://api-docs.deepseek.com/api/create-chat-completion/)、[JSON模式](https://api-docs.deepseek.com/guides/json_mode/)（查阅2026-10-23）。

核心只读取进程环境变量`DEEPSEEK_API_KEY`。Windows入口优先使用已有变量；没有时读取项目外`%USERPROFILE%\.codex\secrets\tagproject-deepseek-api-key.dpapi`，由当前Windows用户解密后临时设置调用进程环境，结束恢复此前值。该加密文件已由指挥端按用户要求保存并回读验证；项目不保存明文。DPAPI文件不能假定在其他用户／电脑上可解密。启动入口不改变默认dry-run。

在项目根目录运行，省略`--out`会生成唯一目录：

```powershell
# 默认离线预览，不调用API
& .\scripts\deepseek_classify.ps1 -CliArguments @('--text-file','tests/fixtures/deepseek_synthetic.txt')

# 显式联网，一次只处理一条教师简介
& .\scripts\deepseek_classify.ps1 -CliArguments @('--teacher-rows','10','--live')

# 配置文件不含密钥；命令参数可覆盖model、endpoint、max-tokens、timeout-seconds等
& .\scripts\deepseek_classify.ps1 -CliArguments @('--text-file','tests/fixtures/deepseek_synthetic.txt','--config','config/deepseek.example.json')
```

直接使用Python时，live需要预先设置该进程的环境密钥：

```powershell
$tagPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $tagPython 'scripts/deepseek_classify.py' --text '研究方向：膜分离与水处理。'
& $tagPython 'scripts/deepseek_classify.py' --teacher-rows '10,4,5205,8099,8730'
& $tagPython 'scripts/deepseek_classify.py' --text-file 'tests/fixtures/deepseek_synthetic.txt' --response-file 'tests/fixtures/deepseek_valid_envelope.json'
& $tagPython -m unittest discover -s tests -v
```

`--text`、UTF-8的`--text-file`、`--teacher-rows`互斥。教师行必须逗号显式列出，不支持范围；离线最多20行，live／回放仅一条。这是输入范围界限，不限制教师标签数。回放不代表真实模型运行。非空输出目录拒绝覆盖。退出码0表示预览／分流或形式校验完成，2表示失败／隔离；0不代表语义审核通过。

默认输出预算8192 token，HTTP超时60秒，最多重试1次（可设0，上限3）；请求256000字节、简介100000字符、响应2000000字节。429、部分5xx及网络／超时有限重试；401／403等不重试，不跟随重定向。不静默截断、不自动分块，预算超限报错。字节预算不是精确模型上下文token计算。

每次发完整紧凑词库：139个L2＋1396个L3来源位置，共1535个合法引用；同名不同位置保留，不做任意Top-K候选截断。合成请求58720 UTF-8字节，教师第10行58891字节。`max_tokens`限制输出，不是标签数量上限。更长输入的显式分段及原文映射是后续工作。

## 输出与校验边界

- `request_01.json`：脱敏请求预览，无认证头；用户消息只有`intro`和`vocabulary`，不传姓名／邮箱列、历史标签或本地教师ID。
- `results.json`：来源、模式、错误／分流、方向、逐字引文、Unicode偏移（起点包含、终点不包含）、词库路径、模型、usage、耗时与待审状态。
- `REVIEW.md`：可读审阅稿。`supported`为模型自报，不能当人类已确认。
- `manifest.json`：配置、提示版本／哈希、词库／代码／结果哈希和网络次数。`source_row_id`为词库A列ID，`excel_row`为物理行，L3数组下标从0开始，均非新正式概念ID。

缺密钥、HTTP错误／超时、空内容、finish_reason=length、非法JSON／结构、伪造引文、未知标签或路径不符等，整条隔离，不保存为成功标签。空／数字／日期／公式等本地分流不调用API。非法原响应不落日志，保留安全错误码、允许的元数据和哈希。脱敏规则不是通用个人信息识别器，新文本仍应避免无关个人信息。

本地校验只能证明结构、词库身份和引用位置，不证明模型声明的角色、教师持续专长、概念范围或方向是否穷尽。全部输出待人工语义审核，不写回原表、不创建概念、不生成正式赋标。usage未知为null，不伪装0；默认费用null。可提供`pricing`中的货币及缓存命中／未命中／输出每百万token单价作“用户提供单价的估算”，不能冒充账单。价格参考[官方价格页](https://api-docs.deepseek.com/quick_start/pricing/)，本次未报告实际人民币费用。

## 实际验证记录

- [32项离线／模拟HTTP测试](../outputs/deepseek_20261023_validation_v1/checks.json)全部通过；初次2处失败及修正保留同目录。覆盖类型分流、脱敏与偏移、重复引文、L2/L3与同名位置、拒判／缺口、无硬标签数上限、非法内容及HTTP重试／超时／重定向等。
- [合成真实调用](../outputs/deepseek_20261023_synthetic_live_v1/REVIEW.md)：HTTP 200，1次无重试；输入11645／输出242／合计11887 token，HTTP 1.9611秒、分类流程1.9835秒；1方向／1标签建议／1待审描述。
- [教师O10真实调用](../outputs/deepseek_20261023_teacher10_live_v1/REVIEW.md)：HTTP 200，1次无重试；输入11675／输出316／合计11991 token，HTTP 2.0658秒、分类流程2.0991秒（不含工作簿读取等CLI全部耗时）；3方向／2标签建议／3条引用[69,93)，两个词库定位合法。
- [语义审阅提醒](../outputs/deepseek_20261023_validation_v1/review_notes.md)：第10行“资源与环境化工”的范围与“膜分离→分离工程”的较粗映射需人审；保留模型真实输出，不为拟合此例重跑或改成预期答案。
- [教师默认dry-run及异常分流](../outputs/deepseek_20261023_teacher_dry_v1/REVIEW.md)、[合成模拟回放](../outputs/deepseek_20261023_synthetic_replay_v1/REVIEW.md)：无真实API调用。

真实外部调用合计2次，仅合成简介和教师第10行各一次，均返回deepseek-flash；提示teacher_ds_v1。无批量分类、训练或改写原件／16例。这是连通和约束验证，不是独立质量或性能实验。
