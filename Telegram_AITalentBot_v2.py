import pdfplumber
import docx
import os
import google.generativeai as genai
import spacy
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import re

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

genai.configure(api_key=api_key)

nlp = spacy.load("en_core_web_sm")

# --- Global variable to store job description ---
job_description = "Cần tuyển Python intern researcher."

# --- Extract text from PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip() or "Không thể trích xuất nội dung từ PDF."

# --- Extract text from DOCX ---
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip() or "Không thể trích xuất nội dung từ DOCX."

# --- Escape special characters for MarkdownV2 ---
def escape_markdown_v2(text):
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)

# --- Analyze CV with AI Gemini ---
def analyze_cv_with_ai(cv_text, job_desc):
    prompt = f"""
    Bạn là một chuyên gia tuyển dụng (HR). Hãy đánh giá CV của ứng viên dựa trên mô tả công việc dưới đây.

    📄 **CV ỨNG VIÊN:**  
    {cv_text}  

    📌 **MÔ TẢ CÔNG VIỆC (JD):**  
    {job_desc}  

    🎯 **Đánh giá CV:**  
    - **Tóm tắt:** Ứng viên là ai? Chuyên môn chính?  
    - **Điểm phù hợp với JD (thang 10):**  
    - **Điểm mạnh:**  
      - Các điểm nổi bật  
    - **Điểm yếu:**  
      - Những kỹ năng còn thiếu  
    - **Cải thiện:**  
      - Làm gì để CV tốt hơn?  

    📌 **Trả lời ngắn gọn theo bullet points, dễ đọc, không lan man.**
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt])
    return response.text.strip()

# --- Format AI response for readability ---
def format_ai_response(ai_response):
    lines = ai_response.split("\n")
    formatted_text = ""

    for line in lines:
        line = escape_markdown_v2(line)  # Escape MarkdownV2 special characters
        line = line.replace("*", "-")  # Replace * with - for bullet points
        formatted_text += f"{line}\n"

    return formatted_text.strip()

# --- Handle PDF/DOCX files ---
async def handle_document(update: Update, context: CallbackContext) -> None:
    file = await context.bot.get_file(update.message.document.file_id)
    filename = update.message.document.file_name
    file_path = f"./{filename}"
    await file.download_to_drive(file_path)

    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        await update.message.reply_text("❌ Định dạng file không được hỗ trợ.")
        return

    if "Không thể trích xuất nội dung" in text:
        await update.message.reply_text(text)
        return

    ai_response = analyze_cv_with_ai(text, job_description)
    formatted_response = format_ai_response(ai_response)
    await update.message.reply_text(formatted_response, parse_mode="MarkdownV2")

# --- Handle job description update ---
async def set_job_description(update: Update, context: CallbackContext) -> None:
    global job_description
    new_jd = " ".join(context.args)
    if new_jd:
        job_description = new_jd
        await update.message.reply_text(f"✅ Mô tả công việc đã được cập nhật:\n{escape_markdown_v2(job_description)}", parse_mode="MarkdownV2")
    else:
        await update.message.reply_text("⚠️ Vui lòng nhập mô tả công việc mới sau lệnh /setjd")

# --- Handle general text messages ---
async def handle_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Tôi có thể giúp bạn đánh giá CV. Hãy gửi file PDF hoặc DOCX.")

# --- Handle `/start` command ---
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Chào bạn! Gửi file PDF hoặc DOCX để tôi trích xuất và đánh giá CV của bạn.")

# --- Start the bot ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setjd", set_job_description))
    app.add_handler(MessageHandler(filters.Document.PDF | filters.Document.DOCX, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Bot AI CV đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()