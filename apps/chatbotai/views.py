import os
import requests
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# AI faqat shu mavzuda gaplashadi
ALLOWED_TOPIC = "Instagram loyihasi"


class AIChatView(APIView):
     def post(self, request):
          user_message = request.data.get("message")
          if not user_message:
               return Response({"error": "Maydon bo'sh bo'lmasligi lozim!!!"}, status=status.HTTP_400_BAD_REQUEST)

          # 🔎 1. Mavzuni tekshirish (asosiy filtr)
          keywords = ["instagram", "post", "story", "follower", "drf", "clone"]
          if not any(word in user_message.lower() for word in keywords):
               return Response({
                    "reply": f"Men faqat {ALLOWED_TOPIC} haqida gaplasha olaman 😊"
               })

          # 🔧 2. OpenAI API so‘rovi
          url = "https://api.openai.com/v1/chat/completions"
          headers = {
               "Authorization": f"Bearer {OPENAI_API_KEY}",
               "Content-Type": "application/json"
          }

          # 🧠 3. AI’ga system prompt orqali yo‘riqnoma beramiz
          data = {
               "model": "gpt-4o-mini",
               "messages": [
                    {
                         "role": "system",
                         "content": f"Sen faqat '{ALLOWED_TOPIC}' mavzusida gaplashasan. "
                                   f"Agar foydalanuvchi boshqa narsani so‘rasa, "
                                   f"muloyimlik bilan bu mavzudan tashqarida ekanligini ayt."
                    },
                    {"role": "user", "content": user_message}
               ]
          }

          # 🚀 4. So‘rov yuborish
          try:
               response = requests.post(url, headers=headers, json=data)
               result = response.json()

               ai_reply = result["choices"][0]["message"]["content"]
               return Response({"reply": ai_reply})

          except Exception as e:
               return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
