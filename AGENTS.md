# TagProject 工作约定

每次开工先读 [STATUS](docs/STATUS.md)，确认当前阶段、任务 Issue 和下一步。唯一活跃主线是教师简介→研究方向→现有标签＋证据。

按工作分支读取：

- 需求与边界：[PROJECT](docs/PROJECT.md)；教师判断：[审核规则](docs/TEACHER_REVIEW_PROTOCOL.md)；术语：[GLOSSARY](GLOSSARY.md)。
- 数据口径：[DATA_AUDIT](docs/DATA_AUDIT.md)；选型依据：[RESEARCH_AND_DECISIONS](docs/RESEARCH_AND_DECISIONS.md)。
- 实验前后：[EXPERIMENTS](docs/EXPERIMENTS.md)；运行工具：[操作指南](docs/TEACHER_PATH_AND_TOOLS.md)。
- 开始任务、切换阶段或维护 Markdown：[Matt 工作流与文档职责](docs/agents/workflow.md)。历史材料按[归档索引](docs/history/README.md)取用。

原始 XLSX、旧16例和已冻结实验材料只读；派生结果与修订分版本保存。旧标签不作独立答案，模型审核不称真人意见、独立金标或准确率。API 只发送脱敏简介和必要词库，密钥只读环境；默认 dry-run，live 显式且有界。用户已授权教师小样及 DeepSeek 接入，完整范围见 PROJECT。

采用 Issue 驱动的串行工作流。当前对话可以完成已明确的小任务；需要委派时可调动 subagent，由主 Agent 汇总验收，并以任务 Issue 明确范围。所有 subagent 调用都显式指定模型 `gpt-6.1-sol`、思考强度 `high`。不自行新增独立对话。

## Agent skills

### Issue tracker

GitHub Issues：normaltank/TagProject。读写任务前查 [issue-tracker](docs/agents/issue-tracker.md)。

### Triage labels

采用五个默认状态标签，含义见 [triage-labels](docs/agents/triage-labels.md)。

### Domain docs

单份 GLOSSARY.md 与按需创建的 docs/adr/；维护前查 [domain](docs/agents/domain.md)。
