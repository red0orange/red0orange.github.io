# Zhijian's Website

This is a Jekyll website for Zhijian Qiao's academic homepage.

## To run locally (not on GitHub Pages, to serve on your own computer)

1. Clone the repository and made updates as detailed above
1. Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
1. Run `bundle install` to install ruby dependencies. If you get errors, delete Gemfile.lock and try again.
1. Use the Jekyll server management script:

```bash
# Start server (recommended - default action)
npm run dev
# or
./jekyll-server.sh        # 默认启动服务器
./jekyll-server.sh start  # 明确启动服务器

# Other commands
./jekyll-server.sh stop     # 停止服务器
./jekyll-server.sh restart  # 重启服务器
./jekyll-server.sh status   # 查看服务器状态
./jekyll-server.sh help     # 显示帮助信息
```

**Note:** The script automatically handles port conflicts and prevents the "directory already being watched" error. When run without parameters, it defaults to starting the server.

```
# Navigation
_data/navigation.yml
_pages/about.md
_pages/publications.html

# Tutorials
_pages/markdown.md
```
