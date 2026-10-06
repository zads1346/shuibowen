# 水波纹（shuibowen）

一个纯静态的摄像头手势水镜网页。手掌和指尖移动会在实时画面中激起涟漪，也可以直接用鼠标或触摸体验演示水面。

## 功能

- WebGL 水面折射、高光与动态涟漪
- MediaPipe 双手关键点追踪
- 水纹强度、恢复速度、镜像和前后摄像头设置
- 清空水面、全屏、摄像头关闭与重新开启
- 页面隐藏或离开时停止摄像头
- 可选 WebMCP 参数控制，只调整水纹参数，不会开启摄像头

## 本地运行

需要 Python 3；测试另需支持现代 JavaScript 的 Node.js（建议 18 或更新版本）。无需 npm 安装或构建。

```sh
git clone https://github.com/zads1346/shuibowen.git
cd shuibowen
python3 scripts/download-assets.py
python3 -m http.server 8000 --directory dist --bind 127.0.0.1
```

Windows 可将 `python3` 换为 `py -3`。打开 <http://localhost:8000>，点击“开启摄像头”并允许浏览器相机权限。摄像头一般仅能在 HTTPS 或 localhost 安全上下文使用，不要直接双击 HTML。手机通过局域网普通 HTTP 地址访问时可能无法启用相机。

下载脚本从固定版本上游获取两份 WASM 和手势模型（共约 27 MB），逐项验证 SHA-256。大二进制不放入 Git 历史；版本、网址和校验值保存在 `scripts/assets.json`。首次准备资源需要网络；准备后运行时从本站的 `dist/vendor` 加载资源，无需运行时 CDN 请求。未准备资源时仍可使用鼠标/触摸演示，但手势识别不可用。

部署时先执行下载脚本，再把完整 `dist/` 放到支持 HTTPS 的静态服务器，确保 `.wasm` 使用 `application/wasm` 类型。没有后端、账户系统或 API 密钥。

## 相机与隐私

应用代码只在用户主动点击后申请视频权限，不申请麦克风。画面和手部推理在当前浏览器本地处理；应用没有录制、照片保存、视频上传或分析统计逻辑。关闭摄像头、隐藏页面或离开页面会释放视频轨道。浏览器与部署平台自身的网络日志和隐私政策另行适用。

## 性能边界

波场为 144×108；渲染约上限 30 帧/秒，手部 CPU 推理最多 10 次/秒；渲染宽度限制 1280 像素，DPR 上限 1.5。以上是代码中的限制，不是实测性能承诺。实际效果取决于设备、浏览器、光照与手部遮挡，低性能手机可能卡顿或发热。手势加载失败后可继续使用鼠标/触摸。

## 检查与测试

资源准备完成后，在仓库根目录运行：

```sh
node --check dist/app.js
node tests/check.cjs
```

已执行：JavaScript 语法检查、两份 WASM 格式验证，以及模拟波场、指针输入、清空、设置、参数合法性和合成摄像头轨道释放检查。测试中的 DOM、WebGL、视频和手部模型使用替身，不能证明真实浏览器画面、GPU 着色器或手势识别效果。

尚未完成真实浏览器完整 UI 回归、真实手机相机与双手追踪测试。此仓库发布不表示这些检查已通过。

## 第三方资源与许可

- MediaPipe Tasks Vision 固定为 `0.10.21`，包括 `vision.mjs` 和 WASM 配套加载脚本；上游 Apache-2.0 许可原文保留在 `dist/vendor/LICENSE`，原包说明保留在 `dist/vendor/README.md`。
- [MediaPipe 上游项目](https://github.com/google-ai-edge/mediapipe) 与 [npm 包](https://www.npmjs.com/package/@mediapipe/tasks-vision/v/0.10.21)。`vision.mjs` 来自该包的 `vision_bundle.mjs`，仅重命名。
- 手势模型使用 Google 发布的 HandLandmarker float16 第 1 版。来源与校验值见下载清单；参见 [官方模型说明](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker)。模型独立于 JavaScript 包，使用和再分发应遵循其上游条款，不应把本仓库说明视为额外授权。
- 仓库未为原创页面代码另行指定开源许可证。仓库公开不等于自动授予额外的复制、修改或分发许可；第三方资源保持各自原有许可。

## 文件结构

```text
dist/                  可直接部署的页面和运行时资源目录
  app.js               波场、WebGL、摄像头与手势交互
  index.html           页面结构
  style.css            页面样式
  vendor/              固定版本 MediaPipe 资源与许可
scripts/assets.json    大资源地址与 SHA-256
scripts/download-assets.py
tests/check.cjs        合成环境检查
```
