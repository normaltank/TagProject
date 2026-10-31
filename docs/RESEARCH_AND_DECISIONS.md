# 教师路线、工具依据与选型记录

本页维护候选方案、官方依据及选择理由。外部资料默认查阅时点为2026-10-23，后续补充另注日期；历史发行信息保留为当日记录，使用前按需要复核。实际结果统一见[EXPERIMENTS](EXPERIMENTS.md)，当前任务见[STATUS](STATUS.md)。

## 2026-10-26补充调查

[近期开放技术调查](research/OPEN_TECH_SCAN_20261026.md)核查GLiNER2.5、UltraBERT、Nemotron 3.5及较早的多语编码器／检索模型，区分发行时间、权重与代码许可、中文适用限制。当时建议按实际错误选择证据抽取或候选检索的小样对照，未运行且未改变当时D-07及 #3→#4→#5 顺序；这三票现已完成，当前阶段见[STATUS](STATUS.md)。新旧标签的对照顺序见[审核规则](TEACHER_REVIEW_PROTOCOL.md)。

## 旧对话方法讨论（2026-10-30归档）

来源为旧对话最近的六视角讨论及交叉质疑，接手来源与读取范围保存在[#13](https://github.com/normaltank/TagProject/issues/13)对应本地证据。**用户要求**将encoder-only、embedding及其他decoder-only方案纳入比较，并从不同行业和观点讨论；用户对BERT“擅长读”的看法是讨论起点，不是本项目效果结论。以下仅归档已有建议，没有新增实测或最终选型。

**旧 Agent 调整后的建议**是让编码器监督分类、embedding判别和decoder方案独立竞争，允许不接生成模型的简单方案获胜；此前“下一票优先检索＋DS”的建议已调整。冻结编码器＋轻量分类头／任务微调、独立embedding匹配判别、decoder直接分类或判别配置均保留候选地位；架构、训练目标与承担的工作分别考虑，不默认把全部组件串成主系统。历史BERT仍是有来源限制的对照，输入未知时不作同条件排名。

共同判别问题是“提到领域”能否支持“教师研究该领域”：保留课程、本人研究活动、他人研究等证据角色与归属，检查主题相关但归属错误、方法外推及已有上位类遗漏。针对反复争议的少量标签补包含／排除范围说明也是建议，无需先重构全库，工作释义不自动成为正式定义。比较须分别衡量共同L2层级上的支持与覆盖、L3细化的有用价值；更细或更多不自动算好，共同L2相等也不证明细标签正确。同时记录无据标签、遗漏、拒判、整条隔离及复核负担，按下文总成本口径计入准备、训练、纠错和定义／标签变化后的维护；更便宜不是唯一胜出条件，额外投入需有可接受的质量收益。

旧 Agent 提出的四步串行探索顺序仅为待审建议：先冻结判别材料和规则；再测词法检索、encoder embedding与decoder embedding等低投入路线的候选覆盖和最终赋标；继而盘点可信样本、评估监督分类可行性；最后让decoder比较完整简介与统一证据片段条件，判断额外增益来自证据识别还是标签映射。旧16例、旧20条和新10条继续只作开发诊断，不能转为独立测试答案。

**截至该次归档尚未决定**具体模型／配置、同条件输入和标签范围版本、未暴露材料与独立答案、分层评价、质量／总成本门槛、预算及扩大规模条件。该归档本身不授权训练、下载、分类调用或新对照，不把上述顺序追认为用户已确认的规格；随后单独授权的本地试跑方法见下节，独立验证和扩大规模条件仍未定。

## 2026-10-31本地试跑的方法依据

按[#15](https://github.com/normaltank/TagProject/issues/15)固定三个公开checkpoint，查阅日期2026-10-31。以下只说明模型任务和本轮实现依据；实际分母、覆盖、耗时及结论集中在[EXPERIMENTS的T-LOCAL-01](EXPERIMENTS.md#t-local-01三个本地模型的共同开发材料试跑)，不把官方能力或许可当本项目效果。

- [MoritzLaurer/mDeBERTa-v3-base-mnli-xnli固定模型卡](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli/blob/8adb042d524ecd5c26d3e3ba0e3fbcf7e2d0864c/README.md)，revision `8adb042d524ecd5c26d3e3ba0e3fbcf7e2d0864c`：多语encoder上的现成MNLI/XNLI分类头，使用`AutoModelForSequenceClassification`，按config读取entailment／neutral／contradiction三类并逐文本对softmax。它不是本项目监督分类头，也不复现历史BERT。卡中提示不支持FP16，因此本轮三者统一FP32。
- [BAAI/bge-m3固定模型卡](https://huggingface.co/BAAI/bge-m3/blob/5617a9f61b028005a4858fdac845db406aefb181/README.md)，revision `5617a9f61b028005a4858fdac845db406aefb181`：只测dense encoder embedding；卡说明query无需额外instruction，[池化配置](https://huggingface.co/BAAI/bge-m3/blob/5617a9f61b028005a4858fdac845db406aefb181/1_Pooling/config.json)与[模块配置](https://huggingface.co/BAAI/bge-m3/blob/5617a9f61b028005a4858fdac845db406aefb181/modules.json)分别指定CLS和归一化。本轮以标准`AutoModel`取CLS并L2归一化，不装FlagEmbedding或加载稀疏／ColBERT头。该官方revision只有`pytorch_model.bin`，格式例外在#15留证，以新版PyTorch的`weights_only=True`加载；另外两者取官方safetensors。
- [Qwen/Qwen3-Embedding-0.6B固定模型卡](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3/README.md)，revision `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`：decoder embedding，按官方Transformers示例使用左padding、last-token pooling及L2归一化；query带英文任务instruction，标签文档不加instruction。卡要求Transformers至少4.51，本轮关闭不需要的生成cache。

运行依赖按[PyTorch官方本地安装说明](https://pytorch.org/get-started/locally/)选择CUDA wheel，安装在项目新runtime，不改全局环境或驱动。三个模型均用标准Transformers类、`trust_remote_code=False`、`eval`和`inference_mode`，匿名下载后仅本地推理；精确文件、权重SHA和依赖版本见本地[模型冻结](../outputs/model_pilot_20261031_v1/executor/models.frozen.json)、[下载核验](../outputs/model_pilot_20261031_v1/executor/models.download.json)及[环境](../outputs/model_pilot_20261031_v1/executor/environment.frozen.json)。

本轮统一标签文档为“末级名称（层级路径：完整路径）”，NLI假设为“这位教师本人研究的领域是{label_name}（上位领域：{parent_path}）。”；Qwen的英文query指令在[冻结配置](../outputs/model_pilot_20261031_v1/executor/config.frozen.json)保存。embedding精确评分全部合法引用，L2直接排名，不把L3最大值投影替代L2分数；NLI对各假设独立保留三类概率，不跨全部标签softmax，entailment>=0.5仅为预注册、未校准的临时诊断规则。三者按公共片段max聚合；高相似度不等于研究支持，winner片段仍需角色与归属核查，长简介的max偏差和跨段限制保留。

这些checkpoint的训练任务、池化和模板不同，只支持本批开发诊断，不作架构因果排名。旧DeepSeek的托管权重revision未核实，历史BERT输入也未知；不能由现成NLI头的结果排除教师监督encoder分类路线，也不预设embedding后必须接DeepSeek。独立答案、未暴露材料和质量／总成本门槛仍需另定。

## 教师候选与总成本

### 部署位置与训练程度是两个维度

部署位置可比较本地加载预训练权重推理与托管API；训练程度另比较直接使用、冻结表示后训练轻量分类头、编码器／小模型的任务微调，以及有条件的蒸馏。**本地运行不等于必须训练，微调也不等于从零预训练。** 托管服务也需区分直接调用与服务支持的定制方式，不能用“API”代替训练程度或质量条件。当前没有从零预训练的业务／数据／资源依据；部署位置、模型、训练方式均未最终选定。

### 已有BERT历史结果与当前DeepSeek候选

用户确认的BERT旧标签来源及尚不清楚的输入条件见[数据审计](DATA_AUDIT.md)。已有历史结果可作对照基线；“本轮未训练BERT”仅指尚未复现或新建S0／S1，不能理解为项目没有BERT赋标结果。冻结20条DeepSeek诊断及随后按[审核规则](TEACHER_REVIEW_PROTOCOL.md)进行的旧标签对照均已完成，结果见[EXPERIMENTS](EXPERIMENTS.md)的T-PILOT-02／T-BERT-01；下一步以[STATUS](STATUS.md)为准。

比较分两层：在共同概念层级上核查标签支持、遗漏与拒判；另行判断DeepSeek新增细方向、证据定位和可解释输出的价值。旧输出不含这些附加字段时，不据此认定旧模型分类错误或BERT架构无法提供证据。原模型输入、时间快照和训练／测试划分未确认，现阶段是历史结果对照，不是控制变量的模型排名。

**待验证判断：** 若旧方案是适配固定标签的小型分类器，应保留其批量效率和领域分类质量的竞争机会；DeepSeek优先验证复杂语境、细方向与证据判断是否带来实际增益，同时检查过度推断和遗漏。既有BERT训练投入已发生，替换决策应比较未来可避免成本、复核返工与维护，历史投入另报，不把旧输出视作可以免费持续更新。当前没有两者可比的质量、延时或总成本结果。

[Bucher与Martini的2024年研究](https://arxiv.org/abs/2406.08660)在其文本分类任务中发现任务微调的BERT类模型优于所测零样本生成模型（查阅2026-10-26）。其任务及模型不含本项目教师简介或当前DeepSeek，只支持“不预定大模型胜出”的实验立场。

### S：BERT类编码器的监督多标签分类（本轮复现／训练未开展）

保留BERT、RoBERTa、XLM-R等预训练编码器作为教师监督多标签分类候选：S0冻结编码器表示，只训练轻量分类头；S1以教师任务答案微调分类头及选定编码器参数，再比较增益是否覆盖标注、训练和维护成本。这里的“S”仅为方案标识，不是已选模型或新系统。官方Transformers文档分别给出[BERT](https://huggingface.co/docs/transformers/en/model_doc/bert)、[RoBERTa](https://huggingface.co/docs/transformers/en/model_doc/roberta)、[XLM-RoBERTa](https://huggingface.co/docs/transformers/en/model_doc/xlm-roberta)的多标签序列分类接口／示例（查阅2026-10-23）；这是可实现性依据，不是本项目适配或准确率证明，具体checkpoint仍待选择。

仅加载基础BERT权重不会自动得到适配本词库的受训分类头；冻结主干仍需训练任务分类头，而任务微调可以更新编码器参数，不能把两种配置混称“全部冻结”。官方[文本分类训练示例](https://github.com/huggingface/transformers/tree/main/examples/pytorch/text-classification)可作后续实现参考，本轮未运行。

S路线从有监督答案学习“简介／片段→既定标签集合”的判别；B路线用标签定义检索候选并重排“片段—概念”的相关性。两者可能使用相近编码器，但训练目标、标签变更方式和证据产出不同，不能把“使用BERT向量”当作已经验证监督分类。固定输出头遇新增／拆分标签可能需要新增训练样本、调整输出与重训；检索更新定义索引也仍需校准与验证，不能假定哪种总成本更低。

旧标签不能直接成为可信细粒度金标；训练和测试需要教师独立人工答案，弱标签另标来源与核验状态。S0/S1必须单独检查长简介的分段与聚合、实际语言和跨语言、长尾样本／多标签不均衡、词库变更和拒判。分类分数本身不提供充分证据，仍需原文片段定位、证据角色／持续性核验；不能以注意力或相似度直接替代证据可靠性审核。后续可先设计有界训练可行性试验来测量质量增益与成本，不要求已经证明训练有效才允许试验；正式扩大再依据实测决定。当前没有运行S0/S1，也没有足够证据排除或认定其优于A/B/C。

### 完整候选与工具分工登记

下表保留启动提示中的方法与工具，方法可以组合、工具各有职责；不是安装清单。既有工具功能、许可和边界的官方链接保留在下文对应条目，本表不新增适配结论。

| 候选／工具 | 在教师主线中的职责 | 当前保留方式与适用边界 |
| --- | --- | --- |
| 规则／关键词／传统文本分类（A） | 建立可接新简介的低复杂度基线，定位证据与候选标签；必要时比较BM25、TF-IDF和轻量分类器 | 后续对照候选；未实施自动标签基线，不以关键词命中直接认定稳定专长 |
| BERT／RoBERTa／XLM-R监督多标签分类（S） | 比较冻结表示＋轻量分类头、任务微调 | 已有用户确认的历史BERT赋标结果；本轮S0／S1未训练，复现条件未核实，另检长文、多语、长尾、标签变更与证据 |
| 标签定义的多语语义检索＋重排（B） | 召回与排序现有概念，结合原文证据判断 | 保留重点验证；模型、阈值和成本未定，不预定胜出 |
| LLM直接分类／先提内容再映射（C） | 比较语义提取、角色判断与受约束概念映射 | 当前已实现DeepSeek API小样工具；本地LLM保留，扩大仍需质量和总成本证据 |
| 弱监督／伪标签／半监督 | 利用未标数据或有来源的弱信号补充训练 | 数据与训练策略；须筛选噪声、分层人工核验，不替代独立测试 |
| 主动学习 | 优先选择值得专家审核的教师案例 | 兼顾错误、不确定性、长尾和多样性；需证明节省人时而未牺牲覆盖 |
| Teacher–Student／蒸馏 | 在教师模型已可靠时研究低成本Student | 非预定主架构；控制Teacher偏差和错误传播，不能由同一Teacher充当唯一裁判 |
| Annif | 自有词库自动标引与多配置比较的框架 | 可承载部分方法，不是新词库或一个固定模型；语言取决于后端与分词，当前未部署 |
| Sentence Transformers | 表示、语义检索、重排及相关训练组件 | 是组件库，不等于一套已适配的分类器；语言范围随checkpoint，当前未安装／实测 |
| VocBench＋SKOS | VocBench用于概念编辑／审校；SKOS为概念、标签与关系的交换标准 | 平台部署暂缓；教师标签的最小定义、别名、范围与来源记录仍需推进，SKOS不是需要安装的模型 |
| BERTopic＋人工审核 | 发现可能未覆盖的主题／短语，进入人工提案 | 仅候选发现；不自动建正式标签，不用测试资料反向完善词库后报提升 |
| pySHACL | 在采用RDF表达时执行已制定的词库约束 | 不自动制定语义规则或判断新标签价值；非RDF阶段可保留等价轻量校验 |
| Label Studio | 人工标注方向、证据与概念映射的界面候选 | 标注工具不等于金标；版本／社区版控件、原文偏移和导出仍需验证，当前未部署 |
| MeSH | 词表记录类型、同义表达与组合治理参考 | 医学领域参考，不照搬为全学科教师标签库或效果证明 |
| CSO Classifier | 词法／语义结合与学术主题识别参考 | 默认计算机领域及其资源，不能直接视为全学科、多语教师专长方案 |
| OpenAlex | 大规模主题赋标、Teacher–Student与保留历史版本的实践参考 | 保留已核查v2及其模型裁判、主主题和长尾限制；公开成绩不作本项目结果 |

暂停的是完整词库重构和整套平台建设，**不是暂停教师任务所需的全部词库维护**。应围绕实际用到的标签整理最小定义、包含／排除范围、必要别名、跨语同义与证据审核状态，先记录歧义和候选、经审核再采用；不要求先修完全库，也不自动把每个研究短语转成新概念。

### 同质量门槛下比较总费效比（尚无实测结论）

比较A/S/B/C时先约定相同的教师标签语义、测试对象、误标／漏标、证据可靠性、有用覆盖和人工复核要求；不能用大量拒判换低误标率，或让某路线接受更低质量后只比推理单价。独立答案及按对象／语言／长尾分层的评价为共同依据；本批16条开发示例不承担这个独立测试角色。

总成本需同时计入：标注／仲裁与数据准备、实验／调参和训练等固定投入；本地推理／API／算力和存储；人工复核、纠错及错误返工；定义／标签／数据变化后的更新、重训、重新校准与运维。标注成本按各路线实际用途和可复用程度核算，不能把训练数据与证据审核的人力一概当免费，也不能忽略无需训练方案的定义维护和审核成本。

在共同质量门槛、相同时间范围和输入分布下，才可比较固定投入F与每条全流程平均成本v，研究训练方案额外固定投入能否被后续处理量N所摊薄。若每条成本没有下降，就不能仅凭摊薄成本论证扩大；不达共同质量底线的方案也不能只靠便宜获选。质量显著提升但成本略高、且业务愿意承担的方案，可以另按质量收益与可接受预算论证其价值，不把每条成本下降设为唯一条件。处理量、更新频率和人工纠错率变化时应重新估算。当前没有实测的经济性或盈亏平衡结论；样本数、checkpoint、硬件与价格均待后续选择，不预定B/C胜出，也不预定训练一定更划算。

## 官方事实：来源方法、时效与许可边界

版本使用连接器直接GET官方GitHub `repos/{owner}/{repo}` 与 `releases/latest`，而非搜索缓存。`logs/research/github_metadata_20261023.json`保存检索URL、发布日期、archive状态与主代码许可元数据；官方正文快照见同目录。以下7仓库均未archived、未disabled；这些只说明查阅时仓库状态／发行记录，不证明质量、语言覆盖或适配本项目。没有安装整套工具。

API的Annif许可为NOASSERTION，进一步阅读其LICENSE.txt才确认主代码Apache-2.0。其他工具的代码许可按仓库元数据核查；模型权重、外部词库、训练数据、依赖和商用功能应分别核实，不从代码许可推断整个方案的权利。第一阶段当时仅研究、没有向外部API提交教师文本；本次另行授权的DeepSeek两次小样调用见当前操作文档。

### Annif：自有词库的标引框架

官方最新稳定发行[v1.4.3](https://github.com/NatLibFi/Annif/releases/tag/v1.4.3)，2026-10-22发布；[主代码LICENSE.txt](https://raw.githubusercontent.com/NatLibFi/Annif/main/LICENSE.txt)为Apache-2.0。官方[Project configuration](https://github.com/NatLibFi/Annif/wiki/Project-configuration)明确同vocab标识的多个项目共用已载入词库，支持多语言SKOS／CSV；语言参数控制建议标签语言。实际文本支持还取决于backend和[Analyzer](https://github.com/NatLibFi/Annif/wiki/Analyzers)，其分词通常按语言配置。不能因多语词库就推断任意语种文本已可识别。

本项目可借其多配置共库、算法比较与批量标引接口；教师持续专长证据、稿件主题证据、拒判、审核、源文偏移和版本迁移仍需项目层实现。监督backend需要可信训练实例；现有旧标签不能未经核验直接承担训练和测试两种角色。是否采用框架取决于原型收益，不是架构前提。

### Sentence Transformers：检索与重排组件

官方[v6.2.0](https://github.com/huggingface/sentence-transformers/releases/tag/v6.2.0)，2026-10-21发布，主代码Apache-2.0。[模型列表](https://sbert.net/docs/sentence_transformer/pretrained_models.html)按checkpoint列语言范围，例如distiluse-v1为15种，v2及部分paraphrase模型为50+；LaBSE偏翻译对齐，不能把其覆盖数量当学术主题适配证明。官方[Retrieve & Re-rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)使用独立编码召回候选，再对文本对联合打分。

适合用规范名、别名、定义、排除例构造概念检索文档，新增概念可重建索引；仍需实际语种、长文本分段、跨领域同名和长尾验证。库不自带本项目概念库，不自动给出真实证据或校准置信度。具体checkpoint／重排器、revision、许可和截断上限在实验开始前冻结；2026-10-23调查时未下载或选定唯一模型，后续固定候选见本页2026-10-31方法记录，该试跑未使用Sentence Transformers库。另用Context7定位到同一官方检索重排文档，未把第三方摘要当效果证据。

### SKOS与VocBench：概念治理参考／可选编辑平台

[W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)是2009-08-18 Recommendation：用URI标识概念，支持带语言的prefLabel／altLabel、定义、broader／related与跨方案映射。它提供语义交换模型，不规定本项目必须三级、必须树结构或必须用RDF数据库。稳定ID与多语同概念是用户要求；持久化方式仍可在关系表、版本化JSON／CSV与RDF之间选择。

VocBench官方[历史页](https://vocbench.uniroma2.it/doc/history.jsf)说明VB3以BSD-3-Clause发布，并面向多语、协作、审核；[版本文档](https://vocbench.uniroma2.it/doc/user/versioning.jsf)描述封存版本、切换和分支。[界面国际化页](https://vocbench.uniroma2.it/doc/sys/internationalization.jsf)说明UI本地化机制，不能与词汇多语言混为一谈。本端history／versioning直读遇502／超时／ConnectError，改从官方页面搜索索引获取正文；查阅结果有缓存时差，未独立核准其当前最新软件发行号。引入前还需直接复核发行包许可、依赖、中文编辑体验和导出流程。

适用于概念治理复杂到需要多人角色和审校流的阶段；当前可以先用最小版本化概念注册表检验语义，不因平台功能多就提前部署整套服务。

### Label Studio：人工证据与概念映射界面候选

官方[1.23.2](https://github.com/HumanSignal/label-studio/releases/tag/1.23.2)，2026-09-29发布，主代码Apache-2.0。官方[Taxonomy](https://labelstud.io/tags/taxonomy)描述层级选择及祖先路径、perRegion；[Labels](https://labelstud.io/tags/labels)支持文本区域标记及多标签。可设计先提证据／内容单元、再映射概念的两个盲审步骤。

当前文档能力不等于已在本地社区版1.23.2验证；`labeling=true`等联合片段／层级功能、稳定ID回写、Unicode偏移与导出需小样实测。多人审核、仲裁、访问管理可能涉及版本／产品差异，未承诺社区版具备完整业务流。若组合控件不适用，可分两步导出再以内部内容单元ID连接，不能牺牲独立基准。

### BERTopic：候选发现

官方[v0.17.4](https://github.com/MaartenGr/BERTopic/releases/tag/v0.17.4)，2025-12-03发布，主代码MIT。[Embedding文档](https://maartengr.github.io/BERTopic/getting_started/embeddings/embeddings.html)说明可替换表示模型与模块；多语表现随表示模型和文本处理而变。用于开发集中的未覆盖短语／主题发现，输出聚类与词项进入提案队列。聚类稳定性、分词、噪声导航、频率偏倚和标签审核成本需另测，不能自动转为正式新概念或用测试集发现词库后再报提升。

### pySHACL：规则执行器

官方[v0.40.1](https://github.com/RDFLib/pySHACL/releases/tag/v0.40.1)，2026-07-28发布，主代码Apache-2.0。[README](https://github.com/RDFLib/pySHACL)定义其为对RDF图执行SHACL约束的验证器。适用于已选择SKOS/RDF交换后检查项目制定的发布规则；它不自动判别学术同义、粒度或是否应增加概念。ID唯一、定义必填、语言规范名、废弃映射、应用规定的无环层级等规则需先有治理约定；其中项目规则不能都宣称由SKOS强制规定。非RDF存储可先做等价本地校验，不必先部署RDF栈。

### MeSH与CSO Classifier：治理与领域识别边界

NLM官方[MeSH Record Types](https://www.nlm.nih.gov/mesh/intro_record_types.html)（2026-03-24复核）区分Descriptor、Qualifier、SCR和组合表达。可借鉴“并非每个短语都成为主类”、不同记录类型和增量维护；医学词库的组织规则不能照搬全学科项目。本次不导入MeSH数据，其数据再利用条款及映射适配未核准，NLM页面不是软件维护或本项目效果证明。

CSO Classifier官方[v4.0.1](https://github.com/angelosalatino/cso-classifier/releases/tag/v4.0.1)，2026-04-18发布，主代码Apache-2.0。[README](https://github.com/angelosalatino/cso-classifier)说明输入标题、摘要、关键词，结合词法／语义与上位主题处理，默认针对Computer Science Ontology，安装会使用英语spaCy资源。可借其领域词库映射思路；不能直接当全学科、多语或教师持续专长分类器。更换领域需要相应词库与语义资源，CSO本体／模型许可和跨语种适配需分别核查，未完成本地实测。

### OpenAlex：已核查2026年10月v2

官方最新发行[v2.0.0](https://github.com/ourresearch/openalex-topic-classification/releases/tag/v2.0.0)，2026-10-06发布。本次从[main分支API](https://api.github.com/repos/ourresearch/openalex-topic-classification/branches/main)核实commit `98df3b96c36128819075dd86949c9f18411fab40`，阅读其固定版本[v2 README](https://github.com/ourresearch/openalex-topic-classification/blob/98df3b96c36128819075dd86949c9f18411fab40/v2/README.md)：检索／shortlist／Teacher数据后训练Qwen3-8B分类头，题目体系与ID不变，改变赋标。代码MIT、数据CC0、分类器权重Apache-2.0，分别列明；检索器及依赖还应单独核查。

官方明确主测试集无人类标注，主结果基于两个模型一致的子集；只benchmark主主题，罕见主题有限制，旧新任务定义也不同。其“已校准”“高吞吐”和公开准确率只针对其数据、答案与硬件，**不能作为本项目指标**。有价值的是独立评测、任务定义变化和保留旧赋标快照的启示；不构成本项目必须采Teacher–Student或沿用其4516主题的理由。v1/BERT不是其当前全部实践。

## 当前选择与替代记录

- **D-01／D-02：旧优先级已被 D-07 替代。** 原计划先 A／B、后 C，原因是输入问题与可信答案不足；当前按用户要求先接入 DeepSeek，保留其他路线作后续对照。
- **D-03：未来正式概念需稳定身份。** 当前保留来源行／路径／出现位置，尚未分配正式概念 ID；正式 ID 形式待库治理时决定。
- **D-04：平台按需引入。** 目前以版本化范围提案与本地审核验证价值；多人治理或交换需求足以覆盖维护成本时再考虑 VocBench／RDF 等平台。
- **D-05：独立验证防泄漏原则保留。** 当前模型开发意见不充当独立答案；后续独立评测需冻结数据分组、词库语义和验证方式。
- **D-06：Teacher–Student 是候选。** 只有质量、噪声筛选及总成本证据支持时才考虑扩大，同一 Teacher 不同时充当唯一训练答案来源和唯一测试裁判。
- **D-07：用户要求优先 DeepSeek 小样接入。** 该工具已实现；连通记录不代表最终选型胜出，后续诊断仍按教师审核规则执行。

原决定的完整理由、替代方案以及 T1–T3／迁移设计见[设计档案](history/RESEARCH_DESIGN_20261023.md)。这些阶段性安排未追认成正式 ADR；新决定仅在满足[领域规则](agents/domain.md)的三项条件时创建 ADR。
