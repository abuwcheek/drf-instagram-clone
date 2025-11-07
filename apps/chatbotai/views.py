import os
import requests
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




load_dotenv()  # .env fayldan kalitlarni o‘qish
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class AIChatView(APIView):
     def post(self, request):
          user_message = request.data.get("message")
          if not user_message:
               data = {
                    'status': 'error',
                    'message': "xabar maydonini to'ldirish shart"
               }
               return Response(data=data)

          # OpenAI API so‘rovi
          url = "https://api.openai.com/v1/chat/completions"
          headers = {
               "Authorization": f"Bearer {OPENAI_API_KEY}",
               "Content-Type": "application/json"
          }
          data = {
               "model": "gpt-4o-mini",
               "messages": [{"role": "user", "content": user_message}],
          }


          try:
               response = requests.post(url, headers=headers, json=data)
               result = response.json()


               ai_reply = result["choices"][0]["message"]["content"]
               return Response({"reply": ai_reply})
          except Exception as e:
               return Response({
                    "status": "error",
                    "message": "AI bilan bog‘lanishda xatolik yuz berdi",
                    "data": str(e)
               })


