from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from domain.utils.formatted_data import get_formatted_braille_data
import louis
import paho.mqtt.client as mqtt
import json

# MQTT 클라이언트 설정
mqttc = mqtt.Client()
mqttc.connect("broker.mqtt-dashboard.com", 1883)

@csrf_exempt
def change_text(request):
  if request.method == 'GET':
    mqttc.connect("broker.mqtt-dashboard.com", 1883)

    recevied_text = request.GET.get('text')
    device = request.GET.get('device')
        
    if not recevied_text:
      return JsonResponse({'error': 'text query parameter is missing'}, status=400)
        
    try:
      braille_chars = louis.translateString(["braille-patterns.cti", "ko-g2.ctb"], recevied_text)
      
      formatted_data = get_formatted_braille_data(braille_chars)
            
      result = {
        'original_text': recevied_text,
        'posco_jamo': formatted_data['mqtt_data']
      }
      
      print(f"json data {formatted_data['json_data']}")
            
      mqttc.publish(f"posco_jamo/{device}", json.dumps(result))
      
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