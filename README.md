# 北京大学成绩自动查询自部署永续运行版

鉴于刷半天树洞全是 xxx 出分了没，便有了这个小工具。

## 功能

-   🚀 全自动过门户验证，查询成绩更新
-   ⏰ 每分钟查询一次成绩，再无需手动刷半天
-   📢 Bark 通知，让你随时随地知道自己考咋样 ~~寄了没、老师调没调~~

![sample](README.assets/sample.png)

## 简要上手教程

```bash
# 克隆项目
git clone https://github.com/zhuozhiyongde/pku-grade-watcher.git

# 切换到 self-deployment 分支
git checkout self-deployment

# 进入项目目录
cd Grade-Watcher

# 复制 config_sample.yaml 为 config.yaml
cp config_sample.yaml config.yaml
```

然后，修改 config.yaml 中的 username、password 和 bark 字段。

```bash
tmux new -s Grade-Watcher
python main.py
```

在成功设置好后，你应当能接收到一条初始化通知：

![init](README.assets/init.png)

如果你的手机并非 iOS，那么你可以尝试 fork 本项目并在 `session.py` 中实现其他的 Notifier。

## 免责说明

1. 本项目仅提供自动查询成绩功能，节省同学时间。
2. 因网络环境问题，不保证查询成功。
3. 仅供学习交流使用，**别设置太快的查询频率人造 DDoS 导致被封号**。