function listen() {
    var source = new EventSource("/stream/");
    var target = document.getElementById("placeholder");
    source.onmessage = function(msg) {
            console.log("Got some new data");
	        target.innerHTML = msg.data + '<br>';
    }
}

listen();
