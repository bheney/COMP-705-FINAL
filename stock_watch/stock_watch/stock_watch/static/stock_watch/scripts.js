function openConfirmation(symbol, name, title, api_url) {
    let confirmationMessage = "Would you like to remove " + name + " from " + title + "?";
    let confirmationWindow = window.open("", "Confirmation", "width=400,height=200");
    confirmationWindow.document.write("<h2>Confirmation</h2>");
    confirmationWindow.document.write("<p>" + confirmationMessage + "</p>");
    confirmationWindow.document.write("<button onclick=\"confirmRemove('" + symbol + "', '" + api_url + "')\">Yes</button>");
    confirmationWindow.document.write("<button onclick=\"closeConfirmation()\">No</button>");
}

function confirmRemove(symbol, url) {
    // Make an AJAX request to the server to remove the stock from the watchlist
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert("Stock with symbol " + symbol + " has been removed.");
            window.close();
        }
    };
    xhr.send(JSON.stringify({ symbol: symbol }));
}

function closeConfirmation() {
    window.close();
}
