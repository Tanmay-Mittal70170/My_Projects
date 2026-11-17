"""RescueRank Telegram bot: text, shared location pins and voice notes -> POST /ingest.

Run (after starting the backend):
    set TELEGRAM_TOKEN=<token from @BotFather>      (Windows cmd)
    py bot.py

Env:
    TELEGRAM_TOKEN   required, read from the environment only
    BACKEND_URL      default http://127.0.0.1:8000
    WHISPER_MODEL    default "small" (use "base" for a faster, less accurate model)
    WHISPER_LANGUAGE optional language code such as "hi" or "en"; empty = auto-detect
"""
import asyncio
import logging
import os
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone

import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
PIN_MEMORY_SECONDS = 60 * 60

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
# httpx/httpcore log full request URLs at INFO, and Telegram API URLs contain the bot token.
for noisy in ("httpx", "httpcore", "telegram", "telegram.ext", "hpack"):
    logging.getLogger(noisy).setLevel(logging.WARNING)
log = logging.getLogger("rescuerank-bot")

LAST_PIN = {}  # chat_id -> (lat, lon, saved_at)
_model = None
_model_lock = threading.Lock()


def get_model():
    global _model
    with _model_lock:
        if _model is None:
            from faster_whisper import WhisperModel
            size = os.environ.get("WHISPER_MODEL", "small")
            log.info("Loading Whisper model '%s' (first run downloads it)...", size)
            _model = WhisperModel(size, device="cpu", compute_type="int8")
        return _model


def transcribe(path: str) -> str:
    model = get_model()
    language = os.environ.get("WHISPER_LANGUAGE") or None
    segments, _info = model.transcribe(path, language=language, beam_size=5, vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments).strip()


def minutes_since(msg) -> float:
    try:
        return max(0.0, (datetime.now(timezone.utc) - msg.date).total_seconds() / 60.0)
    except Exception:
        return 0.0


async def post_ingest(payload: dict):
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(BACKEND_URL + "/ingest", json=payload)
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        log.error("Could not reach backend: %s", type(exc).__name__)
        return None


def build_reply(res: dict, transcript: str = "") -> str:
    rid = res["id"]
    lines = []
    if transcript:
        lines.append("🎙 Heard: " + transcript)
    if res.get("linked_to_earlier"):
        lines.append("✅ Added to your earlier request. ID: %s" % rid)
    elif res.get("merged"):
        lines.append("✅ Received. Request ID: %s\nOthers nearby reported the same need, so your "
                     "report was linked to the same request." % rid)
    else:
        lines.append("✅ Received. Your request ID is %s." % rid)
    fu = res.get("needs_follow_up") or []
    asks = []
    if "location missing" in fu:
        asks.append("• Share your location: tap 📎 then Location (अपनी लोकेशन भेजें)")
    if "people count missing" in fu:
        asks.append("• How many people need help? (कितने लोग हैं?)")
    if "need unclear" in fu:
        asks.append("• What do you need: rescue, medical, food, water or shelter? (क्या मदद चाहिए?)")
    if asks:
        lines.append("To help us reach you faster, please send:\n" + "\n".join(asks))
    lines.append("आपका अनुरोध दर्ज हो गया है। ID: %s" % rid)
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "RescueRank flood help line.\n"
        "Send a text or voice note (English / Hindi / Hinglish) saying what you need and how many "
        "people are with you, then share your location (📎 → Location).\n\n"
        "बताइए क्या मदद चाहिए, कितने लोग हैं, और अपनी लोकेशन भेजें।")


def attach_pin(chat_id: int, payload: dict) -> None:
    pin = LAST_PIN.get(chat_id)
    if pin and time.time() - pin[2] <= PIN_MEMORY_SECONDS:
        payload["lat"], payload["lon"] = pin[0], pin[1]


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    chat_id = update.effective_chat.id
    payload = {"text": msg.text or "", "channel": "telegram", "sender_id": str(chat_id),
               "lat": None, "lon": None, "minutes_ago": minutes_since(msg)}
    attach_pin(chat_id, payload)
    res = await post_ingest(payload)
    if res is None:
        await msg.reply_text("We could not reach the control room just now. Please try again in a minute.")
        return
    await msg.reply_text(build_reply(res))


async def on_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    chat_id = update.effective_chat.id
    loc = msg.location
    LAST_PIN[chat_id] = (loc.latitude, loc.longitude, time.time())
    payload = {"text": "", "channel": "telegram", "sender_id": str(chat_id),
               "lat": loc.latitude, "lon": loc.longitude, "minutes_ago": minutes_since(msg)}
    res = await post_ingest(payload)
    if res is None:
        await msg.reply_text("We could not reach the control room just now. Please share your location again in a minute.")
        return
    await msg.reply_text(build_reply(res))


async def on_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    chat_id = update.effective_chat.id
    media = msg.voice or msg.audio
    transcript = ""
    try:
        tg_file = await context.bot.get_file(media.file_id)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "voice.ogg")
            await tg_file.download_to_drive(path)
            transcript = await asyncio.to_thread(transcribe, path)
    except Exception as exc:
        log.error("Voice transcription failed: %s", type(exc).__name__)
    payload = {"text": transcript, "channel": "telegram", "sender_id": str(chat_id),
               "lat": None, "lon": None, "minutes_ago": minutes_since(msg)}
    attach_pin(chat_id, payload)
    res = await post_ingest(payload)  # still logged when the audio was unclear: never drop a request
    if res is None:
        await msg.reply_text("We could not reach the control room just now. Please try again in a minute.")
        return
    reply = build_reply(res, transcript)
    if not transcript:
        reply = "We could not understand the voice note. Please type your message or record it again.\n" + reply
    await msg.reply_text(reply)


def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        sys.exit("TELEGRAM_TOKEN environment variable is not set.")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(MessageHandler(filters.LOCATION, on_location))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, on_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    log.info("RescueRank bot running; backend at %s", BACKEND_URL)
    application.run_polling()


if __name__ == "__main__":
    main()
