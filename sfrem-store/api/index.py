from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SFREM STORE - HypeSquad Tool</title>
    <style>
        body { background-color: #0f172a; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #1e293b; padding: 30px; border-radius: 12px; display: inline-block; max-width: 400px; width: 90%; box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-top: 40px; border: 1px solid #334155; }
        h1 { color: #38bdf8; margin-bottom: 5px; }
        p.subtitle { color: #c084fc; font-weight: bold; margin-bottom: 25px; }
        input, select, button { width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: none; box-sizing: border-box; }
        input { background: #334155; color: #fff; text-align: center; }
        select { background: #334155; color: #fff; text-align: center; }
        button { background: #a855f7; color: white; font-weight: bold; cursor: pointer; }
        button:hover { background: #9333ea; }
        .result { margin-top: 15px; font-weight: bold; padding: 10px; border-radius: 6px; background: #0f172a; }
    </style>
</head>
<body>
    <div class="card">
        <h1>SFREM STORE</h1>
        <p class="subtitle">Discord HypeSquad Tool</p>
        
        <form method="POST">
            <input type="text" name="token" placeholder="أدخل توكن الحساب (Discord Token)" required>
            <select name="house">
                <option value="1">House of Bravery 💜</option>
                <option value="2">House of Brilliance ❤️</option>
                <option value="3">House of Balance 💚</option>
                <option value="delete">حذف الشارة (Delete Badge)</option>
            </select>
            <button type="submit">تطبيق التغيير</button>
        </form>

        {% if message %}
            <div class="result">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
@app.route('/api/index', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        token = request.form.get('token')
        house = request.form.get('house')
        
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        url = "https://discord.com/api/v9/hypesquad/online"
        
        try:
            if house == "delete":
                res = requests.delete(url, headers=headers)
                if res.status_code == 204:
                    message = "✅ [SFREM STORE] تم حذف الشارة بنجاح!"
                else:
                    message = f"❌ فشل العملية: {res.status_code}"
            else:
                res = requests.post(url, headers=headers, json={"house_id": int(house)})
                if res.status_code == 204:
                    message = "✅ [SFREM STORE] تم تغيير الشارة بنجاح!"
                else:
                    message = f"❌ فشل العملية: {res.status_code}"
        except Exception as e:
            message = "⚠️ حدث خطأ بالاتصال!"
                
    return render_template_string(HTML_TEMPLATE, message=message)

