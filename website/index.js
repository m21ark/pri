function addCard(json, searchTerm) {
  let resultsContainer = document.getElementById("resultsContainer");

  // Create a new card element
  let card = document.createElement("div");
  card.className = "card mb-4";

  // Create card body
  let cardBody = document.createElement("div");
  cardBody.className = "card-body";

  // Set card title
  let title = document.createElement("h5");
  title.className = "card-title";

  // Create a link to the individual animal details page
  let titleLink = document.createElement("a");
  titleLink.href = "animalDetails.html?id=" + encodeURIComponent(json.id);
  titleLink.textContent = json.Name;
  title.appendChild(titleLink);

  cardBody.appendChild(title);

  let txtSize = 200;

  let text = document.createElement("p");
  text.className = "card-text";
  let truncatedDescription =
    json.Text.length > txtSize
      ? json.Text.slice(0, txtSize) + "..."
      : json.Text;
  text.innerHTML = truncatedDescription.replace(
    new RegExp(searchTerm, "ig"),
    "<strong>$&</strong>"
  );
  cardBody.appendChild(text);

  // Append card body to card
  card.appendChild(cardBody);

  // Append card to results container
  resultsContainer.appendChild(card);
}

function search() {
  let searchTerm = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();
  console.log("Searching for: ''" + searchTerm + "''");

  if (searchTerm === "") {
    alert("Empty Search not valid");
    return;
  }

  clearResults();

  let apiUrl = `http://localhost:3000/solr/animals/select?defType=edismax&fl=Name%2C%20Text%2C%20id&indent=true&mm=1&pf=Name%5E2.0%20Features%5E1.5%20Fun_Fact%5E1.5%20Text%5E2.0&ps=10&q.op=OR&q=${searchTerm}&qf=Name%5E2.0%20Features%5E1.2%20Fun_Fact%5E1.2%20Origin%5E1.0%20Diet%5E1.0%20Text%5E1.5%20Genus%5E2.0&rows=30&start=0&tie=0.1&useParams=`;

  // Make a fetch request to the API with a json body
  fetch(apiUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "http://localhost:5400",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);

      // Clear previous results
      clearResults();

      // Store search results in localStorage
      localStorage.setItem("searchResults", JSON.stringify(data.response.docs));

      if (data.response.docs.length === 0) {
        // Display "No results" message
        displayNoResultsMessage();
      } else {
        // Display matching animals
        data.response.docs.forEach((animal) => addCard(animal, searchTerm));
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function getCacheResults() {
  // Retrieve search results from localStorage
  var preservedResults = JSON.parse(localStorage.getItem("searchResults"));

  // Navigate back to the search results page
  if (preservedResults) {
    // Clear previous results
    clearResults();

    if (preservedResults.length === 0) displayNoResultsMessage();
    else preservedResults.forEach((animal) => addCard(animal, ""));

    localStorage.setItem("useCache", "false");
  }
}

function clearResults() {
  let resultsContainer = document.getElementById("resultsContainer");
  resultsContainer.innerHTML = "";
}

function displayNoResultsMessage() {
  let resultsContainer = document.getElementById("resultsContainer");
  let noResultsMessage = document.createElement("p");
  noResultsMessage.textContent = "No results found.";
  resultsContainer.appendChild(noResultsMessage);
}

if (localStorage.getItem("useCache") === null)
  localStorage.setItem("useCache", "false");

if (localStorage.getItem("useCache") === "true") getCacheResults();
