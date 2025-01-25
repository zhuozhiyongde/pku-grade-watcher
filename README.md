# 北京大学成绩自动查询

鉴于刷半天树洞全是 xxx 出分了没，便有了这个小工具。

## 功能

-   🚀 全自动过门户验证，查询成绩更新
-   ⏰ 每 10 分钟查询一次成绩，再无需手动刷半天
-   📢 Bark 通知，让你随时随地知道自己考咋样 ~~寄了没、老师调没调~~

![sample](README.assets/sample.png)

## 简要上手教程

首先，随便新开一个 **私有** 仓库（除非你想让所有人都能看到你的成绩，否则别设为公开）。

然后，按照如下流程设置环境变量：

1. 您需要生成一个 [个人 API 令牌](https://github.com/settings/tokens/new)，然后在仓库的 `Settings -> Secrets and variables -> Actions -> Secrets -> Repository secrets` 中添加如下变量：
    - `API_TOKEN`：个人 GitHub API 令牌
    - `USERNAME`：学号
    - `PASSWORD`：密码
    - `BARK`：Bark 令牌，用于通知成绩更新，请参见 [Bark 官网](https://bark.day.app/)，记得开启通知权限
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
              uses: zhuozhiyongde/pku-grade-watcher@v1.1.0
              with:
                  api-token: ${{ secrets.API_TOKEN }}
                  username: ${{ secrets.USERNAME }}
                  password: ${{ secrets.PASSWORD }}
                  bark: ${{ secrets.BARK }}
                  git-name: Github Action
                  git-email: actions@users.noreply.github.com
                  git-message: 'chore(updates): updated data'
```

在成功设置好后，你应当能接收到一条初始化通知：

![init](README.assets/init.png)

## 免责说明

1. 本项目仅提供自动查询成绩功能，节省同学时间。
2. 因网络环境问题，不保证查询成功。
3. 仅供学习交流使用，**别设置太快的查询频率人造 DDoS 导致被封号**。
4. 实际建议查询频率在 10~20 分钟左右。因为 GitHub Actions 免费版限制了每个工作流最多运行 35 天，而单次运行需要 30s 左右，所以：
    - 10 分钟的频率间隔总共可以运行约 700 天。
    - 15 分钟的频率间隔总共可以运行约 1050 天。
    - 20 分钟的频率间隔总共可以运行约 1400 天。
