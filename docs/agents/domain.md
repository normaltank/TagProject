# Domain Docs

采用单一领域布局：根目录 GLOSSARY.md 与按需创建的 docs/adr/。

- 讨论领域含义前读 GLOSSARY 和相关 ADR；输出沿用已确认词义，遇到歧义用实际案例澄清。
- 术语一旦解决即可更新 GLOSSARY；每词1—2句，只写领域定义，排除实现细节和进度。
- 决策同时满足难逆转、无上下文会意外、存在真实取舍时，才按 domain-modeling 的 ADR 格式记录。其余设计理由维护在对应职责文档或 Issue。
- 新决定替代已有决定时写明理由和替代关系；已冻结记录保留。文件在首次有内容时创建，保持单一权威来源。

阶段与 Markdown 职责见 [workflow](workflow.md)，历史记录见[归档索引](../history/README.md)。
