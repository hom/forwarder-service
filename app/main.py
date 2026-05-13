import json
import logging
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import DATA_DIR
from app.channels import send_sms_to_feishu

logger = logging.getLogger(__name__)

app = FastAPI(title="SMS Forwarder Service")


@app.post("/api/forwarder")
async def forwarder(request: Request):
    """接收转发的短信内容并保存到文件，同时推送到飞书"""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Invalid JSON body"})

    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = DATA_DIR / f"sms_{timestamp}.json"

    # 写入文件
    record = {
        "received_at": datetime.now().isoformat(),
        "data": body,
    }
    filename.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    logger.info(f"SMS saved: {filename.name}")

    # 转发到飞书
    feishu_ok = await send_sms_to_feishu(body)

    return JSONResponse(
        content={"status": "ok", "message": "saved", "file": filename.name, "feishu": feishu_ok}
    )


@app.get("/health")
async def health():
    return {"status": "healthy"}
