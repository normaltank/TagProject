# 当前状态

更新：2026-10-23（Asia/Singapore）。**唯一活跃主线：教师简介→研究方向→现有标签＋原文证据。DeepSeek工具已实现，真实连通已验证。** 用户本次API授权覆盖此前小样阶段“不调用付费API／资料不外发”；全量赋标、训练、平台部署和正式词库迁移仍未开展。

## Matt Setup与Git上传完成

按用户确认的四份草案，保留原AGENTS条款并追加唯一Agent skills块，已写[Issue tracker](agents/issue-tracker.md)、[状态标签](agents/triage-labels.md)、[领域文档规则](agents/domain.md)。跟踪器为normaltank/TagProject的GitHub Issues，单领域布局为GLOSSARY.md＋docs/adr/；后两者未创建空文件，grill with docs尚待指挥端继续。

GitHub五个任务状态标签已核实：新增needs-triage、needs-info、ready-for-agent、ready-for-human，保留wontfix与其他现有标签。使用GitHub官方API及本机Git Credential Manager，未打印／保存访问令牌。

本地main已正常推送至公开[仓库normaltank/TagProject](https://github.com/normaltank/TagProject)。首个已验证提交为[ee10394b6a93cb6843e81ea65f7acbed2a08c4dd](https://github.com/normaltank/TagProject/commit/ee10394b6a93cb6843e81ea65f7acbed2a08c4dd)，包含32个审核文件、246054字节；首次推送后本地HEAD与远端main完全一致。本次文档提交补记完成状态，最终HEAD／远端核对留在本地`outputs/git_upload_prepare_20261023_v1/`，不把运行明细上传。

Sheets、outputs、logs、环境／密钥与缓存均排除；原XLSX和16例前后哈希不变、仍在本地。公开文档去除真实记录内部ID／简介摘录和个人机器路径，原文档副本留本地忽略目录。暂存内容中实际DeepSeek密钥精确比对命中0；范围、依赖与新克隆限制见[README](../README.md)。

本次新增的29项纯合成／模拟HTTP检查通过，不用真实数据或密钥；完整32项及CLI默认词库读取仍依赖两份／词库本地XLSX，不能宣称新克隆已包含数据或全部测试可直接运行。未运行新的DeepSeek API实验，未改分类语义。

## 当前交付

- [教师路径、工具清单与DeepSeek操作](TEACHER_PATH_AND_TOOLS.md)：A规则／传统、S监督BERT类、B语义检索重排、C当前DeepSeek，以及词库／审核工具的优先级。
- [Python入口](../scripts/deepseek_classify.py)、[Windows加密密钥入口](../scripts/deepseek_classify.ps1)、[核心](../tagging/deepseek.py)、[无密钥配置](../config/deepseek.example.json)。默认dry-run，显式live一次一条；可接新简介或指定行，只发送脱敏简介和必要词库。
- [32项离线／模拟HTTP检查](../outputs/deepseek_20261023_validation_v1/checks.json)、[测试日志](../outputs/deepseek_20261023_validation_v1/tests.log)。初次电话脱敏与空单元格定位问题已修复，失败记录保留同目录。
- [合成真实调用](../outputs/deepseek_20261023_synthetic_live_v1/REVIEW.md)、[教师第10行真实调用](../outputs/deepseek_20261023_teacher10_live_v1/REVIEW.md)：各一次HTTP 200，无重试，返回deepseek-flash。合成1方向／1标签建议，第10行3方向／2标签建议／3条[69,93)引文，全部待人工语义审核。
- [语义待审提醒](../outputs/deepseek_20261023_validation_v1/review_notes.md)：资源与环境化工的范围、膜分离→分离工程的较粗粒度仍需人审；保留真实模型输出，不为拟合单例重跑。
- [教师默认预览与异常分流](../outputs/deepseek_20261023_teacher_dry_v1/REVIEW.md)、[合成离线回放](../outputs/deepseek_20261023_synthetic_replay_v1/REVIEW.md)：均无真实API调用。

真实外部请求合计2次，仅合成简介和教师第10行各一次。输入token分别11645／11675，输出242／316，HTTP耗时1.9611／2.0658秒。费用为null，未核对实际账单；连通测试不是准确率或经济性结论。引用可定位、词库合法和JSON通过不能证明方向语义、持续性或标签范围正确。

## 当前能力与下一步

已实现只读选行、异常分流、保留字符偏移的脱敏、完整1535个词库来源引用、API调用／有限重试、本地结构／引文／词库校验、拒判／范围待审／缺口及独立版本结果。预算超限报错，不静默截断；非法输出整条隔离，不写正式赋标。核心只读环境密钥，PowerShell可临时加载项目外当前用户的DPAPI加密文件，不保存明文。

下一步人工审核真实小样和既有16例，维护实际使用标签的最小定义、范围和别名，再按共同质量底线决定有界对照及扩大。A规则／传统、B的Sentence Transformers、S的BERT类监督多标签尚未实施。此前“下一编码任务固定先做A”已由本次DeepSeek优先要求覆盖。没有独立金标、准确率、训练经济性或路线胜出结论。

## 原16条Agent开发示例保留

[v0_2审阅稿](../outputs/teacher_dev_20261023_v0_2/REVIEW.md)、[结构化结果](../outputs/teacher_dev_20261023_v0_2/examples.json)、[定位校验](../outputs/teacher_dev_20261023_v0_2/checks.json)、[manifest](../outputs/teacher_dev_20261023_v0_2/manifest.json)、[真人反馈模板](../outputs/teacher_dev_20261023_v0_2/human_feedback.json)保持不变，v0_1也保留。9条有建议／7条不赋标，34个选取方向、20次建议（3次近似范围待审）、5个候选不赋标、40条精确引文，真人确认0次；不是独立金标，长文未穷尽方向。

原prepare_teacher_examples.py／build_teacher_examples.py只读取、渲染和校验Agent配置，不是自动推断；本次独立DeepSeek模块才可处理新简介。两个原XLSX不写回，旧16例不改动。数据与历史运行事实见[DATA_AUDIT](DATA_AUDIT.md)、[EXPERIMENTS](EXPERIMENTS.md)。

## 保留待续与协作

稿件识别、师稿匹配、跨对象评测、完整词库重构和平台建设继续保留，恢复条件见[PROJECT](PROJECT.md)，第一阶段状态见[快照](history/STATUS_PHASE1_20261023.md)。最小词库定义／别名和证据审核继续，未来共同概念兼容性保留接口约束。

沿用既有指挥Agent 01a166ad-bfb5-7121-a289-4fd922442ffa与执行Agent 01a166ad-3072-7432-a801-dcca8b62fddf；执行端集中写文件，指挥端核查，不新增对话或子代理。
