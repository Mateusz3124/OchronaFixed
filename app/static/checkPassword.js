function checkStrength(){
    let stat = {};
    var inputElement = document.getElementById("passwordInput");
    var text = inputElement.value;
    var textLength = text.length;
    var element = document.getElementById("StrentghOfPassword");
    if (textLength === 0){
        element.textContent = ""
        return
    }
    
    for (let i = 0; i < text.length; i++) {
        let znak = text[i];

        if (stat[znak]) {
            stat[znak] += 1;
        } else {
            stat[znak] = 1;
        }
    }

    let H = 0.0;

    for (let znak in stat) {
        let p_i = stat[znak] / text.length;
        H -= p_i * Math.log2(p_i);
    }

    if (H < 1.5){
        element.textContent = "weak password"
    }
    if (H >= 1.5 && H < 2.5){
        element.textContent = "moderate password"
    }
    if (H >= 2.5){
        element.textContent = "strong password"
    }
}