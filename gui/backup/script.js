var inter = setInterval(clockTicking, 500);

function clockTicking() {
    var rtClock = new Date();
    var hours = rtClock.getHours();
    var minutes = rtClock.getMinutes();
    var seconds = rtClock.getSeconds();
    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    var h2 = document.getElementById("time");
    try {
        h2.innerHTML = hours + ":" + minutes + ":" + seconds;
    } catch (e) {

    }
}
eel.expose(dataUpdate)
function dataUpdate(photosensor,temperature,humidity){;         
    updateHumidity(humidity)  
    updateTemperature(temperature)
    updatePhotosensor(photosensor)
    return "ok"

};


function stopTicking() {
    clearInterval(inter);
    document.getElementById("time").innerHTML = "stoped";
}

function updateHumidity(humidityData){
    document.getElementById("humidity-degree").innerHTML = humidityData + "%";
}


function updateTemperature(temperatureData){
    document.getElementById("thermometer-degree").innerHTML = temperatureData + "°C";
}


function updatePhotosensor(photosensorData){
    document.getElementById("light-degree").innerHTML = photosensorData + "LUX";
}