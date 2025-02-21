from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Order(BaseModel):
    table: int
    item: str
    quantity: int
    code: str
    price: float

class Comanda(BaseModel):
    code: str
    orders: List[Order] = []

comandas: Dict[str, Comanda] = {}
enviadas: Dict[str, Comanda] = {}

@app.post("/orders")
def create_order(order: Order):
    if order.code not in comandas:
        comandas[order.code] = Comanda(code=order.code)
    comandas[order.code].orders.append(order)
    return {"message": "Pedido recebido!", "order": order}

@app.delete("/orders/{code}/{item}")
def delete_order(code: str, item: str):
    if code in comandas:
        order_index = next((index for (index, d) in enumerate(comandas[code].orders) if d.item == item), None)
        if order_index is not None:
            comandas[code].orders.pop(order_index)
            return {"message": f"Pedido {item} da comanda {code} apagado com sucesso!"}
        else:
            raise HTTPException(status_code=404, detail="Pedido não encontrado!")
    else:
        raise HTTPException(status_code=404, detail="Comanda não encontrada!")

@app.get("/comandas", response_model=Dict[str, Comanda])
def get_comandas():
    return comandas

@app.get("/comandas/{code}/description", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def get_description(code: str):
    if code in comandas:
        description = (
            f"<h2>Comanda {code}:</h2>"
            f"<hr>"
            f"<table>"
            f"<tr><th>Item</th><th>Quantidade</th><th>Preço Unitário</th><th>Subtotal</th></tr>"
        )
        total = 0
        for order in comandas[code].orders:
            subtotal = order.price * order.quantity
            total += subtotal
            description += (
                f"<tr>"
                f"<td>{order.item}</td>"
                f"<td>{order.quantity}</td>"
                f"<td>R${order.price:.2f}</td>"
                f"<td>R${subtotal:.2f}</td>"
                f"</tr>"
            )
        description += (
            f"</table>"
            f"<hr>"
            f"<h3>Total a Pagar: R${total:.2f}</h3>"
        )
        return {"message": "Descrição gerada!", "description": description, "total": total}
    return {"message": "Comanda não encontrada!"}

@app.get("/comandas/{code}/total", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def get_total(code: str):
    if code in comandas:
        total = sum(order.price * order.quantity for order in comandas[code].orders)
        return {"message": "Soma total calculada!", "total": total}
    return {"message": "Comanda não encontrada!"}

@app.post("/send-order/{code}")
def send_order(code: str):
    if code in comandas:
        description = (
            f"<h2>Comanda {code}:</h2>"
            f"<hr>"
            f"<table>"
            f"<tr><th>Item</th><th>Quantidade</th></tr>"
        )
        for order in comandas[code].orders:
            description += (
                f"<tr>"
                f"<td>{order.item}</td>"
                f"<td>{order.quantity}</td>"
                f"</tr>"
            )
        description += "</table>"

        enviadas[code] = comandas[code]

        return {"message": "Pedido enviado para o bar/cozinha com sucesso!", "description": description}
    return {"message": "Comanda não encontrada!"}

@app.get("/enviadas", response_model=Dict[str, Comanda])
def get_enviadas():
    return enviadas

@app.get("/comandas/{code}/description", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def get_description(code: str):
    if code in comandas:
        description = (
            f"<h2>Comanda {code}:</h2>"
            f"<hr>"
            f"<table>"
            f"<tr><th>Item</th><th>Quantidade</th><th>Preço Unitário</th><th>Subtotal</th></tr>"
        )
        total = 0
        for order in comandas[code].orders:
            subtotal = order.price * order.quantity
            total += subtotal
            description += (
                f"<tr>"
                f"<td>{order.item}</td>"
                f"<td>{order.quantity}</td>"
                f"<td>R${order.price:.2f}</td>"
                f"<td>R${subtotal:.2f}</td>"
                f"</tr>"
            )
        description += (
            f"</table>"
            f"<hr>"
            f"<h3>Total a Pagar: R${total:.2f}</h3>"
        )
        return {"message": "Descrição gerada!", "description": description, "total": total}
    return {"message": "Comanda não encontrada!"}

@app.delete("/orders/{code}/{item}")
def delete_order(code: str, item: str):
    if code in comandas:
        order_index = next((index for (index, d) in enumerate(comandas[code].orders) if d.item == item), None)
        if order_index is not None:
            comandas[code].orders.pop(order_index)
            return {"message": f"Pedido {item} da comanda {code} apagado com sucesso!"}
        else:
            raise HTTPException(status_code=404, detail="Pedido não encontrado!")
    else:
        raise HTTPException(status_code=404, detail="Comanda não encontrada!")

@app.delete("/comandas/{code}", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def close_comanda(code: str):
    if code in comandas:
        total = sum(order.price * order.quantity for order in comandas[code].orders)
        del comandas[code]
        return {"message": "Comanda fechada!", "total": total}
    return {"message": "Comanda não encontrada!"}

@app.get("/comandas", response_model=Dict[str, Comanda])
def get_comandas():
    return comandas

@app.get("/comandas/{code}", response_model=Comanda)
def get_comanda(code: str):
    return comandas[code]

@app.get("/comandas/{code}/total", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def get_total(code: str):
    if code in comandas:
        total = sum(order.price * order.quantity for order in comandas[code].orders)
        return {"message": "Soma total calculada!", "total": total}
    return {"message": "Comanda não encontrada!"}

@app.get("/comandas/{code}/description", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def get_description(code: str):
    if code in comandas:
        description = (
            f"<h2>Comanda {code}:</h2>"
            f"<hr>"
            f"<table>"
            f"<tr><th>Mesa</th><th>Item</th><th>Quantidade</th><th>Preço Unitário</th><th>Subtotal</th></tr>"
        )
        total = 0
        for order in comandas[code].orders:
            subtotal = order.price * order.quantity
            total += subtotal
            description += (
                f"<tr>"
                f"<td>{order.table}</td>"
                f"<td>{order.item}</td>"
                f"<td>{order.quantity}</td>"
                f"<td>R${order.price:.2f}</td>"
                f"<td>R${subtotal:.2f}</td>"
                f"</tr>"
            )
        description += (
            f"</table>"
            f"<hr>"
            f"<h3>Total a Pagar: R${total:.2f}</h3>"
        )
        return {"message": "Descrição gerada!", "description": description, "total": total}
    return {"message": "Comanda não encontrada!"}

@app.delete("/comandas/{code}", response_model=Union[Dict[str, str], Dict[str, Union[str, float]]])
def close_comanda(code: str):
    if code in comandas:
        total = sum(order.price * order.quantity for order in comandas[code].orders)
        del comandas[code]
        return {"message": "Comanda fechada!", "total": total}
    return {"message": "Comanda não encontrada!"}

@app.delete("/enviadas/{code}/{item}")
def delete_sent_order(code: str, item: str):
    if code in enviadas:
        order_index = next((index for (index, d) in enumerate(enviadas[code].orders) if d.item == item), None)
        if order_index is not None:
            enviadas[code].orders.pop(order_index)
            return {"message": f"Pedido {item} da comanda {code} apagado com sucesso!"}
        else:
            raise HTTPException(status_code=404, detail="Pedido não encontrado!")
    else:
        raise HTTPException(status_code=404, detail="Comanda não encontrada!")
