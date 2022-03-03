from typing import Optional

from chat_maker.editor import ChatEditor
from chat_maker.loader import ChatLoader
from chat_maker.exceptions import NodeExistsError
from chat_maker.initializer import Initializer
from app import app


@app.post("/chat/init/{name}/{aws_region}")
def init_chat(name: str, aws_region: str):
    initializer = Initializer(from_dynamodb=True, aws_region=aws_region)
    result = initializer.init_chat(chat_name=name)
    return result


@app.get("/chat/get/{chat_id}/{aws_region}")
def get_chat(chat_id: str, aws_region: str):
    loader = ChatLoader(chat_id=chat_id, from_dynamodb=True, aws_region=aws_region)
    return loader.get_chat()


@app.put("/chat/update/{chat_id}/{aws_region}/node/add/{node_name}")
def add_node(chat_id: str, aws_region: str, node_name: str):
    editor = ChatEditor(chat_id=chat_id, from_dynamodb=True, aws_region=aws_region)
    try:
        editor.create_node(node_name)
    except Exception as e:
        return {"error": e.__str__()}

    return {
        "chat_id": chat_id,
        "chat_name": editor.chat.name,
        "node_name": node_name,
        "status": "ok",
    }


@app.put("/chat/update/{chat_id}/{aws_region}/node/remove/{node_name}")
def remove_node(chat_id: str, aws_region: str, node_name: str):
    editor = ChatEditor(chat_id=chat_id, from_dynamodb=True, aws_region=aws_region)
    try:
        editor.remove_node(node_name)
    except Exception as e:
        return {"error": e.__str__()}

    return {"chat_id": chat_id, "chat_name": editor.chat.name, "status": "ok"}


@app.put("/chat/update/{chat_id}/{aws_region}/usr_phr/add/"
         "{edited_node}/{user_phrase_name}/{success_node}/{user_phrase_type}")
def add_user_phrase(
    chat_id: str,
    aws_region: str,
    edited_node: str,
    user_phrase_name: str,
    success_node: str,
    user_phrase_type: str,
    user_phrase_items: Optional[str] = None,
):
    editor = ChatEditor(chat_id=chat_id, from_dynamodb=True, aws_region=aws_region)
    usr_phs_items = user_phrase_items.split(",") if user_phrase_items else []
    try:
        editor.add_user_phrase(
            edited_node=edited_node,
            user_phrase_name=user_phrase_name,
            success_node=success_node,
            user_phrase_type=user_phrase_type,
            user_phrase_items=usr_phs_items,
        )
    except Exception as e:
        return {"error": e.__str__()}

    return {
        "chat_id": chat_id,
        "chat_name": editor.chat.name,
        "edited_node": edited_node,
        "user_phrase_name": user_phrase_name,
        "success_node": success_node,
        "user_phrase_type": user_phrase_type,
        "user_phrase_items": usr_phs_items,
        "status": "ok"
    }


@app.put("/chat/update/{chat_id}/{aws_region}/usr_phr/remove/{edited_node}/{user_phrase_name}")
def remove_user_phrase(
        chat_id: str,
        aws_region: str,
        edited_node: str,
        user_phrase_name: str,
):
    editor = ChatEditor(chat_id=chat_id, from_dynamodb=True, aws_region=aws_region)
    try:
        editor.remove_user_phrase(edited_node=edited_node, user_phrase_name=user_phrase_name)
    except Exception as e:
        return {"error": e.__str__()}

    return {
        "chat_id": chat_id,
        "chat_name": editor.chat.name,
        "edited_node": edited_node,
        "status": "ok"
    }
