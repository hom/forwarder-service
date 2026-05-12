# Forwarder Service

一个基于 FastAPI 的 SMS 转发服务，接收 ESP32-S3 等设备 POST 的短信内容并保存到文件。

## 快速开始

### 本地开发

```bash
# 安装依赖
uv sync

# 复制环境变量配置
cp .env.example .env

# 启动服务（开发模式，设置 RELOAD=true 启用热重载）
RELOAD=true uv run python main.py
```

### Docker 部署

```bash
# 使用 docker compose 启动
docker compose up -d

# 或手动构建运行
docker build -t forwarder-service .
docker run -p 8000:8000 --env-file .env forwarder-service
```

### 服务器部署（aliyun-beijing）

项目部署在 `/data/forwarder-service`，通过 venv + openresty 反向代理运行。

```bash
# 首次部署
scp -r . aliyun-beijing:/data/forwarder-service
ssh aliyun-beijing 'cd /data/forwarder-service && python3 -m venv .venv && .venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi uvicorn python-dotenv'
ssh aliyun-beijing 'cd /data/forwarder-service && nohup .venv/bin/python main.py > app.log 2>&1 &'
```

#### 更新部署

代码推送到 GitHub 后，在服务器上拉取并重启：

```bash
ssh aliyun-beijing 'cd /data/forwarder-service && git pull && kill $(pgrep -f "python main.py"); nohup .venv/bin/python main.py > app.log 2>&1 &'
```

如果依赖有变化，需要重新安装：

```bash
ssh aliyun-beijing 'cd /data/forwarder-service && git pull && .venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi uvicorn python-dotenv && kill $(pgrep -f "python main.py"); nohup .venv/bin/python main.py > app.log 2>&1 &'
```

#### Openresty 配置

配置文件：`/etc/openresty/conf.d/forwarder.mengj.com.conf`

域名 `forwarder.mengj.com` 监听 80 端口（HTTP），反向代理到 `localhost:9631`。

## API 接口

### POST /api/forwarder

接收短信 JSON 数据，保存到 `data/` 目录。

请求示例：

```bash
curl -X POST http://forwarder.mengj.com/api/forwarder \
  -H "Content-Type: application/json" \
  -d '{"sender":"+8613800138000","message":"验证码123456","timestamp":"2026/05/12 22:55:21","local_number":"+8618610886029","remark":"无备注"}'
```

响应：

```json
{"status": "ok", "message": "saved", "file": "sms_20260512_225523_200485.json"}
```

保存的文件内容：

```json
{
  "received_at": "2026-05-12T22:55:23.200554",
  "data": {
    "sender": "+8613800138000",
    "message": "验证码123456",
    "timestamp": "2026/05/12 22:55:21",
    "local_number": "+8618610886029",
    "remark": "无备注"
  }
}
```

### GET /health

健康检查接口。

## 配置

通过 `.env` 文件配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| HOST | 0.0.0.0 | 监听地址 |
| PORT | 8000 | 监听端口 |
| LOG_LEVEL | info | 日志级别 |
| DATA_DIR | ./data | 短信数据存储目录 |
| RELOAD | false | 是否启用热重载 |
