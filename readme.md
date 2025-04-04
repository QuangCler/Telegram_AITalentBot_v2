# AI Talent Sourcing Telegram Bot

## 📌 Giới thiệu
Đây là một chatbot Telegram sử dụng AI để phân tích và đánh giá CV dựa trên mô tả công việc của nhà tuyển dụng. Bot hỗ trợ nhận dạng và trích xuất nội dung từ các file PDF và DOCX, sau đó sử dụng mô hình AI để đánh giá độ phù hợp của ứng viên với vị trí công việc.

## 🔧 Công nghệ sử dụng
- **Python 3.9+**
- **Telegram Bot API**
- **Google Gemini AI API**
- **pdfplumber** (để xử lý PDF)
- **python-docx** (để xử lý DOCX)
- **spaCy** (để phân tích ngôn ngữ tự nhiên)
- **dotenv** (để quản lý biến môi trường)

## 🚀 Chức năng chính
### 1️⃣ Phân tích CV
- Người dùng gửi file PDF hoặc DOCX chứa CV.
- Bot sẽ trích xuất nội dung và sử dụng AI để đánh giá CV dựa trên mô tả công việc hiện tại.
- Trả về phản hồi dưới dạng Markdown với điểm số và gợi ý cải thiện.

### 2️⃣ Cập nhật mô tả công việc
- Lệnh `/setjd <mô tả công việc>` cho phép người dùng cập nhật JD (Job Description) mới.
- Mô tả công việc được lưu trữ và sử dụng trong các lần đánh giá CV tiếp theo.

### 3️⃣ Xử lý tin nhắn văn bản
- Khi người dùng gửi tin nhắn không phải file, bot sẽ hướng dẫn cách sử dụng.

### Click vào ảnh để tới trang youtube coi DemoDemo
[![Xem video demo](https://github.com/QuangCler/Telegram_AITalentBot_v2/blob/main/demo.png)](https://youtu.be/0oltPutdLrk)
## ⚙️ Cài đặt và chạy bot
### 1. Cấu hình biến môi trường
Tạo file `.env` và thêm các thông tin cần thiết:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

### 2. Cài đặt thư viện cần thiết
Chạy lệnh sau để cài đặt các thư viện:
```
pip install -r requirements.txt
```

### 3. Chạy bot
```
python your_script_name.py
```

## 🔥 Hướng dẫn sử dụng
1. Gửi file PDF hoặc DOCX chứa CV để bot phân tích.
2. Nếu muốn thay đổi mô tả công việc, sử dụng lệnh:
   ```
   /setjd Cần tuyển Python intern researcher.
   ```
3. Nhận phản hồi đánh giá CV với các tiêu chí: điểm mạnh, điểm yếu, gợi ý cải thiện.

## 📌 Ghi chú
- Bot chỉ hỗ trợ định dạng PDF và DOCX.
- Nội dung CV cần có văn bản rõ ràng để trích xuất thành công.
- AI đánh giá dựa trên thông tin hiện có, không đảm bảo tính chính xác 100%.

## 📞 Liên hệ
Nếu bạn gặp vấn đề hoặc có đề xuất cải tiến, vui lòng liên hệ với chúng tôi!

