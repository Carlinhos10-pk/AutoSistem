function fetchSentOrders() {
    fetch('http://127.0.0.1:8000/enviadas')
    .then(response => response.json())
    .then(data => {
        const sentOrdersList = document.getElementById('sent-orders-list');
        sentOrdersList.innerHTML = '';

        for (const code in data) {
            const comanda = data[code];
            const comandaDiv = document.createElement('div');
            comandaDiv.className = 'order-item';
            
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
                        <td><button type="button" onclick="deleteSentOrder('${code}', '${order.item}')">Remover</button></td>
                    </tr>
                `;
            });
            comandaDiv.appendChild(orderTable);
            
            sentOrdersList.appendChild(comandaDiv);
        }
    })
    .catch((error) => {
        alert('Erro ao buscar pedidos enviados: ' + error);
    });
}

function deleteSentOrder(code, item) {
    fetch(`http://127.0.0.1:8000/enviadas/${code}/${item}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchSentOrders();  // Atualiza a lista de pedidos após remover um pedido
    })
    .catch((error) => {
        alert('Erro ao apagar pedido: ' + error);
    });
}

// Chame a função fetchSentOrders ao carregar a página
window.onload = fetchSentOrders;