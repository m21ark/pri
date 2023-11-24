function addCard(json, searchTerm) {
  let resultsContainer = document.getElementById("resultsContainer");

  // Create a new card element
  let card = document.createElement("div");
  card.className = "card mb-4";

  // Create card body
  let cardBody = document.createElement("div");
  cardBody.className = "card-body";

  // Set card title
  var title = document.createElement("h5");
  title.className = "card-title";

  // Create a link to the individual animal details page
  var titleLink = document.createElement("a");
  titleLink.href =
    "animalDetails.html?name=" +
    encodeURIComponent(json.name) +
    "&description=" +
    encodeURIComponent(json.description) +
    "&link=" +
    encodeURIComponent(json.link);
  titleLink.textContent = json.name;
  title.appendChild(titleLink);

  cardBody.appendChild(title);

  let txtSize = 200;

  let text = document.createElement("p");
  text.className = "card-text";
  let truncatedDescription =
    json.description.length > txtSize
      ? json.description.slice(0, txtSize) + "..."
      : json.description;
  text.innerHTML = truncatedDescription.replace(
    new RegExp(searchTerm, "ig"),
    "<strong>$&</strong>"
  );
  cardBody.appendChild(text);

  // Add 'See More' link
  let seeMore = document.createElement("p");
  seeMore.className = "card-text";
  let link = document.createElement("small");
  link.className = "text-body-secondary";
  let anchor = document.createElement("a");
  anchor.href = json.link;
  anchor.textContent = "See More";
  link.appendChild(anchor);
  seeMore.appendChild(link);
  cardBody.appendChild(seeMore);

  // Append card body to card
  card.appendChild(cardBody);

  // Append card to results container
  resultsContainer.appendChild(card);
}

const mockResponse = [
  {
    name: "Lion",
    description:
      "The lion is a species in the family Felidae; it is a muscular, deep-chested cat with a short, rounded head, a reduced neck and round ears, and a hairy tuft at the end of its tail.",
    link: "https://en.wikipedia.org/wiki/Lion",
  },
  {
    name: "Elephant",
    description:
      "Elephants are large mammals of the family Elephantidae and the order Proboscidea. Three species are currently recognized: the African bush elephant, the African forest elephant, and the Asian elephant.",
    link: "https://en.wikipedia.org/wiki/Elephant",
  },
  {
    name: "Giraffe",
    description:
      "The giraffe is an African even-toed ungulate mammal, the tallest living terrestrial animal, and the largest ruminant. It is traditionally considered to be one species, Giraffa camelopardalis, with nine subspecies.",
    link: "https://en.wikipedia.org/wiki/Giraffe",
  },
  {
    name: "Tiger",
    description:
      "The tiger is the largest cat species, most recognizable for its pattern of dark vertical stripes on reddish-orange fur with a lighter underside.",
    link: "https://en.wikipedia.org/wiki/Tiger",
  },
  {
    name: "Penguin",
    description:
      "Penguins are a group of aquatic flightless birds. They live almost exclusively in the Southern Hemisphere, with only one species, the Galápagos penguin, found north of the equator.",
    link: "https://en.wikipedia.org/wiki/Penguin",
  },
  {
    name: "Kangaroo",
    description:
      "The kangaroo is a marsupial from the family Macropodidae. Kangaroos are endemic to Australia and are the largest living marsupials.",
    link: "https://en.wikipedia.org/wiki/Kangaroo",
  },
  {
    name: "Dolphin",
    description:
      "Dolphins are a widely distributed and diverse group of aquatic mammals. They are an informal grouping within the order Cetacea, excluding whales and porpoises.",
    link: "https://en.wikipedia.org/wiki/Dolphin",
  },
  {
    name: "Koala",
    description:
      "The koala is an arboreal herbivorous marsupial native to Australia. It is the only extant representative of the family Phascolarctidae and its closest living relatives are the wombats.",
    link: "https://en.wikipedia.org/wiki/Koala",
  },
  {
    name: "Hippopotamus",
    description:
      "The common hippopotamus, or hippo, is a large, mostly herbivorous, semiaquatic mammal and ungulate native to sub-Saharan Africa. It is one of only two extant species in the family Hippopotamidae, the other being the pygmy hippopotamus.",
    link: "https://en.wikipedia.org/wiki/Hippopotamus",
  },
  {
    name: "Panda",
    description:
      "The giant panda, also known as the panda bear, is a bear native to South Central China. It is characterised by its bold black-and-white coat and a voracious appetite for bamboo.",
    link: "https://en.wikipedia.org/wiki/Giant_panda",
  },
  {
    name: "Gorilla",
    description:
      "Gorillas are ground-dwelling, predominantly herbivorous apes that inhabit the forests of central Sub-Saharan Africa. The genus Gorilla is divided into two species: the eastern gorillas and the western gorillas, and either four or five subspecies.",
    link: "https://en.wikipedia.org/wiki/Gorilla",
  },
];

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

  // Simulate the response from the server with mock JSON
  let matchingAnimals = mockResponse.filter(
    (animal) =>
      animal.name.toLowerCase().includes(searchTerm) ||
      animal.description.toLowerCase().includes(searchTerm)
  );

  if (matchingAnimals.length === 0) {
    // Display "No results" message
    displayNoResultsMessage();
  } else {
    // Display matching animals
    matchingAnimals.forEach((animal) => addCard(animal, searchTerm));
  }

  // let apiUrl = 'http://localhost:5000/' + searchTerm; // Update with your actual API endpoint
  // console.log("Fetching: " + apiUrl)

  // Make a fetch request to the API
  /*
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => addCard(data))
        .catch(error => console.error('Error fetching data:', error));
    */
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
