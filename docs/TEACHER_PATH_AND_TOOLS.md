# 教师分类工具操作指南

本页维护现有 CLI 的操作、输入输出和限制。路径与工具的候选比较统一在[研究文档](RESEARCH_AND_DECISIONS.md)，审核步骤见[审核规则](TEACHER_REVIEW_PROTOCOL.md)，运行结果见[EXPERIMENTS](EXPERIMENTS.md)。

运行前读取任务 Issue 的输入版本、调用上限和验收条件。参数以 scripts/deepseek_classify.py --help 与配置为准；下文为当前入口用法。

## DeepSeek配置与命令

默认endpoint为`https://api.deepseek.com/chat/completions`、模型`deepseek-flash`；显式禁用thinking，启用`json_object`，temperature=0、stream=false。官方JSON模式仍可能空内容，长度不足会截断；本地另做拒绝校验。来源：[接口首页](https://api-docs.deepseek.com/)、[Chat Completion](https://api-docs.deepseek.com/api/create-chat-completion/)、[JSON模式](https://api-docs.deepseek.com/guides/json_mode/)（查阅2026-10-23）。

核心只读取进程环境变量`DEEPSEEK_API_KEY`。Windows入口优先使用已有变量；没有时读取项目外`%USERPROFILE%\.codex\secrets\tagproject-deepseek-api-key.dpapi`，由当前Windows用户解密后临时设置调用进程环境，结束恢复此前值。项目不保存明文。DPAPI文件不能假定在其他用户／电脑上可解密。启动入口不改变默认dry-run。

核心Python自0.2.0起只在live模式读取该环境密钥，dry-run／回放不读取。上段PowerShell包装器仍可能先读取／解密凭证；需完全避免凭证加载的离线检查直接使用Python入口。

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

当前提示为teacher_ds_v2、校验契约为teacher_output_v2。需要按旧规则解释已有响应时，显式在`--response-file`回放中加`--response-contract teacher_output_v1`；该选项不能用于dry-run或live，不改变旧冻结文件。回放生成的是当前提示的请求预览，manifest的`replay_prompt_is_current_preview_not_original=true`明确它不是当时真实请求；旧契约兼容不代表恢复了原模型／提示或缺失的历史响应。省略该选项按v2重新校验，结果另存版本。

默认输出预算8192 token，HTTP超时60秒，最多重试1次（可设0，上限3）；请求256000字节、简介100000字符、响应2000000字节。429、部分5xx及网络／超时有限重试；401／403等不重试，不跟随重定向。不静默截断、不自动分块，预算超限报错。字节预算不是精确模型上下文token计算。

每次发完整紧凑词库：139个L2＋1396个L3来源位置，共1535个合法引用；同名不同位置保留，不做任意Top-K候选截断。`max_tokens`限制输出，不是标签数量上限。更长输入的显式分段及原文映射是后续工作。

## 输出与校验边界

- `request_01.json`：脱敏请求预览，无认证头；用户消息只有`intro`和`vocabulary`，不传姓名／邮箱列、历史标签或本地教师ID。
- `results.json`：来源、模式、错误／分流、方向、逐字引文、Unicode偏移（起点包含、终点不包含）、词库路径、模型、usage、耗时与待审状态；`output_contract_version`记录校验策略，结构／证据／词库违规的`error_details.field_path`定位固定字段及数组下标。
- `REVIEW.md`：可读审阅稿。`supported`为模型自报，不能当人类已确认。
- `manifest.json`：配置、提示版本／哈希、词库／代码／结果哈希和网络次数。`source_row_id`为词库A列ID，`excel_row`为物理行，L3数组下标从0开始，均非新正式概念ID。

缺密钥、HTTP错误／超时、空内容、finish_reason=length、非法JSON／结构、伪造引文、未知标签或路径不符等，整条隔离，不保存为成功标签。空／数字／日期／公式等本地分流不调用API。非法原响应不落日志，保留安全错误码、允许的元数据和哈希。脱敏规则不是通用个人信息识别器，新文本仍应避免无关个人信息。

重复引用仍报duplicate_label，路径不符仍隔离，不自动修正或合并非法结果。REVIEW显示同一安全违规字段，诊断不回显任意模型值、原文或认证头；JSON无法解析等整包错误未必有细字段定位。v2检查supported方向的角色声明一致性，新增research_interest供弱兴趣线索使用，范围不明保留scope_review。它不能识别模型把课程误声明为研究活动、方法外推或概念范围误判，语义审核仍按[审核规则](TEACHER_REVIEW_PROTOCOL.md)。

本地校验只能证明结构、词库身份和引用位置，不证明模型声明的角色、持续专长、概念范围或方向是否穷尽。旧输出的待人审字段原样保留，新反馈由教师模型单独留版本，不当独立金标；本轮不写回原表、不创建概念或正式赋标。usage未知为null，默认费用null。可提供`pricing`中的货币及缓存命中／未命中／输出每百万token单价作“用户提供单价的估算”，不能冒充账单。价格参考[官方价格页](https://api-docs.deepseek.com/quick_start/pricing/)，既有验证未报告实际人民币费用。
