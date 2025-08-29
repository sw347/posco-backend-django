from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.utils.dot_to_list import braille_to_list
import louis
import paho.mqtt.client as mqtt
import json
import time

# MQTT 클라이언트 설정
mqttc = mqtt.Client()
mqttc.connect("broker.mqtt-dashboard.com", 1883)

@csrf_exempt
def change_text(request):
  if request.method == 'GET':
    mqttc.connect("broker.mqtt-dashboard.com", 1883)

    recevied_text = request.GET.get('text')
        
    if not recevied_text:
      return JsonResponse({'error': 'text query parameter is missing'}, status=400)
        
    try:
      start_time = time.time()
      
      braille_chars = louis.translateString(["braille-patterns.cti", "ko-g1.ctb"], recevied_text)
      
      end_time = time.time()
      elapsed_time = end_time - start_time
      print(f"Total processing time: {elapsed_time:.4f} seconds")
            
      dot_list = braille_to_list(braille_chars)
      
      result = {
        'original_text': recevied_text,
        'posco_jamo': dot_list['one_dimension']
      }
            
      mqttc.publish("posco_jamo", json.dumps(result))
      
      json_result = {
        'posco_jamo': braille_chars
      }
      return JsonResponse(json_result, status = 200)
    except Exception as e:
      error_details = {
          "error": "An error occurred during Braille translation.",
          "message": str(e)
      }
        
      return JsonResponse(error_details, status=500, safe=False)