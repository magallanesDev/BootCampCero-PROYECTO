const movGlobal = {}

xhr = new XMLHttpRequest()
xhr2 = new XMLHttpRequest()


function muestraMovimientos() {
    if (this.readyState === 4 && this.status === 200) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status != 'success') {
            alert("Se ha producido un error en la consulta de movimientos")
            return
        }

        const tbody = document.querySelector(".tabla-movimientos tbody")  // lo insertamos dentro de tbody (mirar mycrypto.html)
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



function recibeRespuestaCoinmarket() {
    
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)
        
        if (respuesta.status.error_message !== null) {
            alert("Se ha producido un error en acceso a Coin Market: " + respuesta.status.error_message)
            return
        }
        
        movGlobal.date = respuesta.status.timestamp.substring(0, 10)
        console.log(movGlobal.date)
        movGlobal.time = respuesta.status.timestamp.substring(11, 23)
        console.log(movGlobal.time)
        movGlobal.moneda_from = document.querySelector("#moneda_from").value
        console.log(movGlobal.moneda_from)
        movGlobal.cantidad_from = document.querySelector("#cantidad_from").value
        console.log(movGlobal.cantidad_from)
        movGlobal.moneda_to = document.querySelector("#moneda_to").value
        console.log(movGlobal.moneda_to)
        movGlobal.cantidad_to = respuesta.data.quote[movGlobal.moneda_to].price
        console.log(movGlobal.cantidad_to)
        document.querySelector("#cantidad_to").setAttribute("placeholder", movGlobal.cantidad_to)

        console.log(movGlobal)
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
        llamaApiStatus()
    }    
}



function recibeRespuestaStatus() {
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
        const respuesta = JSON.parse(this.responseText)

        if (respuesta.status !== 'success') {
            alert("Se ha producido un error en acceso a servidor" + respuesta.mensaje)
            return
        }

        document.querySelector("#invertido").setAttribute("placeholder", respuesta.data.invertido)
        console.log(respuesta.data.invertido)

        document.querySelector("#valor_actual").setAttribute("placeholder", respuesta.data.valor_actual)
        console.log(respuesta.data.valor_actual) 
        
        resultadoInv = respuesta.data.valor_actual - respuesta.data.invertido
        document.querySelector("#resultado").setAttribute("placeholder", resultadoInv)
        console.log(resultadoInv)

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

    xhr.open("GET", `http://localhost:5000/api/v1/par/${movimiento.moneda_from}/${movimiento.moneda_to}/${movimiento.cantidad_from}`, true)
    // xhr.open('GET', `https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=${movimiento.cantidad_from}&symbol=${movimiento.moneda_from}&convert=${movimiento.moneda_to}&CMC_PRO_API_KEY=${API_KEY_COINMARKET}`)
    // si lo quisieramos hacer desde JS pero no es recomendable porque se vería nuestra API-KEY en el navegador.
    xhr.onload = recibeRespuestaCoinmarket
    xhr.send()
    console.log("He lanzado petición a Coin Market")
}   



function llamaApiCreaMovimiento(evento) {
    evento.preventDefault()

    xhr.open("POST", `http://localhost:5000/api/v1/movimiento`, true)
    xhr.onload = recibeRespuestaCreamovimiento

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")

    xhr.send(JSON.stringify(movGlobal))
}



function llamaApiStatus() {
    xhr2.open("GET", `http://localhost:5000/api/v1/status`, true)
    xhr2.onload = recibeRespuestaStatus
    xhr2.send()  
}   



window.onload = function() {
    llamaApiMovimientos()

    llamaApiStatus()
    
    document.querySelector("#calcular")
        .addEventListener("click", llamaApiCoinmarket)
    
    document.querySelector("#ok")
        .addEventListener("click", llamaApiCreaMovimiento)

}