function Zoomandet(x) {
  x.style.width = "12rem";
  x.style.transition = ".5s";
  x.style.opacity = "1";
}

function normalImg(x) {
  x.style.width = "8rem";
}

function searchCards() {
  var input = document.getElementById("searchInput").value.trim().toLowerCase();
  var cards = document.getElementsByClassName("card");

  for (var i = 0; i < cards.length; i++) {
      var cardText = cards[i].getElementsByClassName("card-text")[0].textContent.trim().toLowerCase();
      var card = cards[i];

      if (cardText.includes(input)) {
          card.style.display = "block";
      } else {
          card.style.display = "none";
      }
  }
}
