function checkform(f) {
    if (f.elements[0].value == '') { alert('Name must not be empty'); return false; }
    for (var i=1; i<f.elements.length - 1; i++) {
        var el = f.elements[i];
	if (el.value == 'notselected') {
	    alert('You must select an answer in ' + el.parentElement.firstChild.data);
	    return false;
	}
    }
    return true;
}
