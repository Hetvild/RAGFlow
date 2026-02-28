import uuid


def generate_collection_name(user_id: int, collection_name: str | None = None) -> str:
    """Генерирует безопасное уникальное имя для коллекции Qdrant"""
    collection_name = (
        collection_name.strip().lower().replace(" ", "_")
        if collection_name
        else "default"
    )
    # Оставляем только безопасные символы
    collection_name = "".join(c for c in collection_name if c.isalnum() or c == "_")[
        :30
    ]
    unique_id = uuid.uuid4().hex[:8]
    return f"{user_id}_{collection_name}_{unique_id}"


test = generate_collection_name(user_id=15421234, collection_name="My #Base$%")
print(test)
