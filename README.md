# Forwarder Service

一个基于 FastAPI 的 Python API 服务，接收 POST `/api/forwarder` 请求。

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

## API 接口

### POST /api/forwarder

接收 JSON 数据并返回确认。

```bash
curl -X POST http://localhost:8000/api/forwarder \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
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
| RELOAD | false | 是否启用热重载 |
