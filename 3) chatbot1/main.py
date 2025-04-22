import requests

# Uso de un API_KEY para interconectarnos con el api de DeepSeek
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e'
API_URL = 'https://api.deepseek.com/v1/chat/completions'

def enviar_mensaje(mensaje, modelo = 'deepseek-chat'):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model' : modelo,
        'messages' : [{'role':'user','content':mensaje }]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status() #Comenta o expne si existe un posible error en HTTP
        return response.json()['choices'][0]['message']['content']
    
    except requests.exceptions.HTTPError as err:
        return f"Error de la API: {err.response.text}"
    except Exception as e:
        return f"Error Inesperado: {e}"
    

def main():
    print("Bienvenido al chatbot de DeepSeek. Si usted desea salir escriba 'salir' para terminar")

    while True:
        mensaje_usuario = input("Tú: ")

        if mensaje_usuario.lower() == 'salir':
            print("Chatbot: Hasta luego!")
            break 

        respuesta = enviar_mensaje(mensaje_usuario)
        print(f"Chatbot: {respuesta}")

if __name__ == "__main__":
    main() 
