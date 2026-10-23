# 教师简介的研究方向与标签识别

从教师简介提取有证据支持的研究方向，映射现有词库并保留可追溯证据。当前提供只读数据工具、DeepSeek 分类 CLI 和教师模型小样审核流程；最终模型选择仍需实验依据。

先看 [当前状态](docs/STATUS.md)；任务与规格在 [GitHub Issues](https://github.com/normaltank/TagProject/issues)。

## 文档导航

| 需要了解 | 入口 |
| --- | --- |
| 当前阶段、正在处理的任务、下一步 | [STATUS](docs/STATUS.md) |
| 教师任务范围、结果约定与待续支线 | [PROJECT](docs/PROJECT.md) |
| Matt 工作流、各类 Markdown 的职责与写法 | [工作流](docs/agents/workflow.md) |
| 研究方向、标签建议等领域词义 | [GLOSSARY](GLOSSARY.md) |
| 判断证据、较宽标签、拒判与审核分歧 | [审核规则](docs/TEACHER_REVIEW_PROTOCOL.md) |
| 标签范围的待验证提案 | [工作释义](docs/TEACHER_LABEL_SCOPES.md) |
| 数据字段、分母、质量问题与审计复跑 | [DATA_AUDIT](docs/DATA_AUDIT.md) |
| A／S／B／C 路线、工具依据与选型理由 | [RESEARCH_AND_DECISIONS](docs/RESEARCH_AND_DECISIONS.md) |
| 运行方法与输出含义 | [DeepSeek 操作指南](docs/TEACHER_PATH_AND_TOOLS.md) |
| 实际实验、分母、用量和证据入口 | [EXPERIMENTS](docs/EXPERIMENTS.md) |
| 早期需求、旧计划与未运行实验设计 | [档案索引](docs/history/README.md) |

## 本地运行

Python 依赖见 [requirements.txt](requirements.txt)。已验证环境为 Python 3.12.14；HTTP、JSON 和测试使用标准库。

~~~powershell
python -m pip install -r requirements.txt

# 纯合成与模拟 HTTP 检查，无需教师数据或 API 密钥
python -m unittest discover -s tests -v -k ValidatorTests -k InputAndEnvelopeTests -k HttpTests

# 查看 CLI 参数，运行示例见操作指南
python scripts/deepseek_classify.py --help
~~~

完整测试命令为 python -m unittest discover -s tests -v，其中部分集成检查需要本地工作簿。当前 CLI 即使输入合成简介，也需要来源词库；它不随仓库分发。教师示例生成器用于渲染／校验已写好的判断，自动处理新简介的入口是 DeepSeek CLI。

## 仓库与本地档案

源码、整理后的文档、无密钥配置和合成测试纳入 Git。Sheets、outputs、logs、环境文件、密钥和缓存由 [.gitignore](.gitignore) 排除。

新克隆不含原始工作簿、教师原文、逐项审核、真实 API 结果或密钥。文档中的本地证据链接只在保有原资料的工作区可用；获授权的工作簿放入 Sheets，或通过工具参数指定位置。Windows DPAPI 密钥文件属于原 Windows 用户，不能假定其他账户可解密。
