import json
import time
import logging

import httpx

from app.config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID

logger = logging.getLogger(__name__)

FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_SEND_MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"

# 缓存 token
_token_cache = {"token": "", "expire_at": 0}


async def _get_tenant_access_token() -> str:
    """获取飞书 tenant_access_token，带缓存"""
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expire_at"]:
        return _token_cache["token"]

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            FEISHU_TOKEN_URL,
            json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        )
        data = resp.json()

    if data.get("code") != 0:
        logger.error(f"Failed to get feishu token: {data}")
        raise Exception(f"Feishu token error: {data.get('msg')}")

    token = data["tenant_access_token"]
    expire = data.get("expire", 7200)
    _token_cache["token"] = token
    _token_cache["expire_at"] = now + expire - 300  # 提前5分钟刷新

    return token


async def send_sms_to_feishu(sms_data: dict) -> bool:
    """将短信内容发送到飞书群聊"""
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET or not FEISHU_CHAT_ID:
        logger.warning("Feishu config incomplete, skipping notification")
        return False

    try:
        token = await _get_tenant_access_token()

        # 构建消息内容：将所有字段格式化为文本
        lines = ["📱 收到短信"]
        for key, value in sms_data.items():
            lines.append(f"{key}: {value}")
        content = json.dumps({"text": "\n".join(lines)}, ensure_ascii=False)

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                FEISHU_SEND_MSG_URL,
                params={"receive_id_type": "chat_id"},
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json; charset=utf-8",
                },
                json={
                    "receive_id": FEISHU_CHAT_ID,
                    "msg_type": "text",
                    "content": content,
                },
            )
            result = resp.json()

        if result.get("code") != 0:
            logger.error(f"Feishu send message failed: {result}")
            return False

        logger.info("SMS forwarded to Feishu successfully")
        return True

    except Exception as e:
        logger.error(f"Feishu notification error: {e}")
        return False
