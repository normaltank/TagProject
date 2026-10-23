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
| T-PREP-02 | 20条源材料与初判已冻结，API副本待最终核查 | 下节；该批 DeepSeek 请求为0 |
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

原始初判文件及哈希独立保留。等长 API 副本、17份文本和3条原类型本地路由记录在 [输入索引](../outputs/teacher_prejudge_20261023_v0_2/API_READY_INDEX.json)；[最终派生检查](../outputs/teacher_prejudge_20261023_v0_2/privacy_checks.final.json)通过已列结构及已知回归项，**仍待指挥端逐项核查遮盖边界**，不能把检查通过称为完整隐私或语义验收。

此前作者缩写／编号误识别曾遮盖题名和课程词；失败及过渡副本保留，最终副本已作修订。该批真实 API 请求为0，预测对照、差异审核和实际用量尚未运行。当前先整理规格与任务，不改变初判或进行重试拟合。

## 新运行的记录要求

运行前冻结输入／选择范围、词库、初判／审核规则、代码／提示／配置和调用上限。保存不可变版本或哈希；改动上述条件则另开版本并说明可比性。

每次写入新的输出目录，记录成功／拒判／失败／未运行、原始预测、证据、审核差异、实际 token／耗时／费用来源。缺失值记 null，假设算术与实测分开。结束后更新本页对应运行及任务 Issue 的完成证据；STATUS 只保留当前入口。
