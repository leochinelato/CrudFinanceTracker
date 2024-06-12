from database import get_by_id

id = 1
registro = get_by_id(id, "receita")

registro = {
    "id": registro[0],
    "description": registro[1],
    "amount": registro[2],
    "date": registro[3],
}

print(registro)
