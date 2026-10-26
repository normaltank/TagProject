# 教师打标签的开放技术调查（2026-10-26）

对应 [Issue #7](https://github.com/normaltank/TagProject/issues/7)。查阅日期统一为 **2026-10-26（Asia/Singapore）**；近期窗口约为2026-07-28至10-26。以下区分官方事实、适用性推断与未运行事项；不将公开基准当本项目效果。既有路线与选择见[选型记录](../RESEARCH_AND_DECISIONS.md)，当前执行仍是 [#3→#4→#5](../STATUS.md)。

## 本次建议

先完成冻结20条的 DeepSeek 诊断，再根据错误和成本选一个后续对照：若研究内容／证据提取遗漏突出，优先试 GLiNER2.5 多语抽取；若主要负担是反复发送完整词库，优先试小型多语检索筛候选。两条都能从现成权重起步，不要求先训练。新模型不替代审核规则，也不成为当前小样的新前置条件。

## 近90天：GLiNER2.5／GLiNER2 库

**核实事实。** [v2.0.0](https://github.com/fastino-ai/GLiNER2/releases/tag/v2.0.0) 于2026-08-24发布，加入边界架构、分块、实体属性和联合抽取；[v2.1.0](https://github.com/fastino-ai/GLiNER2/releases/tag/v2.1.0) 于2026-10-09发布，改进推理、训练与schema，明确**权重未变**。库版本2.1与模型架构2.5不能混称。原始[论文](https://arxiv.org/abs/2507.18546) 首投为2025-07-24，不能当2026年新论文。

开放权重 [fastino/gliner2.5-multi-v1](https://huggingface.co/fastino/gliner2.5-multi-v1) 为287M、mDeBERTa主干，支持schema驱动的实体、分类、记录及关系；可直接加载预训练权重，不需先训练本项目分类头。[代码许可](https://github.com/fastino-ai/GLiNER2/blob/main/LICENSE) 与该模型卡的权重许可分别核实，均为Apache-2.0。

模型卡声明多语；[官方README](https://github.com/fastino-ai/GLiNER2#custom-word-splitters) 对中文建议字符切分，同时警告公开权重按空白切词训练，更换切分可能影响质量。[模型配置](https://huggingface.co/fastino/gliner2.5-multi-v1/raw/main/config.json) 的外层 `max_len=4096`、编码器 `max_position_embeddings=512` 同时存在，不能据此承诺中文4096 token质量。长文接口使用重叠分块，返回原文 `start/end`；跨度两端及关系端点须在同块，跨块语义不会自动补齐。Context7也定位到同一官方[长文教程](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/12-long_context.md)。

**适用性推断。** 这是本次优先试验候选：先抽“研究方向／方法／应用对象”原文片段，再映射现有标签，可直接检查证据回指。实体命中仍不能证明持续专长；课程、合作项目、历史经历及否定语境需遵守教师审核规则。建议未来只做有界对照，测片段遗漏、偏移正确性和复核用时；本轮未下载、运行或测量。

## 较早候选：GLiClass

**核实事实。** [论文](https://arxiv.org/abs/2508.07662) 首投2025-08-11；[最新代码发行API](https://api.github.com/repos/Knowledgator/GLiClass/releases/latest) 返回v0.1.20、2026-07-21，窗口之外。[gliclass-x-base模型卡](https://huggingface.co/knowledgator/gliclass-x-base) 是多语mDeBERTa零样本分类器，可直接以 `multi-label` 方式传入标签，无需先训练；[模型元数据](https://huggingface.co/api/models/knowledgator/gliclass-x-base) 创建于2025-07-17，创建日期不等于公开发布日期。未核实该checkpoint的独立中文效果。其[代码许可](https://github.com/Knowledgator/GLiClass/blob/main/LICENSE) 和模型卡权重许可分别均为Apache-2.0。

Context7查到[官方pipeline](https://github.com/Knowledgator/GLiClass/blob/main/gliclass/pipeline.py) 默认 `max_length=1024`、`max_classes=25`；[checkpoint配置](https://huggingface.co/knowledgator/gliclass-x-base/raw/main/config.json) 的位置配置为512。它输出标签和分数，未提供本任务所需的证据跨度。**推断：** 可作少量候选标签的分类对照；1535词全量直接塞入不应假定可行，候选分批、截断及分数可比性均待验证。证据需另配抽取环节，本轮未运行。

## 较早候选：mmBERT（ModernBERT多语路线）

**核实事实。** [论文](https://arxiv.org/abs/2509.06888) 首投2025-09-08，[作者发布文](https://huggingface.co/blog/mmbert) 为2025-09-09；不是近90天新发布。[官方仓库](https://github.com/jhu-clsp/mmBERT) 列140M／307M、1833种语言与8192 token；[base模型卡](https://huggingface.co/jhu-clsp/mmBERT-base) 含中文示例，权重标MIT。仓库未找到LICENSE，官方[许可API](https://api.github.com/repos/jhu-clsp/mmBERT/license) 返回404，因此不把权重MIT扩展为仓库代码许可结论。

**适用性推断。** 可作为监督多标签分类的编码器主干，或后续专门训练的检索组件；基础fill-mask权重没有1535标签任务头，也不自动输出原文证据。冻结主干后训练轻量头仍是训练。现阶段缺可信独立答案，暂不优先于可直接起步的抽取候选；无本项目实测。

## 本月新发布，但暂不优先

**UltraBERT。** [作者发布文](https://huggingface.co/blog/dmis-lab/ultrabert) 日期为2026-10-14，列150M／380M英语编码器、原生32K上下文及可直接使用的 Embed-150M，并声明Apache-2.0；本次未单独审计其代码仓库许可。基础编码器的分类用法仍需任务微调，现成 embedding 才可直接做检索。**推断：** 它证明BERT类路线仍值得保留，但英语定位不足以支持直接替换中文教师流程；暂存为英语／监督路线参考。

**Nemotron 3.5 Embed／Rerank。** [NVIDIA发布文](https://huggingface.co/blog/nvidia/nemotron-retriever-world-class-agentic-retrieval) 日期为2026-10-21。其 [Embed-1B-BF16模型卡](https://huggingface.co/nvidia/Nemotron-3.5-Embed-1B-BF16) 列文本检索评估含中文、32768上下文及OpenMDW-1.1权重条款，不应写成Apache-2.0。发布文明确嵌入模型语言部分保持冻结，纯文本向量预计与相应Nemotron 3模型不变；新增能力重点是图文检索，重排版本为8B。**推断：** 现有输入是简介纯文本，本轮升级理由不足，暂不部署其多模态栈。代码与依赖许可尚未逐项审计。

## 较早但可作为低成本对照：多语检索

[Granite Embedding 97M Multilingual R2模型卡](https://huggingface.co/ibm-granite/granite-embedding-97m-multilingual-r2) 标注2026-04-29发布、权重Apache-2.0；[IBM介绍文](https://huggingface.co/blog/ibm-granite/granite-embedding-multilingual-r2) 是2026-05-14，两者日期分开。模型基于ModernBERT，支持中文，32K上下文，现成权重可通过Sentence Transformers推理；参数规模97M，有ONNX／OpenVINO版本。它不是本月新发布，也不是现成的本项目标签分类头。

另一现成对照是 [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) 与 [Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B)：各自模型卡权重Apache-2.0、32K、多语；不把较早模型包装成本月新技术。检索／重排可直接使用预训练权重，组件代码沿用[已有Sentence Transformers核查](../RESEARCH_AND_DECISIONS.md)，不同模型的依赖仍须在运行前冻结。

**待验证收益。** 用已冻结的标签名称／路径及明确版本的工作释义做索引，先召回候选，再让DeepSeek作证据与范围判断。可能减少重复词库token；但候选漏召回会造成不可恢复漏标，工作释义是否加入也会改变信息条件。先与当前完整词库基线比较候选召回、错标／漏标／拒判和实际总成本，不能仅凭模型小就认定更便宜。GPU／CPU耗时、内存、复核时间与API缓存收益本项目均未测。首次只选一个检索模型，重排器是否加入另看收益。

## 比较边界与后续验收

旧标签隔离保存、原件只读；新旧对照顺序及共同层级规则以[教师审核规则](../TEACHER_REVIEW_PROTOCOL.md)为准。已有工程、开发审核与未运行诊断的分母以[EXPERIMENTS](../EXPERIMENTS.md)为准。

后续对照须另存配置和结果，明确输入／词库／工作释义条件、模型revision、语言、截断或分块策略、上限和失败记录。至少记录：有依据的标签是否被候选环节漏掉；原文证据与角色是否正确；待审／拒判是否增加；实际token、延时、内存和复核成本。20条开发材料用于找问题，不承担全量准确率或训练费效比结论。本次仅查资料与维护文档，没有下载模型、训练、改变冻结材料或新增DeepSeek调用。
