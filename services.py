import requests
import sett
import json
import time


def obtener_Mensaje_whatsapp(message):
    print(message)
    if "type" not in message:
        text = "mensaje no reconocido"
        return text

    typeMessage = message["type"]
    if typeMessage == "text":
        text = message["text"]["body"]
    elif typeMessage == "button":
        text = message["button"]["text"]
    elif (
        typeMessage == "interactive" and message["interactive"]["type"] == "list_reply"
    ):
        text = message["interactive"]["list_reply"]["title"]
    elif (
        typeMessage == "interactive"
        and message["interactive"]["type"] == "button_reply"
    ):
        text = message["interactive"]["button_reply"]["title"]
    else:
        text = "mensaje no reconocido"

    return text


def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + whatsapp_token,
        }

        print("se envia ", data)
        response = requests.post(whatsapp_url, headers=headers, data=data)

        if response.status_code == 200:
            return "mensaje enviado", 200
        else:
            return "error al enviar el mensaje", response.status_code
    except Exception as e:
        return e, 403


def text_Message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {"body": text},
        }
    )
    return data


def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {"id": sedd + "_btn_" + str(i + 1), "title": option},
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body},
                "footer": {"text": footer},
                "action": {"buttons": buttons},
            },
        }
    )
    return data


def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {"id": sedd + "_row_" + str(i + 1), "title": option, "description": ""}
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": body},
                "footer": {"text": footer},
                "action": {
                    "button": "Ver Opciones",
                    "sections": [{"title": "Secciones", "rows": rows}],
                },
            },
        }
    )
    return data


def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {"link": url, "caption": caption, "filename": filename},
        }
    )
    return data


def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {"id": sticker_id},
        }
    )
    return data


def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    # elif media_type == "image":
    #     media_id = sett.images.get(media_name, None)
    # elif media_type == "video":
    #     media_id = sett.videos.get(media_name, None)
    # elif media_type == "audio":
    #     media_id = sett.audio.get(media_name, None)
    return media_id


def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {"message_id": messageId, "emoji": emoji},
        }
    )
    return data


def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            -"type": "text",
            "text": {"body": text},
        }
    )
    return data


def markRead_Message(messageId):
    data = json.dumps(
        {"messaging_product": "whatsapp", "status": "read", "message_id": messageId}
    )
    return data


def administrator_chatbot(text, number, messageId, name):
    text = text.lower()  # Mensaje que envio el usuario
    list = []
    print("el mensaje del cliente es " + text)

    if "hola" in text:
        body = "Hola! 👋 Bienvenido a FNconsorcios. ¿Como podemos ayudarte hoy?"
        footer = "Equipo FNconsorcios"
        options = ["💼 Consultas administrativas ", "Números de emergencia ☎️"]

        replyButtonData = buttonReply_Message(
            number, options, body, footer, "sed1", messageId
        )
        replyReaction = replyReaction_Message(number, messageId, "👋")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "administrativas" in text:
        body = "Tenemos varias áreas de consulta administrativa para elegir. ¿Sobre qué área te gustaría hacer tu consulta?"
        footer = "Equipo FNconsorcios"
        options = ["Sobre expensas", "Sobre el administrador ", "Sobre documentacion"]

        listReplyData = listReply_Message(
            number, options, body, footer, "sed2", messageId
        )
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "documentacion" in text:
        body = "¡Perfecto! ¿Sobre qué tipo de documentación te gustaría obtener información?"
        footer = "Equipo FNconsorcios"
        options = [
            "Contrato de copropiedad 🏠",
            "Contrato de administración 📋",
            "Contrato de inquilino 🏡",
        ]

        listReplyData = listReply_Message(
            number, options, body, footer, "sed3", messageId
        )
        sticker = sticker_Message(number, get_media_id("perro_triste", "sticker"))

        list.append(listReplyData)
        list.append(sticker)

    elif "contrato de inquilino" in text:
        body = "¡Excelente elección! ¿Te gustaría que te enviáramos el contrato de inquilino en formato PDF?"
        footer = "Equipo FNconsorcios"
        options = ["💹 Sí, envía el PDF.", "❌ No, gracias."]

        replyButtonData = buttonReply_Message(
            number, options, body, footer, "sed4", messageId
        )

        list.append(replyButtonData)

    elif "si, envia el pdf" in text:
        sticker = sticker_Message(number, get_media_id("", "sticker"))
        textMessage = text_Message(number, "Enviando contrato de inquilino...")

        enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(
            number, sett.document_url, "Listo 👍🏻", "Contrato de inquilinos.pdf"
        )
        enviar_Mensaje_whatsapp(document)
        time.sleep(3)

        body = "¿Te gustaria programar una reunion con una de nuestras administradoras?"
        footer = "Equipo FNconsorcios"
        options = ["💹 Si, agenda reunion.", "❌ No."]

        replyButtonData = buttonReply_Message(
            number, options, body, footer, "sed4", messageId
        )
        list.append(replyButtonData)
    elif "si, agendá una reunion" in text:
        body = "¡Perfecto! ¿Cuál de las siguientes opciones te gustaría utilizar?"
        footer = "Equipo FNconsorcios"
        options = [
            " 📅 Fecha: 12/01/2024 - ⏰ Hora: 12:00 PM ",
            " 📅 Fecha: 22/03/2024 - ⏰ Hora: 10:00 AM ",
            " 📅 Fecha: 04/02/2024 - ⏰ Hora: 05:00 PM ",
        ]

        listReply = listReply_Message(
            number,
            options,
        )
        list.append(listReply)
    elif "04/02/2024 5:00 PM" in text:
        body = "Excelente, has seleccionado la reunion del 4 de febrero a las 5:00 PM. Te enviare un recordatorio un dia antes. ¿Necesitas ayuda con algo mas hoy?"

        footer = "Equipo FNconsorcios"
        options = ["💹 Si, necesito ayuda.", " ❌ No, gracias."]

        buttonReply = buttonReply_Message(
            number,
            options,
        )
        list.append(buttonReply)

    elif "no, gracias" in text:
        textMessage = text_Message(
            number,
            "¡Perfecto! No dudes en contactarnos si tienes más preguntas. ¡Hasta luego! 😄",
        )
        list.append(buttonReply)

    else:
        data = text_Message(
            number, "No entiendo a que te refieres... ¿Puedo ayudarte con otra cosa?"
        )
        list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)


def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
