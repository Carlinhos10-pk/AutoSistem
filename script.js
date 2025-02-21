function sendOrder() {
    const table = document.getElementById('table').value;
    const item = document.getElementById('item').value;
    const quantity = document.getElementById('quantity').value;
    const code = document.getElementById('code').value;
    const price = document.getElementById('price').value;

    fetch('http://127.0.0.1:8000/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ table: parseInt(table), item, quantity: parseInt(quantity), code, price: parseFloat(price) }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Pedido enviado com sucesso!');
    })
    .catch((error) => {
        alert('Erro ao enviar pedido: ' + error);
    });
}

function fetchOrders() {
    fetch('http://127.0.0.1:8000/comandas')
    .then(response => response.json())
    .then(data => {
        const ordersList = document.getElementById('orders-list');
        ordersList.innerHTML = '';

        for (const code in data) {
            const comanda = data[code];
            const comandaDiv = document.createElement('div');
            comandaDiv.className = 'order-item';

            const codeHeader = document.createElement('h2');
            codeHeader.innerText = `Código: ${comanda.code}`;
            comandaDiv.appendChild(codeHeader);

            const tableHeader = document.createElement('h3');
            tableHeader.innerText = `Mesa: ${comanda.orders[0].table}`;
            comandaDiv.appendChild(tableHeader);

            const orderTable = document.createElement('table');
            orderTable.innerHTML = `
                <tr><th>Item</th><th>Quantidade</th><th>Remover</th></tr>
            `;
            comanda.orders.forEach(order => {
                orderTable.innerHTML += `
                    <tr>
                        <td>${order.item}</td>
                        <td>${order.quantity}</td>
                        <td><button type="button" onclick="deleteOrder('${order.code}', '${order.item}')">Remover</button></td>
                    </tr>
                `;
            });
            comandaDiv.appendChild(orderTable);
            
            ordersList.appendChild(comandaDiv);
        }
    })
    .catch((error) => {
        alert('Erro ao buscar pedidos: ' + error);
    });
}

function fetchTotal() {
    const code = document.getElementById('code').value;

    if (code) {
        fetch(`http://127.0.0.1:8000/comandas/${code}/total`)
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.total !== undefined) {
                document.getElementById('total-amount').innerText = `Total a pagar: R$${data.total.toFixed(2)}`;
            }
        })
        .catch((error) => {
            alert('Erro ao obter total: ' + error);
        });
    } else {
        alert('Por favor, insira o código da comanda.');
    }
}

function sendOrderToKitchen() {
    const code = document.getElementById('code').value;

    if (code) {
        fetch(`http://127.0.0.1:8000/send-order/${code}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch((error) => {
            alert('Erro ao enviar pedido: ' + error);
        });
    } else {
        alert('Por favor, insira o código da comanda.');
    }
}

function deleteOrder(code, item) {
    fetch(`http://127.0.0.1:8000/orders/${code}/${item}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchOrders(); // Atualiza a lista de pedidos após remover um pedido
    })
    .catch((error) => {
        alert('Erro ao apagar pedido: ' + error);
    });
}
