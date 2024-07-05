function search() {
  var query = document.getElementById("quar").value.toLowerCase().trim();
  var fatherContents = document.querySelectorAll(".father_content");
  var cards = document.querySelectorAll(".card");

  // Hide all father_content elements
  for (var i = 0; i < fatherContents.length; i++) {
      fatherContents[i].style.display = "none";
  }

  // Show cards that match the query
  for (var j = 0; j < cards.length; j++) {
      var cardText = cards[j].textContent.toLowerCase();
      if (cardText.includes(query)) {
          cards[j].style.display = "inline-block";
          cards[j].closest(".father_content").style.display = "block"; // Show parent if child matches
      } else {
          cards[j].style.display = "none";
      }
  }
}