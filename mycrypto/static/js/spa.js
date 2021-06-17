const monedas = {
    EUR: 'Euro',
    BTC: 'Bitcoin',
    ETH: 'Ethereum',
}


let losMovimientos
xhr = new XMLHttpRequest()

function recibeRespuesta() {
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status !== 'success') {
            alert("Se ha producido un error  en acceso a servidor" + respuesta.mensaje)
            return
        }
        
        alert(respuesta.mensaje)

        llamaApiMovimientos()
    }    
}

function detallaMovimiento(id) {
    let movimiento
    for (let i=0; i<losMovimientos.length; i++) {
        const item = losMovimientos[i]
        if (item.id == id) {
            movimiento = item
            break
        }
    }
    
    if (!movimiento) return

    document.querySelector("#id").value = id
    document.querySelector("#date").value = movimiento.date
    document.querySelector("#time").value = movimiento.time
    document.querySelector("#moneda_from").value = movimiento.moneda_from
    document.querySelector("#cantidad_from").value = movimiento.cantidad_from.toFixed(6)
    document.querySelector("#moneda_to").value = movimiento.moneda_to
    document.querySelector("#cantidad_to").value = movimiento.cantidad_to.toFixed(6)
}


function muestraMovimientos() {
    if (this.readyState === 4 && this.status === 200) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status != 'success') {
            alert("Se ha producido un error en la consulta de movimientos")
            return
        }

        losMovimientos = respuesta.movimientos
        const tbody = document.querySelector(".tabla-movimientos tbody")  // lo insertamos dentro de tbody (mirar spa.html)
        tbody.innerHTML = ""
        
        for (let i = 0; i < respuesta.movimientos.length; i++) {
            const movimiento = respuesta.movimientos[i]
            const fila = document.createElement("tr")
            fila.addEventListener("click", () => {
                detallaMovimiento(movimiento.id)
            })

            const dentro = `
                <td>${movimiento.date}</td>
                <td>${movimiento.time}</td>
                <td>${movimiento.moneda_from ? monedas[movimiento.moneda_from] : ""}</td>
                <td>${movimiento.cantidad_from}</td>
                <td>${movimiento.moneda_to ? monedas[movimiento.moneda_to] : ""}</td>
                <td>${movimiento.cantidad_to}</td>
            `
            fila.innerHTML = dentro
            
            tbody.appendChild(fila)
        }
    }
}



function llamaApiMovimientos() {
    xhr.open('GET', `http://localhost:5000/api/v1/movimientos`, true)
    xhr.onload = muestraMovimientos
    xhr.send()
}


function capturaFormMovimiento() {
    const movimiento = {}
    movimiento.date = document.querySelector("#date").value
    movimiento.time = document.querySelector("#time").value
    movimiento.moneda_from = document.querySelector("#moneda_from").value
    movimiento.cantidad_from = document.querySelector("#cantidad_from").value
    movimiento.moneda_to = document.querySelector("#moneda_to").value
    movimiento.cantidad_to = document.querySelector("#cantidad_to").value
   
    return movimiento 
}

/*
function validar(movimiento) {
    if (!movimiento.fecha)  {
        alert("Fecha obligatoria")
        return false
    }

    if (movimiento.concepto === "") {
        alert("Concepto obligatorio")
        return false
    }

    if (!document.querySelector("#gasto").checked && !document.querySelector("#ingreso").checked) {
        alert("Elija tipo de movimiento")
        return false
    }

    if (movimiento.esGasto && !movimiento.categoria) {
        alert("Debe seleccionar categoría del gasto")
        return false
    }

    if (!movimiento.esGasto && movimiento.categoria) {
        alert("Un ingreso no puede tener categoría")
        return false
    }
    
    if (movimiento.cantidad <= 0) {
        alert("La cantidad debe ser positiva")
    }
    
    return true
}
*/



function llamaApiCreaMovimiento(ev) {
    ev.preventDefault()

    const movimiento = capturaFormMovimiento()
/*
    if (!validar(movimiento)) {
        return
    }
*/
    xhr.open("POST", `http://localhost:5000/api/v1/movimiento`, true)
    xhr.onload = recibeRespuesta

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    xhr.send(JSON.stringify(movimiento))
    
}



window.onload = function() {
    llamaApiMovimientos()
    
        document.querySelector("#ok")
        .addEventListener("click", llamaApiCreaMovimiento)    
    
}