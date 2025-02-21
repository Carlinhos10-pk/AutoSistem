function fetchDescription() {
    const code = document.getElementById('code').value;

    fetch(`http://127.0.0.1:8000/comandas/${code}/description`)
    .then(response => response.json())
    .then(data => {
        const comandaDetails = document.getElementById('comanda-details');
        comandaDetails.innerHTML = '';

        if (data.description !== undefined) {
            comandaDetails.innerHTML = data.description;
        } else {
            comandaDetails.innerHTML = `<p>${data.message}</p>`;
        }
    })
    .catch((error) => {
        alert('Erro ao obter descrição: ' + error);
    });
}

function closeComanda() {
    const code = document.getElementById('code').value;

    if (code) {
        fetch(`http://127.0.0.1:8000/comandas/${code}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.total !== undefined) {
                document.getElementById('total-amount').innerText = `Total a pagar: R$${data.total.toFixed(2)}`;
            }
        })
        .catch((error) => {
            alert('Erro ao fechar comanda: ' + error);
        });
    } else {
        alert('Por favor, insira o código da comanda.');
    }
}
