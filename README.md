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

### Linux 服务器部署

```bash
# 克隆项目
git clone https://github.com/hom/forwarder-service.git /data/forwarder-service
cd /data/forwarder-service

# 创建虚拟环境并安装依赖
python3 -m venv .venv
.venv/bin/pip install fastapi uvicorn python-dotenv httpx

# 配置环境变量
cp .env.example .env
# 编辑 .env 设置端口、飞书机器人等配置
```

#### Systemd 服务管理

```bash
# 安装服务
sudo cp forwarder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable forwarder
sudo systemctl start forwarder

# 常用命令
sudo systemctl status forwarder   # 查看状态
sudo systemctl restart forwarder  # 重启
sudo systemctl stop forwarder     # 停止
journalctl -u forwarder -f        # 查看实时日志

# 卸载服务
sudo systemctl stop forwarder
sudo systemctl disable forwarder
sudo rm /etc/systemd/system/forwarder.service
sudo systemctl daemon-reload
```

#### 更新部署

```bash
cd /data/forwarder-service
git pull
sudo systemctl restart forwarder

# 如果依赖有变化
.venv/bin/pip install fastapi uvicorn python-dotenv httpx
sudo systemctl restart forwarder
```

#### Nginx / Openresty 反向代理（可选）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## API 接口

### POST /api/forwarder

接收短信 JSON 数据，保存到 `data/` 目录。

请求示例：

```bash
curl -X POST http://localhost:8000/api/forwarder \
  -H "Content-Type: application/json" \
  -d '{"sender":"+8618888888888","message":"验证码123456","timestamp":"2026/05/12 22:55:21","local_number":"+8618888888888","remark":"无备注"}'
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
    "sender": "+8618888888888",
    "message": "验证码123456",
    "timestamp": "2026/05/12 22:55:21",
    "local_number": "+8618888888888",
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
