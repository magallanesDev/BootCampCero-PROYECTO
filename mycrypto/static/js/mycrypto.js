let losMovimientos

xhr = new XMLHttpRequest()


function recibeRespuestaCoinmarket() {
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status.error_message !== null) {
            alert("Se ha producido un error en acceso a Coin Market: " + respuesta.status.error_message)
            return
        }
        
        const movimiento = {}

        movimiento.date = respuesta.status.timestamp.substring(0, 10)
        console.log(movimiento.date)
        movimiento.time = respuesta.status.timestamp.substring(11, 23)
        console.log(movimiento.time)
        movimiento.moneda_from = document.querySelector("#moneda_from").value
        console.log(movimiento.moneda_from)
        movimiento.cantidad_from = document.querySelector("#cantidad_from").value
        console.log(movimiento.cantidad_from)
        movimiento.moneda_to = document.querySelector("#moneda_to").value
        console.log(movimiento.moneda_to)
        movimiento.cantidad_to = respuesta.data.quote[movimiento.moneda_to].price
        console.log(movimiento.cantidad_to)
        document.querySelector("#cantidad_to").setAttribute("placeholder", movimiento.cantidad_to)

    }    
}


function recibeRespuestaCreamovimiento() {
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status !== 'success') {
            alert("Se ha producido un error en acceso a servidor" + respuesta.mensaje)
            return
        }
        
        alert(respuesta.mensaje)

        llamaApiMovimientos()
    }    
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
        
            const dentro = `
                <td>${movimiento.date}</td>
                <td>${movimiento.time}</td>
                <td>${movimiento.moneda_from}</td>
                <td>${movimiento.cantidad_from}</td>
                <td>${movimiento.moneda_to}</td>
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


function llamaApiCoinmarket(evento) {
    evento.preventDefault()
    const movimiento = {}  // creamos el objeto movimiento, lo de abajo son atributos (moneda_from, cantidad_from ...)
    movimiento.moneda_from = document.querySelector("#moneda_from").value
    movimiento.cantidad_from = document.querySelector("#cantidad_from").value
    movimiento.moneda_to = document.querySelector("#moneda_to").value

    xhr.open('GET', `https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=${movimiento.cantidad_from}&symbol=${movimiento.moneda_from}&convert=${movimiento.moneda_to}&CMC_PRO_API_KEY=43095178-7dd8-48a4-8b66-e799480ad420`)
    xhr.onload = recibeRespuestaCoinmarket
    xhr.send()
    console.log("He lanzado petición")

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



function llamaApiCreaMovimiento(evento) {
    evento.preventDefault()

    const movimiento = capturaFormMovimiento()

    xhr.open("POST", `http://localhost:5000/api/v1/movimiento`, true)
    xhr.onload = recibeRespuestaCreamovimiento

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    xhr.send(JSON.stringify(movimiento))
    
}



window.onload = function() {
    llamaApiMovimientos()
    
    document.querySelector("#calcular")
        .addEventListener("click", llamaApiCoinmarket)
    
    
    document.querySelector("#ok")
        .addEventListener("click", llamaApiCreaMovimiento)
                
}