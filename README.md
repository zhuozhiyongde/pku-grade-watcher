# 北京大学成绩自动查询

鉴于刷半天树洞全是 xxx 出分了没，便有了这个小工具。

## 功能

-   🚀 全自动查询成绩更新
-   ⏰ 每天定时查询成绩，再无需手动刷半天
-   📢 Bark 通知，让你随时随地知道自己考咋样 ~~寄了没、老师调没调~~

## 简要上手教程

首先，随便新开一个 **私有** 仓库（除非你想让所有人都能看到你的成绩，否则别设为公开）。

然后，按照如下流程设置环境变量：

1. 您需要生成一个 [个人 API 令牌](https://github.com/settings/tokens/new)，然后在仓库的 `Settings -> Secrets and variables -> Actions -> Secrets -> Repository secrets` 中添加如下变量：
    - `API_TOKEN`：个人 GitHub API 令牌
    - `USERNAME`：学号
    - `PASSWORD`：密码
    - `BARK`：Bark 令牌
2. 请注意，由于需要提交更新后的成绩数据到你的仓库，你还需要在 `Settings -> Actions -> General -> Actions permissions -> Workflow permissions` 中启用 `Read and write permissions` 权限。

最后，在仓库中创建 `.github/workflows/watcher.yml` 文件，内容如下（以每 10 分钟查询一次为例）：

```yml
name: pku-grade-watcher

on:
    push:
        branches:
            - main
    workflow_dispatch:
    schedule:
        - cron: '*/10 * * * *'

jobs:
    watcher:
        runs-on: ubuntu-latest
        steps:
            - name: pku-grade-watcher
              uses: zhuozhiyongde/pku-grade-watcher@latest
              with:
                  api-token: ${{ secrets.API_TOKEN }}
                  username: ${{ secrets.USERNAME }}
                  password: ${{ secrets.PASSWORD }}
                  bark: ${{ secrets.BARK }}
                  git-name: Github Action
                  git-email: actions@users.noreply.github.com
                  git-message: 'chore(updates): updated data'
```

## 免责说明

1. 本项目仅提供自动查询成绩功能，节省同学时间。
2. 因网络环境问题，不保证查询成功。
3. 仅供学习交流使用，**别设置太快的查询频率人造 DDoS 导致被封号**。
