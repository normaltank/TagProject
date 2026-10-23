# Issue tracker: GitHub

仓库：https://github.com/normaltank/TagProject
需求、规格和任务统一记录为此仓库的 GitHub Issues。

- 优先使用可用的 GitHub 工具；gh 可用时也可使用。
- 发布规格或任务：创建 Issue。
- 读取任务：读取正文、标签和评论；更新前核对最新状态。
- 多行正文使用结构化工具参数；使用 gh 时通过 UTF-8 文件和 --body-file 提交。
- 状态标签见 triage-labels.md；关闭任务时保留完成证据和相关提交链接。
- 拆分任务优先使用子 Issue；不可用时以父任务清单和 Part of #编号关联。
- 依赖优先使用原生依赖关系；不可用时记录 Blocked by: #编号。
- 规格作为父 Issue，实施票作为子 Issue；认领、回答及完成证据留在对应任务。拆票时保留规格正文与开启状态，不以派工评论代替任务。
- 公开内容采用脱敏说明；原始教师资料、运行明细和密钥留在本机。

PRs as a request surface: no.

阶段与文档职责见 [workflow](workflow.md)。已确认规格发布后，仓库只保留入口；本地草稿冻结为历史，不作为第二份任务状态。
