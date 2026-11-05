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

### 同日扩大实验的方法补充

[#16](https://github.com/normaltank/TagProject/issues/16)沿用上述固定revision，新增char 2–4gram TF-IDF与冻结表示线性头，查阅日期2026-10-31。[scikit-learn TfidfVectorizer官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)定义字符分析、sublinear TF及L2归一化，归一化向量点积可作cosine；[PyTorch 2.11 BCEWithLogitsLoss官方文档](https://docs.pytorch.org/docs/2.11/generated/torch.nn.BCEWithLogitsLoss.html)给出多标签logit损失。具体词表上限、均值池化、优化器／训练停止和工作点是本项目冻结协议，不是这些文档保证的效果。

共同L2直接分数与同路径L2+L3的max投影预先分开，投影保留child来源；头使用公共片段均值再归一化，检索仍maxchunk。因聚合、训练目标及模板也不同，路线差异不能全部归因于主干架构或训练本身。实测、弱标签目标与当前文本支持的错配、轻量训练收益及当前选择见[EXPERIMENTS的T-SCALE-01](EXPERIMENTS.md#t-scale-01扩大真实材料与冻结表示弱监督头)。

## 2026-11-01：生成、重排与同NLI任务适配的方法

按[#17](https://github.com/normaltank/TagProject/issues/17)新增两个官方固定checkpoint，查阅2026-11-01；只把公开任务能力当选型依据，不当教师效果。

- [Qwen3-1.7B模型卡](https://huggingface.co/Qwen/Qwen3-1.7B/blob/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e/README.md)：本地生成路线使用non-thinking聊天模板，FP16／batch1、greedy、最多384新token，完整简介及139 L2目录，输入≤8192不截断。输出最多一个合法标签／拒判和逐字quote；一次解析，无重发或语义修补。合法label即使quote失败也保留候选提名，输出门另要求schema、exactquote及非拒判。生成无校准标量分数，格式、引用存在、全文支持和证据充分分别审核。
- [Qwen3-Reranker-0.6B模型卡](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B/blob/e61197ed45024b0ed8a2d74b80b4d909f1255473/README.md)：采用官方分行Instruct／Query／Document及yes/no后缀，用最后位置yes/no logit归一化作分数。本人研究支持instruction是本项目固定任务条件；不能把一般相关性训练视作已识别任职、课程或他人研究。它与三版NLI都对公共窗口逐对评分、按max聚合，但只在四基线top1加合法生成提名的≤5共同池内排名，不是完整139类检索。

[PEFT LoRA官方接口](https://huggingface.co/docs/peft/v0.17.0/en/package_reference/lora)说明低秩适配与target_modules。本机固定PEFT0.17.1／accelerate1.11.0与原torch2.11.0+cu128／transformers4.57.6兼容，实际mDeBERTa-v2的query_proj/value_proj与PEFT映射一致。head-only仅更新原pooler/classifier；LoRA额外更新24个q/v模块的rank8／alpha16／dropout0参数，两者共享同任务头和旧90/30监督、模板、全窗口及选择规则，其他主干冻结。它与#16的139输出冻结表示线性头是不同任务配置。

NLI以`entailment_logit−logsumexp(other2)`作margin，case取全窗口最大margin后作二元BCEWithLogits，等价于最大entailment概率的二元BCE而数值更稳定。无据目标是固定文本不支持，不是现实领域的负事实。该多实例弱定位不保证winner是真证据；窗口最大分、全文标签支持和引用充分分开测量。max12／patience3仅据旧val最小BCE选epoch，最早tie；head lr5e-4、LoRA lr1e-4、共享头lr5e-4、AdamW weight_decay.01、effective batch8、seed20261101。实际可训参数、变化tensor、曲线和加载核验留在运行记录。

数据、代表、首次预测与校准门槛先冻结；新held不选提示／epoch／阈值。只在cal20选最大保留且至少5条、支持占保留≥90%的点，否则无自动建议。生成使用固定输出门，未满足同样支持目标也不形成自动建议。全文标签与原生窗口／quote分别匿名后审；头的检索窗口明确是辅助语境，不冒充头归因。分层组bootstrap及空条件分母按冻结协议记录。完整参数与官方权重元数据见本地[协议v2](../outputs/evidence_judge_20261101_v1/executor/protocol_v2.frozen.json)、[模型](../outputs/evidence_judge_20261101_v1/executor/models_v2.frozen.json)及[证据口径](../outputs/evidence_judge_20261101_v1/executor/evidence_quality_policy.frozen.json)。实测及用途取舍集中在[证据判别实验](EXPERIMENTS.md#t-evidence-01证据判别与同nli任务适配)。

在任何cal质量意见前另固定[生成组件离线消融](../outputs/evidence_judge_20261101_v1/executor/component_ablation_protocol.frozen.json)：共同池仅删除四基线均未提名、只由生成提名的label，四判别器直接过滤已存max分数、稳定重选top1，不新增forward／训练／生成。四个诊断配置用同一匿名池意见、同cal规则分别锁点，再用共享配对索引比较含／不含生成的收益。这不是又跑四个模型；原九路线／原池／原预测不变。生成实测耗时及权重成本单列为未来可省组件，减少的判别器序列量可精确计数，未重跑的子池耗时不称实测，也不从本次已用预算倒扣。

本轮取舍是继续保留低成本候选与全139覆盖，当前可直接复核的交付为去gen重排队列；现成NLI保留为独立证据判别对照，未验证重排后串NLI或四基线缺一不可。暂不保留当前生成支路或扩大该NLI LoRA。标签top1与联合证据的点值各有侧重，不能指定架构冠军；所有冻结点在held均未维持90%支持目标，成果统一待复核。具体分母、区间和限制以上述实测入口为准。

## 教师候选与总成本

### #20：多语输入对后续比较的约束

2026-11-01按[#20](https://github.com/normaltank/TagProject/issues/20)修正选型前提：PROJECT一直包含中文、外文及混写，不能把当前教师/稿件输入当成仅中文。完整代表的root AI核查确认英语教师叙述、英语稿件字段及字段间双语实际存在；来源、文字脚本分母和书目/缩写/网址边界集中在[DATA_AUDIT](DATA_AUDIT.md#2026-11-01多语输入与既有评价覆盖盘点)，不把存在性核查推成全表语种比例。Latin-heavy尤其可能是中文正文附英文书目。旧冻结评价尚无预先语种核实且单独计分的独立纯英子集，既有总体AI支持结果不能回答英文、真正混写或其他语言的相对效果。

沿用[2026-10-26技术扫描](research/OPEN_TECH_SCAN_20261026.md)记录的英语定位，UltraBERT不能仅因“本项目是中文任务”排除；它仍是未实跑的候选，是否适合英语输入、中文标签目录和本人研究证据任务须另测。这里修正适用性前提，不把历史扫描改写成新实测，也不据语言存在性指定新模型。BGE/Qwen、mmBERT、现成多语NLI等已测配置的公开多语覆盖，同样不等于本项目验证了所有语种或已找到多语最优。

后续若启动新比较，应对经实际语言/证据角色核查的中文、英文、正文混写及出现的其他语言分层，保留中文附英文书目与短URL噪声等诊断项；再单列“外文输入→现有中文词库”的跨语概念映射，区分标签召回/排序、本人研究归属、原文证据和拒判。当前词库没有完整多语别名，英语编码能力不能直接替代这项验证。旧#15–19阈值、推荐和冻结结果保持原样，本票不开展新模型、标签、稿件分类或师稿匹配实验。

### #19：传统/现代BERT冻结分类与专用encoder重排

2026-11-01核对三份固定官方模型卡：[google-bert/bert-base-chinese](https://huggingface.co/google-bert/bert-base-chinese/blob/8f23c25b06e129b6c986331a13d8d025a92cf0ea/README.md)为中文masked-language-model预训练、Apache-2.0；[jhu-clsp/mmBERT-base](https://huggingface.co/jhu-clsp/mmBERT-base/blob/c5955035435e2bf121cde7f3c8863ef52ff35d82/README.md)为多语ModernBERT主干、MIT；[BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3/blob/953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e/README.md)为成对相关性重排、Apache-2.0。官方语言覆盖和重排能力不能当作本项目研究归属识别效果。

[#19](https://github.com/normaltank/TagProject/issues/19)用标准Transformers `AutoModel`取两BERT最后隐藏层的非特殊有效token均值→L2，再以共同片段均值→L2作为139分类头输入；头训练沿#16v2旧弱目标/超参，主干不更新。专用BGE重排采用官方`AutoModelForSequenceClassification`的plain query/document pair和单logit sigmoid；旧Qwen仍用官方yes/no模板，两者固定同BGE头top5、同标签假设和公共窗。模板/任务训练/候选条件均不同，不能把结果差异全部归因于encoder或decoder架构；全139头和窄池判别分开解释。

复用原torch2.11.0+cu128/Transformers4.57.6，标准类、`trust_remote_code=False`、eval/inference_mode；ModernBERT用SDPA并固定`reference_compile=False`，不升级运行栈，接口依据[官方ModernBERT文档](https://huggingface.co/docs/transformers/v4.57.1/en/model_doc/modernbert)及本机4.57.6实现。mmBERT固定revision实际仅单一`pytorch_model.bin`，采用`weights_only=True`；不下载不存在的safetensors或另换权重。本项目明确的零非特殊token窗口边界、首运行失败和版本修订见本地协议附录/实验记录，不改原输入。

截至#19，原[技术扫描](research/OPEN_TECH_SCAN_20261026.md)的7个模型家族中，Qwen embedding/reranker已有实测，mmBERT在该票补测；GLiNER2.5、GLiClass当时未实跑，已在下述#21补测；UltraBERT、Nemotron3.5和Granite97M仍未实跑。传统中文BERT是#19补充的监督分类缺口；mMiniLM/MacBERT仅核候选元数据、不下载或增加组合。Annif、Label Studio、SKOS等是工具/治理项，不计作已测或未测checkpoint。实际完成范围及选择结论统一见[实验记录](EXPERIMENTS.md)。

本轮校准选择是mmBERT冻结头，held不回调该决定；held没有显示它在联合支持上超过旧BGE头的明确收益。中文BERT节省显存/编码成本，但本设置的全文支持低于旧BGE头；新BGE重排比同池Qwen实测更快，联合支持差区间仍包含0。保留便宜候选参考和版本化AI意见，不据弱val拟合或公开预训练能力扩大主干训练，也不将这些有界结果推广为BERT/encoder家族结论。分母、配对区间、不同候选条件与具体代价均以[实验实测](EXPERIMENTS.md#t-berttools-01中文bertmmbert与同池encoder重排)为准。

### 部署位置与训练程度是两个维度

部署位置可比较本地加载预训练权重推理与托管API；训练程度另比较直接使用、冻结表示后训练轻量分类头、编码器／小模型的任务微调，以及有条件的蒸馏。**本地运行不等于必须训练，微调也不等于从零预训练。** 托管服务也需区分直接调用与服务支持的定制方式，不能用“API”代替训练程度或质量条件。当前没有从零预训练的业务／数据／资源依据；部署位置、模型、训练方式均未最终选定。

### 已有BERT历史结果与当前DeepSeek候选

用户确认的BERT旧标签来源及尚不清楚的输入条件见[数据审计](DATA_AUDIT.md)。已有历史结果可作对照基线；“本轮未训练BERT”仅指尚未复现或新建S0／S1，不能理解为项目没有BERT赋标结果。冻结20条DeepSeek诊断及随后按[审核规则](TEACHER_REVIEW_PROTOCOL.md)进行的旧标签对照均已完成，结果见[EXPERIMENTS](EXPERIMENTS.md)的T-PILOT-02／T-BERT-01；下一步以[STATUS](STATUS.md)为准。

比较分两层：在共同概念层级上核查标签支持、遗漏与拒判；另行判断DeepSeek新增细方向、证据定位和可解释输出的价值。旧输出不含这些附加字段时，不据此认定旧模型分类错误或BERT架构无法提供证据。原模型输入、时间快照和训练／测试划分未确认，现阶段是历史结果对照，不是控制变量的模型排名。

**待验证判断：** 若旧方案是适配固定标签的小型分类器，应保留其批量效率和领域分类质量的竞争机会；DeepSeek优先验证复杂语境、细方向与证据判断是否带来实际增益，同时检查过度推断和遗漏。既有BERT训练投入已发生，替换决策应比较未来可避免成本、复核返工与维护，历史投入另报，不把旧输出视作可以免费持续更新。当前没有两者可比的质量、延时或总成本结果。

[Bucher与Martini的2024年研究](https://arxiv.org/abs/2406.08660)在其文本分类任务中发现任务微调的BERT类模型优于所测零样本生成模型（查阅2026-10-26）。其任务及模型不含本项目教师简介或当前DeepSeek，只支持“不预定大模型胜出”的实验立场。

### S：冻结表示与主干任务微调的多标签分类

保留BERT、RoBERTa、XLM-R等预训练编码器作为教师监督多标签分类候选：S0冻结表示，只训练轻量分类头；S1以教师任务答案微调分类头及选定主干参数，再比较增益是否覆盖标注、训练和维护成本。这里的“S”为方案标识。官方Transformers文档分别给出[BERT](https://huggingface.co/docs/transformers/en/model_doc/bert)、[RoBERTa](https://huggingface.co/docs/transformers/en/model_doc/roberta)、[XLM-RoBERTa](https://huggingface.co/docs/transformers/en/model_doc/xlm-roberta)的多标签序列分类接口／示例（查阅2026-10-23）；这是可实现性依据。#16已实际以BGE及Qwen冻结表示训练S0式弱监督头；当时S1未运行。#17另在原NLI上开展有界任务头／q/v LoRA对照，具体监督与方法按本页2026-11-01记录，不等同于完整教师多标签主干微调方案。

仅加载基础BERT权重不会自动得到适配本词库的受训分类头；冻结主干仍需训练任务分类头，而任务微调可以更新编码器参数，不能把两种配置混称“全部冻结”。官方[文本分类训练示例](https://github.com/huggingface/transformers/tree/main/examples/pytorch/text-classification)可作后续实现参考，本轮未运行。

S路线从有监督答案学习“简介／片段→既定标签集合”的判别；B路线用标签定义检索候选并重排“片段—概念”的相关性。两者可能使用相近编码器，但训练目标、标签变更方式和证据产出不同，不能把“使用BERT向量”当作已经验证监督分类。固定输出头遇新增／拆分标签可能需要新增训练样本、调整输出与重训；检索更新定义索引也仍需校准与验证，不能假定哪种总成本更低。

旧标签不能直接成为可信细粒度金标；#16已先以有来源弱监督实际训练，弱验证拟合与主Agent AI后审分列，独立真人研究质量仍需独立答案。S0/S1应单独检查长文聚合、实际语言、长尾／不均衡、词库变更和拒判。分类分数没有充分证据定位；不能以注意力或相似度替代角色／范围审核。#16保留轻量头收益并建议先修订本人研究角色、包含及缺漏，未在该票扩大主干适配；#17才按新授权重用其AI支持意见作分组任务适配和新材料比较。旧后审保持原样，重用后是已暴露开发监督，不能再当独立测试答案。

### 完整候选与工具分工登记

下表保留启动提示中的方法与工具，方法可以组合、工具各有职责；不是安装清单。既有工具功能、许可和边界的官方链接保留在下文对应条目，本表不新增适配结论。

| 候选／工具 | 在教师主线中的职责 | 当前保留方式与适用边界 |
| --- | --- | --- |
| 规则／关键词／传统文本分类（A） | 建立低复杂度基线，定位候选标签 | #16已运行TF-IDF候选基线，不以关键词命中认定稳定专长 |
| BERT／RoBERTa／XLM-R监督多标签分类（S） | 比较冻结表示＋轻量分类头、主干任务微调 | #16／19已跑冻结表示弱监督139头，#17有NLI任务头／LoRA；#23已复现旧论文BERT及教师迁移。目标2级完整教师监督适配仍未验证，见#27 |
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
- **D-08：按#16实测分别选用候选工具。** L2候选兼顾编码成本时选BGE轻量头，top10覆盖／细方向优先时选Qwen层级检索，词法继续作便宜基线；未证明两者串联或合并的额外收益。不将本轮试探工作点投产，也不据弱拟合扩大主干微调。数值、成对不确定性及条件见[扩大实验](EXPERIMENTS.md#t-scale-01扩大真实材料与冻结表示弱监督头)，不是不可更改的最终架构。

原决定的完整理由、替代方案以及 T1–T3／迁移设计见[设计档案](history/RESEARCH_DESIGN_20261023.md)。这些阶段性安排未追认成正式 ADR；新决定仅在满足[领域规则](agents/domain.md)的三项条件时创建 ADR。

## #21原生多语分类器的精确候选与接口（2026-11-02）

本轮实际固定两个原候选，不先因CPU服务器条件降档。[GLiNER2.5-multi-Decide官方卡](https://huggingface.co/fastino/GLiNER2.5-multi-Decide/blob/e173bca1f0c4217d7a55b3b0c705d5ece8a0218d/README.md)声明Apache2.0、约287M、多语mDeBERTa-v3-base/boundary分类specialist；其公开决策基准是英语，且不直接验证教师研究归属。[GLiClass multilang-ultra官方卡](https://huggingface.co/knowledgator/gliclass-multilang-ultra/blob/33c3ffec64056b0d37173d2dd90b885ac29b72c3/README.md)声明Apache2.0、约1.72B、多语与跨语标签，配置为mT5-XL encoder及cross-attention scorer。公开benchmark只作候选依据，本项目效果须依本轮支持审核。

本地API为gliner2 2.1.0的AutoExtractor.from_pretrained与原生Classifier评分，以及gliclass0.1.22的GLiClassModel和官方UniEncoder输入格式；新venv用transformers5.17，三基线继续旧4.57.6，不改变旧实现。新GLiClass载入报告的mT5嵌入别名缺项经官方tie_weights与完整共享张量逐值核对，实际有效嵌入等于checkpoint；失败尝试与修复另版保留。

在任何新材料分类前，按原生标签池化接口决定两新模型共同逐字使用已冻结document（名称＋原层级路径），任务说明直接复用#18的Qwen研究归属instruction；原三基线的embedding／query／hypothesis格式保持不变。同一正文和词库不称五路字面输入完全相同。全139标签按冻结顺序分块，技术普查以4个合成及全部1551真实窗的无评分token计数确定共同块2、batch8；8／4块在GLiNER分别达615／517token，2块最大475，GLiClass为319，均不裁原200码点窗口。独立sigmoid后全窗max只产生候选语境，不自行证明归属；标签块的上下文耦合与模型内部预处理是比较限制。首预测前的参数／来源hash和合成资源包络见本地`outputs/priority_accuracy_20261102_v1/executor/protocol.frozen.json`、`model_authority.frozen.json`、`complete_token_coverage.frozen.json`；实际质量结论另见[实验记录](EXPERIMENTS.md)。

在原五评分已开始、root尚未查看本轮模型与新标签对应关系且任何cal质量未开放时，另固定两个同模型对照：旧四top1窄池的Qwen完整简介判别，以及旧池并两新模型top1的扩池完整简介判别。前者复用旧窄池每标签max窗作辅助，后者逐值复用前者旧池整篇分数、只评分新增标签；新增标签的辅助窗按GLiNER优先、否则GLiClass的既有top1窗固定选择，不按质量挑窗。它们均native=null，不把辅助窗称整篇forward的原生归因。原五、六分别冻结、七配置最终另冻；只对最终匿名包后审一次，推荐规则仍为cal联合支持、全文S、非穷尽已知@3与固定顺序，耗时不参与。后两配置不是首次新评分前预注册，而是cal质量前有时间与来源记录的设计扩展；其目的分别是完整上下文和新增候选价值，不能把公开模型基准或旧样本结果当作本轮收益。

## #21当前方案与后训练决定（2026-11-03）

当前默认保留cal锁定的旧四直接top1并集→Qwen3-Reranker-0.6B逐窗排序与候选证据，输出实际可用top1–3进入审核。held只能检验此选择，不能用来重新选赢家或阈值；默认的cal高置信条件没有在held维持，故不扩大正式自动赋标。精确分母、配对描述区间和阈值迁移见[实际实验](EXPERIMENTS.md#t-priority-01准确性优先的多语原生分类与整篇对照)。

人工审核需要多方向补漏时，保留BGE全139头top3＋层级辅助作宽候选入口：其冻结初判参照覆盖高于默认，不能仅因联合差区间跨0就判无用；仍须核本人归属与返回窗，不宣称全方向召回。mmBERT联合支持数值较高但相对默认区间跨0，先保留研究比较，不据held改选。两新家族在此次精确配置没有证明应替换默认；扩池虽补足候选机会，未证明稳定联合收益，暂不自动加入默认链。同池整篇仅作上下文研究对照。替换默认或自动合池须在未暴露新组证明本人标签与证据联合支持的收益；本票未穷尽checkpoint、提示、其他工具或新L3配置。

目前不扩大后训练。#17小规模AI意见LoRA未证明稳定超过原NLI；#19中文BERT／mmBERT的冻结主干弱监督头也未证明应替代旧BGE，本票训练0。优先积累可信本人角色、范围纠错、遗漏与失败监督，按连通组隔离训练／验证和未暴露评价，再决定有界适配。万级旧S只是有来源弱监督，不作真值；不因长耗时获准就推定更大训练有效。

个人电脑GPU适合有界离线批量候选生成、逐例落盘与恢复，CPU服务器可接收版本化结果用于查询／审核；这是部署方向，尚未上线服务器。无GPU也可保留原精度模型做容许长时延的离线CPU推理，原精度两例可运行不等于必须降级；实际RAM／指令集／精度运行时须在目标服务器另测。GLiClass bf16在本机CPU很慢是成本事实，不作为质量淘汰标准。默认链CPU端到端未测，已有单例缓存池加最终forward回放不能作新输入服务吞吐；8GB显存共享、连续进程失败及恢复边界见实验记录，不保证所有同容量卡稳定驻留。

## #22前人BERT评价与公平擂台决定（2026-11-04）

前人已交付论文DS标签蒸馏、全参数任务微调、验证选点和可恢复批处理，具有可借鉴的工程价值；教师人工优化是否完成、是否产生当前教师旧S仍无来源链。最接近85%—88%的实物是高置信论文子集对DS的集合一致率，不能据此改选当前教师默认。数据与重算分母分别见[数据审计](DATA_AUDIT.md#2026-11-04前人bert实物与来源链)、[运行登记](EXPERIMENTS.md#t-predecessor-audit-01前人bert实物与指标只读审计)。[HFL官方模型卡](https://huggingface.co/hfl/chinese-roberta-wwm-ext)、[F1定义](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)及[多标签集合accuracy定义](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)由root于2026-11-04查阅；纯预训练底座不等于已有139标签任务头，官方能力不作本项目效果证明。

保持#21锁定候选／证据架构作为当前参赛者；旧论文checkpoint只作跨任务基线，历史教师人工优化模型待补实物，纯预训练加共享监督的基线另命名。拟议新票先核已有教师人工导出及版本，固定全新隔离教师输入／词库／人工答案，集合、首标签、证据、拒判覆盖分别评价；完整多标签解码须在新dev冻结，不能把#21 top1意见当集合冠军。边际成本计人工标注／纠错／复核、训练、推理与回退，并预定最小有用提升和停止门槛。完整[擂台与边际投入规格](../outputs/predecessor_bert_audit_20261104_v1/executor/DUEL_PROTOCOL.md)仅为下一票建议，本票不执行训练／新模型评分或恢复稿件支线。

## #23旧论文BERT实跑后的当前选择（2026-11-04）

按用户“实际打擂台”要求，#23用已有实物完成真实forward及同教师材料对照，结果支持继续保留#21的A候选／证据默认。B-prefix是预定主对手，其held全文标签支持低于A；完整token覆盖的B-overflow改善此前缀迁移，但仍未超过A。该胜负直接来自冻结root AI意见与配对结果，不只凭教师人工模型缺失作判断；分母、置信／覆盖／证据与描述区间集中见[实验记录](EXPERIMENTS.md#t-bert-duel-01旧论文bert实跑复现与教师迁移擂台)。不据本轮held改阈值、挑margin、自动合池或扩大正式赋标。

前人论文模型的已训练成果和高margin成绩确实可以实跑复现，不能说其85%—88%没有依据；该数字只支持已暴露论文保留子集对DS一致，不能移作教师真人准确率。教师迁移的前缀严重裁切、长文max、A窄池与B139池、监督及任务差异都保留，不把本次系统配置比较外推成整个BERT家族无效。B139的较宽候选保留补漏研究价值，完整覆盖辅助也说明不能只测前缀就下全部结论；但未审多标签和新窗口证据仍不能自动赋标。

本轮复用已暴露教师120、旧AI先判／后审，再由root另审新增标签，因此没有实现#22拟议的全新独立人工答案评测。A现阶段领先与“86%教师真人准确率尚未证明”同时成立。继续优先可信本人角色／概念范围纠错、遗漏和失败监督，补教师人工导出／checkpoint来源链并按组隔离未来训练与评价；有明确新范围和预算后再做未暴露独立验证或教师任务适配。当前不追加训练、合池、服务器部署或恢复稿件分类生产；A20回放只是缓存池最终分类的一致性／成本核查，不解决CPU服务器新输入端到端服务性能未知。

## #24Benchmark有效性与目标层级修正（2026-11-04）

用户已明确目标为2级secondary；旧引用L1/L2/L3对应用户0/1/2，定义与业务约定分别见[GLOSSARY](../GLOSSARY.md)／[PROJECT](PROJECT.md#当前用户要求)。#16–23主比较压到139个用户1级中类，故A在当前冻结AI首标签对照领先，只支持继续保留粗层候选诊断，不能宣布目标2级胜出。未来评价以有完整父路径／来源身份的2级多标签与证据为目标，1／0级祖先匹配独立计分。#24本地审计保持冻结；随后用户澄清模糊为简介与标签的标注关系，当前约定及原型见下节#25。

[本地审计报告与新评价设计](../outputs/benchmark_validity_audit_20261104_v1/executor/AUDIT_REPORT.md)逐项核查目标粒度、非穷尽方向、阈值后证据、概率抽样、意见复用／held暴露、训练来源隔离、原生拒判与统计、系统比较和真实复核投入。原件与旧成绩不改；下一轮需新未暴露输入和独立真人双标／审定，按组隔离并冻结开发及封存测试，具体指标组合／质量线和预算尚非既定验收。

方法来源于2026-11-04查阅的[Dwork等holdout复用](https://arxiv.org/abs/1506.02629)、[Datasheets原文](https://arxiv.org/html/1803.09010v8)、[LLM judge原文](https://arxiv.org/html/2306.05685v4)、[官方多标签指标](https://scikit-learn.org/stable/modules/model_evaluation.html)、[分组隔离](https://scikit-learn.org/stable/modules/cross_validation.html)及[校准原论文](https://arxiv.org/abs/1706.04599)，只作设计依据；逐来源支持范围、读取深度与机械证据均集中在报告，不以公开基准替代本项目效果。

## #25证据粒度与未来适审用途（2026-11-04）

用户已澄清模糊是简介→标签关系，根本用途是对应领域教师审对应领域论文。因此保留证据能支持的最具体概念，同时允许明确宽类直接成立，避免目标2级压力导致无据细化。宽细与scope_review分别表达；路径及来源保留同名差异，派生祖先不重复计为专长；审核细则集中见[审核规则](TEACHER_REVIEW_PROTOCOL.md#证据决定粒度与映射状态)。未由本票证明A、DeepSeek或其他模型是细标签冠军。

最小工程选择是新增模型无关离线profile，复用旧v2验证器的结构、角色声明及quote／路径定位，单独补本地0级引用、每个关联方向支持及直接／派生区分。旧实现、契约、数据和冻结结论只读；不搭新插件、治理平台或新ADR。root冻结13个合成语义判断，执行者只运行机械验证，结果入口见[实验记录](EXPERIMENTS.md#t-granularity-01证据决定粒度离线合同试运行)；它不是模型理解试验、真人金标或新Benchmark准确率。

未来师稿匹配应结合主题、问题、方法及成果证据：具体证据支持候选发现，宽类补充发现后核材料，不设“任意2级教师都比任意0／1级教师合适”的固定排序。共享父类不能证明具备所有子专长，简介宽泛也可能只是信息缺失。[PLOS ONE审稿人指引](https://journals.plos.org/plosone/s/reviewer-guidelines)的Invitation to Review要求相关研究专长，并考虑知识、时间及客观性（root于2026-11-04读取）；它只支持此业务方向，不证明本项目匹配效果或当前任何教师适审资格。

下一轮评价须分别报告有据细标签、正确宽粒度保留、越界细化、遗漏、证据支持及定位、拒判／待核，分清直接宽标签和派生祖先；不能以宽命中当细成功，也不将当前材料未知当现实无专长。最终还需未暴露输入与独立答案下的稿件—教师相关性、误配／漏人、合适教师覆盖及复核工作量，P@k等阈值另票确定。本票不重开真实稿件分类、生产匹配或自动邀请。

## #26目标2级细候选的固定开发比较（2026-11-05）

#26比较词法、BGE-M3、Qwen3-Embedding-0.6B及前三top10 fine并集的Qwen3-Reranker-0.6B，完整1396用户2级来源与174宽节点分报，旧139头不冒充细选手。root实际读取的[BGE-M3](https://huggingface.co/BAAI/bge-m3)、[Qwen embedding](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)及[Qwen reranker官方卡](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B)支持CLS／末有效token归一化、query/document区分、yes/no末token与left padding接口；具体字节／参数以本地冻结协议为准，不把公开能力当本项目效果。

在任何cal质量开放前，静态图发现祖先宽池缺19无子中类与艺术／设计两根，另冻／release补前三各top3 coarse减原池，原fine/coarse及212首预测不改。此修正恢复可达性，cal宽S15→14仍保留，不按成绩搜索池；无子分支也不证明该领域教师不能映射其他有据2级。

按预定cal细联合S锁Qwen（10/16，对照重排9/16），成本／宽表不参与。diag重排全文10／联合7，高于Qwen8／6；语言挑战7／4对4／2，保留其候选与补漏价值。固定重排−BGE联合差+18.75pp、95%描述区间[-6.25,+43.75]跨0，保留cal锁点而不宣布稳定最优。全部分层、宽修正与资源见[实验记录](EXPERIMENTS.md#t-fine-01目标2级细标签开发对照)；全1396排序不等全1396质量、长尾／全学科覆盖或完整多标签系统。

下一笔优先独立语义答案、本人角色、跨枝包含／限定与引用定位纠错，并在新独立材料上核验Qwen与重排差异，暂不扩大训练。后审漏映射说明源深度不构成跨枝语义细度全序；原60次非穷尽source映射不是60独立方向，原初判34／6与纠错35／5分列，不把初判缺项当N。当前40已开发暴露，真人空白手册仅备后续judge诊断，填写0；无未暴露test、正式赋标、服务器部署或稿件生产匹配结论，旧A粗层默认不改。

## #27最终候选边界与下一笔投入（2026-11-05）

**已核事实：** #26是三个直接候选排序配置，以及依赖三者各top10细候选并集的Qwen重排系统；宽池补充另版保留。Qwen embedding取向量相似度，没有生成方向／理由；四路均缺自动多标签解码、细／宽选择、拒判及正式阈值，#25的给定判断合同不替代这些决策。#23已真实运行旧论文139头、论文1000及教师120前缀／完整覆盖擂台，不能说BERT还没比；139个用户1级输出不能下推成1396个细标签。#12已测DeepSeek细映射，#17已测本地生成及NLI头／LoRA，#16／19有弱监督头，#18–21有多种判别／多语／整篇配置；本轮目标2级同条件完整语义决策仍未验证。具体源码、效果分母、历史限制和代价见本地[简短核验报告](../outputs/route_selection_audit_20261105_v1/executor/READINESS_AUDIT.md)。

**建议：** 无需先硬淘汰至一个才进BERT擂台。有限保留cal锁定Qwen直接候选、union重排和词法低成本锚点；BGE作为原union提名源的贡献另核，不自动删除或预设全部串联。旧BERT保留共同1级资产对照；目标2级／完整多标签与证据单独验证，若加细检索／判别／定位器，另命名增强系统并计全部组件成本。先解决独立答案、层级／输出合同与候选机会，再用一个既有可运行语义判别／生成配置做有界细层开发补测以证伪“高相似即可本人研究”；保留简单方案获胜机会，不承诺新增组件更准。新开发锁解码／阈值，未暴露评价只作预定比较；旧40可诊断judge误差，60次非穷尽映射不能充当完整方向／长尾答案。

**已核容量约束：** #17生成只能最多选一个139目录标签，不是现成完整细层系统。本票离线、无权重／forward的既有tokenizer计数：空简介的原139模板3179token；换1396细目录、仅最小改写层级文字已43592token，超过旧8192输入守卫和固定Qwen3-1.7B的40960位置配置，加旧384输出为43976。因此不能直接照搬全目录单次生成；候选缩减、分层分批或其他上下文／资源方案须先核容量、漏向与GPU／CPU代价，另命名系统。公式、tokenizer revision、渲染及来源hash见本地[容量记录](../outputs/route_selection_audit_20261105_v1/executor/catalog_capacity.json)；此计数不证明质量或8GB显存可运行。

**投入与待验证：** 优先独立方向、角色、概念范围、引用、细／宽保留与拒判纠错；完整集合漏标、语言／长文／长尾、全流量coverage、证据联合及复核工时一起评。仅在可信train/dev覆盖关键错误后比较同监督轻头与有界任务适配，未审pair不全置负，AI／DS／旧S不当独立真值。检索需维护索引／范围，生成需格式／漏项复核，细头需标注／长尾及词库变更重训；本机GPU结果和末级回放不证明CPU新输入端到端性能。准确性优先，CPU服务器条件不自动排除强模型，可比较GPU离线批量、长时延CPU及人工投入；微调收益和回本仍未知。未来实验／标注／资源只为建议，本票未执行，稿件生产匹配仍暂停。

**一手依据（实际查阅2026-11-05，共4唯一页）：** [QwenLM官方README](https://github.com/QwenLM/Qwen3-Embedding/blob/main/README.md)的Embedding／Reranker Transformers用法区分向量相似度与yes/no成对评分；[BERT官方分类接口](https://huggingface.co/docs/transformers/en/model_doc/bert#transformers.BertForSequenceClassification)给出`num_labels`维输出与多标签示例；[scikit-learn交叉验证导言／组隔离](https://scikit-learn.org/stable/modules/cross_validation.html)及[Dwork等原论文v2摘要](https://arxiv.org/abs/1506.02629)说明调参／自适应复用test的风险。这些只支持方法边界，不充当教师效果或最优架构证据；读取段落及不支持事项见上述报告页面账。

**经验：** 选型先核业务层级／完整输出、候选与输入覆盖、答案来源／隔离，再定位关键错误和最小补测；先查最可能推翻比较的假设。声称未试过某路线前查实际冻结运行，公开能力只形成待验证假设，深度以能改变下一步为止。

## #28完整语义判别补测的冻结边界（2026-11-05）

#28把两套#26固定候选交同一Pro high／8192 JSON语义判别，补本人方向、多标签、细／宽保留、scope_review、无标签、逐字quote及派生祖先合同。池只给选择机会，有限top10／top3及祖先不等全词库召回；旧40＋13已暴露，不能改称独立测试。教师旧清洗只核到设计线索，未建立函数／调用／输入版本／run／S绑定，不能把论文预处理或另写清洗冒充历史，也没有源／清洗因果对照。

比较规则在新预测前固定：root只在全部首响应／失败冻结后先审cal16，技术失败／unknown、错误supported、joint S细／宽及非穷尽known覆盖各自计量；仅一致Pareto优势可给临时后续优先，否则保留原Qwen优先＋RR补充的取舍解释，更多拒判不是自动优势。linked方向／逐引文未核或U不作joint S，不依diag／语言／合成改池、提示、模型或比较规则。实际因未知预留触预算停止，root已审全部101 raw声明、独立复算并锁incomplete/U取舍：保留C1后续优先＋RR补充，dominance=None。cal未完整、其他组全未尝试，不据部分宽层增益宣告完整系统优越。下一步先补独立监督、教师清洗源链、请求状态可追溯及完整输出可用性，再另定有界验证；本票不追加推理／训练。用量、错误类型及限制见[实验记录](EXPERIMENTS.md#t-complete-01完整赋标有限试跑)与[本地结果](../outputs/complete_decision_pilot_20261105_v1/executor/RESULTS.md)。

## #29前人方法继承与教师公平适配（2026-11-05）

前人论文线有真实DS监督全模型微调和可恢复批处理；教师交接也已提出证据、充分度、prior_only／unknown及论文模型继续retrain。当前源码对k=2已有第二标签概率支路，并认识到低margin可能是真多标签；批判应落在具体gate、标签数先验、不可逆信息筛选、同源监督评价和教师适配验证，不能概括为前人没意识到这些问题。教师4000是条目数，人工完成量、清洗／S绑定及教师retrain实物仍缺；论文高置信成绩和#23直接迁移不代替它们。完整阅读范围、实物／设计／未知及当前已有能力见[方法评议](../outputs/predecessor_method_review_20261105_v1/executor/REVIEW.md)。

下一笔建议保留“旧论文encoder→教师继续微调”与“相同通用底座→教师微调”的对称对照，和Qwen直接候选／有限union重排完整方案比较；#16／19冻结头、#17 NLI LoRA、#23直接迁移都未回答该精确问题。当前0／1／2级、完整输入、同可用train-dev、未审pair mask、身份／近重组隔离与未暴露test共同冻结，标签和证据能力分评，并计拒判覆盖、失败、语言／长尾、全流程及复核成本。先检验单模型是否足够，额外组件、困难例分流及后续蒸馏只在有增值时保留；同质量下按组件、标注、算力、复核和维护衡量简洁，不预定检索或BERT胜出。样本数与资源仅待后续定界，当前训练／新推理／正式赋标均0，#28未知费用预留不释放，稿件支线仍暂停。

2026-11-05执行者实际读取[BERT官方分类接口](https://huggingface.co/docs/transformers/en/model_doc/bert)、[Qwen官方用法](https://github.com/QwenLM/Qwen3-Embedding/blob/main/README.md)、[SelectiveNet摘要](https://proceedings.mlr.press/v97/geifman19a.html)、[蒸馏原文摘要](https://arxiv.org/abs/1503.02531)及[组隔离／开发测试官方说明](https://scikit-learn.org/stable/modules/cross_validation.html)；root独立核查STILTs、校准及OpenAlex等一手方法。它们支持候选原理与评价边界，不证明本项目最佳；实际段落、未读全文／失败页和支持范围集中在报告及阅读账。OpenAlex训练复杂链可压成运行时student的启发也只作为后续简化假设。
