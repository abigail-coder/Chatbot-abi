import streamlit as st #Aviso del uso de la livreria
from groq import Groq #Importamos la libreria

#Configuración de la ventana de la web
st.set_page_config(page_title="Mi chat de IA", page_icon = "🎀")

#Titulo a la pagina
st.title("Mi primera aplicación con Streamlit")

#input
nombre = st.text_input("cual es tu nombre")

#crear un boton con funcinalidad

if st.button("Saludar!"):
    st.write(f"Hola {nombre}! Gracias por venir a Talento Tech") #Escribimos un mensaje 
#modelos          0                   1                    2
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#Nos conecta con la API, creando un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #Obtenemos la clave API
    return Groq(api_key = clave_secreta) #Conectamos a la api

#Selecciona el modelo de la ia
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #selecciona el modelo de la ia
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True #Funcionalidad para IA, responde a tiempo real
    ) #Devuelve la respuesta que manda la IA

#Historial de mensaje

def inicializar_estado():
    #si no existe "mensajes" entonces creamos historial
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #Historial vacío

def configurar_pagina():
    st.title("Mi chat de IA") #Titulo
    st.sidebar.title("Configuración")
    opcion = st.sidebar.selectbox(
        "Elegir modelo",#titulo
        options = MODELOS, #opciones deben estar e una lista
        index = 1 #valorPorDefecto
    )
    return opcion #Agrgamos esto para obtener el nombre de modelo

def actualizar_historial(rol, contenido, avatar):
    #El metodo append (dato) agrega datos a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial(): #Guardar la estructura visual 
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height = 400, border = True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""#Variable vacia
    for frase in chat_completo:
        if frase.choices[0].delta.content: #evita el NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content

    return respuesta_completa

def main():
    #!INVOCACIÓN DE FUNCIONES    
    modelo = configurar_pagina() #Agarramos el modelo seleccionado
    clienteUsuario = crear_usuario_groq() #Conecta con la API GROQ
    inicializar_estado() #Se crea en memoria el historial vacio
    area_chat()#Se crea el contenedor de los mensajes 
    mensaje = st.chat_input("Escribir un mensaje...")
    #Verificar que la variable mensaje tenga contenido
    if mensaje:
        actualizar_historial("user", mensaje, "🧠") #Mostramos el mensaje en el chat
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)#Obtenemos la respuesta del IA
        if chat_completo: #verificamos que la variable tenga algo
            with st.chat_message("assistant"):# with sirve para agrupar cosa
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "💞")
                st.rerun()#actualizar el chat

if __name__ == "__main__": #con esto python va a correr todo mi archivo 
    main()