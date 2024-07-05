function searchCards() {
    var input = document.getElementById("searchInput").value.toLowerCase();
    var cards = document.getElementsByClassName("card");

    for (var i = 0; i < cards.length; i++) {
        var cardText = cards[i].getElementsByClassName("card-text")[0].textContent.toLowerCase();
        var card = cards[i];

        if (cardText.includes(input)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    }
}