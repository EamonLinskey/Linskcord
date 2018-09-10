document.addEventListener('DOMContentLoaded', function() {
	if (localStorage.getItem("name") != null) {
		document.querySelector('.name-holder').innerHTML = ;
    	document.querySelector('.name-button').onclick = selectName;
    }
});

function selectName() {
	localStorage.setItem("name" = "eamon")
}