function autoGrow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function sendMessage(event) {
    if (event.keyCode == 13) {
    	message = document.querySelector('.message').value
        
    }
}

