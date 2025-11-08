from flask import Flask, render_template, jsonify, request
from openai import OpenAI, api_key
from dotenv import load_dotenv
from dashscope.audio.asr import Recognition
from http import HTTPStatus
import tempfile
import requests
import os

# 加载.env文件中的环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 基本路由
    @app.route('/')
    def login():
        # 传递环境变量给前端模板
        firebase_config = {
            'apiKey': os.environ.get('FIREBASE_API_KEY', ''),
            'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', ''),
            'projectId': os.environ.get('FIREBASE_PROJECT_ID', ''),
            'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', ''),
            'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', ''),
            'appId': os.environ.get('FIREBASE_APP_ID', ''),
            'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID', '')
        }
        return render_template('login.html', firebase_config=firebase_config)
    
    # 用户主页路由
    @app.route('/userhome')
    def userhome():
        # 传递环境变量给前端模板
        firebase_config = {
            'apiKey': os.environ.get('FIREBASE_API_KEY', ''),
            'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', ''),
            'projectId': os.environ.get('FIREBASE_PROJECT_ID', ''),
            'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', ''),
            'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', ''),
            'appId': os.environ.get('FIREBASE_APP_ID', ''),
            'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID', '')
        }
        amap_config = {
            'security_code': os.environ.get('AMAP_SECURITY_CODE', ''),
            'web_api_key': os.environ.get('AMAP_WEB_API_KEY', '')
        }
        return render_template('userhome.html', firebase_config=firebase_config, amap_config=amap_config)
    
    # 导航页面路由
    @app.route('/navigation')
    def navigation():
        # 传递环境变量给前端模板
        firebase_config = {
            'apiKey': os.environ.get('FIREBASE_API_KEY', ''),
            'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', ''),
            'projectId': os.environ.get('FIREBASE_PROJECT_ID', ''),
            'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', ''),
            'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', ''),
            'appId': os.environ.get('FIREBASE_APP_ID', ''),
            'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID', '')
        }
        amap_config = {
            'security_code': os.environ.get('AMAP_SECURITY_CODE', ''),
            'web_api_key': os.environ.get('AMAP_WEB_API_KEY', '')
        }
        return render_template('navigation.html', firebase_config=firebase_config, amap_config=amap_config)
    
    # 健康检查端点
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "message": "Travel Agent API is running"})
    
    # API路由示例
    @app.route('/api/user/profile', methods=['GET'])
    def get_user_profile():
        # 这里将在后续实现真实的用户资料获取逻辑
        return jsonify({
            "message": "User profile endpoint",
            "implementation": "To be implemented with Firebase integration"
        })
    
    # 注册新用户API端点
    @app.route('/api/auth/register', methods=['POST'])
    def register_user():
        # 这里将在后续实现真实的用户注册逻辑
        return jsonify({
            "message": "User registration endpoint",
            "implementation": "To be implemented with Firebase Authentication"
        })
    
    # 用户登录API端点
    @app.route('/api/auth/login', methods=['POST'])
    def login_user():
        # 这里将在后续实现真实的用户登录逻辑
        return jsonify({
            "message": "User login endpoint",
            "implementation": "To be implemented with Firebase Authentication"
        })
    
    # AI生成旅行计划API端点
    @app.route('/api/ai/plan', methods=['POST'])
    def getAIplan():
        # 获取请求中的计划内容
        data = request.get_json()
        plan_text = data.get('planText', '')
        ai_plan_text = ''
        print('AI生成计划中...')
        try:
            client = OpenAI(
                # 从环境变量读取API密钥
                api_key=os.environ.get('DASHSCOPE_API_KEY', ''),
                # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            completion = client.chat.completions.create(
                model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                messages=[
                    {'role': 'system', 'content': '''你是一个旅行规划专家。你需要根据用户的需求，安排每一天的行程、交通、饮食和住宿等。
                    请使用清晰且简洁的语言风格，不要使用emoji，方便用户随时查看旅行计划。
                    如果用户没有提及预算，请默认预算为中等偏上。如果用户的预算太少，请先说明用户预算过少，之后以最低预算进行规划。
                    如果用户没有提及人数，请默认1人出行。
                    示例： 用户：我一个人去南京旅行2天，帮我制定一个详细的旅行计划。
                    助理：
                    用户的计划是一个人在南京旅行2天，建议选择在新街口或夫子庙附近的酒店，交通方便，预算约300元/晚，2天共600元。
                    以下是详细旅行计划：
                    第一天：
                    9:00 - 12:00：明孝陵，地铁2号线至苜蓿园站，步行或乘坐景区观光车前往，景区联票100元
                    12:00 - 13:30 ： 漫步陵园路，在南京大排档进行午餐，预算150元
                    13:30 - 17:00：美龄宫 & 中山陵，步行或乘坐景区观光车前往，中山陵需预约
                    17:30 - 19:00：夫子庙，地铁2号线转3号线至夫子庙站，晚餐可选择当地特色小吃，预算100元
                    19:30 - 21:00：秦淮河夜游，乘坐游船，欣赏两岸夜景，记得提前前往，预算100元
                    第二天：
                    9:00 - 12:00：南京博物院，乘坐地铁2号线至明故宫站后步行前往，需预约参观
                    12:00 - 13:00：博物院附近午餐，也可以出来后在中山东路上找家小店解决，预算50元
                    13:30 - 16:00：鸡鸣寺 & 玄武湖公园，乘坐地铁2号线转3号线至鸡鸣寺站，游览鸡鸣寺后从解放门进入玄武湖公园，鸡鸣寺门票10元
                    16:30 - 21:00：新街口，乘坐地铁至新街口站，晚餐可在随意一家商场内的餐厅解决，德基广场里有一家很出名的“桂满陇”江浙菜，环境很好，预算200元。
                    之后可逛街购物，可以去看一眼德基广场800万的厕所。
                    总预算：住宿600元 + 景点门票110元 + 餐饮500元 + 交通50元 = 1260元'''},
                    {'role': 'user', 'content': plan_text}
                    ]
            )
            ai_plan_text = completion.choices[0].message.content
            print('AI生成成功')
        except Exception as e:
            print(f"错误信息：{e}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
            ai_plan_text = 'AI生成失败'    # 返回"AI生成"字符串作为示例
        return jsonify({
            "planText": ai_plan_text
        })
    
    # 语音识别API端点
    @app.route('/api/audio/transcribe', methods=['POST'])
    def transcribe_audio():
        from dashscope.audio.asr import Recognition
        from http import HTTPStatus
        import tempfile
        import os
        import subprocess
        
        # 获取上传的音频文件
        audio_file = request.files.get('audio')
        
        if not audio_file:
            return jsonify({"error": "没有提供音频文件"}), 400
        
        # 保存音频文件到本地（覆盖已有的recording.webm）
        # 创建uploads目录（如果不存在）
        upload_dir = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 生成保存路径（始终保存为recording.webm，会覆盖已有的文件）
        save_path = os.path.join(upload_dir, 'recording.webm')
        
        # 保存文件（会自动覆盖已有的文件）
        audio_file.save(save_path)
        print(f"音频文件已保存到: {save_path}")

        try:
            # 使用FFmpeg命令行方式进行转换
            try:
                wav_filename = save_path.replace('.webm', '.wav')
                # 尝试在系统PATH中查找ffmpeg
                ffmpeg_path = "ffmpeg"
                try:
                    subprocess.run([ffmpeg_path, "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # 如果在PATH中找不到，尝试常见的安装路径
                    common_paths = [
                        "C:\\ffmpeg\\bin\\ffmpeg.exe",
                        "D:\\ffmpeg\\bin\\ffmpeg.exe",
                        "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
                        "D:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
                        "C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe"
                    ]
                    ffmpeg_path = None
                    for path in common_paths:
                        if os.path.exists(path):
                            ffmpeg_path = path
                            break
                    
                    # 如果还是找不到，抛出异常
                    if ffmpeg_path is None:
                        raise FileNotFoundError("在常见路径中找不到FFmpeg，请确保已安装FFmpeg并将其添加到系统PATH环境变量中")
                
                # 执行FFmpeg转换，捕获详细的错误输出
                result = subprocess.run([
                    ffmpeg_path, '-i', save_path, 
                    '-acodec', 'pcm_s16le',  # PCM 16位编码
                    '-ar', '16000',           # 16kHz采样率
                    '-ac', '1',               # 单声道
                    wav_filename
                ], capture_output=True, text=True)
                
                # 检查转换是否成功
                if result.returncode != 0:
                    error_message = f"FFmpeg转换失败: {result.stderr}"
                    print(error_message)
                    return jsonify({"error": f"音频格式转换失败: {result.stderr}"}), 500
                
                # 使用转换后的wav文件
                recognition_filename = wav_filename
                format_type = 'wav'
            except FileNotFoundError as e:
                error_message = str(e)
                print(f"FFmpeg未找到: {error_message}")
                return jsonify({"error": error_message}), 500
            except Exception as e:
                error_message = f"FFmpeg转换过程中发生未知错误: {str(e)}"
                print(error_message)
                return jsonify({"error": "音频格式转换过程中发生未知错误"}), 500
            
            # 使用阿里云实时语音识别服务处理音频文件
            recognition = Recognition(
                model='paraformer-realtime-v2',
                format=format_type,  # 根据实际文件格式调整
                sample_rate=16000,
                language_hints=['zh', 'en'],
                callback=None
            )
            
            result = recognition.call(recognition_filename)
            
            # 删除转换后的wav文件（保留原始webm文件）
            if os.path.exists(wav_filename):
                os.unlink(wav_filename)
            
            if result.status_code == HTTPStatus.OK:
                recognized_text = result.get_sentence()
                
                # 如果recognized_text是一个列表（包含多个句子），提取所有句子的文本内容
                if isinstance(recognized_text, list):
                    # 提取每个句子的text字段并组合成一个完整的句子
                    combined_text = ""
                    for sentence in recognized_text:
                        if isinstance(sentence, dict) and "text" in sentence:
                            combined_text += sentence["text"]
                    recognized_text = combined_text
                
                return jsonify({
                    "planText": recognized_text
                })
            else:
                return jsonify({"error": f"语音识别失败: {result.message}"}), 500
                
        except Exception as e:
            # 确保转换后的wav文件被删除
            if 'wav_filename' in locals() and os.path.exists(wav_filename):
                try:
                    os.unlink(wav_filename)
                except:
                    pass
            print(f"语音识别过程中发生错误: {e}")
            return jsonify({"error": f"语音识别过程中发生错误: {str(e)}"}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)